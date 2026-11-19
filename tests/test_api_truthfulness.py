"""Regression tests for truthful, fail-closed API status reporting."""

from fastapi.testclient import TestClient

from api.main import _parse_allowed_origins, app


client = TestClient(app)


def test_health_does_not_claim_unverified_readiness():
    response = client.get("/api/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "unknown"
    assert data["readiness"] == "NOT_CONFIGURED"
    assert data["gates_total"] == 7
    assert data["gates_passed"] == 0


def test_gates_default_to_pending_without_evidence():
    response = client.get("/api/gates")
    assert response.status_code == 200
    gates = response.json()["gates"]
    assert len(gates) == 7
    assert {gate["id"] for gate in gates} == {f"G{i}" for i in range(7)}
    assert all(gate["status"] == "PENDING" for gate in gates)
    assert all(gate["evidence"] == [] for gate in gates)


def test_payment_endpoint_fails_closed_without_attempting_transaction():
    response = client.post("/api/payments/paymob/initiate", json={})
    assert response.status_code == 503
    assert "not configured" in response.json()["detail"].lower()


def test_invoice_generation_fails_closed_without_verified_order():
    response = client.post("/api/documents/invoice", json={})
    assert response.status_code == 503
    assert "no financial document was issued" in response.json()["detail"].lower()


def test_cors_is_not_wildcard_by_default():
    response = client.options(
        "/api/health",
        headers={"Origin": "https://untrusted.example", "Access-Control-Request-Method": "GET"},
    )
    assert "access-control-allow-origin" not in response.headers


def test_cors_rejects_wildcard_origin_configuration():
    import pytest

    with pytest.raises(RuntimeError, match="must not contain a wildcard"):
        _parse_allowed_origins("https://store.example, *")


def test_root_identifies_name_as_provisional():
    data = client.get("/").json()
    assert "provisional" in data["brand"].lower()
    assert "clearance pending" in data["brand"].lower()
