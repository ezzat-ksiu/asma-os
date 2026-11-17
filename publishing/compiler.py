"""Compile Typst documents locally, with zero-cost PDF or Markdown fallbacks."""
from __future__ import annotations

import os
from pathlib import Path
import shutil
import subprocess
import tempfile


class TypstCompiler:
    def __init__(self, executable: str | None = None, *, timeout: float = 60):
        self.executable, self.timeout = executable, timeout

    def compile(self, template_path: str | Path, output_path: str | Path, *,
                metadata: dict[str, str] | None = None) -> str:
        source, output = Path(template_path), Path(output_path)
        if not source.is_file():
            raise FileNotFoundError(source)
        output.parent.mkdir(parents=True, exist_ok=True)
        executable = self.executable or shutil.which("typst")
        if executable:
            fd, temp_name = tempfile.mkstemp(prefix=f".{output.stem}-", suffix=".pdf", dir=output.parent)
            os.close(fd)
            temp = Path(temp_name)
            command = [executable, "compile"]
            for key, value in (metadata or {}).items():
                if not key.replace("_", "").isalnum():
                    raise ValueError(f"Invalid Typst input name: {key}")
                command.extend(["--input", f"{key}={value}"])
            command.extend([str(source), str(temp)])
            try:
                result = subprocess.run(command, capture_output=True, text=True, timeout=self.timeout, check=False)
                if result.returncode:
                    detail = (result.stderr or result.stdout or "Typst compilation failed").strip()
                    raise RuntimeError(detail)
                if not temp.is_file() or temp.stat().st_size == 0:
                    raise RuntimeError("Typst did not produce a PDF")
                os.replace(temp, output)
                return str(output)
            finally:
                temp.unlink(missing_ok=True)

        # ReportLab is optional. If installed, it provides a basic local PDF fallback;
        # otherwise preserve the document source and metadata as a Markdown sidecar.
        try:
            from reportlab.lib.pagesizes import A4
            from reportlab.pdfgen import canvas
        except ImportError:
            markdown = output.with_suffix(".md")
            header = "\n".join(f"- **{key}:** {value}" for key, value in (metadata or {}).items())
            markdown.write_text(f"# {source.stem}\n\n{header}\n\n```typst\n{source.read_text(encoding='utf-8')}\n```\n", encoding="utf-8")
            return str(markdown)
        pdf = output if output.suffix.lower() == ".pdf" else output.with_suffix(".pdf")
        pdf_canvas = canvas.Canvas(str(pdf), pagesize=A4)
        width, height = A4
        y = height - 48
        pdf_canvas.setTitle(source.stem)
        for line in [source.stem, *[f"{key}: {value}" for key, value in (metadata or {}).items()], "", *source.read_text(encoding="utf-8").splitlines()]:
            if y < 48:
                pdf_canvas.showPage(); y = height - 48
            pdf_canvas.drawString(42, y, line[:110])
            y -= 14
        pdf_canvas.save()
        return str(pdf)
