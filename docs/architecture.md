# Q-Guard Architecture

## Purpose

Q-Guard is a local research prototype for an adaptive security gateway combining:

- TLS 1.3 telemetry
- Post-quantum cryptography capability detection
- Simulated QKD/KMS telemetry
- MITM and downgrade detection
- Fail-safe security policy
- Monitoring and reproducible experiments

## Data flow

1. A client connects to the Q-Guard gateway.
2. The handshake analyzer records TLS and certificate metadata.
3. The MITM detection engine evaluates deterministic and statistical findings.
4. The adaptive key-management engine evaluates QKD and PQC availability.
5. The policy engine selects an action.
6. The secure tunnel either continues, re-authenticates, changes security mode,
   requests new keys, or terminates the connection.
7. Telemetry is written to the monitoring and audit subsystems.

## Security states

- NORMAL
- DEGRADED
- SUSPICIOUS
- MITM_SUSPECTED
- BLOCKED

## Security modes

- QKD_ASSISTED
- PQC_ONLY
- HYBRID

Classical-only fallback is not an approved security mode.

## Prototype boundaries

### Real

- FastAPI control plane
- Configuration validation
- PostgreSQL integration
- TLS metadata processing
- Policy evaluation
- Audit events
- Metrics
- Local forwarding

### Simulated

- BB84/QKD behavior
- QBER
- Key generation rate
- Key pool availability
- KMS outages
- QKD noise/eavesdropping conditions

### Research

- Adaptive security-state scoring
- Combined TLS/QKD/PQC anomaly detection
- Hybrid orchestration
- Reproducible attack/degradation experiments

## Planned service boundaries

- `services/analyzer`: TLS and certificate analysis
- `services/detection`: deterministic and ML-based detection
- `services/key_management`: security-mode selection
- `services/policy`: fail-safe decisions
- `services/qkd`: replaceable QKD/KMS adapter
- `services/pqc`: ML-KEM/ML-DSA capability and operation adapters
- `services/tunnel`: controlled secure forwarding
- `services/telemetry`: event and metrics collection
- `persistence`: SQLAlchemy models and repositories
