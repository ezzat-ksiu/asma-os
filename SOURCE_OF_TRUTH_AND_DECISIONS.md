# Source of Truth and Decisions

## Authority order

1. Latest explicit founder decisions.
2. Approved source documents and binding constraints.
3. Latest validated implementation that does not conflict with approved requirements.
4. Current primary-source technical evidence.
5. Conservative engineering judgment; assumptions must be labeled.

## Canonical names

| Term | Canonical use | Status |
|---|---|---|
| FOLIAVERE | Proposed customer-facing product/brand | Provisional; clearance not performed |
| FOLIOMIND | Historical project label used in board-audit material | Founder decision needed before external use |
| ASMA-OS | Internal software and operating-system name | Project identifier, not a company registration claim |
| LUMEYRA | Deployment-era rebrand found on current `main` | Unapproved by supplied brand source; removed from app package names; preserve historical Git records and existing Wrangler target slugs until a deployment migration is approved |

The FOLIAVERE choice follows `brand/brand_system.yaml` and `docs/01_name_and_domains.md`; neither proves legal availability. Do not claim ownership, registration, or domain control. The current runtime should be made consistent with this provisional choice. No historical files or commits are erased.

## Product and evidence decisions

- The board audit recommends beginning with one narrowly scoped 32-page children's product and synthetic portfolio samples. The tiers/prices in finance documents are scenarios until supplier quotes and full unit economics are measured.
- No child-face biometrics or likeness processing in the initial scope; no customer upload capability until consent, storage, deletion, access control and retention are actually implemented.
- Founder approval remains required for print dispatch, public release, paid advertising, refunds outside policy, contracts, provider changes, and policy overrides.
- Human approval may not be bypassed by an agent or a “self-healing” process.
- Gate status means evidence-backed criteria verification; unknown evidence remains PENDING.
- FOLIOMIND is not silently merged with FOLIAVERE. Keep it internal until the founder resolves its intended meaning.

## Decision record

| ID | Decision | Rationale | Revisit when |
|---|---|---|---|
| D-001 | Use FOLIAVERE provisionally for customer surfaces | Approved brand YAML and name strategy agree | Trademark/domain search and founder sign-off |
| D-002 | ASMA-OS is internal system name | Separates platform from customer product | No change unless architecture/product strategy changes |
| D-003 | Treat LUMEYRA as unapproved historic variant | Conflicts with approved brand source | Founder explicitly approves and clearance is documented |
| D-004 | No gate passes without evidence records | Prevents misleading operational status | Evidence evaluator and durable evidence store are implemented |
| D-005 | No live payment/order actions in local demo | Prevents accidental financial activity | Provider sandbox/live approvals and secure authorization exist |
