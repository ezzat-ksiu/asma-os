# FOLIAVERE — Unit Economics, Cash Controls, Tax/Legal Gates and Execution Quality

ملخص تنفيذي 1: أرقام الطباعة والشحن والتغليف الواردة هنا افتراضات تخطيطية وليست عروض أسعار حية.
ملخص تنفيذي 2: هامش الربح الإجمالي يختلف عن مساهمة الطلب بعد رسوم الدفع والاحتياطي وتكلفة الاستحواذ.
ملخص تنفيذي 3: لا تتحول مبيعات الكتب الفردية تلقائياً إلى ARR؛ يجب وجود عقود أو اشتراكات متكررة لادعاء الإيراد السنوي المتكرر.
ملخص تنفيذي 4: لا تعفي عتبات الأرباح الشركة من التسجيل أو المراجعة القانونية والضريبية إذا كان القانون يفرض ذلك قبل البيع.
ملخص تنفيذي 5: لا يُفتح التوسع إلا بأدلة موقعة على التكلفة والجودة والدفع والخصوصية والتسليم، مع إبقاء احتياطي إعادة الطباعة عند 2% كحد أدنى.

## 1. Financial definitions and assumptions

This model is a **planning scenario**, not a supplier quote, tax opinion, audited forecast or promise of profit. Prices are list-price assumptions in USD and are treated as net of VAT/sales tax. Taxes collected for a government are liabilities, not revenue. Supplier prices, shipping, payment fees, FX and packaging must be replaced with live destination-specific data before selling a physical edition.

### 1.1 Price and product mix assumptions

| Tier | Working price | Scope in the initial product catalogue | Image budget |
|---|---:|---|---:|
| Heirloom | USD 199.00 | 32-page illustrated commission; one consolidated proof correction; approved standard hardcover SKU | 44 images × USD 0.05 = USD 2.20 |
| Atelier | USD 399.00 | 32-page commission; expanded editorial direction; one consolidated revision cycle plus final proof; enhanced supplier finish when quoted | 56 images × USD 0.05 = USD 2.80 |
| Grand | USD 649.00 | 32-page commission; deeper editorial planning; two consolidated proof rounds; provenance record; premium options only where live-quoted | 80 images × USD 0.05 = USD 4.00 |

**Important product correction:** a 32-page BookSpec cannot represent an 80–120-page adult legacy novel. A longer memoir needs a separate schema version, proof workflow, word-count economics and print quote. Do not sell the longer book at the 32-page tier price.

The weighted mix used in the following monthly model is Heirloom 50%, Atelier 35%, Grand 15%. The weighted average selling price is:

`(0.50 × 199) + (0.35 × 399) + (0.15 × 649) = USD 336.50 per order`.

This mix is an assumption, not observed sales data.

### 1.2 Cost assumptions by tier

| Cost component | Heirloom | Atelier | Grand | Basis |
|---|---:|---:|---:|---|
| AI image generation | 2.20 | 2.80 | 4.00 | Assumed USD 0.05 per image; replace with provider invoice |
| Printing | 16.00 | 22.00 | 32.00 | ESTIMATE only; exact POD SKU and quote required |
| Shipping | 12.00 | 15.00 | 18.00 | ESTIMATE only; destination and carrier dependent |
| Packaging | 5.00 | 9.00 | 18.00 | ESTIMATE only; premium packaging supplier not yet confirmed |
| LLM / TTS / production compute | 0.60 | 1.00 | 2.00 | ESTIMATE; measure tokens, images, rendering and audio use |
| Payment processing | 3% + 0.30 | 3% + 0.30 | 3% + 0.30 | Simplified planning estimate; actual Paymob pricing is published as 2.75% + EGP 3 for the Standard plan, subject to merchant acceptance and applicable transaction type |
| Reprint reserve | 2% of price | 2% of price | 2% of price | Mandatory minimum reserve; do not spend it as operating profit |
| Variable support / handling | 0.40 | 0.75 | 1.50 | Estimate excluding founder salary |
| Base customer acquisition cost (CAC) | 35.00 | 35.00 | 35.00 | Model assumption; not measured customer data |

