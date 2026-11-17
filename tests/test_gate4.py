"""Gate 4 readiness, CI, scaling, monitoring, publishing, and gate tests."""

from pathlib import Path
from types import SimpleNamespace

import pytest
import yaml

from asma_os_mesh import ASMANodeRegistry, ASMASpecificationEngine, MeshNode, MeshNodeStatus, MeshNodeType
from core.audit import CryptoAuditLedger
from core.health import HealthMonitor
from core.scaling import ScalingEngine
from publishing.report_generator import ReportGenerator
from spec_schema import ASMASpec, ScalingPolicy


ROOT = Path(__file__).resolve().parents[1]


def test_ci_workflow_has_valid_yaml_triggers_and_test_steps():
    workflow_path = ROOT / ".github" / "workflows" / "ci.yml"
    workflow = yaml.load(workflow_path.read_text(encoding="utf-8"), Loader=yaml.BaseLoader)
    assert workflow["name"] == "ASMA-OS CI/CD Pipeline"
    assert workflow["on"]["push"]["branches"] == ["main"]
    assert workflow["on"]["pull_request"]["branches"] == ["main"]
    steps = workflow["jobs"]["test"]["steps"]
    assert any(step.get("uses", "").startswith("actions/checkout@") for step in steps)
    python_setup = next(step for step in steps if step.get("name") == "Set up Python 3.12")
    assert python_setup["with"]["python-version"] == "3.12"
    assert any("requirements.txt" in step.get("run", "") for step in steps)
    assert any("pytest -v" in step.get("run", "") for step in steps)


def test_scaling_engine_recommends_scale_up_down_and_stable():
    engine = ScalingEngine()
    assert engine.evaluate_scaling(2, 30, 30)["recommendation"] == "SCALE_UP"
    assert engine.evaluate_scaling(3, 90, 50)["recommendation"] == "SCALE_UP"
    assert engine.evaluate_scaling(4, 20, 20)["recommendation"] == "SCALE_DOWN"
    assert engine.evaluate_scaling(3, 50, 50)["recommendation"] == "STABLE"
    assert engine.evaluate_scaling(100, 100, 100)["recommendation"] == "STABLE"


def test_scaling_engine_obeys_disabled_policy_and_validates_inputs():
    engine = ScalingEngine(ScalingPolicy(auto_scale_enabled=False))
    assert engine.evaluate_scaling(1, 100, 100)["recommendation"] == "STABLE"
    with pytest.raises(ValueError):
        ScalingEngine().evaluate_scaling(-1, 10, 10)
    with pytest.raises(ValueError):
        ScalingEngine().evaluate_scaling(3, 101, 10)


def _register_active_nodes(registry, count, node_type=MeshNodeType.EXECUTION):
    for index in range(count):
        registry.register_node(
            MeshNode(
                node_id=f"{node_type.value}-{index}",
                node_type=node_type,
                status=MeshNodeStatus.ACTIVE,
            )
        )


def test_apply_scaling_adds_and_removes_only_execution_nodes():
    registry = ASMANodeRegistry()
    _register_active_nodes(registry, 3)
    engine = ScalingEngine()

    scale_up = engine.evaluate_scaling(3, 90, 50)
    added = engine.apply_scaling(registry, scale_up)
    assert len(added) == 1
    assert len(registry.list_active_nodes()) == 4

    registry.register_node(
        MeshNode(node_id="gateway-core", node_type=MeshNodeType.GATEWAY, status=MeshNodeStatus.ACTIVE)
    )
    # The requested scale-down reaches the minimum while preserving the gateway.
    removed = engine.apply_scaling(registry, {"recommendation": "SCALE_DOWN", "target_count": 3})
    assert len(removed) == 2
    assert registry.get_node("gateway-core") is not None
    assert len(registry.list_active_nodes()) == 3
    assert all(registry.get_node(node_id) is None for node_id in removed)


