# FolioMind / ASMA-OS — Independent Board Audit

ملخص تنفيذي 1: هذه مراجعة تنفيذية نقدية لمشروع دار نشر فاخرة مخصصة تعمل بنظام ASMA-OS.
ملخص تنفيذي 2: قائمة الوكلاء والاختبارات تثبت وجود نواة برمجية، ولا تثبت وحدها وجود شركة أو خدمة إنتاج تجارية.
ملخص تنفيذي 3: أكبر المخاطر هي الخصوصية، تعاقدات الموردين، جودة الطباعة، واقتصاديات اكتساب العميل.
ملخص تنفيذي 4: يجب إطلاق منتج واحد محدود المواصفات، مع اعتماد المؤسس قبل الطباعة والنشر والإنفاق.
ملخص تنفيذي 5: كل انتقال تشغيلي يعتمد على دليل قابل للتحقق، وليس على وعد زمني أو نسبة جاهزية تقديرية.

**Board status:** This is a simulated multidisciplinary review produced as one consolidated analysis, not a statement that thirteen independent human advisers were retained or signed off. The signature lines below represent accountable disciplines in the proposed governance model, not real professional attestations.

## 1. Executive verdict

**Decision: proceed only as a controlled proof-of-service, not as a declared global autonomous publishing house.** The supplied V6.0 material describes useful architecture: typed book specifications, a central MCP policy gateway, an agent registry, signed handoffs, a sequential evidence model, a decimal-based unit-economics function, and a founder approval tied to an artifact digest. Those are strong design ingredients. They are not proof of production reliability, legal compliance, child-data deletion, supplier readiness, payment settlement, or customer demand.

This source section was drafted when the project described six gates. The current specification defines seven gates, G0 through G6; a passing local test suite only validates the code paths it exercises. Durable commercial records, production OAuth configuration, live vendor adapters, object-store purge receipts, restore drills, supplier quotes, and actual fulfilment are not established by tests alone. Do not publish “production ready”, “99.9% availability”, “fully autonomous”, or “compliant” until separately measured and evidenced.

### Board members' findings

| Discipline | Finding | Required correction | Sign-off |
|---|---|---|---|
| CEO — Vision & Strategy | The category story is ambitious but the market is not empty. “First” and “world's only” claims are indefensible without exhaustive evidence. | Position around controlled editorial craft, privacy-by-design, and bespoke finished objects. | CEO — strategy owner |
| CTO — Architecture | The code has useful boundaries but in-memory event deduplication and adapters marked “not configured” cannot support a real fulfilment claim. | PostgreSQL unique constraints, transactional outbox, durable checkpoints, provider adapters, observability, restore tests. | CTO — architecture owner |
| CPO — Product | Three audiences and three price tiers create nine combinations before language and customisation permutations. | Start with one 32-page children's product using synthetic portfolio examples; treat adult legacy and B2B as later product lines. | CPO — product owner |
| CMO — Growth | A free personalised preview can improve intent, but it also creates image-upload privacy exposure and model-cost abuse. | Offer a synthetic demo first; introduce a personal preview only after upload consent, rate limits, secure deletion, and no child-face biometric processing are verified. | CMO — growth owner |
| CFO — Finance | The supplied margin model omits customer acquisition, founder labour, taxes, FX, refunds, failed deliveries, chargebacks, sample proofs, and fixed overhead. | Use contribution margin rather than calling per-order remainder “net profit”. Maintain a cash reserve before authorising upgrades. | CFO — finance owner |
| Chief Legal & Compliance Officer | COPPA, GDPR, Egyptian data protection, consumer law, tax, customs, AI transparency, and copyright are distinct obligations. | Counsel-led jurisdiction map and DPIA before collecting real child photos. | Legal — legal owner |
| Chief Brand Officer | Deep ink, warm ivory and restrained metal accents are credible; “gold” alone does not create luxury. | Define material, editorial restraint, typography, and proof of craftsmanship. | Brand — identity owner |
| Head of Operations | One person cannot promise 24/7 human-grade support and fulfilment oversight while studying or otherwise unavailable. | Automate routine status handling; route exceptions to a single inbox; state actual support coverage. | Operations — process owner |
| Head of AI Agent Engineering | Forty-five named agents are not forty-five independent employees. Most should be deterministic workflows, not autonomous LLM personalities. | Keep role identities, but use shared runtimes, small model pools, strict budgets, and policy-enforced MCP tools. | AI Engineering — agent owner |
| Head of Customer Experience | A premium product fails on wrong names, bad proofing, late shipping, or confusing expectations more than on a lack of AI features. | Proof approval, clear revision limits, trackable fulfilment, and graceful recovery policies. | CX — customer owner |
| World Luxury Publishing Expert | POD is a fulfilment model, not a luxury finishing guarantee. The chosen SKU, paper, binding, colour and packaging must be physically sampled. | Sell the product that has been physically inspected, not the supplier's generic category page. | Publishing — production owner |
| MENA & Gulf Markets Expert | Gulf hospitality and schools are viable prospect segments but procurement, vendor onboarding and budget cycles are not instant. | Paid five-copy pilot with clear scope, procurement pack, and outcome metrics. | MENA — regional owner |
| Consumer Psychologist | Personalisation and meaningful gifting can increase perceived relevance, but “make the customer cry” is not an ethical design objective. | Optimise for recognition, dignity, family participation, and trust—not emotional manipulation. | Consumer — research owner |

