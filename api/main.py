from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Dict, Any, Optional
import os

from agents.planning_agent import PlanningAgent
from adapters.supabase_client import SupabaseClient
from adapters.payments.paymob_adapter import PaymobAdapter
from adapters.document_generator import TypstDocumentGenerator

app = FastAPI(
    title="ASMA-OS V6.0 Autonomous API",
    description="Core API Service bridging Storefront, Founder Screen, DeepSeek AI, Paymob, and Typst Document Engine.",
    version="6.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class PlanRequest(BaseModel):
    goal: str
    budget: float = 1000.0

class InvoiceRequest(BaseModel):
    client_name: str
    invoice_id: str
    amount: float
    currency: str = "EGP"
    services: List[Dict[str, Any]]

class PaymentInitiateRequest(BaseModel):
    amount_cents: int
    currency: str = "EGP"
    email: str
    first_name: str
    last_name: str
    phone_number: str

@app.get("/api/health")
def health_check():
    return {
        "status": "online",
        "system": "ASMA-OS V6.0 Engine",
        "gates_operational": 6,
        "deepseek_configured": bool(os.getenv("DEEPSEEK_API_KEY")),
        "supabase_configured": bool(os.getenv("SUPABASE_URL"))
    }

@app.get("/api/gates")
def get_operational_gates():
    try:
        sb = SupabaseClient()
        gates = sb.get_operational_gates()
        return {"status": "success", "gates": gates}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/plan")
def generate_plan(req: PlanRequest):
    try:
        agent = PlanningAgent()
        plan = agent.generate_plan(req.goal, req.budget)
        return {"status": "success", "plan": plan}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/documents/invoice")
def generate_invoice(req: InvoiceRequest):
    try:
        output_path = f"output/invoices/{req.invoice_id}.pdf"
        data = req.model_dump()
        pdf_file = TypstDocumentGenerator.generate_invoice(data, output_path)
        return {
            "status": "success",
            "invoice_id": req.invoice_id,
            "pdf_path": pdf_file,
            "file_exists": os.path.exists(pdf_file)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/payments/paymob/initiate")
def initiate_payment(req: PaymentInitiateRequest):
    try:
        paymob = PaymobAdapter()
        billing_data = {
            "email": req.email,
            "first_name": req.first_name,
            "last_name": req.last_name,
            "phone_number": req.phone_number
        }
        res = paymob.create_payment_intent(
            amount_cents=req.amount_cents,
            currency=req.currency,
            payment_methods=[1234],
            items=[],
            billing_data=billing_data,
            special_reference=f"REF-{os.urandom(4).hex()}"
        )
        return {"status": "success", "payment_data": res}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/payments/paymob/callback")
async def paymob_callback(request: Request):
    try:
        payload = await request.json()
        paymob = PaymobAdapter()
        supplied_hmac = request.headers.get("x-paymob-hmac", "")
        is_valid = paymob.verify_callback_hmac(payload, supplied_hmac)
        return {"verified": is_valid, "received": True}
    except Exception as e:
        return {"verified": False, "error": str(e)}
