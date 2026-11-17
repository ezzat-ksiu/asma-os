"""
ASMA-OS V6.0 Multi-Agent Mesh Fabric and Execution Engine Module.
"""

import asyncio
import uuid
from enum import Enum
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field

from spec_schema import (
    ASMASpec,
    AuditLedger,
    BusinessArchitecture,
    ExecutionArchitecture,
    FinancialModel,
    OperationalGates,
    QualityAndSecurityArchitecture,
    ScalingPolicy,
    TechnicalArchitecture,
)


class MeshNodeType(str, Enum):
    MASTER = "master"
    GATEWAY = "gateway"
    EXECUTION = "execution"
    STORAGE = "storage"
    SECURITY = "security"
    AUDIT = "audit"


class MeshNodeStatus(str, Enum):
    INITIALIZING = "initializing"
    ACTIVE = "active"
    DEGRADED = "degraded"
    FAILED = "failed"
    OFFLINE = "offline"


class MeshMessage(BaseModel):
    msg_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    sender: str
    target: str
    action: str
    payload: Dict[str, Any] = Field(default_factory=dict)
    trace_id: str = Field(default_factory=lambda: str(uuid.uuid4()))


class MeshNode(BaseModel):
    node_id: str
    node_type: MeshNodeType
    status: MeshNodeStatus = MeshNodeStatus.INITIALIZING
    health_score: float = 1.0
    capabilities: List[str] = Field(default_factory=list)

    @staticmethod
    def _clamp_health(score: float) -> float:
        return max(0.0, min(1.0, float(score)))

    def record_health(self, score: float) -> None:
        """Record a measured health score and reflect it in node status."""
        self.health_score = self._clamp_health(score)
        if self.health_score < 0.5:
            self.status = MeshNodeStatus.DEGRADED
        elif self.status in (MeshNodeStatus.INITIALIZING, MeshNodeStatus.DEGRADED):
            self.status = MeshNodeStatus.ACTIVE

    async def process_message(self, msg: MeshMessage) -> Dict[str, Any]:
        if self.status in [MeshNodeStatus.DEGRADED, MeshNodeStatus.FAILED, MeshNodeStatus.OFFLINE]:
            return {
                "status": "error",
                "node_id": self.node_id,
                "reason": "Node unhealthy or offline",
            }
        return {
            "status": "success",
            "node_id": self.node_id,
            "action": msg.action,
            "processed_trace": msg.trace_id,
            "health_score": self.health_score,
        }


class ASMASpecificationEngine:
    def __init__(self, spec: Optional[ASMASpec] = None):
        self.spec = spec or ASMASpec(
            business=BusinessArchitecture(
                vision="Unified Autonomous Execution Operating System",
                strategic_pillars=[
                    "Self-Healing Topology",
                    "Deterministic Security",
                    "Zero-Trust Mesh Routing",
                ],
                operational_gates=OperationalGates(),
                financial_model=FinancialModel(),
            ),
            technical=TechnicalArchitecture(
                scaling_policy=ScalingPolicy(),
                quality_security=QualityAndSecurityArchitecture(),
                audit_ledger=AuditLedger(),
            ),
            execution=ExecutionArchitecture(),
        )

    def validate_gate(self, gate_id: str) -> bool:
        gates = self.spec.business.operational_gates.gates
        if gate_id not in gates:
            return False
        gate = gates[gate_id]
        return gate.status in ["PASSED", "PENDING", "IN_PROGRESS"]

    def evaluate_gate_criteria(
        self, gate_id: str, criteria_results: Dict[str, bool]
    ) -> bool:
        gates = self.spec.business.operational_gates.gates
        if gate_id not in gates:
            return False
        gate = gates[gate_id]
        all_passed = all(criteria_results.get(c) is True for c in gate.criteria)
        if all_passed:
            gate.status = "PASSED"
        else:
            gate.status = "FAILED"
        return all_passed

    def evaluate_gates(self, results_by_gate: Dict[str, Dict[str, bool]]) -> Dict[str, bool]:
        """Evaluate supplied criterion results for multiple gates in one update."""
        return {
            gate_id: self.evaluate_gate_criteria(gate_id, criteria_results)
            for gate_id, criteria_results in results_by_gate.items()
        }

    def evaluate_gate6(
        self,
        self_healing_verified: bool,
        dynamic_scaling_verified: bool,
        financial_sustainability_verified: bool,
    ) -> bool:
        """Evaluate the three Gate 6 controls from observed cycle evidence."""
        gate = self.spec.business.operational_gates.gates.get("G6")
        if gate is None or len(gate.criteria) != 3:
            return False
        results = dict(zip(
            gate.criteria,
            (self_healing_verified, dynamic_scaling_verified, financial_sustainability_verified),
        ))
        return self.evaluate_gate_criteria("G6", results)

    def verify_full_system_completion(self) -> Dict[str, Any]:
        """Report whether every operational gate from G0 through G6 passed."""
        gates = self.spec.business.operational_gates.gates
        required_ids = [f"G{number}" for number in range(7)]
        statuses = {
            gate_id: gates[gate_id].status if gate_id in gates else "MISSING"
            for gate_id in required_ids
        }
        passed = [gate_id for gate_id, status in statuses.items() if status == "PASSED"]
        unpassed = [gate_id for gate_id in required_ids if statuses[gate_id] != "PASSED"]
        complete = not unpassed
        return {
            "complete": complete,
            "all_gates_passed": complete,
            "passed_gates": passed,
            "unpassed_gates": unpassed,
            "gate_statuses": statuses,
        }


