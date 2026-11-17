import subprocess
import os
import tempfile
from pathlib import Path
from typing import Dict, Any

class TypstDocumentGenerator:
    """Generates official PDFs (Invoices, Proposals, Contracts) using Typst CLI."""

    @staticmethod
    def generate_pdf(typst_markup: str, output_path: str) -> str:
        out_file = Path(output_path).resolve()
        out_file.parent.mkdir(parents=True, exist_ok=True)

        with tempfile.NamedTemporaryFile(mode='w', suffix='.typ', delete=False, encoding='utf-8') as tmp:
            tmp.write(typst_markup)
            tmp_path = tmp.name

        try:
            cmd = ["typst", "compile", tmp_path, str(out_file)]
            result = subprocess.run(cmd, capture_output=True, text=True, check=True)
            return str(out_file)
        finally:
            if os.path.exists(tmp_path):
                os.remove(tmp_path)

    @classmethod
    def generate_invoice(cls, invoice_data: Dict[str, Any], output_pdf_path: str) -> str:
        client_name = invoice_data.get("client_name", "Valued Client")
        invoice_id = invoice_data.get("invoice_id", "INV-001")
        amount = invoice_data.get("amount", 0.0)
        currency = invoice_data.get("currency", "EGP")
        services = invoice_data.get("services", [])

        items_typst = ""
        for item in services:
            qty = item.get("qty", 1)
            price = item.get("price", 0)
            items_typst += f'  [{item.get("name")}], [{qty}], [{price} {currency}], [{qty * price} {currency}],\n'

        markup = f"""
#set page(paper: "a4", margin: (x: 2cm, y: 2.5cm))
#set text(size: 11pt, lang: "ar")

#align(right)[
  #text(size: 20pt, weight: "bold", fill: rgb("#0f172a"))[ASMA-OS V6.0 Enterprise] \
  #text(size: 10pt, fill: rgb("#64748b"))[Autonomous Operating System & AI Governance Engine]
]

#v(1em)
#line(length: 100%, stroke: 1pt + rgb("#cbd5e1"))
#v(1em)

#grid(
  columns: (1fr, 1fr),
  [
    *Billed To:* \
    {client_name} \
    Date: {invoice_data.get("date", "2025-03-30")}
  ],
  [
    #align(right)[
      *Invoice ID:* `{invoice_id}` \
      *Status:* Paid via Paymob \
      *Engine Gate:* Gate 6 Automated Execution
    ]
  ]
)

#v(2em)

#table(
  columns: (2fr, 1fr, 1fr, 1fr),
  fill: (x, y) => if y == 0 {{ rgb("#f1f5f9") }} else {{ none }},
  stroke: 0.5pt + rgb("#e2e8f0"),
  [*Service Description*], [*Qty*], [*Unit Price*], [*Total*],
  {items_typst}
)

#v(1.5em)
#align(right)[
  #rect(fill: rgb("#f8fafc"), inset: 10pt, radius: 4pt)[
    *Total Amount:* #text(size: 14pt, weight: "bold", fill: rgb("#0284c7"))[{amount} {currency}]
  ]
]

#v(3em)
#align(center)[
  #text(size: 8pt, fill: rgb("#94a3b8"))[
    Generated automatically by ASMA-OS Gate 6 Governance Engine. Verification Key: {invoice_data.get("verification_hash", "SEC-GATE6-VERIFIED")}
  ]
]
"""
        return cls.generate_pdf(markup, output_pdf_path)
