"""Lulu Print API client with configurable production or sandbox endpoints."""
from __future__ import annotations

import os
from adapters.http import request_json


class LuluAdapter:
    PRODUCTION_URL = "https://api.lulu.com"
    SANDBOX_URL = "https://api.sandbox.lulu.com"

    def __init__(self, client_key: str | None = None, client_secret: str | None = None, *,
                 sandbox: bool = True, base_url: str | None = None, timeout: float = 20):
        self.client_key = client_key or os.getenv("LULU_CLIENT_KEY")
        self.client_secret = client_secret or os.getenv("LULU_CLIENT_SECRET")
        self.base_url = (base_url or (self.SANDBOX_URL if sandbox else self.PRODUCTION_URL)).rstrip("/")
        self.timeout, self._token, self._expires_at = timeout, None, 0

    def _access_token(self) -> str:
        import time
        if self._token and self._expires_at > time.time() + 30:
            return self._token
        if not self.client_key or not self.client_secret:
            raise ValueError("LULU_CLIENT_KEY and LULU_CLIENT_SECRET are required")
        from urllib.parse import urlencode
        # OAuth token endpoint uses form encoding rather than JSON.
        from urllib.request import Request, urlopen
        from urllib.error import HTTPError, URLError
        body = urlencode({"grant_type": "client_credentials", "client_id": self.client_key,
                          "client_secret": self.client_secret}).encode()
        req = Request(f"{self.base_url}/auth/realms/glasstree/protocol/openid-connect/token",
                      data=body, headers={"Content-Type": "application/x-www-form-urlencoded"}, method="POST")
        try:
            with urlopen(req, timeout=self.timeout) as response:
                import json
                result = json.loads(response.read())
        except (HTTPError, URLError, OSError, ValueError) as exc:
            from adapters.http import ProviderAPIError
            raise ProviderAPIError("Lulu", f"token request failed ({type(exc).__name__})") from None
        self._token, self._expires_at = result["access_token"], time.time() + int(result.get("expires_in", 3600))
        return self._token

    def _request(self, path: str, payload: dict) -> dict:
        return request_json("Lulu", f"{self.base_url}{path}", method="POST", payload=payload,
            headers={"Authorization": f"Bearer {self._access_token()}"}, timeout=self.timeout)

    def calculate_cost(self, payload: dict) -> dict:
        return self._request("/print-job-cost-calculations/", payload)

    def create_print_job(self, payload: dict) -> dict:
        if not payload.get("external_id") or not payload.get("line_items"):
            raise ValueError("Lulu print job requires external_id and line_items")
        return self._request("/print-jobs/", payload)
