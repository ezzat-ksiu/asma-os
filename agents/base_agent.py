"""Shared lifecycle and health behavior for ASMA-OS mesh agents."""

from __future__ import annotations

from typing import Any

from pydantic import ConfigDict, Field

from asma_os_mesh import MeshNode, MeshNodeStatus, MeshNodeType


class BaseAgent(MeshNode):
    """A mesh node with explicit startup, task, health, and shutdown hooks."""

    model_config = ConfigDict(validate_assignment=True)

    node_type: MeshNodeType = MeshNodeType.EXECUTION
    initialized: bool = False
    tasks_completed: int = 0
    last_error: str | None = None
    capabilities: list[str] = Field(default_factory=list)

    async def initialize(self) -> dict[str, Any]:
        self.initialized = True
        self.status = MeshNodeStatus.ACTIVE
        self.last_error = None
        self.record_health(1.0)
        return {"status": "initialized", "node_id": self.node_id}

    async def execute_task(self, task_data: dict[str, Any]) -> dict[str, Any]:
        if not self.initialized or self.status != MeshNodeStatus.ACTIVE:
            return {"status": "error", "node_id": self.node_id, "reason": "Agent is not active"}
        self.tasks_completed += 1
        return {"status": "success", "node_id": self.node_id, "result": task_data}

    def report_health(self) -> dict[str, Any]:
        return {
            "node_id": self.node_id,
            "status": self.status.value if isinstance(self.status, MeshNodeStatus) else self.status,
            "health_score": self.health_score,
            "initialized": self.initialized,
            "tasks_completed": self.tasks_completed,
            "last_error": self.last_error,
        }

    async def shutdown(self) -> dict[str, Any]:
        self.initialized = False
        self.status = MeshNodeStatus.OFFLINE
        self.record_health(0.0)
        # record_health marks low health as degraded; shutdown must remain offline.
        self.status = MeshNodeStatus.OFFLINE
        return {"status": "shutdown", "node_id": self.node_id}

    def fail(self, reason: str) -> None:
        self.last_error = reason
        self.status = MeshNodeStatus.FAILED
        self.record_health(0.0)
        self.status = MeshNodeStatus.FAILED

