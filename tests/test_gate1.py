"""Gate 1 integration coverage for agents, mesh routing, and gate evaluation."""

import asyncio

from agents import ExecutionAgent, GatewayAgent
from asma_os_mesh import ASMANodeRegistry, ASMAMeshFabric, ASMASpecificationEngine, MeshMessage, MeshNodeStatus


def test_agents_initialize_and_register_with_registry():
    async def scenario():
        gateway = GatewayAgent(node_id="gateway-1", authorized_senders=["client-1"])
        worker = ExecutionAgent(node_id="execution-1")
        assert (await gateway.initialize())["status"] == "initialized"
        assert (await worker.initialize())["status"] == "initialized"

        registry = ASMANodeRegistry()
        registry.register_node(gateway)
        registry.register_node(worker)
        assert registry.get_node(gateway.node_id) is gateway
        assert registry.get_node(worker.node_id) is worker
        assert len(registry.list_active_nodes()) == 2

    asyncio.run(scenario())


def test_gateway_validates_and_routes_execution_message():
    async def scenario():
        engine = ASMASpecificationEngine()
        registry = ASMANodeRegistry()
        fabric = ASMAMeshFabric(engine, registry)
        gateway = GatewayAgent(node_id="gateway-1", authorized_senders=["client-1"])
        worker = ExecutionAgent(node_id="execution-1")
        await gateway.initialize()
        await worker.initialize()
        registry.register_node(gateway)
        registry.register_node(worker)

        message = MeshMessage(
            sender="client-1",
            target=worker.node_id,
            action="EXECUTE_TASK",
            payload={"task_data": {"task_id": "task-1", "result": "done"}},
        )
        result = await gateway.forward_message(message, fabric)
        assert result["status"] == "success"
        assert result["task_id"] == "task-1"
        assert worker.tasks_completed == 1
        assert fabric.audit_log[-1]["routed_to"] == worker.node_id

    asyncio.run(scenario())


def test_gateway_rejects_unauthorized_sender_and_payload():
    async def scenario():
        registry = ASMANodeRegistry()
        fabric = ASMAMeshFabric(ASMASpecificationEngine(), registry)
        gateway = GatewayAgent(node_id="gateway-1", authorized_senders=["trusted"])
        worker = ExecutionAgent(node_id="execution-1")
        await gateway.initialize()
        await worker.initialize()
        registry.register_node(gateway)
        registry.register_node(worker)

        denied_sender = MeshMessage(sender="untrusted", target=worker.node_id, action="PING")
        assert (await gateway.forward_message(denied_sender, fabric))["status"] == "error"
        addressed_to_gateway = MeshMessage(sender="untrusted", target=gateway.node_id, action="PING")
        assert (await fabric.route_message(addressed_to_gateway))["status"] == "error"
        denied_payload = MeshMessage(
            sender="trusted", target=worker.node_id, action="EXECUTE_TASK",
            payload={"task_data": {"task_id": "x"}, "authorized": False},
        )
        response = await gateway.forward_message(denied_payload, fabric)
        assert response["status"] == "error"
        assert "authorization" in response["reason"]

    asyncio.run(scenario())


def test_execution_failure_degrades_node_and_self_heal_recovers_it():
    async def scenario():
        registry = ASMANodeRegistry()
        worker = ExecutionAgent(node_id="execution-1")
        await worker.initialize()
        registry.register_node(worker)
        fabric = ASMAMeshFabric(ASMASpecificationEngine(), registry)
        message = MeshMessage(
            sender="gateway-1", target=worker.node_id, action="EXECUTE_TASK",
            payload={"task_data": {"simulate_error": True, "error_message": "boom"}},
        )
        result = await fabric.route_message(message)
        assert result["status"] == "error"
        assert worker.status == MeshNodeStatus.FAILED
        assert worker.report_health()["last_error"] == "boom"

        assert fabric.self_heal() == [worker.node_id]
        assert worker.status == MeshNodeStatus.ACTIVE
        assert worker.health_score == 1.0

    asyncio.run(scenario())


def test_gate0_and_gate1_pass_when_all_criteria_are_verified():
    engine = ASMASpecificationEngine()
    gates = engine.spec.business.operational_gates.gates
    results = {
        gate_id: {criterion: True for criterion in gates[gate_id].criteria}
        for gate_id in ("G0", "G1")
    }
    assert engine.evaluate_gates(results) == {"G0": True, "G1": True}
    assert gates["G0"].status == "PASSED"
    assert gates["G1"].status == "PASSED"


def test_agent_lifecycle_reports_health_and_shutdown():
    async def scenario():
        worker = ExecutionAgent(node_id="execution-1")
        await worker.initialize()
        health = worker.report_health()
        assert health["initialized"] is True
        assert health["status"] == "active"
        assert (await worker.shutdown())["status"] == "shutdown"
        assert worker.report_health()["status"] == "offline"

    asyncio.run(scenario())