**Paymob reference:** its public Standard pricing page displays 2.75% + EGP 3 per successful card charge and weekly settlement, with no monthly subscription fee shown on that page. The actual merchant offer, international-card eligibility, refund costs, chargeback costs, FX and settlement conditions must be confirmed in writing. This model simplifies fees to 3% + USD 0.30 only to make the USD tier comparison readable; replace it before approving a live price.

## 2. Decimal unit economics — base case

**Definitions**

- `Direct COGS = image generation + printing + shipping + packaging`.
- `Gross profit = price − direct COGS`.
- `Gross margin = gross profit / price`.
- `Contribution profit = gross profit − payment fee − reprint reserve − LLM/TTS − variable support`.
- `Contribution after CAC = contribution profit − customer acquisition cost`.
- These are pre-tax contribution figures, not net income and not founder take-home pay.

| Tier | Price | Direct COGS | Gross profit | Gross margin | Payment fee | 2% reserve | LLM/TTS + support | Contribution profit | Contribution margin | CAC | Contribution after CAC |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Heirloom | 199.00 | 35.20 | 163.80 | 82.31% | 6.27 | 3.98 | 1.00 | 152.55 | 76.66% | 35.00 | 117.55 |
| Atelier | 399.00 | 48.80 | 350.20 | 87.77% | 12.27 | 7.98 | 1.75 | 328.20 | 82.26% | 35.00 | 293.20 |
| Grand | 649.00 | 72.00 | 577.00 | 88.91% | 19.77 | 12.98 | 3.50 | 540.75 | 83.32% | 35.00 | 505.75 |

**Example — Heirloom calculation:**

- Direct COGS = 2.20 + 16.00 + 12.00 + 5.00 = USD 35.20.
- Gross profit = 199.00 − 35.20 = USD 163.80.
- Payment fee = (199.00 × 3%) + 0.30 = USD 6.27.
- Reprint reserve = 199.00 × 2% = USD 3.98.
- Contribution = 163.80 − 6.27 − 3.98 − 0.60 − 0.40 = USD 152.55.
- Contribution after assumed CAC = 152.55 − 35.00 = USD 117.55.

### 2.1 Weighted average economics

| Metric | Calculation | Weighted value |
|---|---|---:|
| Average selling price | 50%×199 + 35%×399 + 15%×649 | USD 336.50 |
| Average direct COGS | 50%×35.20 + 35%×48.80 + 15%×72.00 | USD 45.48 |
| Average gross profit | 336.50 − 45.48 | USD 291.02 |
| Weighted contribution before CAC | 50%×152.55 + 35%×328.20 + 15%×540.75 | USD 272.26 |
| Weighted contribution after CAC | 272.26 − 35.00 | USD 237.26 |
| Weighted gross margin | 291.02 / 336.50 | 86.48% |
| Weighted contribution margin | 272.26 / 336.50 | 80.91% |
| Weighted contribution after CAC margin | 237.26 / 336.50 | 70.51% |

The weighted direct COGS is USD 45.48 and the weighted gross profit is USD 291.02, calculated from the three-tier mix shown above. The weighted table is a blended scenario and must not be used to quote a specific customer's order.

## 3. Downside, base and upside scenarios

The scenarios differ only by explicit assumptions. They are not probabilities or forecasts.

| Assumption | Downside | Base | Upside |
|---|---:|---:|---:|
| CAC per order | USD 85.00 | USD 35.00 | USD 20.00 |
| Print cost | Base quote estimate ×1.25 | Base quote estimate | Base quote estimate ×0.90 |
| Shipping | Base estimate ×1.50 | Base estimate | Base estimate ×0.90 |
| Packaging | Base estimate ×1.20 | Base estimate | Base estimate |
| Payment fee | 3.5% + USD 0.30 | 3.0% + USD 0.30 | 2.5% + USD 0.30 |
| Reprint reserve | 3.0% | 2.0% | 2.0% |
| Variable support | 2× base | Base | 0.75× base |
| Fixed monthly operating expense | USD 450 | USD 450 | USD 450 |

### Weighted results

