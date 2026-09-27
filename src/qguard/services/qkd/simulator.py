import time
import uuid

from pydantic import BaseModel, ConfigDict

# QKD SIMULATION / RESEARCH MODE
# This is a defensive research prototype running locally. 
# Do NOT claim that this simulator is a physical implementation of QKD.

class QKDStatus(BaseModel):
    model_config = ConfigDict(extra="forbid")
    qber: float
    key_rate_bps: float
    available_key_count: int
    generated_keys: int
    consumed_keys: int
    noise_level: float
    eavesdropping_detected: bool
    channel_status: str
    timestamp: float

class QKDSimulator:
    """Configurable BB84-style simulator for research purposes."""
    
    def __init__(self, base_qber: float = 0.02, base_rate: float = 1000.0):
        self.base_qber = base_qber
        self.base_rate = base_rate
        self._reset_state()
        
    def _reset_state(self) -> None:
        self.qber = self.base_qber
        self.key_rate_bps = self.base_rate
        self.available_keys: list[str] = []
        self.generated_keys_count = 0
        self.consumed_keys_count = 0
        self.noise_level = 0.01
        self.eavesdropping_detected = False
        self.channel_status = "UP"
        self._fractional_keys = 0.0
        
        # Pre-generate some keys
        self._simulate_time_passage(1.0)
        
    def _simulate_time_passage(self, seconds: float = 1.0) -> None:
        """Simulate raw key generation, sifting, and final key pooling."""
        if self.channel_status == "DOWN":
            return
            
        # Simulate base generation rate minus QBER/noise losses
        effective_rate = self.key_rate_bps * (1.0 - self.qber)
        self._fractional_keys += (effective_rate * seconds) / 256.0
        keys_to_generate = int(self._fractional_keys)
        self._fractional_keys -= keys_to_generate
        
        for _ in range(keys_to_generate):
            self.available_keys.append(uuid.uuid4().hex)
            self.generated_keys_count += 1
            
    def get_status(self) -> QKDStatus:
        self._simulate_time_passage(0.1) # Tiny simulation tick
        return QKDStatus(
            qber=self.qber,
            key_rate_bps=self.key_rate_bps,
            available_key_count=len(self.available_keys),
            generated_keys=self.generated_keys_count,
            consumed_keys=self.consumed_keys_count,
            noise_level=self.noise_level,
            eavesdropping_detected=self.eavesdropping_detected,
            channel_status=self.channel_status,
            timestamp=time.time()
        )
        
    def request_key(self) -> str | None:
        """Request and consume a single key from the pool."""
        self._simulate_time_passage(0.1)
        if not self.available_keys:
            return None
        key = self.available_keys.pop(0)
        self.consumed_keys_count += 1
        return key

    def set_noise(self, level: float) -> None:
        """Inject simulated noise into the quantum channel."""
        self.noise_level = min(1.0, max(0.0, level))
        self.qber = self.base_qber + (self.noise_level * 0.1)
        self.key_rate_bps = self.base_rate * (1.0 - self.noise_level)
        
    def set_eavesdropping(self, active: bool) -> None:
        """Simulate an eavesdropper measuring the quantum states."""
        self.eavesdropping_detected = active
        if active:
            # Eavesdropping causes a massive spike in QBER (around 25% minimum for BB84)
            self.qber = max(0.25, self.qber + 0.25)
            self.key_rate_bps *= 0.1
        else:
            self.qber = self.base_qber + (self.noise_level * 0.1)
            self.key_rate_bps = self.base_rate * (1.0 - self.noise_level)
            
    def reset(self) -> None:
        self._reset_state()

# Global simulator instance for Phase 1
simulator = QKDSimulator()
