"""Gate 6 autonomous expansion and final system closure tests."""

import asyncio

from asma_os_mesh import (
    ASMANodeRegistry,
    ASMASpecificationEngine,
    ASMAMeshFabric,
    MeshNode,
    MeshNodeStatus,
    MeshNodeType,
)
from core.audit import CryptoAuditLedger
from core.autonomous_expansion import AutonomousExpansionEngine
from core.scaling import ScalingEngine
from core.sla import SLAMonitor
from services.commercial import TenantOnboardingService


def _system(degraded_node=False, upfront_cost=0.0):
    specification = ASMASpecificationEngine()
    registry = ASMANodeRegistry()
    for index in range(3):
        node = MeshNode(
            node_id=f"execution-{index}",
            node_type=MeshNodeType.EXECUTION,
            status=MeshNodeStatus.ACTIVE,
        )
        if degraded_node and index == 1:
            node.record_health(0.2)
        registry.register_node(node)
    fabric = ASMAMeshFabric(specification, registry)

    sla = SLAMonitor()
    for index in range(1000):
        sla.record_heartbeat("execution-0", is_up=True, response_time_ms=10)

    commercial = TenantOnboardingService(plan_prices={"pro": 100})
    commercial.register_tenant("tenant-1", "pro", "owner@example.com")
    commercial.record_payment("tenant-1", 100, transaction_id="invoice-1")
    if upfront_cost:
        commercial.record_upfront_cost(upfront_cost)

    ledger = CryptoAuditLedger()
    expansion = AutonomousExpansionEngine(
        audit_ledger=ledger,
        specification_engine=specification,
    )
    return specification, registry, fabric, sla, commercial, ledger, expansion


def test_autonomous_cycle_heals_nodes_scales_and_records_healthy_state():
    specification, registry, fabric, sla, commercial, ledger, expansion = _system(degraded_node=True)
    cycle = expansion.run_autonomous_cycle(
        fabric,
        ScalingEngine(),
        sla,
        commercial,
        avg_cpu_pct=90,
        avg_memory_pct=60,
    )

    assert cycle["status"] == "HEALTHY"
    assert cycle["healed_nodes"] == ["execution-1"]
    assert registry.get_node("execution-1").status == MeshNodeStatus.ACTIVE
    assert cycle["scaling_decision"]["recommendation"] == "SCALE_UP"
    assert len(cycle["scaled_nodes"]) == 1
    assert cycle["active_node_count"] == 4
    assert cycle["sla_compliant"] is True
    assert cycle["financial_health"] is True
    assert cycle["audit_recorded"] is True
    assert ledger.verify_integrity() is True
    assert ledger.blocks[-1].action == "AUTONOMOUS_CYCLE"
    assert specification.spec.business.operational_gates.gates["G6"].status == "PASSED"
    assert expansion.get_autonomous_status()["cycle_count"] == 1


def test_autonomous_cycle_enforces_zero_upfront_budget():
    _, _, fabric, sla, commercial, ledger, expansion = _system(upfront_cost=0.01)
    cycle = expansion.run_autonomous_cycle(
        fabric, ScalingEngine(), sla, commercial, avg_cpu_pct=50, avg_memory_pct=50
    )
    assert cycle["financial_metrics"]["upfront_cost_usd"] == 0.01
    assert cycle["upfront_budget_safe"] is False
    assert cycle["positive_arr"] is True
    assert cycle["financial_health"] is False
    assert cycle["status"] == "DEGRADED"
    assert ledger.verify_integrity() is True


def test_autonomous_cycle_marks_missing_sla_measurements_degraded():
    _, _, fabric, _, commercial, _, expansion = _system()
    cycle = expansion.run_autonomous_cycle(
        fabric, ScalingEngine(), SLAMonitor(), commercial
    )
    assert cycle["sla"]["status"] == "NO_DATA"
    assert cycle["sla_compliant"] is False
    assert cycle["status"] == "DEGRADED"


def test_continuous_runner_executes_cycles_without_manual_intervention():
    async def scenario():
        _, _, fabric, sla, commercial, _, expansion = _system()
        results = await expansion.run_continuous(
            fabric,
            ScalingEngine(),
            sla,
            commercial,
            interval_seconds=0,
            max_cycles=2,
        )
        assert len(results) == 2
        assert all(result["status"] == "HEALTHY" for result in results)
        assert expansion.get_autonomous_status()["cycle_count"] == 2
        assert expansion.get_autonomous_status()["continuous_running"] is False

    asyncio.run(scenario())


def test_gate6_evaluation_requires_all_three_verified_controls():
    engine = ASMASpecificationEngine()
    assert engine.evaluate_gate6(True, True, False) is False
    assert engine.spec.business.operational_gates.gates["G6"].status == "FAILED"
    assert engine.evaluate_gate6(True, True, True) is True
    assert engine.spec.business.operational_gates.gates["G6"].status == "PASSED"


def test_full_system_completion_requires_all_seven_gates():
    engine = ASMASpecificationEngine()
    initial = engine.verify_full_system_completion()
    assert initial["complete"] is False
    assert initial["unpassed_gates"] == [f"G{index}" for index in range(7)]

    gates = engine.spec.business.operational_gates.gates
    for gate_id, gate in gates.items():
        assert engine.evaluate_gate_criteria(
            gate_id, {criterion: True for criterion in gate.criteria}
        ) is True

    complete = engine.verify_full_system_completion()
    assert complete["complete"] is True
    assert complete["all_gates_passed"] is True
    assert complete["passed_gates"] == [f"G{index}" for index in range(7)]
    assert complete["unpassed_gates"] == []

    g4 = gates["G4"]
    engine.evaluate_gate_criteria("G4", {criterion: False for criterion in g4.criteria})
    incomplete = engine.verify_full_system_completion()
    assert incomplete["complete"] is False
    assert incomplete["unpassed_gates"] == ["G4"]
