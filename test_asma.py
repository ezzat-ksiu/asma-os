"""
Comprehensive Test Suite for ASMA-OS V6.0 Core Components.
"""

import pytest
import asyncio
from spec_schema import (
    ASMASpec,
    BusinessArchitecture,
    TechnicalArchitecture,
    ExecutionArchitecture,
    OperationalGates,
    GateDetail,
    FinancialModel,
    ScalingPolicy,
    QualityAndSecurityArchitecture,
    AuditLedger,
    AuditEntry,
)
from mcp_server import (
    get_spec_summary,
    get_gate_status,
    list_all_gates,
    get_system_health,
)
from asma_os_mesh import (
    MeshNode,
    MeshNodeType,
    MeshNodeStatus,
    MeshMessage,
    ASMASpecificationEngine,
    ASMANodeRegistry,
    ASMAMeshFabric,
)


# ==========================================
# 1. SPEC SCHEMA TESTS
# ==========================================

def test_asmaspec_defaults():
    spec = ASMASpec(
        business=BusinessArchitecture(
            vision="Test Vision",
            strategic_pillars=["P1", "P2"],
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
    assert spec.version == "6.0"
    assert len(spec.business.operational_gates.gates) == 7
    assert "G0" in spec.business.operational_gates.gates
    assert "G6" in spec.business.operational_gates.gates


def test_gate_details():
    og = OperationalGates()
    g0 = og.gates["G0"]
    assert g0.gate_id == "G0"
    assert g0.status == "PENDING"
    assert len(g0.criteria) >= 3


def test_financial_model():
    fm = FinancialModel()
    assert fm.target_arr_usd == 1000000.0
    assert fm.cac_payback_months == 6


def test_audit_ledger_add_entry():
    ledger = AuditLedger()
    entry = AuditEntry(actor="system", action="INIT", details={"status": "OK"})
    ledger.entries.append(entry)
    assert len(ledger.entries) == 1
    assert ledger.entries[0].action == "INIT"


# ==========================================
# 2. MCP SERVER TESTS
# ==========================================

def test_mcp_get_spec_summary():
    res = get_spec_summary()
    assert res["version"] == "6.0"
    assert res["gates_count"] == 7
    assert isinstance(res["pillars"], list)


def test_mcp_get_gate_status_valid():
    res = get_gate_status("G0")
    assert res["id"] == "G0"
    assert res["status"] == "PENDING"


def test_mcp_get_gate_status_invalid():
    res = get_gate_status("G99")
    assert "error" in res


def test_mcp_list_all_gates():
    gates = list_all_gates()
    assert len(gates) == 7


def test_mcp_get_system_health():
    health = get_system_health()
    assert health["unit_test_coverage_min"] == 95.0
    assert health["security_level"] == "ZERO_TRUST"


# ==========================================
# 3. ASMA MESH & SPEC ENGINE TESTS
# ==========================================

def test_engine_gate_validation():
    engine = ASMASpecificationEngine()
    assert engine.validate_gate("G0") is True
    assert engine.validate_gate("G99") is False


def test_engine_evaluate_gate_criteria_pass():
    engine = ASMASpecificationEngine()
    g0_criteria = engine.spec.business.operational_gates.gates["G0"].criteria
    results = {c: True for c in g0_criteria}
    passed = engine.evaluate_gate_criteria("G0", results)
    assert passed is True
    assert engine.spec.business.operational_gates.gates["G0"].status == "PASSED"


def test_engine_evaluate_gate_criteria_fail():
    engine = ASMASpecificationEngine()
    g0_criteria = engine.spec.business.operational_gates.gates["G0"].criteria
    results = {c: False for c in g0_criteria}
    passed = engine.evaluate_gate_criteria("G0", results)
    assert passed is False
    assert engine.spec.business.operational_gates.gates["G0"].status == "FAILED"


def test_mesh_node_process_message_success():
    node = MeshNode(
        node_id="node-1",
        node_type=MeshNodeType.EXECUTION,
        status=MeshNodeStatus.ACTIVE,
    )
    msg = MeshMessage(sender="master", target="node-1", action="RUN_TASK")
    res = asyncio.run(node.process_message(msg))
    assert res["status"] == "success"
    assert res["action"] == "RUN_TASK"


def test_mesh_node_process_message_failed_status():
    node = MeshNode(
        node_id="node-2",
        node_type=MeshNodeType.EXECUTION,
        status=MeshNodeStatus.FAILED,
    )
    msg = MeshMessage(sender="master", target="node-2", action="RUN_TASK")
    res = asyncio.run(node.process_message(msg))
    assert res["status"] == "error"


def test_node_registry():
    registry = ASMANodeRegistry()
    node = MeshNode(
        node_id="node-1",
        node_type=MeshNodeType.MASTER,
        status=MeshNodeStatus.ACTIVE,
    )
    registry.register_node(node)
    assert registry.get_node("node-1") == node
    assert len(registry.list_active_nodes()) == 1

    unreg = registry.unregister_node("node-1")
    assert unreg == node
    assert registry.get_node("node-1") is None


def test_mesh_fabric_routing_and_healing():
    engine = ASMASpecificationEngine()
    registry = ASMANodeRegistry()
    fabric = ASMAMeshFabric(engine, registry)

    node1 = MeshNode(
        node_id="n1",
        node_type=MeshNodeType.GATEWAY,
        status=MeshNodeStatus.ACTIVE,
    )
    node2 = MeshNode(
        node_id="n2",
        node_type=MeshNodeType.EXECUTION,
        status=MeshNodeStatus.FAILED,
        health_score=0.2,
    )
    registry.register_node(node1)
    registry.register_node(node2)

    msg = MeshMessage(sender="n1", target="n2", action="PING")
    res = asyncio.run(fabric.route_message(msg))
    assert res["status"] == "error"

    healed = fabric.self_heal()
    assert "n2" in healed
    assert node2.status == MeshNodeStatus.ACTIVE

    res2 = asyncio.run(fabric.route_message(msg))
    assert res2["status"] == "success"


# Additional Parameterized Tests
@pytest.mark.parametrize("gate_id", ["G0", "G1", "G2", "G3", "G4", "G5", "G6"])
def test_all_individual_gates_exist(gate_id):
    og = OperationalGates()
    assert gate_id in og.gates
    assert len(og.gates[gate_id].criteria) > 0


def test_scaling_policy_defaults():
    sp = ScalingPolicy()
    assert sp.auto_scale_enabled is True
    assert sp.min_nodes == 3
    assert sp.max_nodes == 100
