"""Gateway agent with explicit sender, action, and payload authorization."""

from __future__ import annotations

from typing import Any

from pydantic import Field

from asma_os_mesh import ASMAMeshFabric, MeshMessage, MeshNodeStatus, MeshNodeType
from agents.base_agent import BaseAgent


class GatewayAgent(BaseAgent):
    node_type: MeshNodeType = MeshNodeType.GATEWAY
    authorized_senders: list[str] = Field(default_factory=list)
    allowed_actions: list[str] = Field(default_factory=lambda: ["PING", "EXECUTE_TASK", "RUN_TASK"])

    async def process_message(self, message: MeshMessage) -> dict[str, Any]:
        if not self.initialized or self.status != MeshNodeStatus.ACTIVE:
            return {"status": "error", "node_id": self.node_id, "reason": "Gateway is not active"}
        authorized, reason = self.authorize_message(message)
        if not authorized:
            return {"status": "error", "node_id": self.node_id, "reason": reason}
        return {
            "status": "success",
            "node_id": self.node_id,
            "action": message.action,
            "validated": True,
            "processed_trace": message.trace_id,
        }

    def authorize_message(self, message: MeshMessage) -> tuple[bool, str | None]:
        if message.sender not in self.authorized_senders and "*" not in self.authorized_senders:
            return False, "Sender is not authorized"
        if message.action not in self.allowed_actions:
            return False, "Action is not allowed"
        if message.action in ("EXECUTE_TASK", "RUN_TASK"):
            task_data = message.payload.get("task_data", message.payload)
            if not isinstance(task_data, dict):
                return False, "Task payload must be an object"
            if message.payload.get("authorized") is False:
                return False, "Payload authorization denied"
        return True, None

    async def forward_message(
        self, message: MeshMessage, fabric: ASMAMeshFabric
    ) -> dict[str, Any]:
        if not self.initialized or self.status != MeshNodeStatus.ACTIVE:
            return {"status": "error", "reason": "Gateway is not active"}
        authorized, reason = self.authorize_message(message)
        if not authorized:
            return {"status": "error", "reason": reason, "node_id": self.node_id}
        if fabric.registry.get_node(message.target) is None:
            return {"status": "error", "reason": f"Target node '{message.target}' not registered."}
        return await fabric.route_message(message)

