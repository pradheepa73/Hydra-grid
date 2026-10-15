"""Shadow Sentinel - Operator Console (Streamlit)."""
import hashlib, hmac, json, os, secrets, time
import requests
import streamlit as st

BACKEND = "http://127.0.0.1:8000"
_KEY_FILE = ".sentinel_keys.json"

def _load_keys():
    if not os.path.exists(_KEY_FILE): return {}
    with open(_KEY_FILE, encoding="utf-8") as f:
        data = json.load(f)
    return {k: bytes.fromhex(v) for k, v in data.items()}

def _signed_request(method, path, api_key_id, payload=None):
    keys = _load_keys()
    key = keys.get(api_key_id)
    if key is None: return None, "Unknown key"
    body = json.dumps(payload).encode() if payload is not None else b""
    nonce = secrets.token_hex(16)
    ts = str(time.time())
    msg = api_key_id.encode() + b"|" + body + b"|" + nonce.encode() + b"|" + ts.encode()
    sig = hmac.new(key, msg, hashlib.sha256).hexdigest()
    headers = {"Content-Type": "application/json", "X-Key": api_key_id,
               "X-Nonce": nonce, "X-Ts": ts, "X-Sig": sig}
    try:
        if method == "GET": r = requests.get(BACKEND + path, headers=headers, timeout=5)
        else: r = requests.post(BACKEND + path, headers=headers, data=body, timeout=5)
        return r, None
    except Exception as e: return None, str(e)

st.set_page_config(page_title="Shadow Sentinel", layout="wide")
st.markdown("""<style>
    .stApp { background: #0a0e1a; color: #e2e8f0; }
    .main .block-container { padding-top: 1rem; max-width: 1500px; }
    div[data-testid="stMetric"] { background: #10182b; border: 1px solid #1f2d4a; border-top: 2px solid #2dd4bf; border-radius: 4px; padding: 14px; }
    div[data-testid="stMetricLabel"] * { color: #7dd3fc !important; text-transform: uppercase; font-weight: 700 !important; }
    div[data-testid="stMetricValue"] * { color: #fff !important; font-family: monospace !important; }
    .stButton > button { background: #16213a; color: #e2e8f0; border: 1px solid #1f2d4a; border-radius: 4px; width: 100%; }
    .stButton > button:hover { background: #2dd4bf; color: #0a0e1a; }
    header, footer { visibility: hidden; }
</style>""", unsafe_allow_html=True)

st.title("SHADOW SENTINEL")
st.caption("Independent Watchdog - Operator Console")

key_id = st.selectbox("Operator Identity", ["operator_admin", "operator_analyst"])

r, err = _signed_request("GET", "/status", key_id)
if err:
    st.error("Backend unreachable: " + err)
    st.stop()

r_status = r.json()
is_active = r_status["active"]
st.subheader("System Status")
c1, c2, c3, c4 = st.columns(4)
c1.metric("Service", r_status["service"])
c2.metric("Activated", str(is_active))
c3.metric("Pending Alerts", r_status["summary"]["pending"])
c4.metric("Log Integrity", "INTACT" if r_status["summary"]["log_integrity"] else "BROKEN")

st.subheader("Alert Queue")
r, err = _signed_request("GET", "/alerts", key_id)
if err: st.error(err)
else:
    data = r.json()
    if not data["all"]: st.info("No alerts. Sentinel is silent.")
    else:
        for idx, alert in enumerate(data["all"]):
            st.write("ALERT " + str(idx) + " - " + alert["status"])
            st.json(alert)
            if alert["status"] == "PENDING":
                cc1, cc2 = st.columns(2)
                if cc1.button("APPROVE", key="ap_" + str(idx)):
                    _signed_request("POST", "/approve", key_id, {"alert_index": idx, "operator": key_id, "reason": "approved"})
                    st.rerun()
                if cc2.button("REJECT", key="rj_" + str(idx)):
                    _signed_request("POST", "/reject", key_id, {"alert_index": idx, "operator": key_id, "reason": "rejected"})
                    st.rerun()
