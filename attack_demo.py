import requests, hmac, hashlib, time, secrets, json
from pathlib import Path

key_file = Path(".sentinel_keys.json")
if not key_file.exists():
    print("ERROR: .sentinel_keys.json not found. Is the backend running?")
else:
    with open(key_file) as f:
        keys = json.load(f)
    
    secret = keys.get("operator_admin", "").encode()
    key = "operator_admin"

    def headers(method, path, body=""):
        ts = str(int(time.time()))
        nonce = secrets.token_hex(16)
        msg = f"{method}{path}{ts}{nonce}{body}".encode()
        sig = hmac.new(secret, msg, hashlib.sha256).hexdigest()
        return {"X-Key": key, "X-Nonce": nonce, "X-Ts": ts, "X-Sig": sig, "Content-Type": "application/json"}

    print("Simulating attack signals (H-D-I-V-S)...")
    
    # H: Heartbeat Loss
    r1 = requests.post("http://127.0.0.1:8000/heartbeat", json={"layer": "SENTRY", "status": "down"}, headers=headers("POST", "/heartbeat", '{"layer":"SENTRY","status":"down"}'))
    print(f"Heartbeat Loss sent: {r1.status_code}")
    
    # D: Decision Contradiction
    body2 = '{"expected":"BLOCK","observed":"ALLOW"}'
    r2 = requests.post("http://127.0.0.1:8000/decision", json={"expected": "BLOCK", "observed": "ALLOW"}, headers=headers("POST", "/decision", body2))
    print(f"Decision Contradiction sent: {r2.status_code}")
    
    # I, V, S: Integrity Failure, View Mismatch, Sustained Pattern
    body3 = '{"integrity_ok":false,"view_match":false,"sustained":true}'
    r3 = requests.post("http://127.0.0.1:8000/evaluate", json={"integrity_ok": False, "view_match": False, "sustained": True}, headers=headers("POST", "/evaluate", body3))
    print(f"Integrity/View/Sustained signals sent: {r3.status_code}")

    print("")
    print("Attack simulation complete. Go to http://localhost:8502 and refresh (Ctrl+F5).")
