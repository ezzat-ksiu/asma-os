import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.resolve()))

import os
import pytest
from fastapi.testclient import TestClient
from adapters.document_generator import TypstDocumentGenerator
from api.main import app

def test_typst_pdf_compilation():
    data = {
        "client_name": "Ezzat - King Salman University",
        "invoice_id": "INV-2025-GATE6",
        "amount": 12500.0,
        "currency": "EGP",
        "date": "2025-03-30",
        "verification_hash": "SHA512-VERIFIED-GATE6",
        "services": [
            {"name": "ASMA-OS V6.0 Enterprise Setup", "qty": 1, "price": 10000.0},
            {"name": "Typst Document Engine Module", "qty": 1, "price": 2500.0}
        ]
    }
    out_pdf = "output/invoices/test_invoice_gate6.pdf"
    res_path = TypstDocumentGenerator.generate_invoice(data, out_pdf)
    assert os.path.exists(res_path)
    assert os.path.getsize(res_path) > 1000
    print(f"\n📄 Generated Live PDF Invoice: {res_path} ({os.path.getsize(res_path)} bytes)")

def test_api_health():
    client = TestClient(app)
    res = client.get("/api/health")
    assert res.status_code == 200
    json_data = res.json()
    assert json_data["status"] == "online"
    assert json_data["gates_operational"] == 6
    print("\n✅ API Health Check Endpoint Verified!")

def test_api_invoice_generation():
    client = TestClient(app)
    req_body = {
        "client_name": "Ezzat Storefront Client",
        "invoice_id": "INV-API-TEST-001",
        "amount": 5000.0,
        "currency": "EGP",
        "services": [
            {"name": "Automated E-commerce Flow", "qty": 1, "price": 5000.0}
        ]
    }
    res = client.post("/api/documents/invoice", json=req_body)
    assert res.status_code == 200
    data = res.json()
    assert data["status"] == "success"
    assert data["file_exists"] is True
    print("\n✅ API PDF Document Generation Endpoint Verified!")
