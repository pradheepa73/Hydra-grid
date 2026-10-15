
# HYDRA-GRID 2026

**A Self-Learning Cyber-Physical Defense Grid for National Smart Substations**

> *Cut One Head. It Grows Stronger.*

[![Tests](https://img.shields.io/badge/tests-46%20passing-brightgreen)]()
[![Python](https://img.shields.io/badge/python-3.11+-blue)]()
[![License](https://img.shields.io/badge/license-All%20Rights%20Reserved-red)]()

---

## Overview

HYDRA-GRID is a software-only, 5-layer defense framework that protects smart grid substations from nation-state cyber-physical attacks. It implements the full **Prevent - Simulate - Detect - Learn - Explain** loop on commodity hardware.

Every layer maps to a documented real-world incident from 2015 to 2025. The project is complemented by **Shadow Sentinel** -- a completely independent watchdog application that monitors the 5 layers from the outside. Shadow Sentinel is described at the end of this document.

---

## The Problem

Every major power grid attack in the last decade succeeded for the same reason: **the commands the attackers sent were valid.**

Traditional defenses -- firewalls, antivirus, signature-based IDS -- fail because no single packet looks malicious. Only the **sequence, physical consequence, and intent** reveal the danger.

| Incident | Year | Why Defenses Failed |
|:---|:---|:---|
| Ukraine (BlackEnergy) | 2015 | Stolen VPN credentials -- traffic looked legitimate |
| Ukraine (Industroyer) | 2016 | Native ICS protocols -- commands were valid |
| Triton | 2017 | Safety controller manipulation looked normal |
| Colonial Pipeline | 2021 | IT breach forced OT shutdown -- no visibility |
| Poland | 2025 | Default credentials + firmware corruption |

**The gap:** Existing tools check syntax or signatures. None checks **intent + sequence + physics together** in a closed, adaptive loop.

---

## The Solution

HYDRA-GRID treats every control command as a **claim about the grid's future state**. It simulates the claim on a digital twin, checks it against physics and learned patterns, and if the claim is dangerous:

1. Quarantines the command
2. Traps the sender
3. Learns the attack signature for instant future detection

**Result:** Attacks are blocked **before** execution. Repeat attacks are blocked in **under 1 millisecond**.

---

## The 5 Layers (S-T-P-I-C)

| Layer | Name | Role |
|:-:|:---|:---|
| 1 | **SENTRY** | Zero Trust gate with 9 integrated defenses |
| 2 | **TWIN** | Digital-twin pre-execution simulation |
| 3 | **PATTERN** | Physics rules + Markov sequence detection |
| 4 | **IMMUNE** | Adaptive attack signature learner |
| 5 | **COUNCIL** | Explainable AI dashboard |

**Loop:** Prevent - Simulate - Detect - Learn - Explain

```
Command - SENTRY - TWIN - PATTERN - IMMUNE - COUNCIL - ALLOW / BLOCK
```

---

## Core Features (10 Total)

| # | Feature | Layer | Counters |
|:-:|:---|:---|:---|
| 1 | Zero Trust Data Diode | SENTRY | Colonial Pipeline 2021 |
| 2 | Modbus TCP Honeypot | SENTRY | Ukraine 2015 |
| 3 | Physics Rule Engine | PATTERN | Ukraine 2016 |
| 4 | Markov Chain Sequence Detector | PATTERN | Ukraine 2016 |
| 5 | Digital Twin Pre-Execution Simulator | TWIN | Ukraine 2016 |
| 6 | Default-Credential Watchdog | SENTRY | Poland 2025 |
| 7 | Firmware Integrity Checker | SENTRY | Poland 2025 |
| 8 | Adaptive Attack Signature Learner | IMMUNE | All attacks |
| 9 | Golden Image Auto-Recovery | IMMUNE | Ukraine 2015 (KillDisk) |
| 10 | Explainable AI Dashboard | COUNCIL | Operator trust |

---

## Security Mechanisms (18 Total)

### Layer 1 - SENTRY (9)
1. HMAC-SHA256 command signing
2. Nonce-based replay prevention
3. Time-window access control
4. Per-source rate limiting
5. Default-credential watchdog
6. Firmware integrity verification (SHA-256)
7. Merkle-tree audit log
8. Self-integrity monitoring
9. Constant-time credential comparison

### Layer 2 - TWIN (1)
10. Pre-execution digital twin simulation (deep copy)

### Layer 3 - PATTERN (2)
11. Physics rule engine
12. Markov chain sequence anomaly detector

### Layer 4 - IMMUNE (3)
13. SHA-256 attack signature hashing
14. Human-in-the-loop signature approval gate
15. Adaptive learning (sub-millisecond repeat detection)

### Cross-Layer (3)
16. AES-256-GCM encrypted audit log
17. HMAC over log entries (keyed integrity)
18. Startup self-test (fail-closed)

---

## Algorithms Used

| Layer | Main Algorithms / Techniques |
|:---|:---|
| **SENTRY** | HMAC-SHA256, SHA-256, Nonce, Merkle Tree |
| **TWIN** | Digital Twin Simulation (no crypto) |
| **PATTERN** | Physics Rules + Markov Chain |
| **IMMUNE** | SHA-256 + Human-in-the-Loop |
| **Cross-Layer** | AES-256-GCM + HMAC + Fail-Closed Self-Test |

**One-liner:** HMAC-SHA256 and SHA-256 for authenticity/integrity, Markov Chain for anomaly detection, Digital Twin for pre-execution simulation, AES-256-GCM for log encryption.

---

## Real Incidents Countered

- **Ukraine 2015 (BlackEnergy)** -> SENTRY + TWIN
- **Ukraine 2016 (Industroyer)** -> PATTERN + TWIN
- **Triton 2017** -> PATTERN + SENTRY
- **Colonial Pipeline 2021** -> SENTRY
- **Poland 2025** -> SENTRY (credentials + firmware)

---

## Repository Structure

```
Hydra-grid/
|-- src/                        # HYDRA-GRID (5 layers)
|   |-- core/
|   |-- layer1_sentry/
|   |-- layer2_twin/
|   |-- layer3_pattern/
|   |-- layer4_immune/
|   \-- layer5_council/
|
|-- shadow_sentinel/            # Independent watchdog (separate application)
|   |-- sentinel.py
|   |-- backend.py
|   \-- frontend.py
|
|-- tests/                      # 46 automated tests
|-- scripts/
|-- docs/
|-- demo/
|-- infra/
|-- README.md
|-- LICENSE
\-- requirements.txt
```

---

## Quick Start

```bash
# 1. Clone the repository
git clone https://github.com/pradheepa73/Hydra-grid.git
cd Hydra-grid

# 2. Create virtual environment
python -m venv .venv
.venv\Scripts\Activate.ps1              # Windows
# source .venv/bin/activate             # Linux/Mac

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run full pipeline
python scripts/run_full_pipeline.py

# 5. Run all tests
python -m pytest tests/ -v
# Expected: 46 passed

# 6. Launch the main dashboard
streamlit run src/layer5_council/dashboard.py
# Open http://localhost:8501
```

---

## Test Coverage

**46 automated tests** across all 5 layers:

| Test Suite | Tests | Coverage |
|:---|:-:|:---|
| test_layer1_sentry.py | 6 | Crypto, replay, credentials, firmware |
| test_layer2_twin.py | 5 | Cascade, voltage, redundant commands |
| test_layer3_pattern.py | 5 | Physics rules, Markov chain |
| test_layer4_immune.py | 5 | Signatures, approval gate |
| test_layer5_council.py | 5 | Pipeline integration |
| test_honeypot.py | 2 | Honeypot capture |
| test_recovery.py | 3 | Golden image restore |
| test_integration.py | 5 | Cross-layer end-to-end |
| test_sentinel.py | 5 | Shadow Sentinel triggers |
| test_sentinel_integration.py | 5 | Sentinel + HYDRA-GRID end-to-end |

---

## Standards Alignment

| Standard | Alignment |
|:---|:---|
| IEC 62443 | Zones-and-conduits via SENTRY |
| NIST SP 800-82 | OT network defense architecture |
| NERC CIP | Access control, integrity monitoring |
| MITRE ATT&CK for ICS | T0813, T0836, T0855 |
| ISO 27001 | Information security management |

---

## Roadmap - Lab to National Deployment

| Phase | Timeline | Deliverable |
|:-:|:---|:---|
| 1 | Current | Lab prototype (5 layers + Shadow Sentinel) |
| 2 | 6-12 months | Hardware-in-the-loop (real PLC) |
| 3 | 12-24 months | Isolated utility pilot |
| 4 | 24+ months | National deployment (PQC + Federated Learning) |

---

## Limitations (Honest)

| Limitation | Mitigation Path |
|:---|:---|
| No wire encryption (Modbus/DNP3) | Post-Quantum Cryptography (Phase 4) |
| Markov chain can be evaded | Adversarial training (Phase 2) |
| Simplified twin physics | Full AC-OPF integration (Phase 2) |
| IMMUNE requires human approval | By design -- intentional safety feature |
| No hardware validation | Phase 2 of roadmap |
| No formal verification | Phase 4 of roadmap |

---

# Shadow Sentinel

**An Independent Watchdog Application for HYDRA-GRID**

> *"The 5 layers protect the grid. Shadow Sentinel protects the 5 layers."*

Shadow Sentinel is a **completely independent application** -- not a layer inside HYDRA-GRID. It runs as a separate process and monitors the 5 defense layers from the outside.

It acts as a **backup safety net**: if the 5 layers are bypassed, corrupted, or fail silently, Shadow Sentinel is the final line of defense that catches the anomaly and alerts the operator.

It does **not** block commands. It does **not** act autonomously. It **only** observes, evaluates, and raises alerts for human review.

---

## Why It Exists

Every defense system has a fundamental question: **What if the defense itself is compromised?**

If an attacker disables SENTRY, corrupts TWIN, tampers with logs, or bypasses PATTERN -- the 5-layer defense fails silently. Shadow Sentinel is the answer.

**Analogy:** Imagine a military base with 5 security guards. What if a trained team silently takes out all 5? That is why bases also have cameras on a separate circuit. Even if all guards are down, the cameras still see everything. **Shadow Sentinel is that camera.**

---

## Core Principle

Shadow Sentinel sits outside the pipeline. It does not trust the layers. It watches them.

- **HYDRA-GRID (5 layers)** -- port 8501
- **Shadow Sentinel Backend** -- port 8000
- **Shadow Sentinel Frontend** -- port 8502

Three separate processes. Two ports. Zero shared state.

---

## Independence From HYDRA-GRID

Shadow Sentinel is **not Layer 6**. It is not part of HYDRA-GRID's internal pipeline. It is a separate, out-of-band watchdog process.

It runs in a different process, uses different ports (8000 and 8502 vs 8501), and shares zero state with the 5 layers. Its only job is to observe the 5 layers from outside the trust boundary.

If SENTRY, TWIN, PATTERN, IMMUNE, or COUNCIL are compromised, Shadow Sentinel remains isolated and can still detect the compromise and raise an alert for human review.

This is why the architecture is described as "**5 layers + 1 independent watchdog**" rather than "6 layers."

---

## Shadow Sentinel as the Backup Plan

Shadow Sentinel is not just an observer -- it is the **backup plan**.

Every defense system assumes its own layers will work. But what happens if they don't? What if an attacker compromises SENTRY, disables TWIN, tampers with PATTERN, poisons IMMUNE, or blinds COUNCIL? In that scenario, HYDRA-GRID alone cannot protect the grid.

This is why Shadow Sentinel exists as a **separate, independent watchdog**. Even if all 5 layers fail, Shadow Sentinel is still running on a different process, watching from the outside, and ready to raise the alarm.

**The 5 layers are the shield. Shadow Sentinel is the safety net.**

---

## The H-D-I-V-S Trigger Model

Shadow Sentinel stays **silent** during normal operation. It activates only when **2 or more** signals fire together.

| Signal | Meaning | Why It's Dangerous |
|:---|:---|:---|
| **H** -- Heartbeat Loss | A layer stopped sending health signals | Layer may be dead or disabled |
| **D** -- Decision Contradiction | A command that should be blocked was allowed | Layer may be bypassed |
| **I** -- Integrity Failure | Logs or hashes changed | Possible tampering |
| **V** -- View Mismatch | Sentinel sees X, system reports Y | System may be lying |
| **S** -- Sustained Pattern | Unusual activity continues | Increases confidence |

**Rule:** 2 out of 5 triggers it. **One signal is coincidence. Two is compromise.**

---

## Shadow Sentinel Security Mechanisms (10 Total)

**Transport Security:**
1. HMAC-SHA256 request signing
2. Nonce anti-replay
3. 30-second timestamp window
4. Per-key rate limiting (30/min)
5. Constant-time comparison
6. Deny-by-default auth

**Data Integrity:**
7. Hash-chained audit log
8. Tamper detection

**Operational Security:**
9. Human-in-the-loop
10. Key file isolation

---

## Shadow Sentinel Quick Start

**Terminal 1 - Backend:**
```bash
uvicorn shadow_sentinel.backend:app --host 127.0.0.1 --port 8000
```

**Terminal 2 - Frontend:**
```bash
streamlit run shadow_sentinel/frontend.py --server.port 8502
```

**Terminal 3 - Tests:**
```bash
python -m pytest tests/test_sentinel.py -v
```

---

## Shadow Sentinel Trigger Scenarios

**Normal Operation:** All 5 layers heartbeat healthy -> Sentinel silent.

**Compromised Layers:** H + D + I + V + S fire -> Sentinel activates -> Alert queued -> Human review required.

**Single Signal (False Positive):** Only H fires -> Sentinel stays silent -> No false positive.

---

## Shadow Sentinel File Structure

```
shadow_sentinel/
|-- __init__.py       # Package init
|-- sentinel.py       # Core watchdog class (H-D-I-V-S logic)
|-- backend.py        # FastAPI backend (HMAC auth)
\-- frontend.py       # Streamlit operator console
```

---

## About the Team

**Team Name:** PRADHEEPA M  
**Project:** HYDRA-GRID 2026 + Shadow Sentinel  
**Event:** OWASP SREC Cyber Week Hackathon 2026  
**Track:** Defense Tech, Communications & National Security

| Member | Role |
|:---|:---|
| **Pradheepa M** (Team Leader) | Backend & Frontend Developer, Solution Finder, Event Coordinator -- all technical and organizational work |
| **Sangeetha Kumari** | Speaker, PPT Creator, Solution Finder |
| **Ayushi Pandey** | Speaker |
| **Pooja T. T** | Team Member |

---

## Acknowledgments

- OWASP SREC Chapter -- for hosting the hackathon
- iTrust Singapore -- SWaT and WADI datasets (research reference)
- MITRE ATT&CK -- ICS attack pattern taxonomy

---

## License

**All Rights Reserved.** Copyright (c) 2026 PRADHEEPA M.

Public visibility does not grant permission to copy, modify, or distribute.

---

## Author

**Pradheepa M**  
B.Sc. Computer Science with Cybersecurity  
**Team Leader -- HYDRA-GRID 2026**  
pradheepa378@gmail.com  

[![LinkedIn](https://img.shields.io/badge/LinkedIn-0A66C2?style=flat-square&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/pradheepa-m-051728372)
[![GitHub](https://img.shields.io/badge/GitHub-181717?style=flat-square&logo=github&logoColor=white)](https://github.com/pradheepa73/Hydra-grid)
[![Email](https://img.shields.io/badge/Email-D14836?style=flat-square&logo=gmail&logoColor=white)](mailto:pradheepa378@gmail.com)

---

<div align="center">

**Two independent systems. One mission.**

**"Cut one head, two grow back."**

</div>
```

---
