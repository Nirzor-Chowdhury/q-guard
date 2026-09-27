from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from qguard.domain.enums import SecurityState
from qguard.services.key_management.qkd_service import qkd_service
from qguard.services.qkd.simulator import QKDStatus

router = APIRouter(prefix="/api/v1/qkd", tags=["qkd"])

class KeyResponse(BaseModel):
    key_material: str
    security_state: SecurityState

class SimulationRequest(BaseModel):
    level: float = 0.0
    active: bool = False

@router.get("/status", response_model=QKDStatus)
def get_status() -> QKDStatus:
    return qkd_service.get_status()

@router.post("/key/consume", response_model=KeyResponse)
def consume_key() -> KeyResponse:
    state = qkd_service.get_security_state()
    key = qkd_service.consume_key()
    
    if not key:
        raise HTTPException(status_code=503, detail="No QKD keys available in pool")
        
    return KeyResponse(key_material=key, security_state=state)

@router.post("/simulation/noise")
def inject_noise(req: SimulationRequest) -> dict:
    qkd_service.inject_noise(req.level)
    return {"status": "noise injected", "level": req.level}

@router.post("/simulation/eavesdrop")
def simulate_eavesdrop(req: SimulationRequest) -> dict:
    qkd_service.simulate_eavesdropping(req.active)
    return {"status": "eavesdropping simulation updated", "active": req.active}

@router.post("/simulation/reset")
def reset_simulator() -> dict:
    qkd_service.reset_simulator()
    return {"status": "simulator reset"}
