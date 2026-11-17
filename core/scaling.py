"""Policy-driven node pool scaling with deterministic, local decisions."""

from __future__ import annotations

import math
from typing import Any

from asma_os_mesh import ASMANodeRegistry, MeshNode, MeshNodeStatus, MeshNodeType
from spec_schema import ScalingPolicy


class ScalingEngine:
    """Recommend and apply bounded changes to a mesh node pool."""

    def __init__(
        self,
        policy: ScalingPolicy | None = None,
        scale_down_cpu_ratio: float = 0.5,
        scale_down_memory_ratio: float = 0.5,
    ) -> None:
        if not 0 < scale_down_cpu_ratio < 1 or not 0 < scale_down_memory_ratio < 1:
            raise ValueError("scale-down ratios must be between zero and one")
        self.policy = policy or ScalingPolicy()
        self.scale_down_cpu_ratio = scale_down_cpu_ratio
        self.scale_down_memory_ratio = scale_down_memory_ratio
        self._next_node_number = 1

    @staticmethod
    def _validate_metrics(active_node_count: int, avg_cpu_pct: float, avg_memory_pct: float) -> None:
        if isinstance(active_node_count, bool) or not isinstance(active_node_count, int) or active_node_count < 0:
            raise ValueError("active_node_count must be a non-negative integer")
        for name, metric in (("avg_cpu_pct", avg_cpu_pct), ("avg_memory_pct", avg_memory_pct)):
            if isinstance(metric, bool) or not isinstance(metric, (int, float)) or not math.isfinite(metric):
                raise ValueError(f"{name} must be a finite number")
            if not 0 <= metric <= 100:
                raise ValueError(f"{name} must be between 0 and 100")

    def _decision(self, recommendation: str, count: int, target: int, reason: str) -> dict[str, Any]:
        return {
            "recommendation": recommendation,
            "action": recommendation,
            "current_count": count,
            "target_count": target,
            "scale_by": abs(target - count),
            "reason": reason,
        }

    def evaluate_scaling(
        self,
        active_node_count: int,
        avg_cpu_pct: float,
        avg_memory_pct: float,
    ) -> dict[str, Any]:
        self._validate_metrics(active_node_count, avg_cpu_pct, avg_memory_pct)
        policy = self.policy
        count = active_node_count
        if not policy.auto_scale_enabled:
            return self._decision("STABLE", count, count, "automatic scaling is disabled")
        if count < policy.min_nodes:
            return self._decision("SCALE_UP", count, policy.min_nodes, "below configured minimum")
        if count > policy.max_nodes:
            return self._decision("SCALE_DOWN", count, policy.max_nodes, "above configured maximum")

        overloaded = avg_cpu_pct >= policy.cpu_threshold_pct or avg_memory_pct >= policy.memory_threshold_pct
        if overloaded:
            increase = max(1, math.ceil(count * 0.25))
            target = min(policy.max_nodes, count + increase)
            if target > count:
                return self._decision("SCALE_UP", count, target, "CPU or memory exceeded its scale-up threshold")
            return self._decision("STABLE", count, count, "already at configured maximum")

        low_load = (
            avg_cpu_pct < policy.cpu_threshold_pct * self.scale_down_cpu_ratio
            and avg_memory_pct < policy.memory_threshold_pct * self.scale_down_memory_ratio
        )
        if low_load and count > policy.min_nodes:
            decrease = max(1, math.ceil(count * 0.1))
            target = max(policy.min_nodes, count - decrease)
            return self._decision("SCALE_DOWN", count, target, "CPU and memory are below scale-down thresholds")
        return self._decision("STABLE", count, count, "resource use is within configured bounds")

    def apply_scaling(self, registry: ASMANodeRegistry, decision: dict[str, Any]) -> list[str]:
        if not isinstance(decision, dict):
            raise TypeError("decision must be a dictionary")
        active = registry.list_active_nodes()
        current_count = len(active)
        action = decision.get("recommendation", decision.get("action", "STABLE"))
        if action not in {"SCALE_UP", "SCALE_DOWN", "STABLE"}:
            raise ValueError(f"unsupported scaling recommendation: {action!r}")
        if action == "STABLE" or not self.policy.auto_scale_enabled:
            return []

        if "target_count" in decision:
            target = decision["target_count"]
            if isinstance(target, bool) or not isinstance(target, int):
                raise ValueError("target_count must be an integer")
        else:
            delta = decision.get("scale_by", 1)
            if isinstance(delta, bool) or not isinstance(delta, int) or delta < 0:
                raise ValueError("scale_by must be a non-negative integer")
            target = current_count + delta if action == "SCALE_UP" else current_count - delta
        target = max(self.policy.min_nodes, min(self.policy.max_nodes, target))
        changed: list[str] = []

        if action == "SCALE_UP":
            while current_count < target:
                while True:
                    node_id = f"autoscale-execution-{self._next_node_number}"
                    self._next_node_number += 1
                    if node_id not in registry.nodes:
                        break
                node = MeshNode(
                    node_id=node_id,
                    node_type=MeshNodeType.EXECUTION,
                    status=MeshNodeStatus.ACTIVE,
                )
                registry.register_node(node)
                current_count += 1
                changed.append(node_id)
            return changed

        remove_count = max(0, current_count - target)
        eligible = sorted(
            (
                node for node in active
                if node.node_type == MeshNodeType.EXECUTION
            ),
            key=lambda node: (node.health_score, node.node_id),
        )
        for node in eligible[:remove_count]:
            registry.unregister_node(node.node_id)
            changed.append(node.node_id)
        return changed
