"""Gelato Print API client. No request occurs until a method is called."""
from __future__ import annotations

import os
from adapters.http import request_json


class GelatoAdapter:
    BASE_URL = "https://order.gelatoapis.com"

    def __init__(self, api_key: str | None = None, *, base_url: str = BASE_URL, timeout: float = 20):
        self.api_key = api_key or os.getenv("GELATO_API_KEY")
        self.base_url, self.timeout = base_url.rstrip("/"), timeout

    def _request(self, path: str, *, method: str = "GET", payload: dict | None = None) -> dict:
        if not self.api_key:
            raise ValueError("GELATO_API_KEY is required")
        return request_json("Gelato", f"{self.base_url}{path}", method=method, timeout=self.timeout,
                            headers={"X-API-KEY": self.api_key}, payload=payload)

    def quote_order(self, order: dict) -> dict:
        return self._request("/v4/orders:quote", method="POST", payload=order)

    def create_order(self, order: dict) -> dict:
        for field in ("orderReferenceId", "customerReferenceId", "items", "shippingAddress"):
            if field not in order:
                raise ValueError(f"Gelato order missing required field: {field}")
        return self._request("/v4/orders", method="POST", payload=order)