## 2. Existing system: strengths and gaps

| Area | Evidence in supplied material | Gap / severity | Closure condition |
|---|---|---|---|
| BookSpec contract | Pydantic strict models, Decimal money, tenant and subject identifiers | Medium: contract completeness still needs schema migration/version strategy | Contract tests, migration compatibility tests, signed schema release |
| Agent roster | 45 distinct names across 15 departments; prompt optimisation merged into one capability | Low: count must not be marketed as 45 autonomous workers | Publish roster as logical roles, not employees |
| MCP policy gateway | Eight toolsets, allowlists, scopes, founder approval and asset-manifest checks | High: SDK HTTP auth and OAuth provider remain integration seams | Real issuer, JWT verification, audience validation, revocation strategy, negative security tests |
| Handoffs | Frozen Pydantic object, tenant/subject, SHA-256 payload fingerprint | Medium: hash without signed provenance and durable storage is not a complete audit chain | Sign handoff envelope, persist immutable event record, verify source and recipient |
| Event routing | Event type → agent → MCP tool | Critical: `_seen` and webhook idempotency defaults are in-memory | Durable event inbox, unique provider event id, atomic payment + outbox transaction |
| Payments | Paymob adapter described and HMAC-tested | Critical: live merchant approval, callback format and settlement unverified | Provider-specific signature test vectors and real low-value captured transaction under lawful account |
| POD | Gelato and Lulu planned | Critical: exact hardcover 32-page SKU and delivery quote not evidenced | Sandbox order, physical sample, landed-cost quote per target country |
| Privacy | 24-hour purge target, no child embeddings/LoRA, no child likeness in marketing | Critical: boolean DPA/ZDR fields do not prove provider contractual terms or deletion from logs/backups | DPA/subprocessor register, real object inventory, verified provider deletion, signed purge receipt |
| Print engineering | Typst source and PDF output | High: PDF output is not automatically PDF/X-4 or printer-approved CMYK | Printer-specific preflight and colour profile test, physical proof |
| AI QA | Four-vote consensus, threshold and critical notes | High: scores are model outputs, not calibrated probability of correctness | Evaluation set, human adjudication, defect taxonomy, inter-rater agreement |
| Founder approval | HMAC bound to action and hash | Medium: key management, rotation, replay prevention and approval expiry need production design | KMS or protected secret, nonce/action record, one-time use, append-only approval log |
| Backups | RPO 15m / RTO 60m target in code | Critical: policy constants do not prove backup cadence or restore time | Repeated restore drill with timings, backup exclusion scans, encrypted copies |
| Commercial proof | $199/$399/$649 tiers | Critical: no validated conversion, CAC, repeat purchase, or return/reprint rates supplied | Paid pilot cohort, fully loaded contribution statement, customer interviews |
| Solo operations | Centralised workflow | Critical: 24/7 autonomy and a 3-minute approval are unproven | Measure exceptions per order, founder minutes per order and interruption load |

## 3. Fatal or near-fatal assumptions to remove