| Scenario | Average selling price | Contribution before CAC | Contribution after CAC | Contribution after CAC per month at 100 orders | Operating surplus after USD 450 fixed cost at 100 orders |
|---|---:|---:|---:|---:|---:|
| Downside | 336.50 | 252.75 | 167.75 | 16,775.25 | 16,325.25 |
| Base | 336.50 | 272.26 | 237.26 | 23,725.75 | 23,275.75 |
| Upside | 336.50 | 277.56 | 257.56 | 25,755.69 | 25,305.69 |

The downside retains positive variable contribution only because the current assumed price points are high relative to the estimated print costs. If a real quote, chargeback, customs duty, reprint rate or CAC is materially worse, prices or product scope must change. Do not use the table to promise profit.

## 4. Monthly order sensitivity — base case

Fixed operating expense is modelled at USD 450 per month. It is an estimate for a lean post-launch technical stack and basic operating tools; it does not include founder salary, company formation, professional legal fees, income tax, VAT payable, unbudgeted refunds, payment reserves, external contractors or the cost of a serious incident.

| Monthly orders | Gross sales | Contribution after CAC | Fixed operating expense | Operating surplus before founder pay and tax |
|---:|---:|---:|---:|---:|
| 10 | 3,365.00 | 2,372.58 | 450.00 | 1,922.58 |
| 50 | 16,825.00 | 11,862.88 | 450.00 | 11,412.88 |
| 100 | 33,650.00 | 23,725.75 | 450.00 | 23,275.75 |
| 500 | 168,250.00 | 118,628.75 | 450.00 | 118,178.75 |

**Critical capacity correction:** 500 books per month is a mathematical sensitivity, not an approved solo-founder operating capacity. At an aspirational three-minute approval per order, 500 orders alone consume 1,500 minutes, or 25 hours, before exceptions, sales, accounting, supplier disputes, compliance requests and support. Do not accept order volume beyond measured processing capacity.

### 4.1 Simplified contribution break-even

`USD 450 fixed monthly operating cost ÷ USD 237.26 contribution after CAC ≈ 1.90 orders`.

The simplified model therefore shows two orders to cover the assumed USD 450 fixed expense. **This is not the company's full break-even point.** The complete break-even must add owner compensation, business registration, legal/accounting, tax, insurance, refunds, chargebacks, replacement freight, software costs, FX loss and cash reserves.

## 5. The USD 1.2 million objective — correct terminology

A one-off printed book is a transaction, not recurring revenue. If the business sells one-time orders, it must not call twelve months of projected book sales “ARR”. The correct term is annualised gross revenue run-rate.

At the assumed weighted average selling price of USD 336.50:

- USD 100,000 monthly gross sales ÷ USD 336.50 ≈ 297.18 average orders per month.
- Rounded operating requirement: approximately 298 orders per month.
- USD 100,000 × 12 = USD 1,200,000 annualised gross sales.

That order volume is not presently compatible with an unmeasured one-founder service. A credible path requires evidence of repeatable B2B volume, a strong exception-handling system and contracted external production capacity. A recurring B2B contract can be described as ARR only if it creates a genuine recurring contractual revenue stream; an annual framework agreement with no minimum purchase is not automatically ARR.

## 6. Negative working capital — reality check

Customer prepayment reduces funding risk but does not automatically create negative working capital. Payment providers may settle later than the POD provider charges; card disputes and refunds can reverse funds; foreign exchange can move; taxes may be due before supplier invoices are reconciled; and the seller may have to pay for a replacement before a dispute is resolved.

**Required cash rules**

1. Never submit a print order using a browser “success” redirect alone; wait for a verified provider event and reconciled amount/currency.
2. Do not spend VAT/sales tax collected from the buyer as operating cash.
3. Keep the 2% reprint reserve ring-fenced from operating surplus.
4. Hold enough cleared cash to cover supplier charge, delivery, payment reversals and one replacement case before releasing the remainder as owner-distributable profit.
5. Record the payment-provider settlement date separately from the event capture date.
6. Reconcile every supplier quote against the final invoice.
7. Stop new orders if cleared funds cannot cover obligations already accepted.

## 7. Revenue-funded upgrade matrix

