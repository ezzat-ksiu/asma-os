"""Resend transactional email client with bounded transient retries."""
from __future__ import annotations

import os
import random
import time
from adapters.http import request_json, ProviderAPIError


class ResendAdapter:
    def __init__(self, api_key: str | None = None, *, timeout: float = 15, max_retries: int = 2,
                 sleep=time.sleep, jitter=random.random):
        self.api_key = api_key or os.getenv("RESEND_API_KEY")
        self.timeout, self.max_retries, self.sleep, self.jitter = timeout, max_retries, sleep, jitter

    def send_transactional_email(self, *, sender: str, to: str | list[str], subject: str,
                                 html: str, idempotency_key: str) -> dict:
        if not self.api_key: raise ValueError("RESEND_API_KEY is required")
        if not all((sender, to, subject, html, idempotency_key)) or len(idempotency_key) > 256:
            raise ValueError("sender, recipient, subject, HTML, and an idempotency key (max 256 chars) are required")
        payload = {"from": sender, "to": [to] if isinstance(to, str) else to, "subject": subject, "html": html}
        for attempt in range(self.max_retries + 1):
            try:
                return request_json("Resend", "https://api.resend.com/emails", method="POST", timeout=self.timeout,
                    headers={"Authorization": f"Bearer {self.api_key}", "Idempotency-Key": idempotency_key}, payload=payload)
            except ProviderAPIError as exc:
                if attempt >= self.max_retries or (exc.status_code is not None and exc.status_code < 500 and exc.status_code != 429):
                    raise
                self.sleep(min(4.0, 0.25 * (2 ** attempt) + 0.1 * self.jitter()))
