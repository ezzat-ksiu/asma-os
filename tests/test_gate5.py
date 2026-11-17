"""Gate 5 commercial onboarding, billing simulation, SLA, and gate tests."""

import time

import pytest

from adapters.billing_adapter import BillingAdapter
from asma_os_mesh import ASMASpecificationEngine
from core.sla import SLAMonitor
from services.commercial import TenantOnboardingService
from spec_schema import FinancialModel


def test_tenant_onboarding_lifecycle_and_free_default_plan():
    service = TenantOnboardingService()
    tenant = service.register_tenant("tenant-free", "free", "owner@example.com")
    assert tenant["status"] == "ACTIVE"
    assert tenant["subscription_status"] == "ACTIVE"
    assert tenant["payment_status"] == "NOT_REQUIRED"
    assert service.get_tenant("tenant-free")["tenant_id"] == "tenant-free"
    with pytest.raises(ValueError):
        service.register_tenant("tenant-free", "free", "another@example.com")
    with pytest.raises(ValueError):
        service.register_tenant("bad-email", "free", "not-an-email")


def test_tenant_onboarding_validates_plan_and_email():
    service = TenantOnboardingService(plan_prices={"starter": 25})
    with pytest.raises(ValueError, match="unsupported plan"):
        service.register_tenant("t1", "unknown", "owner@example.com")
    with pytest.raises(ValueError, match="valid email"):
        service.register_tenant("t1", "starter", "owner-at-example")


def test_signed_billing_events_update_subscription_and_payment_state():
    service = TenantOnboardingService(plan_prices={"starter": 99})
    service.register_tenant("tenant-1", "starter", "owner@example.com")
    adapter = BillingAdapter(tenant_service=service, webhook_secret="local-webhook-secret")
    assert adapter.verify_payment_status("tenant-1") is False

    created = adapter.sign_webhook_event(
        "customer.subscription.created",
        {"event_id": "evt-sub-created", "tenant_id": "tenant-1", "status": "active"},
    )
    created_result = adapter.process_webhook_event("customer.subscription.created", created)
    assert created_result["status"] == "success"
    assert service.get_tenant("tenant-1")["subscription_status"] == "ACTIVE"
    assert adapter.verify_payment_status("tenant-1") is False

    invoice = adapter.sign_webhook_event(
        "invoice.payment_succeeded",
        {
            "event_id": "evt-invoice-paid",
            "data": {
                "object": {
                    "id": "in-100",
                    "metadata": {"tenant_id": "tenant-1"},
                    "amount_paid": 9900,
                    "currency": "usd",
                }
            },
        },
    )
    result = adapter.process_webhook_event("invoice.payment_succeeded", invoice)
    assert result["status"] == "success"
    assert result["payment_recorded"] is True
    assert adapter.verify_payment_status("tenant-1") is True
    assert service.get_financial_metrics()["total_revenue_usd"] == 99.0

    duplicate = adapter.process_webhook_event("invoice.payment_succeeded", invoice)
    assert duplicate["duplicate"] is True
    assert duplicate["payment_recorded"] is False
    assert service.get_financial_metrics()["total_revenue_usd"] == 99.0

    failed = adapter.sign_webhook_event(
        "invoice.payment_failed",
        {"event_id": "evt-invoice-failed", "tenant_id": "tenant-1"},
    )
    assert adapter.process_webhook_event("invoice.payment_failed", failed)["status"] == "success"
    assert adapter.verify_payment_status("tenant-1") is False
    assert service.get_tenant("tenant-1")["subscription_status"] == "PAST_DUE"


def test_billing_adapter_rejects_tampered_stale_and_unknown_events():
    adapter = BillingAdapter(webhook_secret="test-signing-key")
    signed = adapter.sign_webhook_event(
        "customer.subscription.created",
        {"event_id": "evt-1", "tenant_id": "tenant-1", "status": "active"},
    )
    tampered = dict(signed, status="canceled")
    assert adapter.process_webhook_event("customer.subscription.created", tampered)["status"] == "error"

    stale = adapter.sign_webhook_event(
        "customer.subscription.created",
        {"event_id": "evt-old", "tenant_id": "tenant-1", "status": "active"},
        signed_at=int(time.time()) - 3600,
    )
    assert "timestamp" in adapter.process_webhook_event("customer.subscription.created", stale)["reason"]

    unknown = adapter.sign_webhook_event(
        "unknown.event", {"event_id": "evt-unknown", "tenant_id": "tenant-1"}
    )
    assert adapter.process_webhook_event("unknown.event", unknown)["status"] == "error"