Thresholds refer to **cumulative verified net profit after supplier costs, payment fees, refunds, chargebacks, tax liabilities, reserves and operating expenses**, not revenue and not gross contribution. Reaching a threshold authorises a review or budget proposal, not automatic spending.

| Cumulative verified net profit | Upgrade review | Release conditions |
|---:|---|---|
| USD 2,000 | External accounting and legal review | Reconciled books, reserve funded, no overdue supplier obligations, authorised contracting party identified |
| USD 5,000 | Legal entity formation and registration budget | Written jurisdiction comparison, legal advice, tax registration map and confirmation that trading may lawfully continue before formation |
| USD 8,000 | Trademark clearance and first filing budget | Professional clearance in target territories and Nice classes relevant to publishing/software; no filing based only on a quick search |
| USD 10,000 | Paid advertising capability review | Historical conversion and contribution data, refund/chargeback rates, tracking consent, campaign cap and exact founder approval |
| USD 15,000 | Premium packaging trials | Samples and landed quotes; damage test; separate price or add-on; margin remains positive |
| USD 25,000 | Dedicated GPU cost benchmark | Measured API cost versus rented/dedicated GPU total cost, storage, maintenance and privacy impact; no purchase if API remains cheaper |
| USD 30,000 | Premium voice provider review | Voice rights, language quality, commercial model terms, per-minute economics and deletion requirements |

**Legal precedence:** a profit threshold never authorises trading without a registration, permit, adult/legal contracting authority or tax registration that applicable law requires before the transaction. The zero-upfront rule is a spending discipline, not an exemption from law. If the founder is not legally able to enter the relevant commercial contracts in the chosen jurisdiction, the company must not bypass that restriction; use properly authorised adult/legal representation and qualified advice where required.

## 8. Tax and customs routing — conservative rules

The schema's tax router is a decision-support mechanism. It must never issue a final tax conclusion from country codes alone. For each order, store dispatch origin, destination, seller establishment, buyer type, product type, intrinsic value, importer of record, VAT registration, platform deemed-supplier status and the supplier invoice facts.

| Transaction | Routing concept | Required caution |
|---|---|---|
| Domestic Egyptian sale | Egyptian VAT / local tax review | Confirm seller registration, place of supply, invoice requirements, export status and current treatment with an Egyptian tax adviser |
| EU physical goods dispatched within one Member State | Local VAT rules | Confirm the seller's establishment and the supplier's role; do not assume a universal rate |
| EU cross-border intra-Union B2C goods | Union OSS may simplify eligible distance-sale VAT reporting | Product origin, seller establishment, thresholds and place-of-supply rules matter; confirm registration and evidence |
| Imported physical goods into EU | Import VAT applies; IOSS may be used for eligible transactions under the current transitional rules | As of 18 November 2026, the historic EUR 150 intrinsic-value IOSS threshold remains part of the current transitional framework, but the Council agreed to remove it when the EU Customs Data Hub becomes operational, targeted for 1 July 2028. The threshold is therefore not a permanent design constant |
| Low-value imports into EU | Temporary EUR 3 customs duty per item has applied from 1 July 2026 to low-value consignments up to EUR 150 under the transitional measure | This is a customs duty, separate from VAT; confirm item and consignment treatment at the time of dispatch |
| EU B2C digital service | Non-Union OSS may apply to a non-EU supplier for eligible digital services | A printed book is a physical good, not a digital service; do not route it to Non-Union OSS merely because the seller is non-EU |
| EU B2B service | Reverse charge may apply to qualifying cross-border services where the buyer's VAT status is verified | Do not automatically apply reverse charge to physical books/goods; determine transaction classification and place of supply |
| UK printed book | UK VAT review; printed books may have a zero rate under defined conditions | Import VAT, seller registration, place of supply and product classification still require confirmation |
| US physical book | State and local sales-tax nexus review | Thresholds and product taxability vary by state; use an approved tax adviser or tax engine after nexus analysis |

EU transitional update references:

