"""Deterministic, dependency-free planning agent."""

from __future__ import annotations

from typing import Any

from agents.base_agent import BaseAgent


class PlanningAgent(BaseAgent):
    async def plan(self, goal: str, task_data: dict[str, Any] | None = None) -> list[dict[str, Any]]:
        """Normalize supplied steps or split a simple goal into ordered steps."""
        if not self.initialized:
            await self.initialize()
        data = task_data or {}
        supplied_steps = data.get("plan_steps")
        if supplied_steps is None:
            descriptions = [part.strip(" .\n\t") for part in goal.replace(" then ", "\n").splitlines()]
            descriptions = [part for part in descriptions if part]
        else:
            if not isinstance(supplied_steps, list) or not supplied_steps:
                raise ValueError("plan_steps must be a non-empty list")
            descriptions = supplied_steps

        steps: list[dict[str, Any]] = []
        for index, item in enumerate(descriptions, start=1):
            if isinstance(item, str):
                step = {"step_id": f"step-{index}", "description": item, "task_data": {}}
            elif isinstance(item, dict):
                step = dict(item)
                step.setdefault("step_id", f"step-{index}")
                step.setdefault("description", f"Execute step {index}")
                step.setdefault("task_data", {})
                if not isinstance(step["task_data"], dict):
                    raise ValueError(f"task_data for step {index} must be an object")
            else:
                raise ValueError("each plan step must be a string or object")
            steps.append(step)
        return steps
