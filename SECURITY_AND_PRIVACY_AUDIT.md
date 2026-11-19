# Security and Privacy Audit

**Status: remediation required; not a compliance certification.** No credentials or customer data were printed or used.

| Finding | Severity | Evidence | Safe remediation / validation |
|---|---|---|---|
| Historical tracked `.env` | Critical if values were real | Git history includes `.env` before deletion at `5378e73a`; current file ignored | Owner reviews secret categories privately, rotates any live credentials, then plans history cleanup; verify with secret scanner |
| False gate/health claims | High | Old `api/main.py` returned all PASSED and healthy statically | Branch replaces with PENDING/UNKNOWN and tests for no evidence |
| Wildcard credentialed CORS | High | Old API allowed `*` origins with credentials | Branch defaults to no CORS origins and accepts explicit allowlist only; test preflight |
| API has public read-only health/gates | Medium | `/api/health` and `/api/gates` intentionally expose non-customer status; no tenant CRUD exists | Keep responses non-sensitive; private founder summary now requires Auth0 RS256 verification and exact configured subject allowlist |
| Public interactive API docs | Medium | `/docs` and `/redoc` enabled | Disable or protect in production configuration |
| No DB row-level security | High | Migration contains tables, no RLS policies found | Add tenant policies, least-privilege roles, cross-tenant negative tests |
| Public tracked Wrangler cache | Medium | `.wrangler/cache` metadata tracked | Remove cache files from index in reviewed commit; never publish credentials |
| Payment endpoint absent | High for commercial claims | No transaction API on baseline | Added explicit 503 fail-closed path; no payment can be initiated |
| Upload/privacy lifecycle absent | High | No customer upload journey or integrated purge proof | Keep upload disabled until access control, retention, deletion receipts, limits and tests exist |
| CLI can push to main | High operational | `cli.py` menu runs shell command with direct git push | Remove/disable action and avoid `shell=True`; add safe branch/PR workflow |

## Historical credential handling runbook

1. An authorized owner identifies which historical provider credentials were real without copying values into chat, issues, or repo files.
2. Rotate/revoke at each provider account; verify old credentials fail and replacement credentials work in private deployment settings.
3. Review access logs and scopes for unexpected use.
4. Remove secret blobs from history only after a documented recovery/coordination plan; history rewriting affects every clone and requires explicit owner coordination.
5. Re-scan current tree and history with a secret scanner, then document provider/category and rotation date without recording secret values.

## Privacy guardrails

No child-face biometrics; no customer asset intake until consent, purpose limitation, secure storage, authorized access, retention, deletion, backup treatment, and processor terms are implemented. Legal requirements depend on jurisdiction and require qualified counsel. Technical controls do not constitute legal approval.

**Branch update:** API docs/OpenAPI are disabled when `ASMA_ENV=production`; CORS allowlist rejects `*`; `/api/founder/summary` fails closed unless Auth0 domain, audience, token and founder-subject allowlist are configured. The summary returns NOT_CONFIGURED for business data. This does not authenticate public health/gate reads or provide customer/tenant operations. Private functionality remains unavailable pending database/policy integration.
