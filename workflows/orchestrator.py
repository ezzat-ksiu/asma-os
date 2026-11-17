"""LangGraph-based, local-first multi-agent task orchestration."""

from __future__ import annotations

from copy import deepcopy
from typing import Any

from langgraph.checkpoint.memory import InMemorySaver
from langgraph.graph import END, START, StateGraph

from agents.execution_agent import ExecutionAgent
from agents.planning_agent import PlanningAgent
from agents.review_agent import ReviewAgent
from workflows.state import WorkflowState, create_workflow_state


class AutonomousTaskOrchestrator:
    """Plan, execute, review, and recover tasks using LangGraph checkpoints.

    The default checkpointer is process-local InMemorySaver and requires no
    paid service. A caller can inject another LangGraph-compatible checkpointer
    for durable storage when the deployment already provides one.
    """

    def __init__(
        self,
        planning_agent: PlanningAgent | None = None,
        execution_agent: ExecutionAgent | None = None,
        review_agent: ReviewAgent | None = None,
        checkpointer: Any | None = None,
        max_step_retries: int = 1,
        max_fallback_attempts: int = 1,
    ) -> None:
        if max_step_retries < 0 or max_fallback_attempts < 1:
            raise ValueError("retry count must be non-negative and fallback attempts must be positive")
        self.planning_agent = planning_agent or PlanningAgent(node_id="planner")
        self.execution_agent = execution_agent or ExecutionAgent(node_id="executor")
        self.review_agent = review_agent or ReviewAgent(node_id="reviewer")
        self.checkpointer = checkpointer if checkpointer is not None else InMemorySaver()
        self.max_step_retries = max_step_retries
        self.max_fallback_attempts = max_fallback_attempts
        self.graph = self._build_graph()

    @staticmethod
    def _checkpoint(state: WorkflowState, node: str, **details: Any) -> list[dict[str, Any]]:
        history = list(state.get("checkpoint_history", []))
        history.append({
            "node": node,
            "step_index": state.get("current_step_index", 0),
            "status": state.get("status", "PLANNED"),
            **details,
        })
        return history

    async def _plan(self, state: WorkflowState) -> dict[str, Any]:
        try:
            steps = await self.planning_agent.plan(state["input_goal"], state.get("task_data", {}))
            if not steps:
                raise ValueError("planner produced no execution steps")
            return {
                "plan_steps": steps,
                "current_step_index": 0,
                "status": "EXECUTING",
                "checkpoint_history": self._checkpoint(state, "plan", planned_steps=len(steps)),
            }
        except Exception as exc:
            message = f"planning failed: {exc}"
            return {
                "errors": [*state.get("errors", []), message],
                "status": "FAILED",
                "checkpoint_history": self._checkpoint(state, "plan", error=message),
            }

    async def _execute(self, state: WorkflowState) -> dict[str, Any]:
        index = state["current_step_index"]
        step = state["plan_steps"][index]
        step_id = str(step["step_id"])
        attempts = dict(state.get("step_attempts", {}))
        attempts[step_id] = attempts.get(step_id, 0) + 1
        payload = dict(state.get("task_data", {}))
        payload.update(step.get("task_data", {}))
        payload.update({key: value for key, value in step.items() if key not in {"step_id", "description", "task_data"}})
        payload.setdefault("task_id", state["task_id"])
        payload.setdefault("description", step.get("description", ""))

        try:
            if not self.execution_agent.initialized or self.execution_agent.status != "active":
                await self.execution_agent.initialize()
            result = await self.execution_agent.execute_task(payload)
            if not isinstance(result, dict):
                raise TypeError("execution agent must return a dictionary")
        except Exception as exc:
            result = {"status": "error", "reason": str(exc), "retryable": False}

        results = dict(state.get("execution_results", {}))
        results[step_id] = result
        errors = list(state.get("errors", []))
        if result.get("status") != "success":
            errors.append(f"{step_id}: {result.get('reason', 'execution failed')}")
        return {
            "execution_results": results,
            "current_step_result": result,
            "step_attempts": attempts,
            "errors": errors,
            "status": "REVIEWING",
            "checkpoint_history": self._checkpoint(
                state, "execute", step_id=step_id, attempt=attempts[step_id], result_status=result.get("status")
            ),
        }

    async def _review(self, state: WorkflowState) -> dict[str, Any]:
        index = state["current_step_index"]
        step = state["plan_steps"][index]
        step_id = str(step["step_id"])
        attempt = state.get("step_attempts", {}).get(step_id, 1)
        try:
            review = await self.review_agent.review_step(
                step,
                state.get("current_step_result", {}),
                attempt_number=attempt,
                max_retries=self.max_step_retries,
            )
            decision = review.get("decision")
            reason = str(review.get("reason", "review returned no reason"))
            if decision == "retry" and attempt <= self.max_step_retries:
                return {
                    "status": "EXECUTING",
                    "checkpoint_history": self._checkpoint(state, "review", step_id=step_id, decision="retry"),
                }
            if decision != "complete":
                errors = list(state.get("errors", []))
                errors.append(f"{step_id}: {reason}")
                return {
                    "errors": errors,
                    "status": "FALLBACK",
                    "checkpoint_history": self._checkpoint(state, "review", step_id=step_id, decision="fallback", reason=reason),
                }
        except Exception as exc:
            reason = f"review failed: {exc}"
            return {
                "errors": [*state.get("errors", []), f"{step_id}: {reason}"],
                "status": "FALLBACK",
                "checkpoint_history": self._checkpoint(state, "review", step_id=step_id, decision="fallback", reason=reason),
            }

        next_index = index + 1
        complete = next_index >= len(state["plan_steps"])
        status = "COMPLETED" if complete else "EXECUTING"
        return {
            "current_step_index": next_index,
            "status": status,
            "checkpoint_history": self._checkpoint(state, "review", step_id=step_id, decision="complete"),
        }

    async def _fallback(self, state: WorkflowState) -> dict[str, Any]:
        index = state["current_step_index"]
        step = state["plan_steps"][index]
        step_id = str(step["step_id"])
        attempts = dict(state.get("fallback_attempts", {}))
        attempts[step_id] = attempts.get(step_id, 0) + 1
        if attempts[step_id] > self.max_fallback_attempts:
            message = f"{step_id}: fallback attempts exhausted"
            return {
                "fallback_attempts": attempts,
                "errors": [*state.get("errors", []), message],
                "status": "FAILED",
                "checkpoint_history": self._checkpoint(state, "fallback", step_id=step_id, outcome="failed"),
            }
        try:
            if step.get("fallback_error"):
                raise RuntimeError(str(step["fallback_error"]))
            fallback_result = {
                "status": "success",
                "valid": True,
                "fallback_used": True,
                "node_id": "local-deterministic-fallback",
                "task_id": state["task_id"],
                "result": {"completed_step": step.get("description", step_id), "mode": "fallback"},
            }
            results = dict(state.get("execution_results", {}))
            results[step_id] = fallback_result
            return {
                "execution_results": results,
                "current_step_result": fallback_result,
                "fallback_attempts": attempts,
                "status": "REVIEWING",
                "checkpoint_history": self._checkpoint(state, "fallback", step_id=step_id, outcome="recovered"),
            }
        except Exception as exc:
            message = f"{step_id}: fallback failed: {exc}"
            return {
                "fallback_attempts": attempts,
                "errors": [*state.get("errors", []), message],
                "status": "FAILED",
                "checkpoint_history": self._checkpoint(state, "fallback", step_id=step_id, outcome="failed", reason=str(exc)),
            }

    @staticmethod
    def _after_plan(state: WorkflowState) -> str:
        return "stop" if state["status"] == "FAILED" else "execute"

    @staticmethod
    def _after_execute(state: WorkflowState) -> str:
        return "review" if state["status"] == "REVIEWING" else "fallback"

    @staticmethod
    def _after_review(state: WorkflowState) -> str:
        if state["status"] == "COMPLETED":
            return "stop"
        if state["status"] == "FALLBACK":
            return "fallback"
        if state["status"] == "FAILED":
            return "stop"
        return "execute"

    @staticmethod
    def _after_fallback(state: WorkflowState) -> str:
        return "stop" if state["status"] == "FAILED" else "review"

    def _build_graph(self):
        builder = StateGraph(WorkflowState)
        builder.add_node("plan", self._plan)
        builder.add_node("execute", self._execute)
        builder.add_node("review", self._review)
        builder.add_node("fallback", self._fallback)
        builder.add_edge(START, "plan")
        builder.add_conditional_edges("plan", self._after_plan, {"execute": "execute", "stop": END})
        builder.add_conditional_edges("execute", self._after_execute, {"review": "review", "fallback": "fallback"})
        builder.add_conditional_edges("review", self._after_review, {
            "execute": "execute", "fallback": "fallback", "stop": END,
        })
        builder.add_conditional_edges("fallback", self._after_fallback, {"review": "review", "stop": END})
        return builder.compile(checkpointer=self.checkpointer)

    async def ainvoke(
        self,
        task_id: str,
        input_goal: str,
        task_data: dict[str, Any] | None = None,
        thread_id: str | None = None,
    ) -> WorkflowState:
        initial = create_workflow_state(task_id, input_goal, task_data)
        config = {"configurable": {"thread_id": thread_id or task_id}}
        return await self.graph.ainvoke(initial, config=config)

    def get_checkpoint(self, thread_id: str) -> dict[str, Any] | None:
        """Read the latest local LangGraph checkpoint for a task thread."""
        snapshot = self.graph.get_state({"configurable": {"thread_id": thread_id}})
        return deepcopy(snapshot.values) if snapshot and snapshot.values else None


def build_orchestrator(**kwargs: Any) -> AutonomousTaskOrchestrator:
    """Construct the default no-hosted-service workflow runner."""
    return AutonomousTaskOrchestrator(**kwargs)
