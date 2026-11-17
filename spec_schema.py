"""Validated Pydantic v2 models for the ASMA-OS 6.0 specification."""

from datetime import datetime, timezone
from enum import Enum
from typing import Any

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator


class ASMABaseModel(BaseModel):
    model_config = ConfigDict(validate_assignment=True, use_enum_values=True, extra="forbid")


class GateStatus(str, Enum):
    PENDING = "PENDING"
    IN_PROGRESS = "IN_PROGRESS"
    PASSED = "PASSED"
    FAILED = "FAILED"


class GateDetail(ASMABaseModel):
    gate_id: str
    name: str
    description: str
    criteria: list[str] = Field(min_length=1)
    status: GateStatus = GateStatus.PENDING


_GATE_INFO = {
    "G0": ("Economic & Engineering Feasibility", "Zero-cost setup, unit economics validation, initial mesh schema", ["Zero upfront software cost", "Positive unit economics projection", "Schema validation passed"]),
    "G1": ("Core Mesh & Agent Protocol", "MCP server operational, local agent mesh communication, self-healing routing", ["MCP server responds to queries", "Node registry active", "Self-healing trigger verified"]),
    "G2": ("Autonomous Task Orchestration", "Workflow execution, state persistence, deterministic fallback", ["Multi-agent workflow execution", "State checkpointing verified", "Fallback logic on error"]),
    "G3": ("Security, Quality & Compliance", "Zero-trust authentication, static analysis, unit test coverage", ["Unit test coverage >= 95%", "Static security scan clean", "Audit ledger operational"]),
    "G4": ("Production Readiness & CI/CD", "Automated deployment pipeline, scaling policy, health monitoring", ["CI/CD pipeline configuration verified", "Scaling policy limits enforced", "Health checks passing"]),
    "G5": ("Commercial Launch & Market Fit", "User onboarding, monetization engine, SLA compliance", ["First customer onboarded", "Payment integration verified", "SLA >= 99.9%"]),
    "G6": ("Self-Sustaining Autonomous Expansion", "Automated scaling, dynamic resource allocation, continuous self-healing", ["Self-healing without human intervention", "Dynamic node auto-scaling", "Financial sustainability confirmed"]),
}


def _default_gates() -> dict[str, GateDetail]:
    return {key: GateDetail(gate_id=key, name=name, description=description, criteria=criteria)
            for key, (name, description, criteria) in _GATE_INFO.items()}


class OperationalGates(ASMABaseModel):
    gates: dict[str, GateDetail] = Field(default_factory=_default_gates)

    @model_validator(mode="after")
    def check_gate_keys(self):
        for key, gate in self.gates.items():
            if key != gate.gate_id:
                raise ValueError(f"gate key {key!r} does not match gate_id {gate.gate_id!r}")
        return self


class FinancialModel(ASMABaseModel):
    target_arr_usd: float = Field(default=1_000_000.0, ge=0)
    cac_payback_months: int = Field(default=6, ge=0)
    gross_margin_target_pct: float = Field(default=80.0, ge=0, le=100)
    max_upfront_budget_usd: float = Field(default=0.0, ge=0)


class BusinessArchitecture(ASMABaseModel):
    vision: str = "Unified Autonomous Execution Operating System"
    strategic_pillars: list[str] = Field(default_factory=lambda: ["Self-Healing Topology", "Deterministic Security", "Zero-Trust Mesh Routing"])
    operational_gates: OperationalGates = Field(default_factory=OperationalGates)
    financial_model: FinancialModel = Field(default_factory=FinancialModel)


class ScalingPolicy(ASMABaseModel):
    auto_scale_enabled: bool = True
    min_nodes: int = Field(default=3, ge=1)
    max_nodes: int = Field(default=100, ge=1)
    cpu_threshold_pct: float = Field(default=80.0, ge=0, le=100)
    memory_threshold_pct: float = Field(default=85.0, ge=0, le=100)

    @model_validator(mode="after")
    def validate_node_range(self):
        if self.min_nodes > self.max_nodes:
            raise ValueError("min_nodes must not exceed max_nodes")
        return self


class QualityAndSecurityArchitecture(ASMABaseModel):
    unit_test_coverage_min: float = Field(default=95.0, ge=0, le=100)
    security_level: str = "ZERO_TRUST"
    compliance_frameworks: list[str] = Field(default_factory=lambda: ["SOC2", "GDPR", "ISO27001"])


class AuditEntry(ASMABaseModel):
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    actor: str = Field(min_length=1)
    action: str = Field(min_length=1)
    details: dict[str, Any] = Field(default_factory=dict)


class AuditLedger(ASMABaseModel):
    status: str = "ACTIVE"
    entries: list[AuditEntry] = Field(default_factory=list)


class TechnicalArchitecture(ASMABaseModel):
    scaling_policy: ScalingPolicy = Field(default_factory=ScalingPolicy)
    quality_security: QualityAndSecurityArchitecture = Field(default_factory=QualityAndSecurityArchitecture)
    audit_ledger: AuditLedger = Field(default_factory=AuditLedger)


class ExecutionArchitecture(ASMABaseModel):
    orchestration_engine: str = "LangGraph"
    protocol: str = "MCP"
    mesh_topology: str = "P2P_Cluster"


class ASMASpec(ASMABaseModel):
    version: str = "6.0"
    business: BusinessArchitecture = Field(default_factory=BusinessArchitecture)
    technical: TechnicalArchitecture = Field(default_factory=TechnicalArchitecture)
    execution: ExecutionArchitecture = Field(default_factory=ExecutionArchitecture)


class Architecture(ASMABaseModel):
    """Compatibility container for callers that group the three architectures."""
    business: BusinessArchitecture = Field(default_factory=BusinessArchitecture)
    technical: TechnicalArchitecture = Field(default_factory=TechnicalArchitecture)
    execution: ExecutionArchitecture = Field(default_factory=ExecutionArchitecture)

