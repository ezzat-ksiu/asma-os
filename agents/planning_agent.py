"""Deterministic offline planner; external model calls are intentionally opt-in elsewhere."""
from typing import Any
from pydantic import BaseModel, Field
from agents.base_agent import BaseAgent

class PlanningAgent(BaseAgent):
    node_id: str = Field(default="planning_agent_node")
    model_name: str = Field(default="local-deterministic")
    capabilities: list[str] = Field(default_factory=lambda: ["PLAN_TASK"])

    def generate_plan(self, goal: str, budget: float = 0.0) -> dict[str, Any]:
        clean_goal = " ".join(goal.split())[:2000]
        if not clean_goal:
            raise ValueError("goal must not be empty")
        return {
            "goal": clean_goal,
            "budget": budget,
            "strategy": "Review requirements, prepare a reversible implementation, validate locally, and request approval for consequential actions.",
            "execution_steps": ["Clarify and record acceptance criteria", "Implement within configured permissions", "Run local validation and report evidence"],
            "provider": "none",
        }

    async def plan(self, goal: str, task_data: dict[str, Any] | None = None) -> list[dict[str, Any]]:
        """Build an ordered plan locally; callers may provide explicit steps for a task."""
        if not self.initialized:
            await self.initialize()
        supplied = (task_data or {}).get("plan_steps")
        if supplied is not None:
            if not isinstance(supplied, list) or not supplied:
                raise ValueError("plan_steps must be a non-empty list")
            normalized: list[dict[str, Any]] = []
            for index, item in enumerate(supplied, start=1):
                if isinstance(item, str):
                    normalized.append({"step_id": f"step-{index}", "description": item, "task_data": {"result": item}})
                elif isinstance(item, dict):
                    normalized.append({"step_id": str(item.get("step_id", f"step-{index}")), "description": str(item.get("description", f"Step {index}")), "task_data": dict(item.get("task_data", {})), **{key: value for key, value in item.items() if key not in {"step_id", "description", "task_data"}}})
                else:
                    raise TypeError("each plan step must be a string or object")
            return normalized
        goal = " ".join(goal.split())
        if not goal:
            raise ValueError("goal must not be empty")
        return [
            {"step_id": "step-1", "description": f"Prepare requirements for: {goal}", "task_data": {"result": "requirements prepared"}},
            {"step_id": "step-2", "description": "Execute the approved local work", "task_data": {"result": "local work completed"}},
            {"step_id": "step-3", "description": "Review and record the result", "task_data": {"result": "review complete"}},
        ]
