# Development Environment

## Observed on 2026-11-19

| Tool | Observed version/status | Use |
|---|---|---|
| Windows | 10.0.26300.0 | Developer workstation |
| PowerShell | 7.6.9 | Setup and verification |
| Python | 3.12.10 global and `.venv` | API, agents, tests |
| Node.js | v24.21.0 | Astro/Vite apps |
| npm | 11.19.0 | JS dependencies/builds |
| Git | 2.56.0.windows.4 | Version control |
| Typst CLI | 0.15.1 | Typst PDF test executed and passed |
| GitHub CLI | 2.104.0 | Installed; authentication state not inspected |
| Docker CLI | 29.9.2 | Installed; daemon/container operation not tested |
| pnpm | 12.16.1 | Installed; apps use npm lockfiles |
| VS Code | Installed | Version query hit a sandbox working-directory permission error; not required for builds |

No tools were installed during this pass. Existing `.venv` and local `node_modules` directories were preserved. This branch removes both app dependency trees from the Git index but leaves them available locally.

## Dependencies

Python core dependencies are listed in `requirements.txt`; provider integrations use lazy/optional imports. `PostgresAdapter.connect()` requires `asyncpg`, which is not currently declared in either requirements file. Add it when PostgreSQL connectivity becomes part of the chosen runtime. Frontend dependencies are declared in each app's `package.json`; offline `npm ci --dry-run --ignore-scripts` succeeded for both lockfiles.

## Zero-upfront-cost posture

Local builds, tests, Python, Node, Git and free open-source tools are sufficient for the current engineering phase. No paid provider service, hosted database, domain, production transaction, or cloud usage is required to validate the local code. Provider credentials must be supplied privately and only for an explicitly approved sandbox/live test.
