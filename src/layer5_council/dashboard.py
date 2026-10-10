"""HYDRA-GRID 2026 - COUNCIL Dashboard (Defense Command Center)."""
import sys
import os
from datetime import datetime, timezone
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

import streamlit as st
from src.layer5_council import HydraGrid


st.set_page_config(
    page_title="HYDRA-GRID | National Grid Defense",
    page_icon="D",
    layout="wide",
    initial_sidebar_state="collapsed",
)


st.markdown("""
<style>
    :root {
        --bg-base: #0a0e1a;
        --bg-panel: #10182b;
        --bg-elev: #16213a;
        --border: #1f2d4a;
        --accent: #2dd4bf;
        --text: #e2e8f0;
        --text-dim: #94a3b8;
        --green: #22c55e;
        --amber: #f59e0b;
        --red: #ef4444;
    }
    .stApp { background: var(--bg-base); color: var(--text); }
    .stApp::before {
        content: "";
        position: fixed; top: 0; left: 0; right: 0; bottom: 0;
        background-image:
            linear-gradient(rgba(45,212,191,0.025) 1px, transparent 1px),
            linear-gradient(90deg, rgba(45,212,191,0.025) 1px, transparent 1px);
        background-size: 48px 48px;
        pointer-events: none; z-index: 0;
    }
    .main .block-container { padding-top: 1rem; padding-bottom: 2rem; max-width: 1500px; }

    .hydra-header {
        display: flex; align-items: center; justify-content: space-between;
        padding: 14px 22px; margin-bottom: 18px;
        background: linear-gradient(90deg, #0f1a30 0%, #10182b 100%);
        border: 1px solid var(--border); border-left: 4px solid var(--accent);
        border-radius: 4px; box-shadow: 0 4px 24px rgba(0,0,0,0.5);
    }
    .hydra-header-left { display: flex; align-items: center; gap: 14px; }
    .hydra-logo {
        width: 42px; height: 42px; border-radius: 6px;
        background: linear-gradient(135deg, #2dd4bf, #0891b2);
        display: flex; align-items: center; justify-content: center;
        font-size: 22px; color: #fff; font-weight: 700;
        box-shadow: 0 0 20px rgba(45,212,191,0.5);
    }
    .hydra-title { font-size: 20px; font-weight: 700; color: #e2e8f0; margin: 0; line-height: 1.2; }
    .hydra-subtitle { font-size: 11px; color: #94a3b8; letter-spacing: 1.5px; text-transform: uppercase; }
    .hydra-badge {
        font-size: 9px; letter-spacing: 1.5px; padding: 5px 10px;
        background: rgba(239,68,68,0.15); color: #fca5a5;
        border: 1px solid rgba(239,68,68,0.5); border-radius: 3px; font-weight: 700;
    }
    .threat-level {
        font-size: 11px; letter-spacing: 1px; padding: 6px 12px;
        background: rgba(0,0,0,0.3); border: 1px solid; border-radius: 3px;
        font-weight: 700; text-transform: uppercase;
    }
    .hydra-clock {
        font-family: Consolas, monospace; font-size: 12px; color: #7dd3fc;
        padding: 6px 10px; background: rgba(0,0,0,0.3);
        border: 1px solid #1f2d4a; border-radius: 3px; letter-spacing: 1px;
    }
    .hydra-status {
        display: flex; align-items: center; gap: 8px; padding: 6px 12px;
        background: rgba(34,197,94,0.1); border: 1px solid rgba(34,197,94,0.4);
        border-radius: 3px; font-size: 11px; color: #22c55e;
        letter-spacing: 1px; text-transform: uppercase; font-weight: 700;
    }
    .hydra-status-dot {
        width: 8px; height: 8px; border-radius: 50%;
        background: #22c55e; box-shadow: 0 0 10px #22c55e;
        animation: pulse 2s infinite;
    }
    @keyframes pulse { 0%,100% {opacity:1;} 50% {opacity:0.4;} }

    .section-label {
        font-size: 11px; letter-spacing: 2px; text-transform: uppercase;
        color: #2dd4bf; font-weight: 600; margin-bottom: 10px;
        padding-bottom: 6px; border-bottom: 1px solid #1f2d4a;
    }

    .layer-status-bar {
        display: flex; gap: 10px; margin-bottom: 18px;
    }
    .layer-pill {
        flex: 1; display: flex; align-items: center; gap: 10px;
        padding: 10px 14px; background: #10182b;
        border: 1px solid #1f2d4a; border-left: 3px solid #22c55e;
        border-radius: 4px; font-size: 11px; letter-spacing: 1px;
        text-transform: uppercase; color: #e2e8f0; font-weight: 600;
    }
    .layer-pill .dot {
        width: 8px; height: 8px; border-radius: 50%; background: #22c55e;
        box-shadow: 0 0 8px #22c55e; animation: pulse 2s infinite;
    }
    .layer-pill .name { color: #2dd4bf; }
    .layer-pill .stat { margin-left: auto; color: #22c55e; font-size: 10px; }

    .counter-card {
        background: #10182b; border: 1px solid #1f2d4a;
        border-top: 2px solid #2dd4bf; border-radius: 4px;
        padding: 14px 16px; text-align: center;
    }
    .counter-label {
        font-size: 10px; letter-spacing: 1.5px; text-transform: uppercase;
        color: #94a3b8; font-weight: 600; margin-bottom: 6px;
    }
    .counter-value {
        font-family: Consolas, monospace; font-size: 28px; font-weight: 700;
        text-shadow: 0 0 12px currentColor;
    }
    .counter-value.red { color: #ef4444; }
    .counter-value.green { color: #22c55e; }
    .counter-value.cyan { color: #2dd4bf; }

    .topology {
        display: flex; align-items: center; justify-content: center;
        gap: 24px; padding: 20px; background: #10182b;
        border: 1px solid #1f2d4a; border-radius: 4px; margin-bottom: 18px;
    }
    .tp-breaker {
        width: 100px; padding: 14px 0; text-align: center;
        border-radius: 4px; font-family: Consolas, monospace;
        font-size: 12px; font-weight: 700; letter-spacing: 1px;
        border: 2px solid; position: relative;
    }
    .tp-breaker.closed {
        background: rgba(34,197,94,0.1); border-color: #22c55e; color: #86efac;
        box-shadow: 0 0 16px rgba(34,197,94,0.3);
    }
    .tp-breaker.open {
        background: rgba(239,68,68,0.12); border-color: #ef4444; color: #fca5a5;
        box-shadow: 0 0 16px rgba(239,68,68,0.4);
    }
    .tp-breaker .id {
        font-size: 16px; display: block; margin-bottom: 2px;
    }
    .tp-line {
        flex: 1; height: 2px; background: #2dd4bf;
        box-shadow: 0 0 8px #2dd4bf; max-width: 60px;
    }

    div[data-testid="stMetric"] {
        background: #10182b; border: 1px solid #1f2d4a;
        border-top: 2px solid #2dd4bf; border-radius: 4px;
        padding: 14px 16px;
    }
    div[data-testid="stMetricLabel"] {
        color: #7dd3fc !important; text-transform: uppercase;
        letter-spacing: 1.5px; font-size: 11px !important; font-weight: 700 !important;
    }
    div[data-testid="stMetricValue"] {
        color: #ffffff !important; font-family: Consolas, monospace !important;
        font-weight: 700 !important; font-size: 26px !important;
        text-shadow: 0 0 12px rgba(45,212,191,0.5);
    }

    .stButton > button {
        background: #16213a; color: #e2e8f0; border: 1px solid #1f2d4a;
        border-radius: 4px; padding: 10px 16px; text-transform: uppercase;
        letter-spacing: 1px; font-size: 11px; font-weight: 600;
        transition: all 0.15s ease; width: 100%;
    }
    .stButton > button:hover {
        background: #2dd4bf; color: #0a0e1a; border-color: #2dd4bf;
        box-shadow: 0 0 20px rgba(45,212,191,0.5);
    }

    .log-entry {
        display: flex; align-items: center; gap: 12px; padding: 10px 14px;
        margin-bottom: 6px; background: #10182b;
        border-left: 3px solid; border-radius: 3px;
        font-family: Consolas, monospace; font-size: 12px;
    }
    .log-entry.block {
        border-left-color: #ef4444;
        background: linear-gradient(90deg, rgba(239,68,68,0.08), #10182b);
    }
    .log-entry.allow {
        border-left-color: #22c55e;
        background: linear-gradient(90deg, rgba(34,197,94,0.06), #10182b);
    }
    .log-verdict {
        font-weight: 700; font-size: 10px; letter-spacing: 1.5px;
        padding: 3px 8px; border-radius: 3px; min-width: 60px; text-align: center;
    }
    .log-verdict.block {
        background: rgba(239,68,68,0.15); color: #fca5a5;
        border: 1px solid rgba(239,68,68,0.4);
    }
    .log-verdict.allow {
        background: rgba(34,197,94,0.15); color: #86efac;
        border: 1px solid rgba(34,197,94,0.4);
    }
    .log-layer { color: #2dd4bf; font-weight: 600; font-size: 11px; letter-spacing: 1px; min-width: 70px; }
    .log-source { color: #94a3b8; font-size: 11px; min-width: 120px; }
    .log-command { color: #e2e8f0; font-size: 12px; flex: 1; }
    .log-reason { color: #94a3b8; font-size: 11px; font-style: italic; flex: 2; }

    #MainMenu, footer, header { visibility: hidden; }
    hr { border: none; border-top: 1px solid #1f2d4a; margin: 16px 0; }
    .stCaption, small { color: #94a3b8 !important; font-size: 11px; }

    /* Fix metric label readability */
    div[data-testid="stMetricLabel"],
    div[data-testid="stMetricLabel"] * {
        color: #7dd3fc !important;
    }
    div[data-testid="stMetricValue"],
    div[data-testid="stMetricValue"] * {
        color: #ffffff !important;
    }

    /* ========== FORCE METRIC STYLING (override Streamlit defaults) ========== */
    div[data-testid="stMetric"] {
        background: #10182b !important;
        border: 1px solid #1f2d4a !important;
        border-top: 2px solid #2dd4bf !important;
        border-radius: 4px !important;
        padding: 14px 16px !important;
    }
    div[data-testid="stMetric"] label,
    div[data-testid="stMetric"] label p,
    div[data-testid="stMetric"] label div,
    div[data-testid="stMetric"] > label,
    div[data-testid="stMetric"] > label > div,
    div[data-testid="stMetric"] > label > div > p {
        color: #7dd3fc !important;
        background: transparent !important;
        background-color: transparent !important;
        text-transform: uppercase !important;
        letter-spacing: 1.5px !important;
        font-size: 11px !important;
        font-weight: 700 !important;
    }
    div[data-testid="stMetric"] div[data-testid="stMetricValue"],
    div[data-testid="stMetric"] div[data-testid="stMetricValue"] > div,
    div[data-testid="stMetric"] div[data-testid="stMetricValue"] > div > div {
        color: #ffffff !important;
        background: transparent !important;
        background-color: transparent !important;
        font-family: Consolas, monospace !important;
        font-weight: 700 !important;
        font-size: 26px !important;
        text-shadow: 0 0 12px rgba(45, 212, 191, 0.5) !important;
    }
    /* Remove any leftover highlight from mark elements */
    div[data-testid="stMetric"] mark,
    div[data-testid="stMetricLabel"] mark,
    div[data-testid="stMetricValue"] mark {
        background: transparent !important;
        color: inherit !important;
    }
</style>
""", unsafe_allow_html=True)