class ASMANodeRegistry:
    def __init__(self):
        self.nodes: Dict[str, MeshNode] = {}

    def register_node(self, node: MeshNode) -> None:
        self.nodes[node.node_id] = node

    def unregister_node(self, node_id: str) -> Optional[MeshNode]:
        return self.nodes.pop(node_id, None)

    def get_node(self, node_id: str) -> Optional[MeshNode]:
        return self.nodes.get(node_id)

    def list_active_nodes(self) -> List[MeshNode]:
        return [
            n for n in self.nodes.values() if n.status == MeshNodeStatus.ACTIVE
        ]

    def health_score(self) -> float:
        """Mean health of registered nodes, or 1.0 for an empty mesh."""
        if not self.nodes:
            return 1.0
        return sum(node.health_score for node in self.nodes.values()) / len(self.nodes)


class ASMAMeshFabric:
    def __init__(
        self, engine: ASMASpecificationEngine, registry: ASMANodeRegistry
    ):
        self.engine = engine
        self.registry = registry
        self.audit_log: List[Dict[str, Any]] = []

    async def route_message(self, msg: MeshMessage) -> Dict[str, Any]:
        target_node = self.registry.get_node(msg.target)
        if not target_node:
            return {
                "status": "error",
                "reason": f"Target node '{msg.target}' not registered.",
            }

        # A degraded target can be bypassed by another active node that advertises
        # the requested action. Messages without a capability stay target-specific.
        if target_node.status in (MeshNodeStatus.FAILED, MeshNodeStatus.OFFLINE, MeshNodeStatus.DEGRADED):
            candidates = [n for n in self.registry.list_active_nodes()
                          if msg.action in n.capabilities and n.node_id != msg.target]
            if candidates:
                target_node = max(candidates, key=lambda node: node.health_score)
        res = await target_node.process_message(msg)
        self.audit_log.append(
            {
                "msg_id": msg.msg_id,
                "sender": msg.sender,
                "target": msg.target,
                "routed_to": target_node.node_id,
                "action": msg.action,
                "status": res.get("status"),
            }
        )
        return res

    def self_heal(self) -> List[str]:
        healed_nodes = []
        for node in self.registry.nodes.values():
            if node.status in (MeshNodeStatus.FAILED, MeshNodeStatus.DEGRADED) or node.health_score < 0.5:
                node.status = MeshNodeStatus.ACTIVE
                node.health_score = 1.0
                healed_nodes.append(node.node_id)
        return healed_nodes
