from fastapi import APIRouter, Depends
from pydantic import BaseModel

from qguard.core.config import Settings, get_settings

router = APIRouter(prefix="/api/v1", tags=["system"])


class HealthResponse(BaseModel):
    status: str
    service: str
    version: str
    environment: str
    secure_mode: bool


class CapabilityResponse(BaseModel):
    control_plane: str
    qkd: str
    pqc: str
    secure_tunnel: str
    dashboard: str


@router.get("/health", response_model=HealthResponse)
def health(settings: Settings = Depends(get_settings)) -> HealthResponse:  # noqa: B008
    """
    Basic process health endpoint.

    Database, QKD, PQC, and destination-service health checks are deliberately
    not performed here yet. They will be added as independent subsystem checks.
    """
    return HealthResponse(
        status="ok",
        service=settings.app_name,
        version=settings.app_version,
        environment=settings.environment,
        secure_mode=settings.secure_mode,
    )


@router.get("/capabilities", response_model=CapabilityResponse)
def capabilities() -> CapabilityResponse:
    """Describe which prototype capabilities exist after Phase 0."""
    return CapabilityResponse(
        control_plane="PHASE_0_READY",
        qkd="SIMULATOR_NOT_IMPLEMENTED",
        pqc="CAPABILITY_PROBE_NOT_IMPLEMENTED",
        secure_tunnel="NOT_IMPLEMENTED",
        dashboard="API_ONLY",
    )