if "grid" not in st.session_state:
    st.session_state.grid = HydraGrid(demo_mode=True)
grid = st.session_state.grid
snap = grid.snapshot()
events = snap["events"]
blocks = sum(1 for e in events if e["verdict"] == "BLOCK")
allows = sum(1 for e in events if e["verdict"] == "ALLOW")
learned = snap["immune_stats"]["approved"]

if blocks == 0:
    tl, tc, td = "5", "#22c55e", "NORMAL"
elif blocks <= 2:
    tl, tc, td = "4", "#84cc16", "ELEVATED"
elif blocks <= 5:
    tl, tc, td = "3", "#f59e0b", "GUARDED"
elif blocks <= 8:
    tl, tc, td = "2", "#f97316", "HIGH"
else:
    tl, tc, td = "1", "#ef4444", "CRITICAL"

now_utc = datetime.now(timezone.utc).strftime("%H:%M:%S UTC")


st.markdown(
    '<div class="hydra-header">'
    '<div class="hydra-header-left">'
    '<div class="hydra-logo">H</div>'
    '<div>'
    '<div class="hydra-title">HYDRA-GRID 2026</div>'
    '<div class="hydra-subtitle">National Grid Defense Command</div>'
    '</div></div>'
    '<div style="display:flex; gap:10px; align-items:center;">'
    '<div class="hydra-badge">CLASSIFIED // MISSION CRITICAL</div>'
    '<div class="threat-level" style="border-color:' + tc + '; color:' + tc + ';">'
    '<span style="display:inline-block; width:8px; height:8px; border-radius:50%; background:' + tc + '; margin-right:8px; box-shadow:0 0 10px ' + tc + ';"></span>'
    'DEFCON ' + tl + ' &mdash; ' + td + '</div>'
    '<div class="hydra-clock">' + now_utc + '</div>'
    '<div class="hydra-status"><span class="hydra-status-dot"></span><span>ONLINE</span></div>'
    '</div></div>',
    unsafe_allow_html=True,
)


