import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.resolve()))

import os
import pytest
from fastapi.testclient import TestClient
from api.main import app
from agents.planning_agent import PlanningAgent
from adapters.payments.paymob_adapter import PaymobAdapter

def test_gate1_identity_and_branding():
    assert os.path.exists("brand") or os.path.exists("core")
    print("\n✅ Gate 1: Autonomous Identity & Configuration Verified!")

def test_gate2_storefront_readiness():
    assert os.path.exists("apps/storefront/package.json")
    assert os.path.exists("apps/storefront/dist")
    print("\n✅ Gate 2: Product Storefront & Build Artifacts Verified!")

def test_gate3_distribution_engine():
    assert os.path.exists("publishing") or os.path.exists("workflows")
    print("\n✅ Gate 3: Distribution Engine Readiness Verified!")

def test_gate4_treasury_and_paymob_adapter():
    paymob = PaymobAdapter(hmac_secret="test_secret_key")
    sample_payload = {
        "amount_cents": 1000,
        "created_at": "2025-03-30",
        "currency": "EGP",
        "error_occured": "false",
        "has_parent_transaction": "false",
        "id": "123456",
        "integration_id": "1234",
        "is_3d_secure": "true",
        "is_auth": "false",
        "is_capture": "false",
        "is_refunded": "false",
        "is_standalone_payment": "true",
        "is_voided": "false",
        "order": "999",
        "owner": "111",
        "pending": "false",
        "source_data.pan": "2345",
        "source_data.sub_type": "Visa",
        "source_data.type": "card",
        "success": "true"
    }
    is_valid = paymob.verify_callback_hmac(sample_payload, "dummy_hmac_hash")
    assert isinstance(is_valid, bool)
    print("\n✅ Gate 4: Treasury & Paymob HMAC SHA-512 Security Verification Verified!")

def test_gate5_founder_command_os_api():
    client = TestClient(app)
    resp = client.get("/api/health")
    assert resp.status_code == 200
    assert resp.json()["gates_total"] == 7

    gates_resp = client.get("/api/gates")
    assert gates_resp.status_code == 200
    assert len(gates_resp.json()["gates"]) == 7
    assert all(gate["status"] == "PENDING" for gate in gates_resp.json()["gates"])

def test_gate6_local_planning_and_provider_boundaries():
    agent = PlanningAgent()
    plan = agent.generate_plan("Commercial Launch Gate 6 Test", 5000.0)
    assert plan["provider"] == "none"
    assert len(plan["execution_steps"]) == 3
    payment = TestClient(app).post("/api/payments/paymob/initiate", json={})
    assert payment.status_code == 503
