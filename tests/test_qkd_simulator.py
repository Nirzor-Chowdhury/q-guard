from qguard.domain.enums import SecurityState
from qguard.services.key_management.qkd_service import QKDKeyManagementService
from qguard.services.qkd.simulator import QKDSimulator


def test_simulator_initial_state():
    sim = QKDSimulator(base_qber=0.01, base_rate=1000.0)
    status = sim.get_status()
    assert status.qber == 0.01
    assert status.key_rate_bps == 1000.0
    assert status.available_key_count > 0

def test_key_consumption():
    sim = QKDSimulator()
    initial_consumed = sim.get_status().consumed_keys
    
    key = sim.request_key()
    assert key is not None
    assert len(key) == 32 # UUID hex is 32 chars
    
    status = sim.get_status()
    assert status.consumed_keys == initial_consumed + 1

def test_depleted_key_pool():
    sim = QKDSimulator()
    sim._fractional_keys = 0.0 # Force depletion of fraction
    sim.available_keys = [] # Force depletion
    assert sim.request_key() is None

def test_qkd_service_state_evaluation():
    svc = QKDKeyManagementService()
    svc.reset_simulator()
    
    assert svc.get_security_state() == SecurityState.NORMAL
    
    svc.inject_noise(0.8)
    assert svc.get_security_state() == SecurityState.DEGRADED
    
    svc.simulate_eavesdropping(True)
    assert svc.get_security_state() == SecurityState.SUSPICIOUS

def test_eavesdropping_qber_spike():
    sim = QKDSimulator(base_qber=0.01)
    sim.set_eavesdropping(True)
    status = sim.get_status()
    assert status.qber >= 0.25
    assert status.eavesdropping_detected is True
