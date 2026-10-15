# Shadow Sentinel

**An Independent Watchdog for HYDRA-GRID**

> *"The 5 layers protect the grid. Shadow Sentinel protects the 5 layers."*

---

## What It Is

Shadow Sentinel is a completely independent application — not a layer — that monitors the 5 primary defense layers of HYDRA-GRID. It does not block commands, does not act autonomously, and only observes, evaluates, and raises alerts for human review.

---

## Why It Exists

Every defense system has a fundamental question: what if the defense itself is compromised? If an attacker disables SENTRY, corrupts TWIN, tampers with logs, or bypasses PATTERN, the 5-layer defense fails silently. Shadow Sentinel is the answer.

Analogy: a military base has 5 security guards. What if a trained team silently takes them all out? That is why bases also have cameras on a separate circuit. Even if all guards are down, the cameras still see everything. Shadow Sentinel is that camera.

---

## Core Principle

Shadow Sentinel sits outside the pipeline. It does not trust the layers. It watches them.

HYDRA-GRID (5 layers) on port 8501. Shadow Sentinel backend on port 8000. Shadow Sentinel frontend on port 8502. Three processes. Two ports. Zero shared state.

---

## H-D-I-V-S Trigger Model

Sentinel stays silent during normal operation. Activates when 2 or more signals fire together.

- **H** — Heartbeat Loss: layer stopped sending health signals
- **D** — Decision Contradiction: a command that should be blocked was allowed
- **I** — Integrity Failure: logs or hashes changed
- **V** — View Mismatch: sentinel sees X, system reports Y
- **S** — Sustained Pattern: unusual activity continues

Rule: 2 of 5 triggers it. One signal is coincidence. Two is compromise.

---

## Security Mechanisms (10)

Transport: HMAC-SHA256 signing, nonce anti-replay, 30-second timestamp window, per-key rate limit (30/min), constant-time compare, deny-by-default auth.
Integrity: hash-chained audit log, tamper detection.
Operational: human-in-the-loop, key file isolation.

---

## Algorithms

HMAC-SHA256 · SHA-256 · constant-time compare · CSPRNG · timestamp window · hash-chain (Merkle-style) · multi-signal voting (2 of 5) · sliding window.

---

## Stack

Python 3.11+ · FastAPI · Uvicorn · Streamlit · cryptography · requests · pytest.

---

## Workflow

1. Sentinel detects 2+ signals. 2. Writes PENDING alert. 3. Operator opens console. 4. Reviews details. 5. Approves or rejects. 6. Action is hash-chained. No autonomous response. Ever. Human authority is final.

---

## API Endpoints

GET /status · POST /heartbeat · POST /decision · POST /evaluate · GET /alerts · POST /approve · POST /reject · GET /audit. All require HMAC headers X-Key, X-Nonce, X-Ts, X-Sig.

---

## Quick Start

Backend: `uvicorn shadow_sentinel.backend:app --host 127.0.0.1 --port 8000`
Frontend: `streamlit run shadow_sentinel/frontend.py --server.port 8502`
Tests: `python -m pytest tests/test_sentinel.py -v`

---

## Trigger Scenarios

Normal: all signals healthy → silent. Compromised: H+D+I+V+S → activates → human review. Single signal: only H → stays silent → no false positive.

---

## Design Principles

Separation of duties · independent verification · fail-safe · human authority · tamper-evident · zero autonomy.

---

## Threat Model

Attacker disables SENTRY → H+I. Modifies TWIN → I+V. Bypasses PATTERN → D. Deletes logs → I. Floods system → S. Compromises dashboard → V.

---

## Limitations

Same machine in prototype → separate VM in production. Keys in file → HSM/Vault. No wire encryption → mTLS. In-memory nonces → Redis. No formal verification → Phase 4.

---

## File Structure

    shadow_sentinel/
      __init__.py
      sentinel.py   # H-D-I-V-S logic
      backend.py    # FastAPI + HMAC
      frontend.py   # Streamlit console

---

## Team

PRADHEEPA M · HYDRA-GRID 2026 + Shadow Sentinel · OWASP SREC Cyber Week Hackathon 2026.
M1 — AI & Simulation. M2 — Network & Recovery. M3 — UI & Documentation.

---

## License

All Rights Reserved. Copyright (c) 2026 PRADHEEPA M.

---

## Author

Pradheepa M — B.Sc. Computer Science with Cybersecurity
pradheepa378@gmail.com
https://github.com/pradheepa73/Hydra-grid

<div align="center">

"Two independent systems. One mission. Cut one head, two grow back."

</div>
