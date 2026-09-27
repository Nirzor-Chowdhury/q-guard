from pydantic import BaseModel, ConfigDict, Field

from qguard.domain.enums import SecurityMode, SecurityState


class SecuritySnapshot(BaseModel):
    """Common telemetry shape shared by later modules."""

    model_config = ConfigDict(extra="forbid")

    connection_id: str
    state: SecurityState = SecurityState.NORMAL
    security_mode: SecurityMode | None = None

    tls_version: str | None = None
    key_exchange_group: str | None = None
    certificate_fingerprint: str | None = None

    pqc_available: bool = False
    qkd_available: bool = False
    qber: float | None = Field(default=None, ge=0.0, le=1.0)
    qkd_key_rate_bits_per_second: float | None = Field(default=None, ge=0.0)

    anomaly_score: float | None = Field(default=None, ge=0.0, le=1.0)
