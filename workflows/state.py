"""Typed workflow state and zero-cost initial state construction."""

from __future__ import annotations

from typing import Any, TypedDict


class WorkflowState(TypedDict):
    task_id: str
    input_goal: str
    plan_steps: list[dict[str, Any]]
    current_step_index: int
    execution_results: dict[str, dict[str, Any]]
    errors: list[str]
    status: str
    checkpoint_history: list[dict[str, Any]]
    task_data: dict[str, Any]
    current_step_result: dict[str, Any]
    step_attempts: dict[str, int]
    fallback_attempts: dict[str, int]


WORKFLOW_STATUSES = {
    "PLANNED", "EXECUTING", "REVIEWING", "COMPLETED", "FALLBACK", "FAILED"
}


def create_workflow_state(
    task_id: str,
    input_goal: str,
    task_data: dict[str, Any] | None = None,
) -> WorkflowState:
    """Create a complete initial graph state without external infrastructure."""
    if not task_id.strip():
        raise ValueError("task_id must not be empty")
    if not input_goal.strip():
        raise ValueError("input_goal must not be empty")
    return {
        "task_id": task_id,
        "input_goal": input_goal,
        "plan_steps": [],
        "current_step_index": 0,
        "execution_results": {},
        "errors": [],
        "status": "PLANNED",
        "checkpoint_history": [],
        "task_data": dict(task_data or {}),
        "current_step_result": {},
        "step_attempts": {},
        "fallback_attempts": {},
    }
