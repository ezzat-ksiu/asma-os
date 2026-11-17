"""Signed, idempotent local billing webhook simulator."""

from __future__ import annotations

from copy import deepcopy
from datetime import datetime, timezone
from decimal import Decimal, InvalidOperation
import hashlib
import hmac
import json
import secrets
import time
from typing import Any

from services.commercial import TenantOnboardingService


class BillingAdapter:
    """Simulate payment-provider event handling without connecting to a provider.

    Pass a stable secret from the application's secret store in real deployments.
    If omitted, a random process-local secret is generated for local simulation.
    """

    SUPPORTED_EVENTS = {
        "customer.subscription.created",
        "customer.subscription.updated",
        "customer.subscription.deleted",
        "invoice.payment_succeeded",
        "invoice.payment_failed",
    }

    def __init__(
        self,
        tenant_service: TenantOnboardingService | None = None,
        webhook_secret: str | None = None,
        customer_tenant_map: dict[str, str] | None = None,
        signature_tolerance_seconds: int = 300,
    ) -> None:
        if signature_tolerance_seconds < 0:
            raise ValueError("signature_tolerance_seconds must be non-negative")
        self.tenant_service = tenant_service
        self.webhook_secret = webhook_secret or secrets.token_hex(32)
        self.customer_tenant_map = dict(customer_tenant_map or {})
        self.signature_tolerance_seconds = signature_tolerance_seconds
        self._tenant_states: dict[str, dict[str, str]] = {}
        self._processed_event_ids: set[str] = set()

    @staticmethod
    def _canonical_payload(payload: dict[str, Any]) -> str:
        return json.dumps(payload, sort_keys=True, separators=(",", ":"), ensure_ascii=False, allow_nan=False)

    def _signature(self, event_type: str, payload_without_signature: dict[str, Any]) -> str:
        signed_at = payload_without_signature.get("signed_at")
        canonical = self._canonical_payload(payload_without_signature)
        message = f"{event_type}.{signed_at}.{canonical}".encode("utf-8")
        return hmac.new(self.webhook_secret.encode("utf-8"), message, hashlib.sha256).hexdigest()

    def sign_webhook_event(
        self,
        event_type: str,
        payload: dict[str, Any],
        signed_at: int | None = None,
    ) -> dict[str, Any]:
        """Create a signed payload envelope for local development and tests."""
        if not isinstance(payload, dict):
            raise TypeError("payload must be a dictionary")
        envelope = deepcopy(payload)
        envelope["signed_at"] = int(time.time()) if signed_at is None else int(signed_at)
        envelope.pop("signature", None)
        envelope["signature"] = self._signature(event_type, {k: v for k, v in envelope.items() if k != "signature"})
        return envelope

    @staticmethod
    def _event_object(payload: dict[str, Any]) -> dict[str, Any]:
        data = payload.get("data")
        if isinstance(data, dict) and isinstance(data.get("object"), dict):
            return data["object"]
        return payload

    def _tenant_id(self, payload: dict[str, Any], event_object: dict[str, Any]) -> str | None:
        metadata = event_object.get("metadata")
        tenant_id = (
            payload.get("tenant_id")
            or event_object.get("tenant_id")
            or (metadata.get("tenant_id") if isinstance(metadata, dict) else None)
        )
        customer_id = event_object.get("customer") or payload.get("customer_id")
        if tenant_id is None and customer_id is not None:
            tenant_id = self.customer_tenant_map.get(str(customer_id))
        return str(tenant_id) if tenant_id is not None else None

    def _tenant_state(self, tenant_id: str) -> dict[str, str]:
        if tenant_id not in self._tenant_states:
            tenant = self.tenant_service.get_tenant(tenant_id) if self.tenant_service else None
            if tenant is not None:
                self._tenant_states[tenant_id] = {
                    "subscription_status": tenant["subscription_status"],
                    "payment_status": tenant["payment_status"],
                }
            else:
                self._tenant_states[tenant_id] = {
                    "subscription_status": "PENDING",
                    "payment_status": "PENDING",
                }
        return self._tenant_states[tenant_id]

    def _update_tenant(self, tenant_id: str, subscription_status: str, payment_status: str | None = None) -> None:
        state = self._tenant_state(tenant_id)
        state["subscription_status"] = subscription_status.upper()
        if payment_status is not None:
            state["payment_status"] = payment_status.upper()
        if self.tenant_service is not None:
            self.tenant_service.update_subscription(
                tenant_id,
                subscription_status=state["subscription_status"],
                payment_status=state["payment_status"],
            )

    @staticmethod
    def _amount_usd(event_object: dict[str, Any]) -> Decimal:
        currency = str(event_object.get("currency", "usd")).lower()
        if currency != "usd":
            raise ValueError(f"unsupported currency: {currency}")
        if "amount_usd" in event_object:
            raw_amount = event_object["amount_usd"]
        elif "amount_paid" in event_object:
            # Stripe-style amount_paid values are in the currency's minor unit.
            raw_amount = Decimal(str(event_object["amount_paid"])) / Decimal("100")
        elif "amount" in event_object:
            raw_amount = event_object["amount"]
        else:
            raise ValueError("payment event is missing amount_usd or amount_paid")
        try:
            amount = Decimal(str(raw_amount))
        except (InvalidOperation, ValueError) as exc:
            raise ValueError("payment amount must be numeric") from exc
        if not amount.is_finite() or amount < 0:
            raise ValueError("payment amount must be finite and non-negative")
        return amount.quantize(Decimal("0.01"))

    def process_webhook_event(self, event_type: str, payload: dict) -> dict:
        if not isinstance(payload, dict):
            return {"status": "error", "reason": "payload must be a dictionary"}
        signature = payload.get("signature")
        signed_at = payload.get("signed_at")
        unsigned_payload = {key: value for key, value in payload.items() if key != "signature"}
        try:
            timestamp = int(signed_at)
            if abs(int(time.time()) - timestamp) > self.signature_tolerance_seconds:
                return {"status": "error", "reason": "webhook signature timestamp is outside tolerance"}
            expected = self._signature(event_type, unsigned_payload)
            if not isinstance(signature, str) or not hmac.compare_digest(expected, signature):
                return {"status": "error", "reason": "invalid webhook signature"}
        except (TypeError, ValueError, OverflowError, json.JSONDecodeError):
            return {"status": "error", "reason": "invalid webhook signature"}
        try:
            # Reject unsupported event types even when correctly signed.
            if event_type not in self.SUPPORTED_EVENTS:
                return {"status": "error", "reason": f"unsupported event_type: {event_type}"}
            event_object = self._event_object(unsigned_payload)
            tenant_id = self._tenant_id(unsigned_payload, event_object)
            if not tenant_id:
                return {"status": "error", "reason": "event is missing a tenant identity"}
            if self.tenant_service is not None and self.tenant_service.get_tenant(tenant_id) is None:
                return {"status": "error", "reason": f"unknown tenant: {tenant_id}"}
            event_id = str(unsigned_payload.get("event_id") or unsigned_payload.get("id") or signature)
            if event_id in self._processed_event_ids:
                state = self._tenant_state(tenant_id)
                return {
                    "status": "success",
                    "duplicate": True,
                    "payment_recorded": False,
                    "event_id": event_id,
                    "tenant_id": tenant_id,
                    **state,
                }

            current_state = self._tenant_state(tenant_id)
            payment_recorded = False
            if event_type == "customer.subscription.created":
                subscription_status = str(event_object.get("status", "active")).upper()
                payment_status = "NOT_REQUIRED" if subscription_status in {"FREE", "NOT_REQUIRED"} else current_state["payment_status"]
                self._update_tenant(tenant_id, subscription_status, payment_status)
            elif event_type == "customer.subscription.updated":
                subscription_status = str(event_object.get("status", "active")).upper()
                if subscription_status == "TRIALING":
                    self._update_tenant(tenant_id, subscription_status)
                elif subscription_status in {"ACTIVE", "PAST_DUE", "UNPAID", "CANCELED", "CANCELLED", "INCOMPLETE"}:
                    self._update_tenant(tenant_id, subscription_status)
                else:
                    return {"status": "error", "reason": "unsupported subscription status"}
            elif event_type == "customer.subscription.deleted":
                self._update_tenant(tenant_id, "CANCELED")
            elif event_type == "invoice.payment_succeeded":
                amount = self._amount_usd(event_object)
                transaction_id = str(
                    unsigned_payload.get("event_id")
                    or event_object.get("id")
                    or unsigned_payload.get("id")
                    or event_id
                )
                if self.tenant_service is not None:
                    payment_recorded = self.tenant_service.record_payment(
                        tenant_id, float(amount), transaction_id=transaction_id
                    )
                else:
                    payment_recorded = True
                self._update_tenant(tenant_id, "ACTIVE", "PAID")
            elif event_type == "invoice.payment_failed":
                self._update_tenant(tenant_id, "PAST_DUE", "FAILED")

            self._processed_event_ids.add(event_id)
            return {
                "status": "success",
                "duplicate": False,
                "event_id": event_id,
                "tenant_id": tenant_id,
                "payment_recorded": payment_recorded,
                **self._tenant_state(tenant_id),
            }
        except (KeyError, TypeError, ValueError) as exc:
            return {"status": "error", "reason": str(exc)}

    def verify_payment_status(self, tenant_id: str) -> bool:
        state = self._tenant_state(tenant_id)
        subscription_is_active = state["subscription_status"] in {"ACTIVE", "TRIALING"}
        payment_is_valid = state["payment_status"] in {"PAID", "NOT_REQUIRED"}
        return subscription_is_active and payment_is_valid
