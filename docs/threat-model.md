# Threat Model

## Incidents Countered

| Incident | Year | Vector | Counter |
|:---|:---|:---|:---|
| Ukraine (BlackEnergy) | 2015 | Stolen VPN credentials | SENTRY + TWIN |
| Ukraine (Industroyer) | 2016 | Native ICS protocols | PATTERN + TWIN |
| Triton | 2017 | Safety controller manipulation | PATTERN + SENTRY |
| Colonial Pipeline | 2021 | IT breach to OT shutdown | SENTRY |
| Poland | 2025 | Default credentials + firmware | SENTRY |

## Attack Classes Defended

| Attack | Defense |
|:---|:---|
| Forged commands | HMAC-SHA256 signature verification |
| Replay attacks | Nonce store |
| Off-hours attacks | Time-window access control |
| Burst/flood attacks | Per-source rate limiting |
| Default credentials | Banned-credential watchdog |
| Firmware tampering | SHA-256 integrity check |
| Log tampering | Merkle tree + HMAC |
| Cascade commands | Digital Twin pre-execution simulation |
| Novel sequences | Markov chain anomaly detection |
| Repeat attacks | IMMUNE signature learning |
| Defense-layer compromise | Shadow Sentinel independent watchdog |

## MITRE ATT&CK for ICS Mapping

- T0813 - Denial of Control -> SENTRY + TWIN
- T0836 - Modify Parameter -> PATTERN physics rules
- T0855 - Unauthorized Command Message -> SENTRY signing

## Out of Scope

- Physical access to substation
- Supply chain compromise
- Zero-day exploits in SCADA software
- Insider threat with valid credentials (partial mitigation via human-in-the-loop)

## Standards Alignment

- IEC 62443 (Industrial Cybersecurity)
- NIST SP 800-82 (ICS Security Guide)
- NERC CIP (North American Grid)
- MITRE ATT&CK for ICS
- ISO 27001