- European Commission, 9 November 2026, Council agreement to remove the EUR 150 IOSS threshold when the Customs Data Hub is operational, targeted 1 July 2028: https://taxation-customs.ec.europa.eu/news/commission-welcomes-council-agreement-removing-eur150-threshold-vat-import-one-stop-shop-2026-11-09_en
- European Commission, 8 June 2026, temporary EUR 3 customs duty per item for eligible consignments up to EUR 150 from 1 July 2026 until 1 July 2028: https://taxation-customs.ec.europa.eu/news/guidance-and-legal-text-temporary-flat-fee-low-value-imports-which-will-apply-until-1-july-2028-2026-06-08_en

## 9. Child privacy, consent and copyright controls

### 9.1 COPPA and parental verification

The FTC COPPA Rule applies to covered online services collecting personal information from children under 13. Operators must provide notice, obtain verifiable parental consent where required, provide parental access/deletion controls, maintain security and limit retention to what is necessary. A payment card is not a universal substitute for the prescribed consent process. The actual method must fit the FTC rule and guidance for the data use and disclosure. Marketing consent must remain separate from service fulfilment and third-party disclosure must be explained.

### 9.2 GDPR and UK Children's Code

- GDPR Article 8 sets conditions where consent is the lawful basis for direct-to-child information society services; national age thresholds can vary between 13 and 16.
- GDPR Article 17 provides a right to erasure subject to its conditions and exceptions; it does not mean every backup or statutory financial record is instantly erased regardless of legal retention obligations.
- UK ICO Children's Code applies to relevant online services likely to be accessed by children and requires high-privacy default settings and child-best-interest considerations.
- The service is adult-directed in the initial release. Children do not create accounts or upload photographs.

### 9.3 Egyptian personal-data law

Egypt's Personal Data Protection Law No. 151/2020 and Executive Regulations must be assessed for the actual controller, processors, cross-border transfers, licensing/permits, records and data-subject rights. The Egyptian Arabic official text prevails over unofficial translations. Do not treat GDPR or COPPA compliance as a substitute for Egyptian legal review.

### 9.4 Deletion and zero retention

- A `purge_window_seconds` policy field is not proof of deletion.
- Verify deletion from temporary upload, object storage, provider file store, generation jobs, caches, derived assets and any controlled copies.
- If a provider does not support the required deletion or has retention terms incompatible with the product, do not send personal child data to it.
- Do not place source photographs, face embeddings or LoRA weights in ordinary database backups.
- Keep a signed deletion receipt containing asset IDs, provider status and artifact hashes, not the deleted image itself.

### 9.5 Copyright

The U.S. Copyright Office's January 2025 report says copyrightability of AI outputs depends on sufficient human authorship; prompts alone do not establish copyright. Preserve actual creative selection, arrangement and human editing. Do not promise full ownership of all AI-generated elements. A personal perpetual licence grants only the rights stated in the customer order and does not transfer ownership of third-party fonts, models, stock assets or generic production components.

## 10. Seven Zero-Clock gates — capabilities and team state

| Gate | Exit evidence | Capabilities unlocked | Effective team |
|---:|---|---|---|
| 0 — Foundations | Schema test report, policy manifest, security test report and signed artifact hashes | Local deterministic workflow, validated contracts, policy gateway and evidence ledger | One founder + tested deterministic core |
| 1 — Cost truth | Live print quote, image-cost invoice and sandbox print receipt | SKU-level cost calculation, supplier comparison, minimum price floor and margin alert | One founder + pricing/quote agents |
| 2 — Compliance spine | Processor register, consent control report and purge control report | Lawful provider routing, adult/customer permissions, operational deletion workflow and blocked unsafe paths | One founder + compliance agents; legal counsel remains external when necessary |
| 3 — Portfolio engine | Six sample-book manifest entries, six redacted vault manifests and visual QA report | Public sample portfolio, bilingual samples, certificate and controlled vault | One founder + creative/production/QA agents |
| 4 — First paid order | Captured payment receipt, persistent webhook idempotency report and first order receipt | Verified payment-to-order chain and one live print fulfilment | One founder + configured payment/POD adapters |
| 5 — Autonomous fulfilment | Backup restore drill and hands-off fulfilment receipt | Durable event routing, tested recovery, shipment tracking and low-exception order flow | One founder + provider services + ASMA runtime; still not a human 24/7 service |
| 6 — Scale and upgrade | Net-profit statement meeting gate threshold plus tax-readiness review | Upgrade eligibility, controlled expansion and measured capacity increase | One founder + evidence-backed external providers; no hiring assumed |