1. **“100% autonomous” is not an acceptable current claim.** The system requires founder approval for print/publish/spend and exceptional safety, privacy, tax and support cases. Describe it as AI-assisted, evidence-gated operations under founder control.
2. **“24-hour deletion” is not achieved by a policy field.** It requires deletion across object storage, temporary upload buffers, AI provider records where deletion is supported, queues, caches, thumbnails, logs, backups and local developer copies. Backups should never contain source child photos or derived biometrics; deletion receipts should record each system's result.
3. **A shared B2C tenant is not enough.** All read/write operations must scope both `tenant_id` and `subject_id`, and database row-level security must independently enforce it.
4. **A model score of 0.85 does not equal 85% correctness.** Thresholds are internal acceptance rules until calibrated against labelled test data.
5. **“1-of-1” is a production promise, not a legal copyright guarantee.** A unique serial and one-time commissioned design do not create exclusive copyright in every AI-generated element. Contracts must define reprints, source files, licences, and reuse of generic templates.
6. **The three-minute review target is not a service promise.** Page-level exceptions, names, cultural details, typography, child safety and print defects can require deeper review.
7. **The proposed pricing does not imply a luxury moat.** Commodity photo books sell far below $199; premium prices require demonstrable editorial craft, personal service, distinct visual quality and trusted delivery.
8. **The 32-page-only schema cannot support a 60–120-page adult legacy book.** The schema must represent page-count classes, format constraints, and separate pipelines without making all tiers identical.
9. **B2B physical books are not automatically eligible for reverse-charge VAT.** Tax treatment depends on transaction structure, place of supply, goods movement, customer status and country rules.
10. **Zero upfront and live 24/7 hosting are mutually inconsistent.** Use static pages and a provider-hosted payment link for the first supervised transaction; fund a persistent API and database only from cleared proceeds.

## 4. The Impossible Additions — 24 capabilities worth adding

Each item states the capability, strategic reason, and a no-subscription starting path. “$0-upfront” means no fixed subscription or capital expense; it does not mean labour, API use or legal obligations are free.

| # | Addition | Why it matters | $0-upfront starting method |
|---:|---|---|---|
| 1 | Book Truth Ledger | Stops claims, names, dates and family relationships from being invented by a model. | Store approved facts and source references in JSON; reject unsupported assertions. |
| 2 | Customer Voice & Consent Manifest | Separates the subject's story, buyer's wishes and permission to use third-party information. | Pydantic consent matrix and manual confirmation flow. |
| 3 | Product SKU Contract | Connects page count, trim, stock, binding, cover and printer limits to one tested product. | Versioned YAML SKU file and supplier sample checklist. |
| 4 | Printer Golden Sample Archive | Enables visual comparison against the physically approved copy. | Photograph each approved sample under controlled lighting; store SHA-256 manifest. |
| 5 | Arabic Typography Regression Suite | Detects shaping, punctuation, kashida, diacritics, numerals and RTL/LTR failures. | Open fonts, Typst fixtures, rendered-page snapshots and pixel-diff thresholds. |
| 6 | Name and Fact Proofing Screen | Prevents expensive personal-name and relationship errors. | Human proof step with highlighted proper nouns before print approval. |
| 7 | Consent Revocation Workflow | Lets a parent/subject withdraw permission and triggers asset and processor deletion. | One revocation record and idempotent purge workflow. |
| 8 | Privacy Asset Graph | Tracks every derivative of a source upload. | Asset IDs with parent-child links, data class, storage location and digest. |
| 9 | Provider Subprocessor Registry | Prevents unknown model and fulfilment vendors receiving sensitive data. | Version-controlled provider register and contract/setting evidence. |
| 10 | Prompt Injection Firewall | Prevents text inside uploaded documents from becoming tool instructions. | Treat source text as data; schema-validate outputs; disallow model-selected tools. |
| 11 | Cost Governor | Prevents retries, upscales and model loops from draining cash. | Deterministic per-job token/image budgets and stop conditions. |
| 12 | Generation Replay Record | Makes defective pages reproducible and diagnosable. | Save non-sensitive prompt/version/model metadata and output digests. |
| 13 | Editorial Style Linter | Enforces reading level, voice, banned clichés and story continuity. | Local rules + test corpus + bounded model critique. |
| 14 | Child-Safety Story Bible | Prevents age-inappropriate themes, shame, stereotypes and unsafe instructions. | Age-band policy, story checklist and deterministic blocks. |
| 15 | Accessibility Export Check | Makes ebooks and web previews more usable to more families. | Alt-text fields, keyboard test, contrast checks and tagged-PDF evaluation where supported. |
| 16 | Refund and Reprint Root-Cause Map | Converts defects into corrective action rather than treating every complaint as isolated. | Classify each issue and link it to page, supplier, model and process. |
| 17 | Cash-Reserve Waterfall | Protects tax, refunds, supplier payments and working capital before upgrades. | Spreadsheet/Decimal ledger with reserve priorities. |
| 18 | Supplier Failover Qualification | Avoids promising fulfilment when one printer is unavailable. | Quote both suppliers for each SKU and hold a tested alternative. |
| 19 | Service Recovery Playbook | Turns late, damaged or incorrect orders into consistent remedies. | Prewritten decision tree and supplier claim evidence bundle. |
| 20 | B2B Procurement Pack | Reduces friction with hotel and school purchasing teams. | PDF with product spec, data-flow map, sample contract schedule and pilot scope. |
| 21 | Provenance Certificate | Lets the buyer verify serial, issue metadata and approved public facts. | Signed manifest and public verification endpoint without private data. |
| 22 | Customer Export & Portability | Trust improves when the buyer can export final files and their own submitted content. | Download bundle with explicit retention and licence statement. |
| 23 | Model and Supplier Kill Switch | Stops a newly unsafe, costly or failed integration quickly. | Deterministic feature flag default-off and provider circuit breaker. |
| 24 | Founder Workload Meter | Reveals whether the solo operating model is actually sustainable. | Measure minutes per order, exceptions, daily pages awaiting approval and open incidents. |

