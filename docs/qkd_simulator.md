# QKD Simulator & Key Management Interface

## Overview
This subsystem provides a realistic software simulation of a BB84 QKD environment. It models quantum key generation, error rates (QBER), sifting, noise, and eavesdropping.

**IMPORTANT:** This is a purely simulated research environment. It does NOT generate physically secure quantum keys.

## Architecture
- **QKDSimulator**: Generates simulated keys based on configured bitrates, tracking QBER and available key pools.
- **QKDKeyManagementService**: Maps raw simulator telemetry into the Q-Guard `SecurityState` domain (e.g., converting a massive QBER spike into a `SUSPICIOUS` state).

## Replacing with Real Hardware
To connect physical QKD devices:
1. Replace `QKDSimulator` with an ETSI GS QKD 014 / 020 compliant REST client.
2. Update `QKDKeyManagementService` to fetch keys and status from the real KMS rather than the local simulator.
3. Keep the `SecurityState` translation logic intact.

## API Endpoints
- `GET /api/v1/qkd/status`
- `POST /api/v1/qkd/key/consume`
- `POST /api/v1/qkd/simulation/noise`
- `POST /api/v1/qkd/simulation/eavesdrop`
- `POST /api/v1/qkd/simulation/reset`