def test_scaling_respects_minimum_node_count():
    registry = ASMANodeRegistry()
    _register_active_nodes(registry, 3)
    removed = ScalingEngine().apply_scaling(
        registry, {"recommendation": "SCALE_DOWN", "target_count": 0}
    )
    assert removed == []
    assert len(registry.list_active_nodes()) == 3


def test_health_monitor_reports_full_readiness_for_healthy_mesh():
    registry = ASMANodeRegistry()
    _register_active_nodes(registry, 3)
    ledger = CryptoAuditLedger()
    ledger.append_entry("system", "READY", {"healthy": True})

    report = HealthMonitor().check_system_health(registry, ledger)
    assert report["ready"] is True
    assert report["overall_readiness_score"] == 100.0
    assert report["active_nodes"] == 3
    assert report["total_nodes"] == 3
    assert report["ledger_integrity"] is True


def test_health_monitor_degrades_readiness_for_node_and_ledger_failures():
    registry = ASMANodeRegistry()
    _register_active_nodes(registry, 2)
    failed = MeshNode(
        node_id="failed-node",
        node_type=MeshNodeType.EXECUTION,
        status=MeshNodeStatus.FAILED,
        health_score=0.0,
    )
    registry.register_node(failed)
    ledger = CryptoAuditLedger()
    ledger.append_entry("system", "START", {})
    object.__setattr__(ledger.blocks[0], "action", "TAMPERED")

    report = HealthMonitor().check_system_health(registry, ledger)
    assert report["ready"] is False
    assert report["ledger_integrity"] is False
    assert report["components"]["audit_ledger"] == "FAILED"
    assert report["overall_readiness_score"] < 90.0


def test_report_generator_falls_back_to_markdown_without_typst(tmp_path, monkeypatch):
    monkeypatch.setattr("publishing.report_generator.shutil.which", lambda _: None)
    requested_pdf = tmp_path / "system-report.pdf"
    result = ReportGenerator().generate_spec_report(ASMASpec(), str(requested_pdf))
    output = Path(result)
    assert output.suffix == ".md"
    markdown = output.read_text(encoding="utf-8")
    assert "ASMA-OS System Specification" in markdown
    assert "Version:** 6.0" in markdown
    assert "Typst CLI is not installed" in markdown


def test_report_generator_compiles_pdf_when_typst_is_available(tmp_path, monkeypatch):
    monkeypatch.setattr("publishing.report_generator.shutil.which", lambda _: "typst")
    commands = []

    def fake_compile(command, **kwargs):
        commands.append(command)
        Path(command[-1]).write_bytes(b"%PDF-test")
        return SimpleNamespace(returncode=0, stdout="", stderr="")

    monkeypatch.setattr("publishing.report_generator.subprocess.run", fake_compile)
    output_path = tmp_path / "spec.pdf"
    result = ReportGenerator().generate_spec_report(ASMASpec(), str(output_path))
    assert result == str(output_path)
    assert output_path.read_bytes().startswith(b"%PDF")
    assert "--input" in commands[0]
    assert any(argument.startswith("version=6.0") for argument in commands[0])


def test_report_generator_falls_back_when_typst_compile_fails(tmp_path, monkeypatch):
    monkeypatch.setattr("publishing.report_generator.shutil.which", lambda _: "typst")
    monkeypatch.setattr(
        "publishing.report_generator.subprocess.run",
        lambda *args, **kwargs: SimpleNamespace(returncode=1, stdout="", stderr="compile error"),
    )
    result = ReportGenerator().generate_spec_report(ASMASpec(), str(tmp_path / "bad.pdf"))
    assert Path(result).suffix == ".md"
    assert "compile error" in Path(result).read_text(encoding="utf-8")


def test_gate4_criteria_evaluation_marks_gate_passed():
    engine = ASMASpecificationEngine()
    gate = engine.spec.business.operational_gates.gates["G4"]
    results = {criterion: True for criterion in gate.criteria}
    assert engine.evaluate_gate_criteria("G4", results) is True
    assert gate.status == "PASSED"
