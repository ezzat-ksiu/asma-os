"""Heartbeat-based availability tracking and SLA evaluation."""

from __future__ import annotations

from collections import deque
from datetime import datetime, timezone
import math


class SLAMonitor:
    """Calculate observed uptime over a rolling set of heartbeat samples."""

    def __init__(self, target_uptime_pct: float = 99.9, max_samples: int = 100_000) -> None:
        if not math.isfinite(target_uptime_pct) or not 0 <= target_uptime_pct <= 100:
            raise ValueError("target_uptime_pct must be between 0 and 100")
        if max_samples < 1:
            raise ValueError("max_samples must be positive")
        self.target_uptime_pct = float(target_uptime_pct)
        self._heartbeats: deque[dict] = deque(maxlen=max_samples)

    def record_heartbeat(self, node_id: str, is_up: bool, response_time_ms: float) -> None:
        if not isinstance(node_id, str) or not node_id.strip():
            raise ValueError("node_id must not be empty")
        if not isinstance(is_up, bool):
            raise TypeError("is_up must be a boolean")
        if isinstance(response_time_ms, bool) or not isinstance(response_time_ms, (int, float)):
            raise ValueError("response_time_ms must be a finite non-negative number")
        if not math.isfinite(response_time_ms) or response_time_ms < 0:
            raise ValueError("response_time_ms must be a finite non-negative number")
        self._heartbeats.append({
            "node_id": node_id,
            "is_up": is_up,
            "response_time_ms": float(response_time_ms),
            "timestamp": datetime.now(timezone.utc).isoformat(),
        })

    def calculate_uptime_percentage(self) -> float:
        if not self._heartbeats:
            return 0.0
        successes = sum(1 for heartbeat in self._heartbeats if heartbeat["is_up"])
        return round(successes / len(self._heartbeats) * 100.0, 4)

    def get_sla_status(self) -> dict:
        total = len(self._heartbeats)
        uptime = self.calculate_uptime_percentage()
        up_samples = [heartbeat for heartbeat in self._heartbeats if heartbeat["is_up"]]
        average_response = (
            round(sum(sample["response_time_ms"] for sample in up_samples) / len(up_samples), 2)
            if up_samples else None
        )
        compliant = total > 0 and uptime >= self.target_uptime_pct
        return {
            "status": "NO_DATA" if total == 0 else ("COMPLIANT" if compliant else "BREACHED"),
            "compliant": compliant,
            "uptime_percentage": uptime,
            "target_uptime_percentage": self.target_uptime_pct,
            "heartbeat_count": total,
            "successful_heartbeats": len(up_samples),
            "failed_heartbeats": total - len(up_samples),
            "average_response_time_ms": average_response,
            "last_heartbeat": self._heartbeats[-1]["timestamp"] if total else None,
        }