A gate counts only after its predecessor gates have passed and all required evidence signatures verify. Local test booleans are not business evidence.

## 11. Evidence plan for Gates 0–4

| Gate | Evidence artifact | Producer / signer | Verification method | Block condition |
|---:|---|---|---|---|
| 0 | `schema_tests_report` | CI test runner / QA signer | Build log, commit hash, test report hash and signature | Any failing schema or security test |
| 0 | `policy_manifest` | Policy engine | Exported agent/toolset allowlist and policy hash | Unknown agent, excessive scope or missing deny rule |
| 0 | `security_test_report` | Security test harness | Cross-tenant, replay, founder-approval and secret-scan report | Any cross-subject or unauthorised side effect |
| 1 | `live_print_quote` | Gelato/Lulu quote adapter | Provider quote ID, SKU, destination, currency and quote payload hash | Quote missing, expired or mismatched SKU |
| 1 | `image_cost_invoice` | Image provider billing export | Usage ID and invoice line reconciliation | Cost assumed rather than measured |
| 1 | `sandbox_print_receipt` | POD adapter | Provider sandbox order ID, PDF hash and status | No successful SKU-level sandbox receipt |
| 2 | `processor_dpa_register` | DPA monitor / privacy review | Signed DPA, subprocessor list, region and retention evidence | Any personal-data processor unapproved |
| 2 | `consent_control_report` | Consent auditor | Consent evidence and negative test report | Missing notice, authority or purpose evidence |
| 2 | `purge_control_report` | Privacy purger | Delete test across all controlled locations and provider receipts | Any deletion location unverified or failed |
| 3 | `portfolio_manifest` quantity 6 | Portfolio pipeline / QA signer | Six unique sample manifests, fictional-content flag and file hashes | Fewer than six or any customer asset used without permission |
| 3 | `vault_manifest` quantity 6 | Vault publisher / QA signer | Six redacted public records, noindex/default public policy and access tests | Any private field or unapproved publication |
| 3 | `visual_qa_report` | QA consensus | Rendered-page review, typography/RTL checks and image QA | Any critical clipping, typo or safety issue |
| 4 | `payment_capture_receipt` | Paymob adapter / payment gatekeeper | Provider transaction, amount, currency and capture status | Callback unverified or amount mismatch |
| 4 | `webhook_idempotency_report` | Security test harness | Duplicate event replay against durable database constraint | Second side effect on duplicate or failed retry semantics |
| 4 | `first_order_receipt` | Fulfilment dispatcher | Paid order, approved proof, founder signature, supplier quote and POD order ID | Any missing prerequisite |

All evidence records should bind `tenant_id`, `subject_id`, `artifact_sha256`, signer identity, signature and relevant amount/quantity. Gate evidence must be stored separately from customer content and must not include deleted sensitive data.

## 12. Fifteen numeric quality acceptance standards

These are proposed release thresholds. A printer's stricter template requirement overrides the generic target. Passing a model score does not replace physical proof inspection.

