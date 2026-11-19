# Company Operations Handbook (Working Draft)

This handbook describes a proposed low-commitment operating model. It is not a promise that these services are currently available.

## Order controls

1. Accept no personal photos or child-sensitive data in the current demo.
2. Confirm customer authority, consent, scope, spelling and rights before work begins.
3. Quote only from current supplier and shipping evidence; label estimates.
4. Verify payment through signed provider events and durable idempotency before any production dispatch.
5. Generate a proof, run text/print/safety checks, record artifact digest, and obtain customer plus founder approval.
6. Dispatch only after the approval record is authenticated and bound to exact artifact and quote hashes.
7. Record supplier order and tracking references; communicate delays and exceptions honestly.
8. Handle refunds/reprints under a published policy with founder approval where required.
9. Apply documented retention and deletion rules, including provider backups and evidence that excludes deleted content.

## Incident and escalation

Stop the affected workflow for suspected account compromise, cross-tenant data access, payment mismatch, unsafe content, incorrect customer name, missing approval, lost artifact, duplicate supplier dispatch, or unverified deletion. Preserve minimal audit metadata, contain access, notify the owner, and follow legal advice for customer/regulatory notifications. Do not let autonomous retry loops perform an irreversible action.

## Role of automation

Agents may classify, draft, validate deterministic schemas, and prepare recommendations. Human approval remains mandatory for public release, supplier dispatch, paid advertising, contract actions, policy overrides, and non-routine refunds. Every agent/tool must use scoped permissions and leave an attributable audit event before it is trusted with business data.
