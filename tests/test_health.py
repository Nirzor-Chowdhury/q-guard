from fastapi.testclient import TestClient

from qguard.main import app

client = TestClient(app)


def test_health_endpoint() -> None:
    response = client.get("/api/v1/health")

    assert response.status_code == 200

    body = response.json()

    assert body["status"] == "ok"
    assert body["service"] == "Q-Guard"
    assert body["environment"] in {
        "development",
        "test",
        "staging",
        "production",
    }


def test_capabilities_endpoint() -> None:
    response = client.get("/api/v1/capabilities")

    assert response.status_code == 200

    body = response.json()

    assert body["control_plane"] == "PHASE_0_READY"
    assert body["qkd"] == "SIMULATOR_NOT_IMPLEMENTED"
    assert body["pqc"] == "CAPABILITY_PROBE_NOT_IMPLEMENTED"
