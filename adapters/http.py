"""Small JSON-over-HTTPS helper shared by provider adapters."""
from __future__ import annotations

import json
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen


class ProviderAPIError(RuntimeError):
    def __init__(self, provider: str, message: str, status_code: int | None = None):
        super().__init__(f"{provider}: {message}")
        self.provider, self.status_code = provider, status_code


def request_json(provider: str, url: str, *, method: str = "GET", headers: dict | None = None,
                 payload: dict | None = None, timeout: float = 20) -> dict:
    body = json.dumps(payload).encode() if payload is not None else None
    request_headers = {"Accept": "application/json", **(headers or {})}
    if body is not None:
        request_headers.setdefault("Content-Type", "application/json")
    request = Request(url, data=body, headers=request_headers, method=method)
    try:
        with urlopen(request, timeout=timeout) as response:
            raw = response.read()
    except HTTPError as exc:
        raise ProviderAPIError(provider, f"request failed (HTTP {exc.code})", exc.code) from None
    except (URLError, TimeoutError, OSError) as exc:
        raise ProviderAPIError(provider, f"network request failed ({type(exc).__name__})") from None
    if not raw:
        return {}
    try:
        value = json.loads(raw)
    except (UnicodeDecodeError, json.JSONDecodeError):
        raise ProviderAPIError(provider, "provider returned invalid JSON") from None
    if not isinstance(value, dict):
        raise ProviderAPIError(provider, "provider returned a non-object JSON response")
    return value