st.markdown(
    '<div class="layer-status-bar">'
    '<div class="layer-pill"><span class="dot"></span><span class="name">SENTRY</span><span class="stat">ACTIVE</span></div>'
    '<div class="layer-pill"><span class="dot"></span><span class="name">TWIN</span><span class="stat">ACTIVE</span></div>'
    '<div class="layer-pill"><span class="dot"></span><span class="name">PATTERN</span><span class="stat">ACTIVE</span></div>'
    '<div class="layer-pill"><span class="dot"></span><span class="name">IMMUNE</span><span class="stat">ACTIVE</span></div>'
    '<div class="layer-pill"><span class="dot"></span><span class="name">COUNCIL</span><span class="stat">ACTIVE</span></div>'
    '</div>',
    unsafe_allow_html=True,
)


c1, c2, c3 = st.columns(3)
with c1:
    st.markdown('<div class="counter-card"><div class="counter-label">Threats Blocked</div><div class="counter-value red">' + str(blocks) + '</div></div>', unsafe_allow_html=True)
with c2:
    st.markdown('<div class="counter-card"><div class="counter-label">Commands Allowed</div><div class="counter-value green">' + str(allows) + '</div></div>', unsafe_allow_html=True)
with c3:
    st.markdown('<div class="counter-card"><div class="counter-label">Signatures Learned</div><div class="counter-value cyan">' + str(learned) + '</div></div>', unsafe_allow_html=True)


