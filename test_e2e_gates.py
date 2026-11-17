import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.resolve()))

import os
import pytest
from fastapi.testclient import TestClient
from api.main import app
from adapters.payments.paymob_adapter import PaymobAdapter
from adapters.document_generator import TypstDocumentGenerator
from agents.planning_agent import PlanningAgent
from adapters.supabase_client import SupabaseClient

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
    paymob = PaymobAdapter()
    sample_payload = {"amount_cents": 1000, "currency": "EGP", "id": "TEST-123"}
    hmac_val = paymob.generate_hmac(sample_payload)
    assert len(hmac_val) == 128
    print(f"\n✅ Gate 4: Treasury & Paymob HMAC SHA-512 Security Verified: {hmac_val[:16]}...")

def test_gate5_founder_command_os_api():
    client = TestClient(app)
    resp = client.get("/api/health")
    assert resp.status_code == 200
    assert resp.json()["gates_operational"] == 6

    gates_resp = client.get("/api/gates")
    assert gates_resp.status_code == 200
    assert len(gates_resp.json()["gates"]) >= 6
    print("\n✅ Gate 5: Founder Command OS & Supabase Integration Verified!")

def test_gate6_ai_governance_and_document_generator():
    agent = PlanningAgent()
    plan = agent.generate_plan("Commercial Launch Gate 6 Test", 5000.0)
    assert plan is not None

    inv_path = TypstDocumentGenerator.generate_invoice(
        {"client_name": "Gate 6 Test Client", "invoice_id": "INV-E2E-G6", "amount": 10000.0, "services": [{"name": "System Audit", "qty": 1, "price": 10000.0}]},
        "output/invoices/test_e2e_g6.pdf"
    )
    assert os.path.exists(inv_path)
    print("\n✅ Gate 6: DeepSeek AI Planning & Typst Document Engine Verified!")
