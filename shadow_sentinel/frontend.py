import streamlit as st

st.markdown("""
<style>
    /* Dark background */
    .stApp { background-color: #0E1117 !important; }
    /* White text for everything else */
    .stApp, p, span, h1, h2, h3, h4, h5, h6, label { color: #FFFFFF !important; }
    /* Grey for small labels (Service, Activated, etc.) */
    div[data-testid="stMetricLabel"] { color: #B0B0B0 !important; }
    /* BRIGHT GREEN for metric values (Shadow Sentinel, False, etc.) */
    div[data-testid="stMetricValue"] > div, div[data-testid="stMetricValue"] {
        color: #00FF00 !important;
        font-weight: bold !important;
    }
    /* Green border around the metric cards */
    div[data-testid="metric-container"] {
        border: 1px solid #00FF00 !important;
        background-color: #1A1A1A !important;
        padding: 15px !important;
        border-radius: 8px !important;
    }
    /* Light grey for subtitles */
    .stCaption, .stMarkdown p { color: #D0D0D0 !important; }
</style>
""", unsafe_allow_html=True)
"""Shadow Sentinel - Operator Console (Streamlit)."""
import hashlib, hmac, json, os, secrets, time
import requests

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











