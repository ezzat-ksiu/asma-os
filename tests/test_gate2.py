"""Gate 2 orchestration, persistence, fallback, and gate evaluation tests."""

import asyncio

from agents.execution_agent import ExecutionAgent
from asma_os_mesh import ASMASpecificationEngine
from workflows.orchestrator import AutonomousTaskOrchestrator
from workflows.state import create_workflow_state


def test_workflow_state_has_requested_fields_and_defaults():
    state = create_workflow_state("task-1", "prepare report")
    assert state["task_id"] == "task-1"
    assert state["input_goal"] == "prepare report"
    assert state["plan_steps"] == []
    assert state["current_step_index"] == 0
    assert state["execution_results"] == {}
    assert state["errors"] == []
    assert state["status"] == "PLANNED"
    assert state["checkpoint_history"] == []


def test_end_to_end_plan_execute_review_complete():
    async def scenario():
        orchestrator = AutonomousTaskOrchestrator()
        result = await orchestrator.ainvoke(
            "task-e2e",
            "prepare and review report",
            task_data={"plan_steps": ["prepare report", "review report"]},
        )
        assert result["status"] == "COMPLETED"
        assert [step["description"] for step in result["plan_steps"]] == ["prepare report", "review report"]
        assert len(result["execution_results"]) == 2
        assert all(value["status"] == "success" for value in result["execution_results"].values())
        assert [entry["node"] for entry in result["checkpoint_history"]].count("plan") == 1
        assert [entry["node"] for entry in result["checkpoint_history"]].count("review") == 2

    asyncio.run(scenario())


def test_checkpointer_retains_state_after_workflow_finishes():
    async def scenario():
        orchestrator = AutonomousTaskOrchestrator()
        result = await orchestrator.ainvoke(
            "task-checkpoint",
            "checkpoint this task",
            task_data={"plan_steps": ["step one", "step two"]},
        )
        snapshot = orchestrator.get_checkpoint("task-checkpoint")
        assert snapshot is not None
        assert snapshot["status"] == "COMPLETED"
        assert snapshot["checkpoint_history"] == result["checkpoint_history"]
        assert len(snapshot["checkpoint_history"]) >= 5

    asyncio.run(scenario())


def test_execution_failure_uses_deterministic_fallback_without_crashing():
    async def scenario():
        orchestrator = AutonomousTaskOrchestrator()
        result = await orchestrator.ainvoke(
            "task-fallback",
            "run risky step",
            task_data={
                "plan_steps": [
                    {"step_id": "risky", "description": "risky step", "task_data": {"simulate_error": True}}
                ]
            },
        )
        assert result["status"] == "COMPLETED"
        assert result["execution_results"]["risky"]["fallback_used"] is True
        assert result["fallback_attempts"]["risky"] == 1
        assert any(record["node"] == "fallback" for record in result["checkpoint_history"])
        assert result["errors"]

    asyncio.run(scenario())


def test_review_rejection_triggers_fallback_and_completes():
    async def scenario():
        orchestrator = AutonomousTaskOrchestrator()
        result = await orchestrator.ainvoke(
            "task-review-fallback",
            "validate generated output",
            task_data={
                "plan_steps": [
                    {"step_id": "invalid", "description": "invalid output", "task_data": {"valid": False}}
                ]
            },
        )
        assert result["status"] == "COMPLETED"
        assert result["execution_results"]["invalid"]["fallback_used"] is True
        assert result["fallback_attempts"]["invalid"] == 1

    asyncio.run(scenario())


def test_retryable_agent_failure_is_retried_before_fallback():
    class FlakyExecutionAgent(ExecutionAgent):
        calls: int = 0

        async def execute_task(self, task_data):
            self.calls += 1
            if self.calls == 1:
                return {"status": "error", "reason": "temporary", "retryable": True}
            return {"status": "success", "result": "recovered", "valid": True}

    async def scenario():
        worker = FlakyExecutionAgent(node_id="flaky")
        orchestrator = AutonomousTaskOrchestrator(execution_agent=worker)
        result = await orchestrator.ainvoke(
            "task-retry", "retry a transient step",
            task_data={"plan_steps": ["retry this single step"]},
        )
        assert result["status"] == "COMPLETED"
        assert worker.calls == 2
        assert result["fallback_attempts"] == {}
        assert result["step_attempts"]["step-1"] == 2

    asyncio.run(scenario())


def test_fallback_failure_returns_failed_state_instead_of_raising():
    async def scenario():
        orchestrator = AutonomousTaskOrchestrator()
        result = await orchestrator.ainvoke(
            "task-fallback-fails",
            "exercise terminal failure",
            task_data={
                "plan_steps": [
                    {
                        "step_id": "bad-fallback",
                        "description": "step with broken fallback",
                        "task_data": {"simulate_error": True},
                        "fallback_error": "fallback unavailable",
                    }
                ]
            },
        )
        assert result["status"] == "FAILED"
        assert any("fallback failed" in error for error in result["errors"])

    asyncio.run(scenario())


def test_gate2_criteria_evaluation_marks_gate_passed():
    engine = ASMASpecificationEngine()
    gate = engine.spec.business.operational_gates.gates["G2"]
    verified = {criterion: True for criterion in gate.criteria}
    assert engine.evaluate_gate_criteria("G2", verified) is True
    assert gate.status == "PASSED"
