"""Deterministic output review and retry/fallback decision agent."""

from __future__ import annotations

from typing import Any

from agents.base_agent import BaseAgent


class ReviewAgent(BaseAgent):
    async def review_step(
        self,
        step: dict[str, Any],
        result: dict[str, Any],
        attempt_number: int = 1,
        max_retries: int = 1,
    ) -> dict[str, Any]:
        if not self.initialized:
            await self.initialize()
        status = result.get("status")
        if status != "success":
            if result.get("retryable") and attempt_number <= max_retries:
                return {"decision": "retry", "reason": result.get("reason", "Retryable execution error")}
            return {"decision": "fallback", "reason": result.get("reason", "Execution did not succeed")}
        if result.get("valid") is False or result.get("reject") is True:
            return {"decision": "fallback", "reason": "Step output failed validation"}
        if result.get("retry") is True and attempt_number <= max_retries:
            return {"decision": "retry", "reason": "Output requested a retry"}
        return {"decision": "complete", "reason": "Step output accepted"}
