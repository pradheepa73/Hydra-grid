"""HYDRA-GRID 2026 - COUNCIL Dashboard (Defense-Grade UI)."""
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

import streamlit as st

from src.layer5_council import HydraGrid


st.set_page_config(
    page_title="HYDRA-GRID | National Grid Defense",
    page_icon="shield",
    layout="wide",
    initial_sidebar_state="collapsed",
)


st.markdown("""
<style>
    :root {
        --bg-base:    #0a0e1a;
        --bg-panel:   #10182b;
        --bg-elev:    #16213a;
        --border:     #1f2d4a;
        --accent:     #2dd4bf;
        --text:       #e2e8f0;
        --text-dim:   #94a3b8;
        --green:      #22c55e;
        --amber:      #f59e0b;
        --red:        #ef4444;
    }
    .stApp {
        background: var(--bg-base);
        color: var(--text);
        font-family: Inter, Segoe UI, sans-serif;
    }
    .stApp::before {
        content: "";
        position: fixed;
        top: 0; left: 0; right: 0; bottom: 0;
        background-image:
            linear-gradient(rgba(45, 212, 191, 0.025) 1px, transparent 1px),
            linear-gradient(90deg, rgba(45, 212, 191, 0.025) 1px, transparent 1px);
        background-size: 48px 48px;
        pointer-events: none;
        z-index: 0;
    }
    .main .block-container {
        padding-top: 1.5rem;
        padding-bottom: 2rem;
        max-width: 1400px;
    }
    .hydra-header {
        display: flex;
        align-items: center;
        justify-content: space-between;
        padding: 16px 24px;
        margin-bottom: 24px;
        background: linear-gradient(90deg, #0f1a30 0%, #10182b 100%);
        border: 1px solid var(--border);
        border-left: 4px solid var(--accent);
        border-radius: 4px;
        box-shadow: 0 4px 24px rgba(0,0,0,0.4);
    }
    .hydra-header-left {
        display: flex;
        align-items: center;
        gap: 16px;
    }
    .hydra-logo {
        width: 44px; height: 44px;
        border-radius: 6px;
        background: linear-gradient(135deg, #2dd4bf, #0891b2);
        display: flex; align-items: center; justify-content: center;
        font-size: 22px;
        box-shadow: 0 0 20px rgba(45, 212, 191, 0.4);
    }
    .hydra-title {
        font-size: 22px;
        font-weight: 700;
        letter-spacing: 0.5px;
        color: var(--text);
        margin: 0;
        line-height: 1.2;
    }
    .hydra-subtitle {
        font-size: 12px;
        color: var(--text-dim);
        letter-spacing: 1.5px;
        text-transform: uppercase;
        margin-top: 2px;
    }
    .hydra-status {
        display: flex;
        align-items: center;
        gap: 10px;
        padding: 8px 14px;
        background: rgba(34, 197, 94, 0.1);
        border: 1px solid rgba(34, 197, 94, 0.4);
        border-radius: 4px;
        font-size: 12px;
        color: #22c55e;
        letter-spacing: 1px;
        text-transform: uppercase;
        font-weight: 600;
    }
    .hydra-status-dot {
        width: 8px; height: 8px;
        border-radius: 50%;
        background: #22c55e;
        box-shadow: 0 0 10px #22c55e;
    }
    .section-label {
        font-size: 11px;
        letter-spacing: 2px;
        text-transform: uppercase;
        color: #2dd4bf;
        font-weight: 600;
        margin-bottom: 12px;
        padding-bottom: 6px;
        border-bottom: 1px solid #1f2d4a;
    }
    div[data-testid="stMetric"] {
        background: #10182b;
        border: 1px solid #1f2d4a;
        border-top: 2px solid #2dd4bf;
        border-radius: 4px;
        padding: 14px 16px;
    }
    div[data-testid="stMetricLabel"] {
        color: #94a3b8 !important;
        text-transform: uppercase;
        letter-spacing: 1px;
        font-size: 10px !important;
        font-weight: 600;
    }
    div[data-testid="stMetricValue"] {
        color: #e2e8f0 !important;
        font-family: Consolas, monospace !important;
        font-weight: 700 !important;
        font-size: 24px !important;
    }
    .stButton > button {
        background: #16213a;
        color: #e2e8f0;
        border: 1px solid #1f2d4a;
        border-radius: 4px;
        padding: 10px 16px;
        text-transform: uppercase;
        letter-spacing: 1px;
        font-size: 11px;
        font-weight: 600;
        width: 100%;
    }
    .stButton > button:hover {
        background: #2dd4bf;
        color: #0a0e1a;
        border-color: #2dd4bf;
        box-shadow: 0 0 20px rgba(45, 212, 191, 0.4);
    }
    .log-entry {
        display: flex;
        align-items: center;
        gap: 12px;
        padding: 10px 14px;
        margin-bottom: 6px;
        background: #10182b;
        border-left: 3px solid;
        border-radius: 3px;
        font-family: Consolas, monospace;
        font-size: 12px;
    }
    .log-entry.block {
        border-left-color: #ef4444;
        background: linear-gradient(90deg, rgba(239, 68, 68, 0.08), #10182b);
    }
    .log-entry.allow {
        border-left-color: #22c55e;
        background: linear-gradient(90deg, rgba(34, 197, 94, 0.06), #10182b);
    }
    .log-verdict {
        font-weight: 700;
        font-size: 10px;
        letter-spacing: 1.5px;
        padding: 3px 8px;
        border-radius: 3px;
        min-width: 60px;
        text-align: center;
    }
    .log-verdict.block {
        background: rgba(239, 68, 68, 0.15);
        color: #fca5a5;
        border: 1px solid rgba(239, 68, 68, 0.4);
    }
    .log-verdict.allow {
        background: rgba(34, 197, 94, 0.15);
        color: #86efac;
        border: 1px solid rgba(34, 197, 94, 0.4);
    }
    .log-layer {
        color: #2dd4bf;
        font-weight: 600;
        font-size: 11px;
        letter-spacing: 1px;
        min-width: 70px;
    }
    .log-source {
        color: #94a3b8;
        font-size: 11px;
        min-width: 120px;
    }
    .log-command {
        color: #e2e8f0;
        font-size: 12px;
        flex: 1;
    }
    .log-reason {
        color: #94a3b8;
        font-size: 11px;
        font-style: italic;
        flex: 2;
    }
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    hr {
        border: none;
        border-top: 1px solid #1f2d4a;
        margin: 20px 0;
    }
    .stCaption, small {
        color: #94a3b8 !important;
        font-size: 11px;
    }
</style>
""", unsafe_allow_html=True)


