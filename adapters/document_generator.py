"""Typst compilation and explicitly non-binding invoice preview generation."""
import os
import json
import subprocess
import tempfile
from pathlib import Path
from typing import Any

class TypstDocumentGenerator:
    @staticmethod
    def generate_pdf(typst_markup: str, output_path: str) -> str:
        out_file = Path(output_path).resolve()
        out_file.parent.mkdir(parents=True, exist_ok=True)
        with tempfile.NamedTemporaryFile(mode="w", suffix=".typ", delete=False, encoding="utf-8") as tmp:
            tmp.write(typst_markup)
            tmp_path = tmp.name
        try:
            subprocess.run(["typst", "compile", tmp_path, str(out_file)], capture_output=True, text=True, check=True)
            return str(out_file)
        finally:
            if os.path.exists(tmp_path):
                os.remove(tmp_path)

    @staticmethod
    def _text(value: Any) -> str:
        # JSON quoting safely encodes quotes, slashes, newlines, and control chars
        # as a Typst string literal, so supplied text cannot become Typst code.
        return "#text(" + json.dumps(str(value), ensure_ascii=False) + ")"

    @classmethod
    def generate_invoice(cls, invoice_data: dict[str, Any], output_pdf_path: str) -> str:
        """Render a demo preview. This output is never an invoice or payment proof."""
        currency = str(invoice_data.get("currency", "EGP"))
        rows = []
        for item in invoice_data.get("services", []):
            qty, price = item.get("qty", 1), item.get("price", 0)
            rows.append("[" + cls._text(item.get("name", "Sample item")) + "], [" + cls._text(qty) + "], [" + cls._text(f"{price} {currency}") + "], [" + cls._text(f"{qty * price} {currency}") + "],")
        items = "\n".join(rows) or '[—], [—], [—], [—],'
        markup = f'''
#set page(paper: "a4", margin: (x: 2cm, y: 2cm))
#set text(size: 11pt)
#align(center)[#text(size: 19pt, weight: "bold")[DOCUMENT PREVIEW — NOT AN INVOICE]]
#v(0.6em)
#align(center)[#text(size: 12pt, fill: rgb("#8b3d2f"))[DEMO ONLY · NOT VALID FOR PAYMENT, TAX, OR PROOF OF TRANSACTION]]
#line(length: 100%, stroke: 1pt + rgb("#999999"))
#v(1em)
#grid(columns: (1fr, 1fr), [Recipient: {cls._text(invoice_data.get("client_name", "Sample recipient"))} \\ Reference: {cls._text(invoice_data.get("invoice_id", "DEMO"))}], [Date: {cls._text(invoice_data.get("date", "Not specified"))} \\ Status: NOT PAID / NOT VERIFIED])
#v(1em)
#table(columns: (2fr, 1fr, 1fr, 1fr), stroke: 0.5pt + rgb("#bbbbbb"), [*Description*], [*Qty*], [*Unit price*], [*Line total*], {items})
#v(1em)
#align(right)[#text(weight: "bold")[Preview amount: {cls._text(invoice_data.get("amount", "Not specified"))} {cls._text(currency)}]]
#v(2em)
#align(center)[This fictional document is for layout testing only. It does not establish an order, debt, payment, tax treatment, or legal relationship.]
'''
        return cls.generate_pdf(markup, output_pdf_path)
