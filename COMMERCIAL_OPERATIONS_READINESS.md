# Commercial Operations Readiness

## Decision

**Not ready for paid customer launch.** The repository contains planning, in-memory simulations and provider adapters; it does not show a completed order, settlement, shipment, refund, support case, validated unit economics, or customer cohort.

## Evidence required before pilot

| Area | Required evidence | Current state |
|---|---|---|
| Product scope | Exact SKU, page count, paper/binding, proof and revision rules | Concept docs; no production SKU confirmed |
| Supplier | Written country/SKU shipping quote, sample and quality review | Not verified |
| Pricing | Landed cost incl. shipping, fees, taxes, reprint/refund reserve and CAC | Estimates only |
| Payment | Merchant eligibility, test-mode callback, idempotency, refunds/settlement | Adapter only; endpoint disabled |
| Customer demand | Consented interviews and paid pilot evidence | None verified |
| Fulfillment | Test order, tracking, damage/late response procedure | None verified |
| Support | Published hours, response owner, escalation and refund policy | Draft-level only |
| Privacy/legal | Counsel review, processor terms, consent/retention/deletion controls | Not approved |

## Operational runbook required

Customer intake and consent → quote and scope → payment verification → content/rights review → production proof → customer and founder approval → supplier dispatch → tracking and delivery → feedback/support → retention/deletion. Each transition needs an owner, evidence, timeout, rollback, and customer-visible status. Exceptions halt; agents may draft but not make reserved commitments.

## Financial controls

Use decimal currency arithmetic and track actual revenue, refunds, payment fees, supplier invoices, shipping, tax liabilities, replacement costs and acquisition spend. Keep projections separate from actuals. The $1M ARR, six-month CAC payback and 80% gross-margin values in the architecture are targets, not performance. Zero-upfront-cost applies to discretionary software/service commitments, not the false claim that commerce can operate without working capital, legal costs or fulfillment funding.
