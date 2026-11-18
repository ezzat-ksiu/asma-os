# FOLIAVERE project workspace

FOLIAVERE is the customer-facing publishing concept and a **working name pending trademark, domain, and seller-identity review**. ASMA-OS is the internal operating-system name. This repository contains the concept package and local implementation scaffold; it does not establish that the service is commercially launched, legally cleared, or connected to live providers.

## Project package

The source deliverables and their output mapping are listed in [docs/README.md](docs/README.md). Approved source documents are retained in `docs/`; the customer-facing brand system and web implementation live in `brand/` and `apps/storefront/`.

## Local development

- Python: activate `.venv`, then run `python -m pytest -v`.
- Storefront: `cd apps/storefront && npm run build`.
- Founder console: `cd apps/founder-screen && npm run build`.
- API: run `uvicorn api.main:app` from the repository root after installing `requirements.txt`.

The default API is local-first. Payment initiation, invoice issuance, provider calls, and public vault publication remain disabled or empty until real configuration, evidence, consent, and review are supplied. Never place credentials in source control; configure local environment variables from `.env.example` files.

## Product and operational boundaries

- Portfolio titles and AV-001…AV-006 records are fictional samples, not customer orders or completed print runs.
- Edition prices, cost and financial figures in source documents are planning assumptions, not live quotes, sales or ARR.
- Personalised checkout, print dispatch, public release, legal notices and paid marketing require the documented approvals and external verification.
- No child photographs or face biometrics are accepted in the initial concept.
- Names, domains, provider integrations, legal compliance, and printer quality remain unverified until independently checked.

See [docs/00_board_audit.md](docs/00_board_audit.md), [docs/01_name_and_domains.md](docs/01_name_and_domains.md), and [docs/10_finance_execution_quality.md](docs/10_finance_execution_quality.md) for controlling decisions and evidence status.