## 5. Risk Register

Likelihood and impact are qualitative planning estimates, not measured actuarial frequencies. “High” means the risk deserves a pre-launch control.

| ID | Risk | Likelihood | Impact | Mitigation / evidence required |
|---|---|---|---|---|
| R01 | Child photo disclosed to an unapproved processor | Medium | Critical | No upload until provider DPA, purpose, region, retention and access controls are verified; synthetic-only portfolio. |
| R02 | Purge job reports success while a derivative remains | Medium | Critical | Asset graph; enumerate every derivative; verify DELETE and provider acknowledgement; signed receipts. |
| R03 | Child biometric embedding or LoRA generated accidentally | Low–Medium | Critical | Prohibit by design; tests inspect manifests and code paths; no face similarity for minors. |
| R04 | Cross-customer exposure within shared B2C tenant | Medium | Critical | `tenant_id + subject_id` in every query; PostgreSQL RLS; adversarial tests. |
| R05 | Webhook replay duplicates payment or print order | Medium | High | Unique `(provider, event_id)`; transactional inbox/outbox; provider-specific signature validation. |
| R06 | Forged founder approval or replayed signature | Low–Medium | Critical | KMS/secret rotation, one-time action ID, signed hash, nonce, audit trail, expiration and revocation. |
| R07 | Incorrect book printed after file changes | Medium | High | Approval bound to exact PDF and cover hashes plus supplier quote and SKU. Any change invalidates approval. |
| R08 | Printer rejects PDF or produces wrong trim/colour | Medium | High | SKU-specific preflight, sample copy, physical proof, printer acceptance receipt. |
| R09 | Arabic RTL layout corruption | Medium | High | Golden test corpus, mixed-script tests, manual print proof. |
| R10 | AI hallucinated family facts | Medium | High | Book Truth Ledger, source-supported writing, fact-check workflow, highlighted proof. |
| R11 | AI content unsafe for child age | Low–Medium | Critical | Deterministic policy + independent moderation + parent preview; block on uncertainty. |
| R12 | Customer assumes full copyright exclusivity | Medium | High | Clear personal/commercial licence terms; human authorship disclosure; no unsupported exclusivity claim. |
| R13 | Trademark opposition or domain dispute | Medium | High | Clearance search across phonetic variants, classes and territories before public investment. |
| R14 | EU VAT/import duty incorrectly calculated | High | High | Country-of-origin, destination, goods value and supplier route stored; tax review; no auto-collection before registration. |
| R15 | US sales-tax nexus develops unnoticed | Medium | High | Monitor state-by-state thresholds and marketplace/seller obligations; specialist review. |
| R16 | Payment account unavailable to an Egypt-based founder | Medium | Critical | Confirm account eligibility and business documentation with provider before accepting orders; lawful adult entity/account holder where required. |
| R17 | Customer acquisition cost exceeds contribution | High | High | Track CAC by cohort and channel; stop paid activity until validated. |
| R18 | Refund/chargeback erases apparent profit | Medium | High | Refund reserve, shipping evidence, transparent product previews and chargeback response pack. |
| R19 | POD supplier delays / customs charges surprise customer | High | Medium–High | Destination-specific checkout estimate and conservative delivery window; notify buyer of import duties. |
| R20 | Solo founder unavailable during exception | High | High | No 24/7 response claim; automatic acknowledgement; clear operating coverage and escalation policy. |
| R21 | Model API outage, price change or terms change | Medium | High | Provider adapter, fallback model, price cap, kill switch, periodic terms review. |
| R22 | Excessive generation retries inflate cost | Medium | Medium | Retry cap, image budget, deterministic stop and founder escalation. |
| R23 | SEO pages classified as scaled content abuse | High if auto-published | High | Publish only researched, distinct, genuinely useful pages; no bulk thin pages. |
| R24 | Social platform API restrictions or account ban | Medium | Medium–High | Founder-owned accounts, approved scopes, manual publication fallback and content archive. |
| R25 | B2B procurement cycle consumes founder capacity without paid pilot | High | Medium | Paid pilot, qualification rubric, explicit scope, no free custom work. |
| R26 | Product is perceived as AI novelty rather than a luxury book | High | High | Physical samples, strong editorial design, craft proof, customer interviews and clear human curation. |
| R27 | False “world's first / #1 / 99.9%” marketing claims | Medium | High | Evidence-backed claims register and pre-publication review. |
| R28 | Data breach through logs, previews or support email | Medium | Critical | Redaction, short retention, access controls, incident playbook and no photos in ordinary email. |
| R29 | Font/image/model licence incompatible with commercial output | Medium | High | Asset licence register, model-specific licence checks, preserve notices and source records. |
| R30 | Unprofitable premium packaging added prematurely | Medium | Medium | Paid sample and contribution test; no tooling or bulk commitment before validated demand. |

