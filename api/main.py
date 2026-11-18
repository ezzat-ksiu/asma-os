"""Local-first API contracts. Provider operations remain disabled until configured."""
from __future__ import annotations

import os
from fastapi import FastAPI, HTTPException, Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

from asma_os_mesh import ASMASpecificationEngine
from agents.planning_agent import PlanningAgent
from adapters.identity.auth0_verifier import Auth0Verifier

app = FastAPI(title="FOLIAVERE Operations API", description="Private operational API for the FOLIAVERE working name; ASMA-OS is internal infrastructure.", version="6.0.0")
origins = [item.strip() for item in os.getenv("ASMA_CORS_ORIGINS", "").split(",") if item.strip()]
app.add_middleware(CORSMiddleware, allow_origins=origins, allow_credentials=bool(origins), allow_methods=["GET", "POST"], allow_headers=["Authorization", "Content-Type", "Idempotency-Key"])
bearer = HTTPBearer(auto_error=False)

def require_founder(credentials: HTTPAuthorizationCredentials | None = Depends(bearer)):
    if credentials is None:
        raise HTTPException(status_code=401, detail="Authentication required")
    try:
        claims = Auth0Verifier().verify_token(credentials.credentials)
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid or unverifiable access token") from None
    allowed = {subject.strip() for subject in os.getenv("FOUNDER_AUTH0_SUBJECTS", "").split(",") if subject.strip()}
    if not allowed or claims.get("sub") not in allowed:
        raise HTTPException(status_code=403, detail="Founder access is not configured for this subject")
    return claims

class PlanRequest(BaseModel):
    goal: str = Field(min_length=1, max_length=2000)
    budget: float = Field(default=0, ge=0, le=1_000_000)

@app.get("/api/health")
def health_check():
    return {"status": "online", "service": "local-api", "brand_status": "working_name_pending_clearance", "gates_total": 7, "provider_integrations": "not_verified"}

@app.get("/api/gates")
def get_operational_gates():
    gates = ASMASpecificationEngine().spec.business.operational_gates.gates
    return {"status": "success", "gates": [gate.model_dump(mode="json") for gate in gates.values()]}

@app.post("/api/plan")
def generate_plan(req: PlanRequest):
    return {"status": "success", "plan": PlanningAgent().generate_plan(req.goal, req.budget), "mode": "deterministic_local"}

@app.post("/api/documents/invoice", status_code=503)
def generate_invoice():
    raise HTTPException(status_code=503, detail="Invoicing is unavailable until seller identity, tax treatment, and payment records are verified.")

@app.post("/api/payments/paymob/initiate", status_code=503)
def initiate_payment():
    raise HTTPException(status_code=503, detail="Payment initiation is not enabled in this workspace.")

@app.post("/api/payments/paymob/callback", status_code=503)
def paymob_callback():
    raise HTTPException(status_code=503, detail="Payment callbacks are not enabled in this workspace.")

@app.get("/v1/public/vault/{serial}")
def public_vault_record(serial: str):
    # No records are public until explicit consent and reviewed publication data exist.
    raise HTTPException(status_code=404, detail="No approved public record exists for this serial.")

@app.get("/v1/founder/dashboard")
def founder_dashboard(_claims: dict = Depends(require_founder)):
    return {"pending_print_approvals": [], "sla": None, "financial_ledger": None, "artifacts": [], "data_status": "no_verified_operational_records"}

@app.post("/v1/artifacts/{artifact_id}/sign-off", status_code=503)
def sign_off_artifact(artifact_id: str, _claims: dict = Depends(require_founder)):
    raise HTTPException(status_code=503, detail="Artifact signing is unavailable until a protected artifact registry and signing key are configured.")