def test_subscription_cancellation_disables_payment_verification():
    service = TenantOnboardingService(plan_prices={"pro": 50})
    service.register_tenant("tenant-cancel", "pro", "owner@example.com")
    adapter = BillingAdapter(tenant_service=service, webhook_secret="test")
    paid = adapter.sign_webhook_event(
        "invoice.payment_succeeded",
        {"event_id": "evt-paid", "tenant_id": "tenant-cancel", "amount_usd": 50},
    )
    adapter.process_webhook_event("invoice.payment_succeeded", paid)
    assert adapter.verify_payment_status("tenant-cancel") is True

    canceled = adapter.sign_webhook_event(
        "customer.subscription.deleted",
        {"event_id": "evt-cancel", "tenant_id": "tenant-cancel"},
    )
    assert adapter.process_webhook_event("customer.subscription.deleted", canceled)["status"] == "success"
    assert adapter.verify_payment_status("tenant-cancel") is False
    assert service.get_tenant("tenant-cancel")["status"] == "SUSPENDED"


def test_sla_monitor_calculates_and_reports_99_9_percent_uptime():
    monitor = SLAMonitor(target_uptime_pct=99.9)
    for index in range(1000):
        monitor.record_heartbeat("node-1", is_up=index < 999, response_time_ms=12.5)
    assert monitor.calculate_uptime_percentage() == 99.9
    status = monitor.get_sla_status()
    assert status["compliant"] is True
    assert status["status"] == "COMPLIANT"
    assert status["failed_heartbeats"] == 1
    assert status["average_response_time_ms"] == 12.5


def test_sla_monitor_detects_breach_and_empty_measurements():
    monitor = SLAMonitor()
    assert monitor.calculate_uptime_percentage() == 0.0
    assert monitor.get_sla_status()["status"] == "NO_DATA"
    for index in range(1000):
        monitor.record_heartbeat("node-1", is_up=index < 998, response_time_ms=20)
    assert monitor.calculate_uptime_percentage() == 99.8
    assert monitor.get_sla_status()["compliant"] is False


def test_sla_monitor_validates_heartbeat_data():
    monitor = SLAMonitor()
    with pytest.raises(ValueError):
        monitor.record_heartbeat("", True, 1)
    with pytest.raises(TypeError):
        monitor.record_heartbeat("node", 1, 1)
    with pytest.raises(ValueError):
        monitor.record_heartbeat("node", True, float("inf"))


def test_financial_metrics_calculate_and_compare_financial_model_targets():
    model = FinancialModel()
    monthly_price = 83_333.34
    service = TenantOnboardingService(
        financial_model=model,
        plan_prices={"launch": monthly_price},
    )
    service.register_tenant("tenant-growth", "launch", "finance@example.com")
    billing = BillingAdapter(tenant_service=service, webhook_secret="metrics-secret")
    invoice = billing.sign_webhook_event(
        "invoice.payment_succeeded",
        {"event_id": "evt-growth", "tenant_id": "tenant-growth", "amount_usd": monthly_price},
    )
    billing.process_webhook_event("invoice.payment_succeeded", invoice)
    service.record_operating_cost(16_666.67)
    service.record_acquisition_cost("tenant-growth", 400_000.02)

    metrics = service.get_financial_metrics()
    assert metrics["total_revenue_usd"] == monthly_price
    assert metrics["projected_arr_usd"] == 1_000_000.08
    assert metrics["cac_payback_months"] == 6.0
    assert metrics["gross_margin_pct"] == 80.0
    assert metrics["financial_model_targets"]["target_arr_usd"] == 1_000_000.0
    assert metrics["financial_model_targets"]["cac_payback_months"] == 6
    assert metrics["financial_model_targets"]["gross_margin_target_pct"] == 80.0
    assert metrics["alignment_met"] is True


def test_financial_metrics_report_unmet_targets_without_observed_revenue():
    service = TenantOnboardingService(
        financial_model=FinancialModel(),
        plan_prices={"starter": 10},
    )
    service.register_tenant("tenant-pending", "starter", "owner@example.com")
    metrics = service.get_financial_metrics()
    assert metrics["total_revenue_usd"] == 0
    assert metrics["projected_arr_usd"] == 0
    assert metrics["cac_payback_months"] is None
    assert metrics["gross_margin_pct"] is None
    assert metrics["alignment_met"] is False


def test_gate5_criteria_evaluation_marks_gate_passed():
    engine = ASMASpecificationEngine()
    gate = engine.spec.business.operational_gates.gates["G5"]
    results = {criterion: True for criterion in gate.criteria}
    assert engine.evaluate_gate_criteria("G5", results) is True
    assert gate.status == "PASSED"
