import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.resolve()))

import os
import shutil
import pytest
from fastapi.testclient import TestClient
from adapters.document_generator import TypstDocumentGenerator
from api.main import app

@pytest.mark.skipif(shutil.which("typst") is None, reason="Typst CLI is an optional local publishing dependency")
def test_typst_pdf_compilation():
    data = {
        "client_name": "Fictional sample recipient",
        "invoice_id": "DEMO-PREVIEW-001",
        "amount": 12500.0,
        "currency": "EGP",
        "date": "Not specified",
        "services": [
            {"name": "Fictional sample service", "qty": 1, "price": 10000.0},
            {"name": "Layout preview", "qty": 1, "price": 2500.0}
        ]
    }
    out_pdf = "output/invoices/test_invoice_gate6.pdf"
    res_path = TypstDocumentGenerator.generate_invoice(data, out_pdf)
    assert os.path.exists(res_path)
    assert os.path.getsize(res_path) > 1000
    print(f"\nGenerated demo-only document preview: {res_path} ({os.path.getsize(res_path)} bytes)")

def test_api_health():
    client = TestClient(app)
    res = client.get("/api/health")
    assert res.status_code == 200
    json_data = res.json()
    assert json_data["status"] == "unknown"
    assert json_data["readiness"] == "NOT_CONFIGURED"
    assert json_data["gates_total"] == 7
    print("\n✅ API Health Check Endpoint Verified!")

def test_api_invoice_generation_is_disabled_without_commercial_verification():
    client = TestClient(app)
    res = client.post("/api/documents/invoice", json={})
    assert res.status_code == 503
