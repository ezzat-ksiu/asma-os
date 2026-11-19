# FOLIAVERE / ASMA-OS

FOLIAVERE is the provisional customer-facing working name in the approved brand system. Trademark and domain clearance have not been established. FOLIOMIND remains an unconfirmed project label. ASMA-OS is the internal software platform name.

## Current status

This repository contains approved research and strategy documents, local core modules, provider adapter scaffolds, an Astro concept storefront, a React founder-console demo, and a FastAPI local API. It is not a verified production service or commercial launch.

The current storefront is a concept demonstration only. There is no checkout, customer upload, production book fulfillment, or authenticated founder operations system. The API reports gate evidence as pending until real checks and artifacts are integrated. Payment initiation is disabled.

## Local development

Requirements observed: Python 3.12, Node.js 24, npm 11, Git. A local `.venv` already exists.

```powershell
.venv\Scripts\python.exe -m pip install -r requirements.txt
.venv\Scripts\python.exe -m pytest -v

Push-Location apps\storefront
npm ci
npm run build
Pop-Location

Push-Location apps\founder-screen
npm ci
npm run build
Pop-Location
```

See [INSTALL_AND_VERIFY.md](INSTALL_AND_VERIFY.md), [MASTER_PROJECT_STATUS.md](MASTER_PROJECT_STATUS.md), and [docs/README.md](docs/README.md).

## Security and launch boundaries

- Never place credentials in source or commit `.env` files.
- Historical repository history contained a `.env`; owners must privately review and rotate any real credentials.
- No live payment, customer communication, supplier order, public deployment, or legal approval is established.
- Do not use estimates or synthetic portfolio examples as actual supplier quotes or customer results.
- Do not report a gate as passed without auditable verification evidence.
