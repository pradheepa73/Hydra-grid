# Architecture

HYDRA-GRID is a software-only, 5-layer defense framework for smart grid substations. Every command passes through the pipeline in strict order.

## Command Flow

    Command -> SENTRY -> IMMUNE -> PATTERN -> TWIN -> ALLOW / BLOCK

## The 5 Layers

### Layer 1 - SENTRY
Zero Trust gate. Enforces cryptographic command signing, nonce-based replay prevention, time-window access control, per-source rate limiting, default-credential watchdog, firmware integrity, Merkle-tree audit log, self-integrity monitoring, and constant-time credential comparison.

### Layer 2 - TWIN
Digital twin pre-execution simulation. Deep-copies the grid state, applies the command to the copy, checks for physics violations. Blocks the command if the simulation shows a cascade or voltage collapse below the safe floor.

### Layer 3 - PATTERN
Physics rule engine + Markov chain sequence detector. Blocks impossible commands and flags low-probability sequences.

### Layer 4 - IMMUNE
Adaptive attack signature learner. Every blocked attack is hashed into a SHA-256 signature. The next attempt is matched in under 1 millisecond. Requires human approval for signature deployment.

### Layer 5 - COUNCIL
Unified pipeline + Streamlit operator dashboard. Plain-English explanations for every decision.

## Shadow Sentinel (Independent)

Shadow Sentinel is NOT a layer of HYDRA-GRID. It runs as a separate application in a different process, on different ports (8000 backend, 8502 frontend), sharing zero state with the 5 layers.

It monitors the 5 layers using the H-D-I-V-S trigger model:

- H - Heartbeat Loss
- D - Decision Contradiction
- I - Integrity Failure
- V - View Mismatch
- S - Sustained Pattern

Rule: 2 or more signals fire together -> activate -> alert the operator.

## Fail-Safe Design

- If HYDRA-GRID crashes -> SENTRY fails closed (IT to OT commands blocked).
- If TWIN is unavailable -> PATTERN rules still apply.
- If IMMUNE is unavailable -> falls back to last known good signatures.
- If dashboard fails -> grid continues operating.
