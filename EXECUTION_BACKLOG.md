# Execution Backlog

| Priority | Item | Owner | Acceptance / next action |
|---|---|---|---|
| P0 | Unsupported healthy/PASSED claims | Engineering | **Done in this branch:** API defaults to UNKNOWN/PENDING without evidence; tests pass |
| P0 | Historical `.env` exposure | Founder / security | Privately identify affected providers, rotate any real credentials, coordinate history cleanup |
| P0 | Secure API and founder actions | Backend/security | Implement Auth0 JWT verification and role authorization before any private/business route |
| P0 | UTF-8 defects | Frontend | README and active founder HTML corrected; scan all active source/assets and rendered Arabic |
| P1 | Bilingual customer site | Frontend/content | **Concept routes implemented**; still needs full approved catalog, copy review, accessibility and product content |
| P1 | Deployment routing | DevOps | Resolve Vercel API catch-all vs Cloudflare static hosting; staging acceptance, no deploy without approval |
| P1 | Tenant-scoped persistence | Database | Migrations, RLS/isolation, restore and integration tests |
| P1 | Product SKU and supplier quotes | Operations/founder | Written quote, sample QA and complete landed cost; no fabricated unit costs |
| P1 | Agent manifest/permissions | AI/security | Role IDs, allowlists, approval boundary tests; implement a bounded first workflow |
| P1 | Current test/build pipeline | QA | **Done in this branch:** full Python suite and both frontend builds passed locally; verify CI run after push/PR |
| P2 | Generated dependency files | DevOps | **Done in this branch:** 11,191 node_modules entries removed from index; local directories retained |
| P2 | Dangerous CLI shell/push action | Engineering | **Done in this branch:** fixed argv, shell disabled, no push option; tests pass |
| P2 | Market refresh/customer discovery | Commercial | Dated primary research and consented interviews; assumptions labeled |
| P3 | Production monitoring/backups/SLO | Operations | Measured telemetry, alerts, restore/recovery exercise |

## Execution register

Completed in this branch: dedicated branch creation; baseline evidence; truthful API statuses; closed payment/invoice endpoints; CORS and production-doc defaults; bilingual concept website; truthful founder demo; safe CLI; 15 required handover documents plus an operating handbook; broader CI; dependency index cleanup. Full Python tests and both frontend builds passed. External provider actions, authentication/persistence, legal/commercial readiness and production deployment remain unverified.
