# HYDRA-GRID 2026

A Self-Learning Cyber-Physical Defense Grid for National Smart Substations

> Cut One Head. It Grows Stronger.

## Overview

HYDRA-GRID is a software-only, 5-layer defense framework that protects smart grid
substations from nation-state cyber-physical attacks. It implements the full
Prevent -> Simulate -> Detect -> Learn -> Explain loop on commodity hardware.

## The 5 Layers (S-T-P-I-C)

| Layer | Name | Role |
|:-:|:---|:---|
| 1 | SENTRY | Zero Trust gate with 9 integrated defenses |
| 2 | TWIN | Digital-twin pre-execution simulation |
| 3 | PATTERN | Physics rules + Markov sequence detection |
| 4 | IMMUNE | Adaptive attack signature learner |
| 5 | COUNCIL | Explainable AI dashboard |

## Real Incidents Countered

- Ukraine 2015 (BlackEnergy) -> SENTRY + TWIN
- Ukraine 2016 (Industroyer) -> PATTERN + TWIN
- Triton 2017 -> PATTERN + SENTRY
- Colonial Pipeline 2021 -> SENTRY
- Poland 2025 -> SENTRY (credentials + firmware)

## Quick Start

    pip install -r requirements.txt
    python scripts/run_full_pipeline.py
    python -m pytest tests/ -v
    streamlit run src/layer5_council/dashboard.py

## Test Coverage

26 automated tests across all 5 layers.

## Team

- M1 - AI and Simulation
- M2 - Network and Recovery
- M3 - UI and Documentation

## License

MIT
