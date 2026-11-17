"""Local tenant onboarding and financial metric tracking."""

from __future__ import annotations

from copy import deepcopy
from datetime import datetime, timezone
from decimal import Decimal, InvalidOperation, ROUND_HALF_UP
import re
from typing import Any

from spec_schema import FinancialModel


_CENT = Decimal("0.01")
_EMAIL_PATTERN = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")


def _money(value: Any, field_name: str) -> Decimal:
    try:
        amount = Decimal(str(value))
    except (InvalidOperation, TypeError, ValueError) as exc:
        raise ValueError(f"{field_name} must be a valid amount") from exc
    if not amount.is_finite() or amount < 0:
        raise ValueError(f"{field_name} must be finite and non-negative")
    return amount.quantize(_CENT, rounding=ROUND_HALF_UP)


class TenantOnboardingService:
    """Manage tenant lifecycle, observed transactions, and financial targets.

    No payment provider, email service, or external account is contacted.
    Plan prices and costs are supplied by the caller; the default plan is free.
    """

    def __init__(
        self,
        financial_model: FinancialModel | None = None,
        plan_prices: dict[str, float] | None = None,
    ) -> None:
        self.financial_model = financial_model or FinancialModel()
        raw_prices = plan_prices if plan_prices is not None else {"free": 0.0}
        if not raw_prices:
            raise ValueError("at least one plan must be configured")
        self.plan_prices = {str(name).strip().lower(): _money(price, "plan price") for name, price in raw_prices.items()}
        if any(not name for name in self.plan_prices):
            raise ValueError("plan names must not be empty")
        self.tenants: dict[str, dict[str, Any]] = {}
        self._payments: list[dict[str, Any]] = []
        self._operating_costs = Decimal("0.00")
        self._upfront_costs = Decimal("0.00")
        self._acquisition_costs: dict[str, Decimal] = {}
        self._transaction_ids: set[str] = set()

    def register_tenant(self, tenant_id: str, plan_type: str, contact_email: str) -> dict[str, Any]:
        tenant_id = tenant_id.strip() if isinstance(tenant_id, str) else ""
        plan_type = plan_type.strip().lower() if isinstance(plan_type, str) else ""
        contact_email = contact_email.strip() if isinstance(contact_email, str) else ""
        if not tenant_id:
            raise ValueError("tenant_id must not be empty")
        if tenant_id in self.tenants:
            raise ValueError(f"tenant {tenant_id!r} is already registered")
        if plan_type not in self.plan_prices:
            raise ValueError(f"unsupported plan_type: {plan_type!r}")
        if not _EMAIL_PATTERN.fullmatch(contact_email):
            raise ValueError("contact_email must be a valid email address")
        is_free = self.plan_prices[plan_type] == 0
        tenant = {
            "tenant_id": tenant_id,
            "plan_type": plan_type,
            "contact_email": contact_email,
            "status": "ACTIVE",
            "subscription_status": "ACTIVE" if is_free else "PENDING",
            "payment_status": "NOT_REQUIRED" if is_free else "PENDING",
            "monthly_price_usd": float(self.plan_prices[plan_type]),
            "created_at": datetime.now(timezone.utc).isoformat(),
        }
        self.tenants[tenant_id] = tenant
        return deepcopy(tenant)

    def get_tenant(self, tenant_id: str) -> dict[str, Any] | None:
        tenant = self.tenants.get(tenant_id)
        return deepcopy(tenant) if tenant else None

    def update_subscription(
        self,
        tenant_id: str,
        subscription_status: str | None = None,
        payment_status: str | None = None,
    ) -> dict[str, Any]:
        if tenant_id not in self.tenants:
            raise KeyError(f"unknown tenant: {tenant_id}")
        tenant = self.tenants[tenant_id]
        if subscription_status is not None:
            tenant["subscription_status"] = subscription_status.upper()
        if payment_status is not None:
            tenant["payment_status"] = payment_status.upper()
        tenant["status"] = "SUSPENDED" if tenant["subscription_status"] in {"CANCELED", "CANCELLED"} else "ACTIVE"
        return deepcopy(tenant)

    def record_payment(self, tenant_id: str, amount_usd: float, transaction_id: str | None = None) -> bool:
        if tenant_id not in self.tenants:
            raise KeyError(f"unknown tenant: {tenant_id}")
        amount = _money(amount_usd, "amount_usd")
        if transaction_id and transaction_id in self._transaction_ids:
            return False
        if transaction_id:
            self._transaction_ids.add(transaction_id)
        self._payments.append({
            "tenant_id": tenant_id,
            "amount_usd": amount,
            "transaction_id": transaction_id,
        })
        self.update_subscription(tenant_id, subscription_status="ACTIVE", payment_status="PAID")
        return True

    def record_operating_cost(self, amount_usd: float) -> None:
        self._operating_costs += _money(amount_usd, "amount_usd")

    def record_upfront_cost(self, amount_usd: float) -> None:
        self._upfront_costs += _money(amount_usd, "amount_usd")

    def record_acquisition_cost(self, tenant_id: str, amount_usd: float) -> None:
        if tenant_id not in self.tenants:
            raise KeyError(f"unknown tenant: {tenant_id}")
        self._acquisition_costs[tenant_id] = (
            self._acquisition_costs.get(tenant_id, Decimal("0.00")) + _money(amount_usd, "amount_usd")
        )

    def get_financial_metrics(self) -> dict[str, Any]:
        total_revenue = sum((payment["amount_usd"] for payment in self._payments), Decimal("0.00"))
        monthly_recurring_revenue = sum(
            (
                self.plan_prices[tenant["plan_type"]]
                for tenant in self.tenants.values()
                if tenant["subscription_status"] in {"ACTIVE", "TRIALING"}
                and self.plan_prices[tenant["plan_type"]] > 0
            ),
            Decimal("0.00"),
        )
        projected_arr = monthly_recurring_revenue * 12
        gross_margin = (
            ((total_revenue - self._operating_costs) / total_revenue * Decimal("100"))
            if total_revenue > 0 else None
        )
        paying_tenants = [
            tenant for tenant in self.tenants.values()
            if tenant["subscription_status"] in {"ACTIVE", "TRIALING"}
            and self.plan_prices[tenant["plan_type"]] > 0
        ]
        active_acquisition_costs = sum(
            (self._acquisition_costs.get(tenant["tenant_id"], Decimal("0.00")) for tenant in paying_tenants),
            Decimal("0.00"),
        )
        average_cac = active_acquisition_costs / len(paying_tenants) if paying_tenants else None
        average_monthly_gross_profit = (
            (monthly_recurring_revenue / len(paying_tenants)) * gross_margin / Decimal("100")
            if paying_tenants and gross_margin is not None else None
        )
        cac_payback = (
            average_cac / average_monthly_gross_profit
            if average_cac is not None and average_monthly_gross_profit and average_monthly_gross_profit > 0
            else (0.0 if average_cac == 0 and average_cac is not None else None)
        )
        model = self.financial_model
        rounded_margin = round(float(gross_margin), 2) if gross_margin is not None else None
        rounded_payback = round(float(cac_payback), 2) if cac_payback is not None else None
        upfront_budget_safe = self._upfront_costs <= Decimal(str(model.max_upfront_budget_usd))
        arr_target_met = projected_arr >= Decimal(str(model.target_arr_usd))
        cac_target_met = rounded_payback is not None and rounded_payback <= model.cac_payback_months
        margin_target_met = rounded_margin is not None and rounded_margin >= model.gross_margin_target_pct
        return {
            "total_revenue_usd": float(total_revenue),
            "monthly_recurring_revenue_usd": float(monthly_recurring_revenue),
            "projected_arr_usd": float(projected_arr),
            "cac_payback_months": rounded_payback,
            "gross_margin_pct": rounded_margin,
            "upfront_cost_usd": float(self._upfront_costs),
            "upfront_budget_usd": model.max_upfront_budget_usd,
            "upfront_budget_safe": upfront_budget_safe,
            "zero_upfront_cost": self._upfront_costs == 0,
            "financial_model_targets": {
                "target_arr_usd": model.target_arr_usd,
                "cac_payback_months": model.cac_payback_months,
                "gross_margin_target_pct": model.gross_margin_target_pct,
                "max_upfront_budget_usd": model.max_upfront_budget_usd,
            },
            "alignment": {
                "arr_target_met": arr_target_met,
                "cac_payback_within_target": cac_target_met,
                "gross_margin_target_met": margin_target_met,
                "upfront_budget_safe": upfront_budget_safe,
            },
            "alignment_met": all((arr_target_met, cac_target_met, margin_target_met, upfront_budget_safe)),
            "tenant_count": len(self.tenants),
            "active_paying_tenant_count": len(paying_tenants),
        }
