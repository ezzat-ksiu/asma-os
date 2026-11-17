"""Readiness checks for selected SOC 2, GDPR, and ISO 27001 control areas."""

from __future__ import annotations

from typing import Any


class ComplianceEngine:
    """Evaluate explicit control evidence; this is not a certification opinion."""

    _framework_controls = {
        "SOC2": {
            "access_control": ("access_control", "rbac_enabled"),
            "audit_logging": ("audit_logging", "audit_ledger_operational", "audit_ledger_active", "audit_ledger"),
            "encryption_in_transit": ("encryption_in_transit", "tls_enabled"),
            "incident_response": ("incident_response", "incident_response_plan"),
        },
        "GDPR": {
            "consent_management": ("consent_management", "consent_tracking"),
            "data_minimization": ("data_minimization",),
            "data_subject_rights": ("data_subject_rights", "subject_access_requests"),
            "breach_notification": ("breach_notification", "breach_notification_process"),
            "data_retention_policy": ("data_retention_policy",),
            "encryption_at_rest": ("encryption_at_rest",),
        },
        "ISO27001": {
            "information_security_policy": ("information_security_policy", "security_policy"),
            "risk_assessment": ("risk_assessment", "risk_register"),
            "access_control": ("access_control", "rbac_enabled"),
            "incident_response": ("incident_response", "incident_response_plan"),
            "asset_inventory": ("asset_inventory",),
            "audit_logging": ("audit_logging", "audit_ledger_operational", "audit_ledger_active", "audit_ledger"),
        },
    }

    @staticmethod
    def _control_sources(system_config: dict[str, Any], framework: str) -> list[dict[str, Any]]:
        sources = [system_config]
        for name in ("controls", "security_controls", "compliance_controls"):
            nested = system_config.get(name)
            if isinstance(nested, dict):
                sources.append(nested)
        framework_config = system_config.get(framework.lower())
        if isinstance(framework_config, dict):
            sources.append(framework_config)
        return sources

    @classmethod
    def _evaluate(cls, system_config: dict[str, Any], framework: str) -> dict[str, Any]:
        if not isinstance(system_config, dict):
            raise TypeError("system_config must be a dictionary")
        sources = cls._control_sources(system_config, framework)
        missing: list[str] = []
        for control, aliases in cls._framework_controls[framework].items():
            present = False
            for source in sources:
                for alias in aliases:
                    value = source.get(alias)
                    if value is True:
                        present = True
                    elif alias in {"audit_ledger_operational", "audit_ledger_active", "audit_ledger"} and isinstance(value, dict):
                        present = value.get("status") == "ACTIVE"
                    if present:
                        break
                if present:
                    break
            if not present:
                missing.append(control)
        return {"compliant": not missing, "missing_controls": missing}

    @classmethod
    def verify_soc2_compliance(cls, system_config: dict) -> bool:
        return cls._evaluate(system_config, "SOC2")["compliant"]

    @classmethod
    def verify_gdpr_compliance(cls, system_config: dict) -> bool:
        return cls._evaluate(system_config, "GDPR")["compliant"]

    @classmethod
    def verify_iso27001_compliance(cls, system_config: dict) -> bool:
        return cls._evaluate(system_config, "ISO27001")["compliant"]

    @classmethod
    def get_compliance_report(cls, system_config: dict) -> dict[str, Any]:
        frameworks = {
            framework: cls._evaluate(system_config, framework)
            for framework in cls._framework_controls
        }
        return {
            "compliant": all(result["compliant"] for result in frameworks.values()),
            "frameworks": frameworks,
            **{framework: result["compliant"] for framework, result in frameworks.items()},
        }
