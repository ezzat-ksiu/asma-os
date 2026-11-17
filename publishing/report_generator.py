"""Generate specification reports with Typst or a Markdown fallback."""

from __future__ import annotations

import json
import os
from pathlib import Path
import shutil
import subprocess
import tempfile

from spec_schema import ASMASpec


class ReportGenerator:
    """Render ASMA-OS reports without requiring a paid document service."""

    def __init__(self, typst_executable: str | None = None, template_path: str | None = None) -> None:
        self.typst_executable = typst_executable
        self.template_path = Path(template_path) if template_path else Path(__file__).with_name("template.typ")

    @staticmethod
    def _metadata(spec: ASMASpec) -> dict:
        gates = spec.business.operational_gates.gates
        return {
            "title": "ASMA-OS System Specification",
            "version": spec.version,
            "vision": spec.business.vision,
            "gate_count": len(gates),
            "gates": [
                {
                    "id": gate.gate_id,
                    "name": gate.name,
                    "status": str(gate.status),
                    "criteria": list(gate.criteria),
                }
                for gate in gates.values()
            ],
            "orchestration_engine": spec.execution.orchestration_engine,
            "protocol": spec.execution.protocol,
            "mesh_topology": spec.execution.mesh_topology,
            "scaling_policy": spec.technical.scaling_policy.model_dump(mode="json"),
            "quality_security": spec.technical.quality_security.model_dump(mode="json"),
            "financial_model": spec.business.financial_model.model_dump(mode="json"),
        }

    @staticmethod
    def _markdown(metadata: dict, render_error: str | None = None) -> str:
        lines = [
            f"# {metadata['title']}",
            "",
            f"- **Version:** {metadata['version']}",
            f"- **Vision:** {metadata['vision']}",
            f"- **Orchestration:** {metadata['orchestration_engine']}",
            f"- **Protocol:** {metadata['protocol']}",
            f"- **Mesh topology:** {metadata['mesh_topology']}",
            f"- **Configured gates:** {metadata['gate_count']}",
            "",
            "## Operational gates",
            "",
            "| Gate | Name | Status |",
            "| --- | --- | --- |",
        ]
        lines.extend(
            f"| {gate['id']} | {gate['name']} | {gate['status']} |"
            for gate in metadata["gates"]
        )
        lines.extend([
            "",
            "## Scaling policy",
            "",
            "Scaling policy JSON:",
            json.dumps(metadata["scaling_policy"], indent=2, ensure_ascii=False),
            "",
            "## Quality and security",
            "",
            "Quality and security JSON:",
            json.dumps(metadata["quality_security"], indent=2, ensure_ascii=False),
            "",
            "## Financial model",
            "",
            "Financial model JSON:",
            json.dumps(metadata["financial_model"], indent=2, ensure_ascii=False),
        ])
        if render_error:
            lines.extend(["", f"> PDF rendering unavailable; generated this Markdown report instead ({render_error})."])
        return "\n".join(lines) + "\n"

    def _typst_command(self) -> str | None:
        return self.typst_executable or shutil.which("typst")

    def generate_spec_report(
        self,
        spec: ASMASpec,
        output_path: str = "publishing/system_spec_report.pdf",
    ) -> str:
        metadata = self._metadata(spec)
        requested = Path(output_path).expanduser()
        requested.parent.mkdir(parents=True, exist_ok=True)
        executable = self._typst_command()
        error: str | None = None

        if executable and self.template_path.is_file():
            descriptor, temporary_name = tempfile.mkstemp(
                prefix=f".{requested.stem}-", suffix=".pdf", dir=str(requested.parent)
            )
            os.close(descriptor)
            temporary_pdf = Path(temporary_name)
            gate_summary = "; ".join(
                f"{gate['id']} {gate['name']} [{gate['status']}]"
                for gate in metadata["gates"]
            )
            scaling = metadata["scaling_policy"]
            quality = metadata["quality_security"]
            summary = (
                f"Vision: {metadata['vision']} | Engine: {metadata['orchestration_engine']} | "
                f"Protocol: {metadata['protocol']} | Nodes: {scaling['min_nodes']}–{scaling['max_nodes']} | "
                f"CPU limit: {scaling['cpu_threshold_pct']}% | Memory limit: {scaling['memory_threshold_pct']}% | "
                f"Security: {quality['security_level']} | Gates: {gate_summary}"
            )
            command = [
                executable,
                "compile",
                "--input", f"title={metadata['title']}",
                "--input", f"version={metadata['version']}",
                "--input", f"summary={summary}",
                str(self.template_path),
                str(temporary_pdf),
            ]
            try:
                completed = subprocess.run(
                    command, capture_output=True, text=True, timeout=60, check=False
                )
                if completed.returncode != 0:
                    error = (completed.stderr or completed.stdout or "Typst compilation failed").strip()
                    raise RuntimeError(error)
                if not temporary_pdf.is_file() or temporary_pdf.stat().st_size == 0:
                    raise RuntimeError("Typst completed without producing a PDF")
                os.replace(temporary_pdf, requested)
                return str(requested)
            except (OSError, subprocess.SubprocessError, RuntimeError) as exc:
                error = str(exc)
            finally:
                temporary_pdf.unlink(missing_ok=True)
        elif executable:
            error = f"Typst template not found: {self.template_path}"
        else:
            error = "Typst CLI is not installed"

        markdown_path = requested.with_suffix(".md")
        markdown_path.write_text(self._markdown(metadata, error), encoding="utf-8")
        return str(markdown_path)
