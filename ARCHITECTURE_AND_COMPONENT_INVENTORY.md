# Architecture and Component Inventory

## Current topology

| Layer | Components | Current evidence / limitation |
|---|---|---|
| Storefront | Astro 4 app at `apps/storefront` | Only `src/pages/index.astro` is active; one Arabic page |
| Founder console | React 18 / Vite 5 at `apps/founder-screen` | Active `.jsx` path is a static status card; TSX is stale/inactive |
| API | FastAPI at `api/main.py` | In-memory/default status only; no auth or persistence connection |
| Domain core | `spec_schema.py`, `asma_os_mesh.py`, `core/` | Local libraries; not wired into API operational status |
| Agents | `agents/` | Base, gateway, execution, planning, review abstractions; no 45-role executor |
| Workflow | `workflows/` | plan/execute/review graph with local checkpoint behavior; no connected durable store |
| Commercial | `services/commercial.py`, billing adapter | Local/in-memory logic; no real order or settlement proof |
| Integrations | storage, identity, POD, payment, notifications adapters | Interfaces/scaffolds; not live-verified |
| Database | `database/001_initial_schema.sql`, `PostgresAdapter` | Schema and wrapper only; no runtime wiring/RLS; asyncpg absent from requirements |
| Deploy | Vercel catch-all and Cloudflare Pages configs | Conflicting routing topology; current deployments not verified |

## Request/data path (intended, not operational)

`Browser → authenticated API → validated tenant/order data → durable DB and audit evidence → approved workflow → QA and founder approval → provider adapter`.

Current active path is materially shorter: browser loads static Astro/React content; the React card optionally calls a fixed public health URL. Do not infer order processing from adapter availability.

## Repo hygiene

At audit start, 11,311 files were tracked; 11,191 were in `node_modules` (most `dist` files were package-internal). This branch removes both app `node_modules` trees from the Git index while leaving their local directories intact. Existing tracked built output is retained for now because deployment configuration references generated assets; remove it only after the deployment/build pipeline is tested from a clean clone. Preserve a recoverable branch and do not rewrite shared history.

## Runtime architecture decision

Use one API service and a single role/permission registry before considering multiple agent services. Keep Astro and founder UI static/local until authenticated APIs and data lifecycle exist. The current Vercel catch-all routes all paths into the API, so the desired storefront/API hosting split must be explicitly selected and tested before deployment.
