"""Mesh and audit-ledger health aggregation."""

from __future__ import annotations

import math
from typing import Any

from asma_os_mesh import ASMANodeRegistry, MeshNodeStatus
from core.audit import CryptoAuditLedger


class HealthMonitor:
    """Aggregate node availability, node scores, and audit integrity."""

    def __init__(self, readiness_threshold: float = 90.0) -> None:
        if not 0 <= readiness_threshold <= 100:
            raise ValueError("readiness_threshold must be between 0 and 100")
        self.readiness_threshold = readiness_threshold

    def check_system_health(
        self,
        registry: ASMANodeRegistry,
        audit_ledger: CryptoAuditLedger,
    ) -> dict[str, Any]:
        nodes = list(registry.nodes.values())
        active_nodes = [node for node in nodes if node.status == MeshNodeStatus.ACTIVE]
        total = len(nodes)
        normalized_health = []
        for node in nodes:
            try:
                score = float(node.health_score)
                normalized_health.append(max(0.0, min(1.0, score)) if math.isfinite(score) else 0.0)
            except (TypeError, ValueError):
                normalized_health.append(0.0)
        node_health_score = sum(normalized_health) / total if total else 0.0
        active_ratio = len(active_nodes) / total if total else 0.0
        ledger_integrity = audit_ledger.verify_integrity()
        readiness_score = round(
            (node_health_score * 50.0) + (active_ratio * 20.0) + (30.0 if ledger_integrity else 0.0),
            2,
        )
        ready = (
            total > 0
            and len(active_nodes) == total
            and ledger_integrity
            and readiness_score >= self.readiness_threshold
        )
        return {
            "ready": ready,
            "overall_readiness_score": readiness_score,
            "readiness_score": readiness_score,
            "active_nodes": len(active_nodes),
            "total_nodes": total,
            "average_node_health": round(node_health_score, 4),
            "ledger_integrity": ledger_integrity,
            "components": {
                "mesh": "HEALTHY" if total and len(active_nodes) == total and node_health_score >= 0.8 else "DEGRADED",
                "audit_ledger": "HEALTHY" if ledger_integrity else "FAILED",
            },
        }
