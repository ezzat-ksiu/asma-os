"""Paymob Intention API client and SHA-512 callback verification."""
from __future__ import annotations

import hashlib
import hmac
import os
from threading import Lock
from adapters.http import request_json


class PaymobAdapter:
    def __init__(self, secret_key: str | None = None, *, hmac_secret: str | None = None,
                 base_url: str = "https://accept.paymob.com", timeout: float = 20):
        self.secret_key = secret_key or os.getenv("PAYMOB_SECRET_KEY")
        self.hmac_secret = hmac_secret or os.getenv("PAYMOB_HMAC_SECRET")
        self.base_url, self.timeout = base_url.rstrip("/"), timeout
        self._seen, self._lock = set(), Lock()

    def create_payment_intent(self, *, amount_cents: int, currency: str, payment_methods: list[int],
                              items: list[dict], billing_data: dict, special_reference: str,
                              notification_url: str | None = None, redirection_url: str | None = None) -> dict:
        if not self.secret_key or amount_cents <= 0 or not special_reference:
            raise ValueError("secret key, positive amount, and stable special_reference are required")
        body = {"amount": amount_cents, "currency": currency, "payment_methods": payment_methods,
                "items": items, "billing_data": billing_data, "special_reference": special_reference}
        if notification_url: body["notification_url"] = notification_url
        if redirection_url: body["redirection_url"] = redirection_url
        return request_json("Paymob", f"{self.base_url}/v1/intention/", method="POST", timeout=self.timeout,
            headers={"Authorization": f"Token {self.secret_key}"}, payload=body)

    def verify_callback_hmac(self, callback: dict, supplied_hmac: str) -> bool:
        if not self.hmac_secret or not supplied_hmac:
            return False
        obj = callback.get("obj", callback)
        fields = ("amount_cents", "created_at", "currency", "error_occured", "has_parent_transaction",
                  "id", "integration_id", "is_3d_secure", "is_auth", "is_capture", "is_refunded",
                  "is_standalone_payment", "is_voided", "order", "owner", "pending", "source_data.pan",
                  "source_data.sub_type", "source_data.type", "success")
        values = []
        for field in fields:
            value = obj
            for part in field.split("."):
                value = value.get(part, "") if isinstance(value, dict) else ""
            if isinstance(value, bool): value = str(value).lower()
            elif isinstance(value, dict): value = value.get("id", "")
            values.append(str(value))
        digest = hmac.new(self.hmac_secret.encode(), "".join(values).encode(), hashlib.sha512).hexdigest()
        return hmac.compare_digest(digest, supplied_hmac.lower())

    def accept_callback_once(self, event_id: str, callback: dict, supplied_hmac: str) -> bool:
        if not self.verify_callback_hmac(callback, supplied_hmac):
            return False
        with self._lock:
            if event_id in self._seen: return False
            self._seen.add(event_id)
        return True
