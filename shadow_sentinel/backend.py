"""Shadow Sentinel - Backend API (FastAPI)."""
import hashlib
import hmac
import json
import os
import secrets
import time
from collections import defaultdict
from typing import Optional

from fastapi import FastAPI, Header, HTTPException, Request
from pydantic import BaseModel

from shadow_sentinel.sentinel import ShadowSentinel


app = FastAPI(title="Shadow Sentinel API", version="1.0")
_KEY_FILE = ".sentinel_keys.json"


def _load_or_create_keys():
    if os.path.exists(_KEY_FILE):
        with open(_KEY_FILE, encoding="utf-8") as f:
            data = json.load(f)
        return {k: bytes.fromhex(v) for k, v in data.items()}
    keys = {"hydra_grid": secrets.token_bytes(32).hex(),
            "operator_admin": secrets.token_bytes(32).hex(),
            "operator_analyst": secrets.token_bytes(32).hex()}
    with open(_KEY_FILE, "w", encoding="utf-8") as f:
        json.dump(keys, f)
    return {k: bytes.fromhex(v) for k, v in keys.items()}


KEYS = _load_or_create_keys()
SEEN_NONCES = set()
RATE = defaultdict(list)
sentinel = ShadowSentinel()
LAYERS = ["SENTRY", "TWIN", "PATTERN", "IMMUNE", "COUNCIL"]


def _verify(api_key_id, body, nonce, ts, sig):
    try:
        ts_val = float(ts)
    except ValueError:
        return False, "Invalid timestamp"
    if abs(time.time() - ts_val) > 30:
        return False, "Timestamp outside window"
    if nonce in SEEN_NONCES:
        return False, "Nonce reuse detected"
    SEEN_NONCES.add(nonce)
    now = time.time()
    RATE[api_key_id] = [t for t in RATE[api_key_id] if now - t < 60]
    if len(RATE[api_key_id]) >= 30:
        return False, "Rate limit exceeded"
    RATE[api_key_id].append(now)
    key = KEYS.get(api_key_id)
    if not key:
        return False, "Unknown API key"
    msg = api_key_id.encode() + b"|" + body + b"|" + nonce.encode() + b"|" + ts.encode()
    expected = hmac.new(key, msg, hashlib.sha256).hexdigest()
    if not hmac.compare_digest(expected, sig):
        return False, "Invalid signature"
    return True, "OK"


def _auth_guard(api_key_id, body, nonce, ts, sig):
    ok, reason = _verify(api_key_id, body, nonce, ts, sig)
    if not ok:
        sentinel._append_log("AUTH_FAIL", {"key": api_key_id, "reason": reason})
        raise HTTPException(status_code=401, detail=reason)


class HeartbeatIn(BaseModel):
    layer: str


class DecisionIn(BaseModel):
    command: str
    expected: str
    observed: str


class EvaluateIn(BaseModel):
    expected_hashes: dict
    expected_views: dict


class ApprovalIn(BaseModel):
    alert_index: int
    operator: str
    reason: Optional[str] = ""


@app.get("/status")
def status():
    return {"service": "Shadow Sentinel", "active": sentinel.is_activated(), "summary": sentinel.summary()}


@app.post("/heartbeat")
async def heartbeat(payload: HeartbeatIn, request: Request,
                    x_key: str = Header(...), x_nonce: str = Header(...),
                    x_ts: str = Header(...), x_sig: str = Header(...)):
    _auth_guard(x_key, await request.body(), x_nonce, x_ts, x_sig)
    sentinel.heartbeat(payload.layer)
    return {"ok": True}


@app.post("/decision")
async def decision(payload: DecisionIn, request: Request,
                   x_key: str = Header(...), x_nonce: str = Header(...),
                   x_ts: str = Header(...), x_sig: str = Header(...)):
    _auth_guard(x_key, await request.body(), x_nonce, x_ts, x_sig)
    sentinel.record_expected(payload.command, payload.expected)
    sentinel.record_observed(payload.command, payload.observed)
    return {"ok": True}


@app.post("/evaluate")
async def evaluate(payload: EvaluateIn, request: Request,
                   x_key: str = Header(...), x_nonce: str = Header(...),
                   x_ts: str = Header(...), x_sig: str = Header(...)):
    _auth_guard(x_key, await request.body(), x_nonce, x_ts, x_sig)
    fired, active, _ = sentinel.evaluate(LAYERS, payload.expected_hashes, payload.expected_views)
    return {"activated": fired, "signals": active}


@app.get("/alerts")
def alerts(x_key: str = Header(...), x_nonce: str = Header(...),
           x_ts: str = Header(...), x_sig: str = Header(...)):
    _auth_guard(x_key, b"", x_nonce, x_ts, x_sig)
    return {"pending": sentinel.pending_alerts(), "all": sentinel.alert_queue}


@app.post("/approve")
async def approve(payload: ApprovalIn, request: Request,
                  x_key: str = Header(...), x_nonce: str = Header(...),
                  x_ts: str = Header(...), x_sig: str = Header(...)):
    _auth_guard(x_key, await request.body(), x_nonce, x_ts, x_sig)
    return {"ok": sentinel.approve(payload.alert_index, payload.operator)}


@app.post("/reject")
async def reject(payload: ApprovalIn, request: Request,
                 x_key: str = Header(...), x_nonce: str = Header(...),
                 x_ts: str = Header(...), x_sig: str = Header(...)):
    _auth_guard(x_key, await request.body(), x_nonce, x_ts, x_sig)
    return {"ok": sentinel.reject(payload.alert_index, payload.operator, payload.reason)}


@app.get("/audit")
def audit(x_key: str = Header(...), x_nonce: str = Header(...),
          x_ts: str = Header(...), x_sig: str = Header(...)):
    _auth_guard(x_key, b"", x_nonce, x_ts, x_sig)
    return {"log": sentinel.log, "integrity": sentinel.verify_log_chain()}
