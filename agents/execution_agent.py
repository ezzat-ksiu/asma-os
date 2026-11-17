"""Execution agent with deterministic simulated task handling."""

from __future__ import annotations

from typing import Any
from pydantic import Field

from asma_os_mesh import MeshMessage, MeshNodeStatus, MeshNodeType
from agents.base_agent import BaseAgent


class ExecutionAgent(BaseAgent):
    node_type: MeshNodeType = MeshNodeType.EXECUTION
    capabilities: list[str] = Field(default_factory=lambda: ["PING", "EXECUTE_TASK", "RUN_TASK"])

    async def execute_task(self, task_data: dict[str, Any]) -> dict[str, Any]:
        if not self.initialized or self.status != MeshNodeStatus.ACTIVE:
            return {"status": "error", "node_id": self.node_id, "reason": "Agent is not active"}
        if task_data.get("simulate_error"):
            reason = str(task_data.get("error_message", "Simulated execution failure"))
            self.fail(reason)
            return {"status": "error", "node_id": self.node_id, "reason": reason}
        self.tasks_completed += 1
        self.record_health(min(1.0, self.health_score + 0.01))
        return {
            "status": "success",
            "node_id": self.node_id,
            "task_id": task_data.get("task_id"),
            "result": task_data.get("result", task_data),
            "tasks_completed": self.tasks_completed,
            "valid": task_data.get("valid", True),
            "retry": task_data.get("retry", False),
        }

    async def process_message(self, msg: MeshMessage) -> dict[str, Any]:
        if msg.action in ("EXECUTE_TASK", "RUN_TASK"):
            task_data = msg.payload.get("task_data", msg.payload)
            if not isinstance(task_data, dict):
                return {"status": "error", "node_id": self.node_id, "reason": "Task payload must be an object"}
            return await self.execute_task(task_data)
        if msg.action == "PING":
            if self.status != MeshNodeStatus.ACTIVE:
                return {"status": "error", "node_id": self.node_id, "reason": "Node unhealthy or offline"}
            return {"status": "success", "node_id": self.node_id, "action": msg.action, "health_score": self.health_score}
        return {"status": "error", "node_id": self.node_id, "reason": "Unsupported action"}