if "grid" not in st.session_state:
    st.session_state.grid = HydraGrid(demo_mode=True)
if "log" not in st.session_state:
    st.session_state.log = []

grid = st.session_state.grid


st.markdown("""
<div class="hydra-header">
    <div class="hydra-header-left">
        <div class="hydra-logo">&#x1F6E1;</div>
        <div>
            <div class="hydra-title">HYDRA-GRID 2026</div>
            <div class="hydra-subtitle">National Grid Defense System</div>
        </div>
    </div>
    <div class="hydra-status">
        <span class="hydra-status-dot"></span>
        <span>System Online</span>
    </div>
</div>
""", unsafe_allow_html=True)


st.markdown('<div class="section-label">Live Grid State - Substation A</div>', unsafe_allow_html=True)

snap = grid.snapshot()
col1, col2, col3, col4 = st.columns(4)
col1.metric("Voltage", f"{snap['grid']['voltage']:.2f} pu")
col2.metric("Breaker B1", snap["grid"]["breakers"]["B1"])
col3.metric("Breaker B2", snap["grid"]["breakers"]["B2"])
col4.metric("Breaker B3", snap["grid"]["breakers"]["B3"])

st.markdown("---")

st.markdown('<div class="section-label">Threat Simulation Console</div>', unsafe_allow_html=True)
st.caption("Trigger simulated attacks to test defense layers in real time.")

col_a, col_b, col_c = st.columns(3)

with col_a:
    if st.button("Legitimate Operator Command", use_container_width=True):
        st.session_state.log.append(grid.process("SCADA_MASTER", "B1", "OPEN"))
        st.rerun()

with col_b:
    if st.button("IT Network Intrusion", use_container_width=True):
        st.session_state.log.append(grid.process("IT_NET", "B3", "OPEN"))
        st.rerun()

with col_c:
    if st.button("Coordinated Cascade Attack", use_container_width=True):
        grid.process("SCADA_MASTER", "B1", "OPEN")
        st.session_state.log.append(grid.process("SCADA_MASTER", "B2", "OPEN"))
        st.rerun()

st.markdown("---")

log_col, stat_col = st.columns([3, 1])

with log_col:
    st.markdown('<div class="section-label">Defense Event Log</div>', unsafe_allow_html=True)
    events = snap["events"]
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
    st.metric("Learned Signatures", stats["approved"])
    st.metric("Pending Approval", stats["pending"])
    st.metric("Rejected", stats["rejected"])

st.markdown("---")
st.markdown(
    '<div style="display: flex; justify-content: space-between; padding: 8px 0; '
    'font-size: 10px; color: #94a3b8; letter-spacing: 1.5px; text-transform: uppercase;">'
    '<span>HYDRA-GRID 2026 - 5-Layer Defense Framework</span>'
    '<span>SENTRY / TWIN / PATTERN / IMMUNE / COUNCIL</span>'
    '</div>',
    unsafe_allow_html=True,
)
