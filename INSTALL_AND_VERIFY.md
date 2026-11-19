# Install and Verify

This guide uses the existing local environment and does not activate paid services.

## Python

```powershell
.venv\Scripts\python.exe -m pip install -r requirements.txt
.venv\Scripts\python.exe -m pytest -v
```

Do not run provider tests against live credentials by default. Tests that write tracked artifacts should run in a disposable checkout or use a temporary output directory.

## Storefront and founder app

```powershell
Push-Location apps\storefront
npm ci
npm run build
Pop-Location

Push-Location apps\founder-screen
npm ci
npm run build
Pop-Location
```

Use the package lockfile for reproducibility; if a lockfile is missing or stale, resolve that in a separate reviewed change. Current Node/npm versions observed: 24.21.0 / 11.19.0.

## API local smoke check

```powershell
.venv\Scripts\python.exe -m uvicorn api.main:app --host 127.0.0.1 --port 8000
Invoke-RestMethod http://127.0.0.1:8000/api/health
Invoke-RestMethod http://127.0.0.1:8000/api/gates
```

Expected default state: readiness `NOT_CONFIGURED`, gates `PENDING`, zero gate evidence, payment initiation `503`. Do not treat local readiness as production availability.

## Optional CORS configuration

Set `ASMA_CORS_ALLOWED_ORIGINS` to an explicit comma-separated list of exact trusted origins. Never use `*` with credentials. No value is required for same-origin/local API tests.
