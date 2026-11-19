# Database and Integrations

## Current database state

`database/001_initial_schema.sql` creates audit, mesh, gate and checkpoint tables. `adapters/postgres_adapter.py` wraps an asyncpg-style pool, but `asyncpg` is not a declared dependency and the API/workflow/commercial service do not use the adapter. The current schema has no row-level security, tenant ownership constraints or tested migration runner. The audit table is not the same as the in-memory hash-chained `CryptoAuditLedger`.

## Required persistence work

- Introduce migration versioning and transactional application.
- Define tenant/order/artifact/evidence ownership and foreign keys.
- Enforce tenant-scoped access in the database, not just API filters.
- Add RLS policies and least-privilege service roles where supported.
- Persist idempotency records and webhook event IDs under unique constraints.
- Persist audit hash-chain entries with canonical serialization and integrity verification.
- Define encrypted backup, restore test, retention, deletion, and evidence handling.
- Add integration tests using a free local PostgreSQL option only when available; do not require a paid hosted service.

## Adapter boundaries

Auth0, Paymob, R2, Gelato, Lulu and Resend modules are client scaffolds. Test them with injected fake transports and provider sandbox credentials only. Require timeouts, bounded retries, redacted logs, idempotency, signature verification, error mapping and circuit breakers. Do not initiate payment, send email, upload customer assets, or create print jobs in ordinary local tests.

Cloudflare's current R2 documentation confirms a distinct S3-compatible API and documents lifecycle configuration. The documented lifecycle behavior says expiration is typically processed within 24 hours and existing objects may take longer, so lifecycle expiry must not be represented as immediate purge or a guaranteed 24-hour deletion SLA. Direct `purge_prefix` deletion and provider-side lifecycle cleanup are separate controls; deletion needs a verified receipt and backup/replica treatment. Astro documents file-based localized routes; this site uses static `/ar/` and `/en/` routes and has not yet enabled framework-level i18n validation.

References checked 2026-11-19: [Cloudflare R2 S3 API setup](https://developers.cloudflare.com/r2/get-started/s3/), [Cloudflare R2 lifecycle behavior](https://developers.cloudflare.com/r2/buckets/object-lifecycles/), [Astro i18n routing](https://docs.astro.build/en/guides/internationalization/). These establish platform behavior, not this project's live account configuration.

## Hosting topology

Current `vercel.json` sends all routes to the API while Cloudflare configs describe static assets. Choose one documented deployment topology, map `/api/*` and static routes deliberately, then verify staging without exposing customer data. This audit did not verify a live deployment or service account.
