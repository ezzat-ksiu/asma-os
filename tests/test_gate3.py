"""Gate 3 tests for zero-trust security, audit integrity, and compliance checks."""

import pytest

from asma_os_mesh import ASMASpecificationEngine
from core.audit import AuditBlock, CryptoAuditLedger
from core.compliance import ComplianceEngine
from core.security import ZeroTrustSecurityManager


def test_node_token_generation_and_validation():
    token = ZeroTrustSecurityManager.generate_node_token("node-1", "local-test-secret")
    assert len(token) == 64
    assert ZeroTrustSecurityManager.validate_node_token("node-1", token, "local-test-secret")
    assert not ZeroTrustSecurityManager.validate_node_token("node-2", token, "local-test-secret")
    assert not ZeroTrustSecurityManager.validate_node_token("node-1", token, "different-secret")
    assert not ZeroTrustSecurityManager.validate_node_token("node-1", "invalid", "local-test-secret")


def test_node_token_rejects_empty_identity_or_secret():
    with pytest.raises(ValueError):
        ZeroTrustSecurityManager.generate_node_token("", "secret")
    with pytest.raises(ValueError):
        ZeroTrustSecurityManager.generate_node_token("node", "")


def test_payload_sanitization_removes_injection_keys_recursively():
    payload = {
        "safe": "value",
        "$where": "malicious",
        "__proto__": {"polluted": True},
        "settings": {"theme": "dark", "constructor": "bad", "user.name": "bad"},
        "items": [1, {"$ne": None, "ok": True}],
    }
    clean = ZeroTrustSecurityManager.sanitize_payload(payload)
    assert clean == {"safe": "value", "settings": {"theme": "dark"}, "items": [1, {"ok": True}]}
    deeply_nested = current = {}
    for _ in range(40):
        current["child"] = {}
        current = current["child"]
    assert ZeroTrustSecurityManager.sanitize_payload(deeply_nested) == {}


def test_static_security_scan_reports_clean_and_risky_source(tmp_path):
    clean_root = tmp_path / "clean"
    clean_root.mkdir()
    (clean_root / "module.py").write_text("def add(a, b):\n    return a + b\n", encoding="utf-8")
    clean_result = ZeroTrustSecurityManager.static_security_scan(str(clean_root))
    assert clean_result["status"] == "PASS"
    assert clean_result["clean"] is True
    assert clean_result["files_scanned"] == 1

    risky_root = tmp_path / "risky"
    risky_root.mkdir()
    unsafe_assignment = "API" + "_KEY = " + '"hard-coded-value"'
    unsafe_call = "ev" + "al(user_input)"
    (risky_root / "unsafe.py").write_text(unsafe_assignment + "\nresult = " + unsafe_call + "\n", encoding="utf-8")
    risky_result = ZeroTrustSecurityManager.static_security_scan(str(risky_root))
    assert risky_result["status"] == "FAIL"
    assert {item["rule"] for item in risky_result["findings"]} >= {
        "possible_hardcoded_secret", "dynamic eval call",
    }


def test_static_security_scan_invalid_path_is_a_failure(tmp_path):
    result = ZeroTrustSecurityManager.static_security_scan(str(tmp_path / "missing"))
    assert result["status"] == "FAIL"
    assert result["files_scanned"] == 0


def test_audit_ledger_appends_immutable_hash_chained_blocks():
    ledger = CryptoAuditLedger()
    first = ledger.append_entry("system", "START", {"state": "ready", "nested": {"count": 1}})
    second = ledger.append_entry("agent-1", "EXECUTE", {"task_id": "task-1"})
    assert isinstance(first, AuditBlock)
    assert first.previous_hash == "0" * 64
    assert second.previous_hash == first.block_hash
    assert len(first.block_hash) == 64
    assert ledger.verify_integrity() is True
    with pytest.raises((AttributeError, TypeError)):
        first.details["nested"]["count"] = 9
    with pytest.raises((AttributeError, TypeError)):
        first.actor = "attacker"


def test_audit_ledger_detects_tampered_block():
    ledger = CryptoAuditLedger()
    ledger.append_entry("system", "CREATE", {"value": 1})
    ledger.append_entry("system", "UPDATE", {"value": 2})
    object.__setattr__(ledger.blocks[0], "action", "TAMPERED")
    assert ledger.verify_integrity() is False


def test_compliance_framework_checks_and_report():
    config = {
        "controls": {
            "access_control": True,
            "audit_logging": True,
            "encryption_in_transit": True,
            "incident_response": True,
            "consent_management": True,
            "data_minimization": True,
            "data_subject_rights": True,
            "breach_notification": True,
            "data_retention_policy": True,
            "encryption_at_rest": True,
            "information_security_policy": True,
            "risk_assessment": True,
            "asset_inventory": True,
        }
    }
    assert ComplianceEngine.verify_soc2_compliance(config) is True
    assert ComplianceEngine.verify_gdpr_compliance(config) is True
    assert ComplianceEngine.verify_iso27001_compliance(config) is True
    report = ComplianceEngine.get_compliance_report(config)
    assert report["compliant"] is True
    assert all(result["compliant"] for result in report["frameworks"].values())


def test_compliance_report_identifies_missing_controls():
    report = ComplianceEngine.get_compliance_report({"access_control": True})
    assert report["compliant"] is False
    assert report["SOC2"] is False
    assert "audit_logging" in report["frameworks"]["SOC2"]["missing_controls"]
    assert report["GDPR"] is False


def test_gate3_passes_when_every_criterion_is_verified():
    engine = ASMASpecificationEngine()
    gate = engine.spec.business.operational_gates.gates["G3"]
    criteria_results = {criterion: True for criterion in gate.criteria}
    assert engine.evaluate_gate_criteria("G3", criteria_results) is True
    assert gate.status == "PASSED"
