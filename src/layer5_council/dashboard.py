"""HYDRA-GRID Layer 5 - COUNCIL dashboard (Streamlit)."""
import streamlit as st
import time

from src.layer5_council import HydraGrid


st.set_page_config(page_title="HYDRA-GRID 2026", page_icon="🐉", layout="wide")

st.title("🐉 HYDRA-GRID 2026")
st.caption("A Self-Learning Cyber-Physical Defense Grid for National Smart Substations")
st.markdown("> *Cut One Head. It Grows Stronger.*")

# Session state
if "grid" not in st.session_state:
    st.session_state.grid = HydraGrid(demo_mode=True)
if "log" not in st.session_state:
    st.session_state.log = []

grid = st.session_state.grid

# --- TOP: GRID STATE ---
st.header("⚡ Live Grid State")
snap = grid.snapshot()
col1, col2, col3, col4 = st.columns(4)
col1.metric("Voltage (pu)", snap["grid"]["voltage"])
col2.metric("Breaker B1", snap["grid"]["breakers"]["B1"])
col3.metric("Breaker B2", snap["grid"]["breakers"]["B2"])
col4.metric("Breaker B3", snap["grid"]["breakers"]["B3"])

# --- MIDDLE: ATTACK CONTROLS ---
st.header("🎮 Attack Simulator")
col_a, col_b, col_c = st.columns(3)

with col_a:
    if st.button("✅ Legitimate OPEN B1"):
        result = grid.process("SCADA_MASTER", "B1", "OPEN")
        st.session_state.log.append(result)

with col_b:
    if st.button("🚨 IT_NET Attack B3"):
        result = grid.process("IT_NET", "B3", "OPEN")
        st.session_state.log.append(result)

with col_c:
    if st.button("💀 Cascade Attack B1+B2"):
        grid.process("ATTACKER", "B1", "OPEN")
        result = grid.process("ATTACKER", "B2", "OPEN")
        st.session_state.log.append(result)

# --- BOTTOM: EVENT LOG ---
st.header("📜 Defense Event Log")
if snap["events"]:
    for e in reversed(snap["events"][-15:]):
        if e["verdict"] == "BLOCK":
            st.error(f"🚨 [{e['layer']}] {e['source']} → {e['command']} — {e['reason']}")
        else:
            st.success(f"✅ [{e['layer']}] {e['source']} → {e['command']} — {e['reason']}")
else:
    st.info("No events yet. Try an attack above.")

# --- IMMUNE STATS ---
st.header("🧠 IMMUNE Layer Stats")
stats = snap["immune_stats"]
c1, c2, c3 = st.columns(3)
c1.metric("Learned Signatures", stats["approved"])
c2.metric("Pending Approval", stats["pending"])
c3.metric("Rejected", stats["rejected"])

st.caption("HYDRA-GRID 2026 — 5 layers: SENTRY · TWIN · PATTERN · IMMUNE · COUNCIL")