| # | Quality dimension | Acceptance standard | Measurement / evidence |
|---:|---|---|---|
| 1 | Page count | Exact match to the approved BookSpec; 32 pages for initial Heirloom/Atelier/Grand | Automated PDF page count and spec comparison |
| 2 | Proper names | 100% exact match to customer-approved spelling and order | Text diff plus critical-name checklist |
| 3 | Text completeness | 100% source manuscript segments represented in final layout | Segment-to-page coverage report |
| 4 | Glyph integrity | 0 missing-glyph boxes or replacement characters | Font/glyph preflight and visual page render |
| 5 | Font embedding | 100% required fonts embedded or legally/technically converted as allowed by printer | PDF font inspection |
| 6 | Overflow / clipping | 0 text overflow, 0 clipped captions, 0 hidden essential artwork | Automated bounding checks plus visual QA |
| 7 | Effective image resolution | At least 300 PPI at final placed size when required by the selected printer SKU | Image dimension and placement calculation |
| 8 | Bleed | Exact match to the selected supplier template; no generic guessed bleed | Template comparison and preflight |
| 9 | Safe area | 100% critical text and faces inside the supplier's safe area | Geometry check against SKU template |
| 10 | Text contrast | Web UI normal text ≥4.5:1; large text ≥3:1; print text separately proofed for legibility | WCAG contrast calculation and physical proof review |
| 11 | Text fidelity | QA score ≥0.98 on exact manuscript segments | OCR/text comparison; uncertain OCR requires visual inspection |
| 12 | QA consensus | Four distinct votes; at least three pass; mean score ≥0.85 | Signed vote manifest and consensus calculation |
| 13 | Safety | 0 unresolved critical safety/privacy flags | Deterministic scan + independent model review |
| 14 | Colour / physical finish | Critical colour patches target ΔE00 ≤5 only when a colour-managed proof and measuring instrument are available; otherwise visual proof grade must pass | ICC profile, proof record and measured report where available |
| 15 | QR and provenance | 100% QR scans resolve to the intended authorised page; serial is unique; public page contains only approved metadata | Automated QR test, unique constraint and public-projection test |

## 13. Final ordered execution checklist — one founder, zero upfront subscriptions

### Gate 0 — Establish the trustworthy core

- [ ] Preserve the current source and create a versioned repository branch.
- [ ] Verify Python dependency lock, Pydantic version and deterministic test output.
- [ ] Confirm exactly 45 unique agent identities and 15 departments.
- [ ] Verify all eight MCP toolsets and negative permission tests.
- [ ] Replace any production in-memory idempotency or event store before a live payment.
- [ ] Create the signed evidence key registry and test tampering and replay.
- [ ] Keep child image upload, biometric matching and child LoRA disabled.
- [ ] Make all unconfigured adapters fail closed; never report a placeholder adapter as successful.

### Gate 1 — Replace estimates with evidence

- [ ] Select one specific 32-page hardcover SKU and one first shipping destination.
- [ ] Retrieve live print and shipping quotes from Gelato and/or Lulu.
- [ ] Compare paper, cover, trim, binding, stock, page-count rules, cover template and delivery.
- [ ] Generate a sample image invoice for the exact production route.
- [ ] Record payment fee and settlement rules from the merchant offer.
- [ ] Recalculate the tier price floors with live quotes and the 2% reserve.
- [ ] Run a supplier sandbox print order and save its receipt.

### Gate 2 — Make privacy and legal controls real

- [ ] Confirm legal contracting authority and seller/merchant eligibility before taking money.
- [ ] Have qualified counsel review Egyptian, target-market, consumer, IP and tax requirements.
- [ ] Create the processor/subprocessor register and link signed DPAs and retention terms.
- [ ] Verify AuthN/AuthZ, tenant and subject isolation, least privilege and secret storage.
- [ ] Test deletion through all controlled storage and provider locations; record a purge receipt.
- [ ] Keep marketing consent separate; keep public vault opt-in.
- [ ] Publish privacy and consumer terms only after facts and legal review are complete.

### Gate 3 — Build the proof portfolio

- [ ] Complete the six fictional sample books AV-001 through AV-006.
- [ ] Generate English, Arabic and French samples with language-specific proofing.
- [ ] Compile all sample PDFs using exact font, trim, bleed and cover templates.
- [ ] Create six digital mockups and label them as mockups.
- [ ] Produce one physical sample of the exact launch SKU.
- [ ] Create six redacted vault sample pages with opt-in/public metadata rules.
- [ ] Pass all 15 quality standards and produce a signed visual QA report.

### Gate 4 — Accept the first live order

- [ ] Activate a merchant account only after eligibility and lawful seller details are confirmed.
- [ ] Complete hosted checkout, payment callback verification and persistent idempotency.
- [ ] Verify the amount, currency, order ID, settlement and refund handling.
- [ ] Obtain customer proof approval and founder approval bound to exact artifact and quote hashes.
- [ ] Submit the live POD order and store the supplier order ID.
- [ ] Track delivery and collect any issue evidence.
- [ ] Reconcile payment, supplier invoice, fee, reserve and contribution.