## 6. Board priority order

1. Lock the legal operating model and the adult/guardian contracting route; no circumventing age or identity rules.
2. Freeze a single initial product SKU, customer promise, and service boundary.
3. Prove one physical sample and fully landed cost for one shipping destination.
4. Prove privacy controls using synthetic assets first; do not collect child photos during prototype testing.
5. Complete database durability and provider event idempotency before a live automated fulfilment promise.
6. Obtain paid pilot demand before adding new product lines, agents, servers, advertising or premium packaging.
7. Publish only what has passed evidence review.

## 7. Decision Log

| Decision | Owner | Why |
|---|---|---|
| Do not claim first, #1, 99.9%, full autonomy or legal compliance without evidence | CEO + Legal | Prevents false and risky representations. |
| Start with one 32-page illustrated children's SKU using synthetic demo content | CPO | Minimises variation and risk. |
| Treat all agents as logical software roles, not human employees | CTO | Accurate operational description. |
| Keep child likenesses out of public marketing and prohibit child face embeddings/LoRA | Legal + AI Engineering | Minimises child-data exposure. |
| Make live print quote and physical proof mandatory before commercial dispatch | Publishing + CFO | A POD category page is not a production guarantee. |
| Use contribution margin, not “net profit per book”, for first economics | CFO | Keeps missing overhead visible. |
| Defer paid ads until $10,000 verified cumulative net profit and separate founder approval | CEO + CFO | Protects cash and discipline. |
| Domain and final company name remain unregistered until clearance | Brand + Legal | Avoids preventable collision. |
| Publish a realistic founder support window, not 24/7 human support | Operations + CX | Solo founder cannot honestly promise continuous human coverage. |

---

**Discipline signatures:** CEO / Strategy; CTO / Architecture; CPO / Product; CMO / Growth; CFO / Finance; Chief Legal & Compliance Officer; Chief Brand Officer; Head of Operations; Head of AI Agent Engineering; Head of Customer Experience; World Luxury Publishing Expert; MENA & Gulf Markets Expert; Consumer Psychologist & Behavioral Economist. These are governance roles for the proposed Board, not signatures by separately engaged professionals.
