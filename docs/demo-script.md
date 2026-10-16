# Demo Script - 5 Minutes

## Setup

1. Start HYDRA-GRID dashboard: streamlit run src/layer5_council/dashboard.py
2. Start Shadow Sentinel backend: uvicorn shadow_sentinel.backend:app --port 8000
3. Start Shadow Sentinel frontend: streamlit run shadow_sentinel/frontend.py --server.port 8502
4. Open both browsers: http://localhost:8501 and http://localhost:8502

## Minute 0-1 - The Problem

Nation-state attackers target power grids by sending commands that look valid. Firewalls miss them because nothing looks like malware. Ukraine 2015, Ukraine 2016, Triton, Colonial Pipeline, Poland 2025 - all succeeded the same way.

## Minute 1-2 - IT Network Attack

Click IT Network Intrusion.

This attack came from the IT network. Our SENTRY layer blocks it with Zero Trust - IT can never send commands to the OT grid. This is the exact control Ukraine 2015 and Colonial Pipeline lacked.

## Minute 2-3 - Digital Twin Blocks a Cascade

Click Coordinated Cascade Attack once.

The attacker tries to open two breakers. Our Digital Twin simulates it on a copy of the grid first. It sees the voltage would drop to 0.40 - below our safe floor. The command is blocked before it reaches the real grid.

## Minute 3-4 - IMMUNE Learns

Click Coordinated Cascade Attack again.

Same attack, second attempt. IMMUNE catches it instantly - under 1 millisecond. The system learned the signature. Cut one head, two grow back.

## Minute 4-5 - Shadow Sentinel

Switch to http://localhost:8502.

Even if all 5 layers were compromised, Shadow Sentinel is watching from outside. It uses 5 signals - Heartbeat, Decision, Integrity, View, Sustained Pattern. Two or more fire together -> alert a human operator. No autonomous action.

## Closing

5 layers. 18 security mechanisms. 41 automated tests. Plus 1 independent watchdog. Zero hardware. Runs on a laptop. Two independent systems. One mission.
