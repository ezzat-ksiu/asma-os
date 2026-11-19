"""ASMA-OS API with evidence-based status and disabled transaction boundaries."""

from __future__ import annotations

import os
from typing import Any

from fastapi import Depends, FastAPI, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from fastapi.middleware.cors import CORSMiddleware

from spec_schema import ASMASpec, GateStatus
from adapters.identity.auth0_verifier import Auth0Verifier
from core.auth import AuthenticationNotConfigured, AuthenticationRejected, authorize_founder_token


app = FastAPI(
    title="ASMA-OS API",
    description="Local development API. Operational capabilities are reported only when evidence is configured.",
    version="6.0.0",
    docs_url=None if os.getenv("ASMA_ENV", "").lower() == "production" else "/docs",
    redoc_url=None if os.getenv("ASMA_ENV", "").lower() == "production" else "/redoc",
    openapi_url=None if os.getenv("ASMA_ENV", "").lower() == "production" else "/openapi.json",
)

# No browser origins are trusted by default. Configure an explicit comma-separated
# allowlist for a deployment; credentials are never combined with wildcard CORS.
def _parse_allowed_origins(value: str) -> list[str]:
    origins = [origin.strip() for origin in value.split(",") if origin.strip()]
    if "*" in origins:
        raise RuntimeError("ASMA_CORS_ALLOWED_ORIGINS must not contain a wildcard")
    return origins


allowed_origins = _parse_allowed_origins(os.getenv("ASMA_CORS_ALLOWED_ORIGINS", ""))
if allowed_origins:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=allowed_origins,
        allow_credentials=True,
        allow_methods=["GET", "POST"],
        allow_headers=["Authorization", "Content-Type", "Idempotency-Key"],
    )

# Gate status is deliberately not inferred from scaffold presence or test count.
# A gate remains PENDING until an evidence-backed evaluator is connected.
_spec = ASMASpec()
_bearer = HTTPBearer(auto_error=False)


def _gate_payload() -> list[dict[str, Any]]:
    return [
        {
            "id": gate_id,
            "name": gate.name,
            "description": gate.description,
            "criteria": gate.criteria,
            "status": gate.status.value if isinstance(gate.status, GateStatus) else gate.status,
            "evidence": [],
        }
        for gate_id, gate in _spec.business.operational_gates.gates.items()
    ]


@app.get("/")
def read_root() -> dict[str, str]:
    return {
        "status": "available",
        "brand": "FOLIAVERE (provisional; clearance pending)",
        "system": "ASMA-OS",
        "health": "/api/health",
        "gates": "/api/gates",
    }


@app.get("/health")
@app.get("/api/health")
def health_check() -> dict[str, Any]:
    gates = _gate_payload()
    return {
        "status": "unknown",
        "readiness": "NOT_CONFIGURED",
        "version": "6.0.0",
        "brand": "FOLIAVERE (provisional; clearance pending)",
        "gates_total": len(gates),
        "gates_passed": sum(gate["status"] == "PASSED" for gate in gates),
        "components": {"database": "NOT_CONFIGURED", "providers": "NOT_CONFIGURED"},
    }


@app.get("/api/gates")
def get_gates() -> dict[str, Any]:
    return {"gates": _gate_payload()}


def require_founder_identity(
    credentials: HTTPAuthorizationCredentials | None = Depends(_bearer),
) -> dict[str, str]:
    allowed_subjects = [
        item.strip()
        for item in os.getenv("ASMA_FOUNDER_SUBJECTS", "").split(",")
        if item.strip()
    ]
    if not os.getenv("AUTH0_DOMAIN") or not os.getenv("AUTH0_AUDIENCE") or not allowed_subjects:
        raise HTTPException(status_code=503, detail="Founder authentication is not configured")
    if credentials is None or credentials.scheme.lower() != "bearer":
        raise HTTPException(status_code=401, detail="Bearer authentication required", headers={"WWW-Authenticate": "Bearer"})
    try:
        return authorize_founder_token(credentials.credentials, Auth0Verifier(), allowed_subjects)
    except AuthenticationNotConfigured:
        raise HTTPException(status_code=503, detail="Founder authentication is not configured") from None
    except AuthenticationRejected:
        raise HTTPException(status_code=401, detail="Founder authentication failed", headers={"WWW-Authenticate": "Bearer"}) from None


@app.get("/api/founder/summary")
def founder_summary(identity: dict[str, str] = Depends(require_founder_identity)) -> dict[str, Any]:
    """Authenticated founder surface; business data remains absent until persisted."""
    return {
        "subject": identity["subject"],
        "data_status": "NOT_CONFIGURED",
        "print_approvals": "NOT_CONFIGURED",
        "financial_ledger": "NOT_CONFIGURED",
        "sla_measurements": "NOT_CONFIGURED",
    }


@app.post("/api/payments/paymob/initiate", status_code=503)
def disabled_payment_initiation() -> None:
    """Fail closed until payment credentials and an approved checkout exist."""
    raise HTTPException(
        status_code=503,
        detail="Payment initiation is not configured. No transaction was attempted.",
    )


@app.post("/api/documents/invoice", status_code=503)
def disabled_invoice_generation() -> None:
    """Do not issue financial documents without a verified order and ledger."""
    raise HTTPException(
        status_code=503,
        detail="Invoice generation is not configured. No financial document was issued.",
    )
