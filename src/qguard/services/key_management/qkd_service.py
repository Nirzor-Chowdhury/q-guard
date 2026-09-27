
from qguard.domain.enums import SecurityState
from qguard.services.qkd.simulator import QKDStatus, simulator


class QKDKeyManagementService:
    """Service to interface with QKD hardware or simulator."""
    
    def __init__(self, max_normal_qber: float = 0.08, min_suspicious_qber: float = 0.20):
        self.max_normal_qber = max_normal_qber
        self.min_suspicious_qber = min_suspicious_qber
        
    def get_status(self) -> QKDStatus:
        return simulator.get_status()
        
    def consume_key(self) -> str | None:
        return simulator.request_key()
        
    def get_security_state(self) -> SecurityState:
        """Evaluate QKD telemetry and return a SecurityState."""
        status = self.get_status()
        
        if status.eavesdropping_detected or status.qber >= self.min_suspicious_qber:
            return SecurityState.SUSPICIOUS
            
        if status.qber > self.max_normal_qber or status.noise_level > 0.5:
            return SecurityState.DEGRADED
            
        return SecurityState.NORMAL

    def inject_noise(self, level: float) -> None:
        simulator.set_noise(level)
        
    def simulate_eavesdropping(self, active: bool) -> None:
        simulator.set_eavesdropping(active)
        
    def reset_simulator(self) -> None:
        simulator.reset()

qkd_service = QKDKeyManagementService()
