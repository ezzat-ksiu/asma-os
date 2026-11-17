"""Autonomous self-healing, scaling, SLA, and financial expansion cycles."""

from __future__ import annotations

import asyncio
from copy import deepcopy
import math
from typing import Any, Callable

from asma_os_mesh import ASMAMeshFabric, ASMASpecificationEngine, MeshNodeStatus
from core.audit import CryptoAuditLedger
from core.scaling import ScalingEngine
from core.sla import SLAMonitor
from services.commercial import TenantOnboardingService


class AutonomousExpansionEngine:
    """Run repeatable operating cycles with auditable, local-only decisions."""

    def __init__(
        self,
        audit_ledger: CryptoAuditLedger | None = None,
        workload_metrics_provider: Callable[[Any], dict[str, float]] | None = None,
        specification_engine: ASMASpecificationEngine | None = None,
        required_sla_pct: float = 99.9,
    ) -> None:
        if not math.isfinite(required_sla_pct) or not 0 <= required_sla_pct <= 100:
            raise ValueError("required_sla_pct must be between 0 and 100")
        self.audit_ledger = audit_ledger or CryptoAuditLedger()
        self.workload_metrics_provider = workload_metrics_provider
        self.specification_engine = specification_engine
        self.required_sla_pct = required_sla_pct
        self._cycle_count = 0
        self._last_cycle: dict[str, Any] | None = None
        self._continuous_running = False

    @staticmethod
    def _safe_metric(value: Any) -> float | None:
        try:
            number = float(value)
        except (TypeError, ValueError):
            return None
        return number if math.isfinite(number) else None

    def run_autonomous_cycle(
        self,
        fabric: ASMAMeshFabric,
        scaling_engine: ScalingEngine,
        sla_monitor: SLAMonitor,
        commercial_service: TenantOnboardingService,
        avg_cpu_pct: float | None = None,
        avg_memory_pct: float | None = None,
    ) -> dict[str, Any]:
        self._cycle_count += 1
        cycle_id = f"cycle-{self._cycle_count}"
        errors: list[str] = []
        healed_nodes: list[str] = []
        scaling_decision: dict[str, Any] = {
            "recommendation": "STABLE", "current_count": len(fabric.registry.list_active_nodes()),
            "target_count": len(fabric.registry.list_active_nodes()), "reason": "not evaluated",
        }
        scaled_nodes: list[str] = []
        sla_status: dict[str, Any] = {"status": "NO_DATA", "uptime_percentage": 0.0, "compliant": False}
        financial_metrics: dict[str, Any] = {}
        ledger_recorded = False

        try:
            healed_nodes = fabric.self_heal()
        except Exception as exc:
            errors.append(f"self-healing failed: {exc}")

        try:
            if self.workload_metrics_provider is not None:
                workload = self.workload_metrics_provider(fabric.registry)
                cpu = workload.get("avg_cpu_pct", 0.0) if avg_cpu_pct is None else avg_cpu_pct
                memory = workload.get("avg_memory_pct", 0.0) if avg_memory_pct is None else avg_memory_pct
            else:
                cpu = 50.0 if avg_cpu_pct is None else avg_cpu_pct
                memory = 50.0 if avg_memory_pct is None else avg_memory_pct
            scaling_decision = scaling_engine.evaluate_scaling(
                len(fabric.registry.list_active_nodes()), cpu, memory
            )
            scaled_nodes = scaling_engine.apply_scaling(fabric.registry, scaling_decision)
        except Exception as exc:
            errors.append(f"scaling failed: {exc}")

        try:
            sla_status = sla_monitor.get_sla_status()
        except Exception as exc:
            errors.append(f"SLA evaluation failed: {exc}")

        try:
            financial_metrics = commercial_service.get_financial_metrics()
        except Exception as exc:
            errors.append(f"financial evaluation failed: {exc}")

        try:
            ledger_integrity_before = self.audit_ledger.verify_integrity()
        except Exception as exc:
            ledger_integrity_before = False
            errors.append(f"audit integrity check failed: {exc}")
        if not ledger_integrity_before:
            errors.append("audit ledger integrity check failed")

        active_nodes = fabric.registry.list_active_nodes()
        policy = scaling_engine.policy
        node_count = len(active_nodes)
        no_failed_nodes = all(
            node.status not in {MeshNodeStatus.DEGRADED, MeshNodeStatus.FAILED}
            for node in fabric.registry.nodes.values()
        )
        self_healing_verified = no_failed_nodes
        scaling_verified = (
            policy.auto_scale_enabled
            and policy.min_nodes <= node_count <= policy.max_nodes
            and scaling_decision.get("recommendation") in {"SCALE_UP", "SCALE_DOWN", "STABLE"}
        )
        uptime = float(sla_status.get("uptime_percentage", 0.0) or 0.0)
        sla_compliant = (
            bool(sla_status.get("compliant"))
            and uptime >= self.required_sla_pct
        )
        upfront_cost = float(financial_metrics.get("upfront_cost_usd", float("inf")))
        positive_arr = float(financial_metrics.get("projected_arr_usd", 0.0) or 0.0) > 0
        upfront_budget_safe = (
            upfront_cost == 0.0
            and bool(financial_metrics.get("upfront_budget_safe", False))
        )
        financial_health = positive_arr and upfront_budget_safe
        cycle_status = (
            "HEALTHY"
            if self_healing_verified and scaling_verified and sla_compliant and financial_health and not errors
            else "DEGRADED"
        )
        cycle = {
            "cycle_id": cycle_id,
            "status": cycle_status,
            "healed_nodes": healed_nodes,
            "unhealthy_nodes_remaining": [
                node.node_id for node in fabric.registry.nodes.values()
                if node.status in {MeshNodeStatus.DEGRADED, MeshNodeStatus.FAILED}
            ],
            "workload": {
                "avg_cpu_pct": self._safe_metric(cpu) if "cpu" in locals() else None,
                "avg_memory_pct": self._safe_metric(memory) if "memory" in locals() else None,
            },
            "scaling_decision": scaling_decision,
            "scaled_nodes": scaled_nodes,
            "active_node_count": node_count,
            "self_healing_verified": self_healing_verified,
            "scaling_verified": scaling_verified,
            "sla": sla_status,
            "sla_compliant": sla_compliant,
            "financial_metrics": financial_metrics,
            "positive_arr": positive_arr,
            "upfront_budget_safe": upfront_budget_safe,
            "financial_health": financial_health,
            "audit_ledger_integrity_before": ledger_integrity_before,
            "errors": errors,
        }

        if self.specification_engine is not None:
            try:
                self.specification_engine.evaluate_gate6(
                    self_healing_verified,
                    scaling_verified,
                    financial_health,
                )
            except Exception as exc:
                errors.append(f"Gate 6 evaluation failed: {exc}")
                cycle["errors"] = errors

        try:
            self.audit_ledger.append_entry(
                actor="autonomous-expansion-engine",
                action="AUTONOMOUS_CYCLE",
                details=cycle,
            )
            ledger_recorded = True
        except Exception as exc:
            errors.append(f"audit recording failed: {exc}")
            cycle["errors"] = errors
            cycle["status"] = "DEGRADED"
        cycle["audit_ledger_integrity"] = self.audit_ledger.verify_integrity()
        cycle["audit_recorded"] = ledger_recorded
        if not cycle["audit_ledger_integrity"]:
            cycle["status"] = "DEGRADED"
        self._last_cycle = deepcopy(cycle)
        return cycle

    def get_autonomous_status(self) -> dict[str, Any]:
        return {
            "status": self._last_cycle.get("status", "IDLE") if self._last_cycle else "IDLE",
            "cycle_count": self._cycle_count,
            "continuous_running": self._continuous_running,
            "last_cycle": deepcopy(self._last_cycle),
            "audit_ledger_integrity": self.audit_ledger.verify_integrity(),
        }

    async def run_continuous(
        self,
        fabric: ASMAMeshFabric,
        scaling_engine: ScalingEngine,
        sla_monitor: SLAMonitor,
        commercial_service: TenantOnboardingService,
        interval_seconds: float = 30.0,
        stop_event: asyncio.Event | None = None,
        max_cycles: int | None = None,
    ) -> list[dict[str, Any]]:
        """Run unattended cycles until stopped, cancelled, or the test limit is met."""
        if not math.isfinite(interval_seconds) or interval_seconds < 0:
            raise ValueError("interval_seconds must be finite and non-negative")
        if max_cycles is not None and max_cycles < 1:
            raise ValueError("max_cycles must be positive")
        self._continuous_running = True
        results: list[dict[str, Any]] = []
        try:
            while stop_event is None or not stop_event.is_set():
                results.append(self.run_autonomous_cycle(
                    fabric, scaling_engine, sla_monitor, commercial_service
                ))
                if max_cycles is not None and len(results) >= max_cycles:
                    break
                if stop_event is None:
                    await asyncio.sleep(interval_seconds)
                elif not stop_event.is_set():
                    try:
                        await asyncio.wait_for(stop_event.wait(), timeout=interval_seconds)
                    except asyncio.TimeoutError:
                        pass
            return results
        finally:
            self._continuous_running = False