st.markdown("---")
st.markdown('<div class="section-label">Live Grid Topology - Substation A</div>', unsafe_allow_html=True)

b1_state = snap["grid"]["breakers"]["B1"]
b2_state = snap["grid"]["breakers"]["B2"]
b3_state = snap["grid"]["breakers"]["B3"]

def breaker_box(name, state):
    cls = "open" if state == "OPEN" else "closed"
    return '<div class="tp-breaker ' + cls + '"><span class="id">' + name + '</span>' + state + '</div>'

st.markdown(
    '<div class="topology">'
    '<div class="tp-line"></div>'
    + breaker_box("B1", b1_state) +
    '<div class="tp-line"></div>'
    + breaker_box("B2", b2_state) +
    '<div class="tp-line"></div>'
    + breaker_box("B3", b3_state) +
    '<div class="tp-line"></div>'
    '</div>',
    unsafe_allow_html=True,
)


col1, col2, col3, col4 = st.columns(4)
col1.metric("Voltage", str(snap["grid"]["voltage"]) + " pu")
col2.metric("Active Breakers", str(sum(1 for s in [b1_state, b2_state, b3_state] if s == "CLOSED")) + " / 3")
col3.metric("Events Logged", str(len(events)))
col4.metric("System Uptime", "100%")

st.markdown("---")


st.markdown('<div class="section-label">Threat Simulation Console</div>', unsafe_allow_html=True)
st.caption("Trigger simulated attacks to test defense layers in real time.")

col_a, col_b, col_c = st.columns(3)
with col_a:
    if st.button("Legitimate Operator Command", use_container_width=True):
        grid.process("SCADA_MASTER", "B1", "OPEN")
        st.rerun()
with col_b:
    if st.button("IT Network Intrusion", use_container_width=True):
        grid.process("IT_NET", "B3", "OPEN")
        st.rerun()
with col_c:
    if st.button("Coordinated Cascade Attack", use_container_width=True):
        grid.process("SCADA_MASTER", "B1", "OPEN")
        grid.process("SCADA_MASTER", "B2", "OPEN")
        st.rerun()

st.markdown("---")


log_col, stat_col = st.columns([3, 1])

with log_col:
    st.markdown('<div class="section-label">Defense Event Log</div>', unsafe_allow_html=True)
    if events:
        for e in reversed(events[-12:]):
            verdict = e["verdict"]
            cls = "block" if verdict == "BLOCK" else "allow"
            st.markdown(
                '<div class="log-entry ' + cls + '">'
                '<span class="log-verdict ' + cls + '">' + verdict + '</span>'
                '<span class="log-layer">' + e["layer"] + '</span>'
                '<span class="log-source">' + e["source"] + '</span>'
                '<span class="log-command">' + e["command"] + '</span>'
                '<span class="log-reason">' + e["reason"] + '</span>'
                '</div>',
                unsafe_allow_html=True,
            )
    else:
        st.info("Awaiting events. Trigger a simulation above to begin monitoring.")

with stat_col:
    st.markdown('<div class="section-label">IMMUNE Engine</div>', unsafe_allow_html=True)
    stats = snap["immune_stats"]
    st.metric("Learned", stats["approved"])
    st.metric("Pending", stats["pending"])
    st.metric("Rejected", stats["rejected"])

st.markdown("---")
st.markdown(
    '<div style="display:flex; justify-content:space-between; padding:8px 0; '
    'font-size:10px; color:#94a3b8; letter-spacing:1.5px; text-transform:uppercase;">'
    '<span>HYDRA-GRID 2026 - 5-Layer Defense Framework</span>'
    '<span>SENTRY / TWIN / PATTERN / IMMUNE / COUNCIL</span>'
    '</div>',
    unsafe_allow_html=True,
)