### Gate 5 — Prove repeatable fulfilment and recovery

- [ ] Run a real restore drill and prove measured RPO/RTO before publishing targets.
- [ ] Verify backup encryption and scan backups for prohibited face-data classes.
- [ ] Repeat the paid fulfilment journey without manual database repairs.
- [ ] Measure founder minutes per order, exceptions, defect rate and reprint rate.
- [ ] Keep order capacity below the measured service limit.

### Gate 6 — Scale and release upgrades

- [ ] Calculate cumulative net profit after all liabilities and reserves.
- [ ] Obtain tax-readiness review for the destinations actually served.
- [ ] Compare product and B2B channel contribution, not only gross sales.
- [ ] Unlock the next funded upgrade only after its threshold and legal prerequisites are satisfied.
- [ ] Expand one country, SKU or institutional segment at a time, with fresh quote and compliance evidence.
- [ ] Reopen paid advertising only after the USD 10,000 verified profit lock and exact founder approval.

## 14. Reference and legal source register

- U.S. FTC, *Complying with COPPA: Frequently Asked Questions*: https://www.ftc.gov/business-guidance/resources/complying-coppa-frequently-asked-questions
- U.S. FTC, 2025 COPPA Rule amendments (Federal Register, April 22, 2025): https://www.govinfo.gov/content/pkg/FR-2025-04-22/pdf/2025-05904.pdf
- EU General Data Protection Regulation, Regulation (EU) 2016/679: https://eur-lex.europa.eu/eli/reg/2016/679/oj/eng
- UK ICO, Children's Code / Age Appropriate Design Code: https://ico.org.uk/for-organisations/uk-gdpr-guidance-and-resources/childrens-information/childrens-code-guidance-and-resources/introduction-to-the-childrens-code/
- Egyptian Personal Data Protection Law No. 151/2020 and Executive Regulations (Egyptian Arabic official text prevails; current reference guide reviewed 30 October 2026): https://legalin.law/en/our-knowledge/guide/personal-data-protection-law/
- U.S. Copyright Office, *Copyright and Artificial Intelligence — Part 2*: https://www.copyright.gov/ai/
- European Commission, EU AI Act transparency obligations under Article 50 (apply from 2 August 2026): https://digital-strategy.ec.europa.eu/en/faqs/transparency-obligations-under-article-50-ai-act
- European Commission, IOSS threshold reform agreement and expected Customs Data Hub application: https://taxation-customs.ec.europa.eu/news/commission-welcomes-council-agreement-removing-eur150-threshold-vat-import-one-stop-shop-2026-11-09_en
- European Commission, EUR 3 transitional customs duty for eligible low-value imports from 1 July 2026: https://taxation-customs.ec.europa.eu/news/guidance-and-legal-text-temporary-flat-fee-low-value-imports-which-will-apply-until-1-july-2028-2026-06-08_en
- Paymob pricing: https://paymob.com/en/pricing

## 15. Decision Log

| Decision | Owner | Why |
|---|---|---|
| Treat all supplier and CAC inputs as estimates until verified | CFO + Operations | Model assumptions cannot be represented as actual costs or performance. |
| Keep at least 2% of gross order price as a reprint reserve | CFO | Protects against repeat production and delivery defects. |
| Use contribution margin and after-CAC contribution, not a misleading “net margin” | CFO | Exposes acquisition and variable cost before owner pay and tax. |
| Call USD 1.2M from one-off books annualised revenue, not ARR | CEO + CFO | ARR requires a real recurring contract or subscription stream. |
| Keep tax routing conservative and jurisdiction-specific | Chief Legal & Compliance Officer | Physical goods, digital services and B2B services have different tax treatment. |
| Make legal and tax obligations override the revenue-funded upgrade ladder | CEO + Legal | Zero-upfront spending policy cannot override law. |
| Capacity is set by measured founder workload and exception rate | Head of Operations | A 500-order spreadsheet scenario is not proof of a feasible solo operation. |

**Sign-off:** CFO — unit economics and cash controls; Chief Legal & Compliance Officer — jurisdiction and rights gates; Head of Operations — capacity and quality; CEO — execution order.
