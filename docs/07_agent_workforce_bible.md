# ASMA-OS — Workforce Bible for the 45 Logical Agent Roles

ملخص تنفيذي 1: يضم ASMA-OS خمسةً وأربعين دوراً برمجياً موزعة على خمس عشرة إدارة، وليس خمسةً وأربعين موظفاً بشرياً.
ملخص تنفيذي 2: تعمل الأدوار عبر محرك تنفيذ مشترك وبوابة MCP واحدة وصلاحيات محددة، ولا تمتلك مفاتيح مزودي الخدمات مباشرة.
ملخص تنفيذي 3: تم دمج `prompt_self_optimizer` كمهارة داخل `seasonal_trend_scout` للمحافظة على 45 هوية مستقلة بالضبط.
ملخص تنفيذي 4: كل وكيل له مدخلات ومخرجات ومصادر معرفة ومؤشرات أداء، وتبقى القرارات المالية والقانونية والطباعة والنشر العام للمؤسس.
ملخص تنفيذي 5: لا تعني كثرة الوكلاء الاستقلال أو الجاهزية؛ النجاح يقاس بدقة التسليم، وتكلفة الطلب، وانخفاض الاستثناءات، وسلامة البيانات.

## 1. Operating contract

- **One human owner; zero human employees in the operating design.** This describes the intended operating model, not a claim that external print providers, payment companies, cloud providers or legal advisers do not participate.
- **45 logical agent identities across 15 departments.** They share runtimes, provider adapters, databases and evaluation harnesses. They are not 45 separately hosted services or 45 autonomous legal persons.
- **One central gateway:** every external tool call is authorised through `ASMA_MCP_Server`. Models cannot call payment, storage, print, social or identity APIs directly.
- **One evidence ledger:** all consequential outputs carry tenant, subject, artifact hash, source agent, tool invocation, model version, policy version and result.
- **One founder approval surface:** the founder is the only authority for print dispatch, public release, paid advertising, refunds above policy threshold, contract execution, provider changes and policy overrides.
- **No self-approval:** an agent cannot approve its own output, issue its own authority, mint new credentials or change its own policy.
- **No child face biometrics in the initial product:** no face embeddings or LoRA training for minors. Customer photographs are not accepted in the initial release.
- **Capability alias:** `prompt_self_optimizer` resolves to a skill owned by `seasonal_trend_scout`, not a 46th agent identity.

## 2. Department chart

| Department | Agent count | MCP toolset | Primary output |
|---|---:|---|---|
| Executive | 2 | `executive_control` | Routing, approvals and company state |
| Intake | 2 | `intake_support` | Normalised brief and validated BookSpec |
| Commerce | 3 | `commerce_finance` | Verified payment, tax route and price model |
| Compliance | 5 | `privacy_compliance` | Consent, safety, purge and processor evidence |
| Creative | 7 | `creative_rnd` | Pedagogy, story, localisation and illustration assets |
| Production | 4 | `production_quality` | Print layouts, cover, audio and mockups |
| Quality | 5 | `production_quality` | Independent QA votes and release verdict |
| Fulfilment | 2 | `fulfilment_operations` | Supplier order and shipment status |
| Marketing | 4 | `growth_b2b` | Brand strategy, approved social, video and ad draft |
| Acquisition & Growth | 4 | `growth_b2b` | Leads, SEO drafts, vault record and referral |
| B2B Enterprise | 2 | `growth_b2b` | Business prospect and commercial proposal |
| Support | 2 | `intake_support` | Support reply draft and verified feedback |
| Innovation & R&D | 1 | `creative_rnd` | Trend report and prompt optimisation skill |
| Finance | 1 | `commerce_finance` | Reconciled ledger and upgrade evidence |
| Operations | 1 | `fulfilment_operations` | Health, backup and recovery evidence |
| **Total** | **45** | **8 toolsets** | **One operating system** |

## 3. Individual agent job files — all 45 identities

### 1. `asma_chief_orchestrator` — Chief Operating Orchestrator

- **Department / MCP:** Executive / `executive_control`.
- **Mission:** Accept validated events, choose the allowed workflow, enforce bounded transitions, prevent duplicate execution and route exceptions to the correct owner.
- **Inputs:** Signed `AgentEvent`, BookSpec version, evidence references, tenant and subject claims, policy manifest.
- **Outputs:** Task route, immutable handoff, workflow checkpoint reference, blocked-state reason and execution audit event.
- **Knowledge sources:** LangGraph state-machine and persistence documentation; Model Context Protocol specification; Google SRE book (error budgets and incident response); *Designing Data-Intensive Applications* by Martin Kleppmann; NIST AI Risk Management Framework.
- **KPIs:** 100% of routed events have an event ID and tenant/subject; 0 cross-tenant dispatches; 0 unbounded loops; 100% of unknown events fail closed; duplicate side effects = 0 in integration tests.

### 2. `founder_screen` — Founder Decision Interface

- **Department / MCP:** Executive / `executive_control`.
- **Mission:** Show only critical page defects and consequential actions; collect the founder's cryptographic decision against one immutable artifact and action.
- **Inputs:** QA report, critical page indexes, final artifact hash, supplier quote hash, requested action, approval policy.
- **Outputs:** One-time signed approval or rejection, reason code, action record and audit receipt.
- **Knowledge sources:** OWASP ASVS; W3C WCAG 2.2; human-in-the-loop design literature; NIST Digital Identity Guidelines; secure approval and replay-prevention patterns.
- **KPIs:** 100% approvals bind to exact action and artifact hash; 0 approvals reusable across changed files; 0 browser-exposed secrets; median critical-page review time measured separately from the aspirational three-minute target.

### 3. `intake_concierge` — Customer Brief Concierge

- **Department / MCP:** Intake / `intake_support`.
- **Mission:** Convert an adult customer's request into a concise, language-aware, minimal-data brief without inventing personal facts.
- **Inputs:** Order form, customer language, product tier, permitted story facts and consent notice version.
- **Outputs:** Normalised brief, missing-field list, ambiguity questions and data-minimisation report.
- **Knowledge sources:** *Jobs to Be Done* framework; Nielsen Norman Group conversational UX guidance; plain-language standards; W3C internationalisation guidance; WCAG 2.2 input and error-prevention criteria.
- **KPIs:** 100% required order fields validated; zero invented personal facts; fewer than one avoidable clarification loop per median order after calibration; zero child-direct accounts in the initial release.

### 4. `spec_compiler` — Book Specification Compiler

- **Department / MCP:** Intake / `intake_support`.
- **Mission:** Compile the brief into a versioned, strict BookSpec and report all validation failures before work begins.
- **Inputs:** Normalised brief, product catalogue, page-count contract, cost quote reference and tenant context.
- **Outputs:** Validated BookSpec, schema version, canonical digest, field-level errors and migration compatibility result.
- **Knowledge sources:** Pydantic v2 documentation; JSON Schema specification; semantic versioning; *Designing Data-Intensive Applications* schema evolution chapters; contract testing patterns.
- **KPIs:** 100% compiled specs pass schema validation; zero untyped monetary floats; 100% of schema changes have migration tests; zero product/page-count mismatch entering production.

### 5. `payment_gatekeeper` — Payment Verification Officer

- **Department / MCP:** Commerce / `commerce_finance`.
- **Mission:** Verify the payment provider's actual signature scheme, event status, order, currency and amount; commit the payment event once.
- **Inputs:** Raw provider callback, provider event ID, checkout order, expected amount and currency, provider-specific verification configuration.
- **Outputs:** Verified payment receipt, deduplication result, ledger transaction and outbox event.
- **Knowledge sources:** Paymob developer documentation for the contracted API version; PCI DSS; payment-provider webhook security guidance; OWASP API Security Top 10; transactional outbox and idempotency patterns.
- **KPIs:** 100% invalid signatures rejected; 0 duplicate ledger effects; 100% successful events matched to order/amount/currency; 100% test coverage for event replay and failure retry.

### 6. `tax_router` — Indirect Tax and Customs Router

- **Department / MCP:** Commerce / `commerce_finance`.
- **Mission:** Route transactions by product type, seller establishment, dispatch country, destination, buyer type and verified tax facts; send ambiguous cases to manual review.
- **Inputs:** `TaxFacts`, seller registration status, verified VAT ID, physical/digital classification, value and dispatch route.
- **Outputs:** Provisional tax path, required registration questions, customs flags and tax-review evidence request.
- **Knowledge sources:** EU VAT Directive and OSS/IOSS guidance; HMRC VAT on goods and digital services; IRS/state sales-tax nexus materials; OECD International VAT/GST Guidelines; Egyptian Tax Authority publications.
- **KPIs:** 100% unknown or incomplete facts routed to manual review; zero automatic reverse-charge on physical goods without a supported rule; 100% tax invoices retain jurisdiction and source facts; zero tax advice claims generated as final legal conclusions.

### 7. `pricing_optimizer` — Pricing and Contribution Analyst

- **Department / MCP:** Commerce / `commerce_finance`.
- **Mission:** Calculate unit contribution from Decimal-only supplier quotes, fees, tax-excluded revenue, reprint reserve and support costs.
- **Inputs:** Tier, live print quote, shipping quote, image invoice, payment fee schedule, packaging quote and refund/reprint history.
- **Outputs:** Price floor, contribution margin, downside sensitivity, quote expiry rule and recommendation for founder review.
- **Knowledge sources:** *Financial Intelligence for Entrepreneurs*; contribution-margin accounting; activity-based costing; cash conversion cycle concepts; provider price documentation.
- **KPIs:** 100% of monetary input values are Decimal or exact decimal strings; 2% minimum reprint reserve; quote-to-invoice variance tracked for every order; no product dispatch below approved contribution floor.

### 8. `consent_auditor` — Consent Evidence Auditor

- **Department / MCP:** Compliance / `privacy_compliance`.
- **Mission:** Check adult authority, parental authority where applicable, notice version, processing purpose and separate optional marketing consent.
- **Inputs:** Consent record, age band, verification method evidence, policy notice version and exact data purposes.
- **Outputs:** Consent status, deficiencies, processing restrictions and review evidence.
- **Knowledge sources:** FTC COPPA Rule and FAQs; GDPR Articles 5, 6, 8, 12–14 and 17; Egyptian Personal Data Protection Law No. 151/2020 and Executive Regulations; UK ICO Children's Code.
- **KPIs:** 100% of personal-data processing tied to a purpose and evidence record; 0 bundled marketing consent; 0 child photo processing in v1; all failed consent checks block the relevant tool.

### 9. `safety_guard` — Primary Content Safety Reviewer

- **Department / MCP:** Compliance / `privacy_compliance`.
- **Mission:** Combine deterministic policy scans with a separate model-based review of manuscript and artwork metadata; fail closed on high-severity issues.
- **Inputs:** Manuscript, age band, policy categories, artwork manifest and cultural/localisation flags.
- **Outputs:** Safety report, severity, blocked categories, remediation instructions and evidence digest.
- **Knowledge sources:** NIST AI Risk Management Framework; OWASP Top 10 for LLM Applications; UNICEF policy guidance on AI and children; child-development age bands; internal content safety taxonomy.
- **KPIs:** 100% high-severity deterministic flags block the workflow; 100% reviewed content has a versioned report; false-negative rate measured on a curated evaluation set; 0 unsafe work forwarded to production.

### 10. `privacy_purger` — Sensitive Asset Deletion Operator

- **Department / MCP:** Compliance / `privacy_compliance`.
- **Mission:** Delete assets across every controlled storage and processing location and collect verifiable provider and local deletion receipts.
- **Inputs:** Asset IDs, tenant/subject, data class, retention policy, provider deletion status and deletion request.
- **Outputs:** Per-location deletion results, failure alerts, signed purge receipt and residual-data exception list.
- **Knowledge sources:** GDPR storage limitation and erasure guidance; Egyptian PDPL and Executive Regulations; Cloudflare R2 object deletion documentation; provider-specific API deletion contracts; NIST media sanitisation guidance.
- **KPIs:** For any future approved sensitive-photo feature, deletion is completed and evidenced within the published policy limit; 100% of failed provider deletions escalate; 0 source-photo or biometric objects in routine backups; 100% of purge receipts identify all controlled locations.

### 11. `legal_scribe` — Rights, Licence and Notice Recorder

- **Department / MCP:** Compliance / `privacy_compliance`.
- **Mission:** Record customer grants, source-material provenance, real human editing decisions, personal licence terms and required consumer notices.
- **Inputs:** Customer rights declaration, manuscript edit history, licensed assets, model terms, personalised-goods disclosure and order terms.
- **Outputs:** Rights register, authorship log digest, licence summary and missing-rights block.
- **Knowledge sources:** U.S. Copyright Office AI report Part 2; WIPO copyright basics; Berne Convention principles; EU Consumer Rights Directive Article 16(c); applicable platform and font licences.
- **KPIs:** 100% commissioned assets have provenance fields; 0 claims of full AI-output copyright ownership; 100% of third-party licences are recorded; 0 personalised-goods sales without pre-purchase disclosure where required.

### 12. `dpa_compliance_monitor` — Processor Contract Monitor

- **Department / MCP:** Compliance / `privacy_compliance`.
- **Mission:** Verify provider contracts, subprocessors, processing locations, retention settings, deletion mechanics and data-transfer controls before any personal data is sent.
- **Inputs:** Provider register, DPA, subprocessor list, product plan, zero-retention evidence and transfer route.
- **Outputs:** Processor clearance matrix, blocked provider list, contract exceptions and review evidence.
- **Knowledge sources:** GDPR Article 28 and Chapter V; EDPB international transfer guidance; Egyptian PDPL transfer provisions; NIST privacy framework; individual provider DPAs and data-processing terms.
- **KPIs:** 100% of processors are recorded before personal data is sent; no Boolean-only DPA clearance; every provider status links to signed terms and configuration evidence; zero undisclosed processors in the data map.

### 13. `pedagogy_architect` — Learning Objective and Discussion Designer

- **Department / MCP:** Creative / `creative_rnd`.
- **Mission:** Translate a buyer-approved theme into one age-appropriate narrative objective and optional adult-child discussion prompts without claiming clinical or guaranteed educational outcomes.
- **Inputs:** Age band, language, buyer brief, inclusion needs and story scope.
- **Outputs:** Objective, vocabulary ceiling, discussion prompts and age-safety constraints.
- **Knowledge sources:** UNICEF child-rights and participation guidance; UNESCO literacy resources; National Association for the Education of Young Children developmentally appropriate practice; dialogic reading research; age-appropriate language design.
- **KPIs:** 100% books carry one explicit narrative objective; all prompts are age-reviewed; zero medical, therapeutic or guaranteed learning claims; reading-level tests recorded for every language edition.

### 14. `story_architect` — Narrative Structure Architect

- **Department / MCP:** Creative / `creative_rnd`.
- **Mission:** Design plot, page beats, character arc, conflict resolution and emotional register within the BookSpec constraints.
- **Inputs:** BookSpec, pedagogy plan, audience, page count, tone and factual boundaries.
- **Outputs:** Outline, page map, continuity bible and scene-level generation plan.
- **Knowledge sources:** Aristotle's *Poetics*; Robert McKee's *Story*; narrative transportation research; children's literature craft guidance; internal story-quality rubric.
- **KPIs:** 100% outlines account for every page; no unresolved plot dependencies; all customer-supplied facts are traceable; revision rate from QA tracked by story defect category.

### 15. `story_writer` — Manuscript Writer

- **Department / MCP:** Creative / `creative_rnd`.
- **Mission:** Draft original prose from the approved outline while maintaining voice, factual accuracy, reading level and word budget.
- **Inputs:** Page map, character bible, vocabulary ceiling, source facts and language instructions.
- **Outputs:** Manuscript, page text segments, content provenance references and writer self-check.
- **Knowledge sources:** *The Chicago Manual of Style*; plain-language guidance; age-appropriate literature craft; narrative voice and dialogue frameworks; internal house style.
- **KPIs:** 0 unapproved factual additions; 100% pages within word budget; grammar defect rate measured in QA; similarity screening and originality review completed before release.

### 16. `translator_ar_fr` — Arabic/French Localisation Editor

- **Department / MCP:** Creative / `creative_rnd`.
- **Mission:** Localise meaning, names, idioms and reading rhythm across Arabic, English and French without literal translation errors.
- **Inputs:** Approved source manuscript, locale, names, dialect preference and glossary.
- **Outputs:** Localised manuscript, terminology table, transliteration approvals and RTL/LTR metadata.
- **Knowledge sources:** W3C Internationalisation and Unicode Bidirectional Algorithm; Unicode CLDR; Arabic typography and orthography references; Académie française resources; internal market-specific style sheets.
- **KPIs:** 100% proper names reviewed; zero missing text blocks; all Arabic pages pass bidi regression; translation fidelity defects reported per 1,000 words; accents and punctuation validated.

### 17. `character_keeper` — Character Continuity Director

- **Department / MCP:** Creative / `creative_rnd`.
- **Mission:** Maintain a safe fictional character reference sheet for visual continuity without retaining prohibited child biometric templates.
- **Inputs:** Approved character description, silhouette, outfit, palette, scene requirements and asset rights.
- **Outputs:** Character bible, allowed variation matrix and short-lived generation reference.
- **Knowledge sources:** BFL reference-image documentation and terms; visual continuity methods; character design principles; internal illustration style guide; privacy-by-design requirements.
- **KPIs:** 100% illustrations trace to an approved character bible; wardrobe/palette deviations scored; 0 child face embeddings and child LoRA; all source references have rights metadata.

### 18. `illustrator` — Scene Illustration Generator

- **Department / MCP:** Creative / `creative_rnd`.
- **Mission:** Produce page illustrations that match scene action, character bible, brand direction and print-safe composition.
- **Inputs:** Storyboard, character guide, art prompt, aspect ratio, print dimensions and asset manifest.
- **Outputs:** Page images, generation metadata, seed/reference lineage where available and asset manifest update.
- **Knowledge sources:** Approved image-provider API and terms; composition and visual storytelling; colour theory; print reproduction fundamentals; internal brand illustration prompt bible.
- **KPIs:** 100% pages have an image disposition (image or intentional typographic page); composition QA above approved threshold; 0 unlicensed or nonconsensual likeness; regeneration rate and cost tracked per page.

### 19. `upscaler` — Print Asset Preparation Engineer

- **Department / MCP:** Creative / `creative_rnd`.
- **Mission:** Convert approved images to the exact pixel dimensions, colour profile and resolution requested by the selected printer SKU.
- **Inputs:** Approved image, trim size, bleed template, effective PPI, colour profile and format requirement.
- **Outputs:** Print asset, effective resolution report, dimensions and source/output hashes.
- **Knowledge sources:** ImageMagick documentation; Pillow documentation; printer technical sheets; ICC colour management basics; print production standards.
- **KPIs:** 100% assets meet SKU-specific effective-resolution rules; zero accidental aspect-ratio distortion; every output hash stored; no asset is silently upscaled and described as native high resolution.

### 20. `typesetter` — Book Composition and RTL Specialist

- **Department / MCP:** Production / `production_quality`.
- **Mission:** Compose final multilingual book pages, embedded fonts, captions, front matter, colophon and printer-specific PDF output.
- **Inputs:** Approved manuscript, print images, trim/bleed template, font package, brand system and selected printer profile.
- **Outputs:** Editable Typst source, PDF, font report, page map and preflight manifest.
- **Knowledge sources:** Typst official documentation; Unicode Bidirectional Algorithm; W3C Arabic layout guidance; PDF Association standards; exact POD printer specification.
- **KPIs:** 100% page count and text completeness; 100% required fonts embedded; zero overflow or clipping; zero missing-glyph defects; every PDF passes selected printer preflight.

### 21. `cover_designer` — Cover and Jacket Designer

- **Department / MCP:** Production / `production_quality`.
- **Mission:** Design front, spine and back cover around the actual printer template and approved title hierarchy.
- **Inputs:** Book title, brand system, page count, selected stock, binding template, barcode/identifier requirements and cover artwork.
- **Outputs:** Cover source, separate foil layer when supported, spine calculation, print PDF and mockup source.
- **Knowledge sources:** Type and grid systems; book-cover hierarchy; supplier cover-template documentation; PDF print standards; brand identity rules.
- **KPIs:** Zero spine-width mismatch; 100% title and author-name fidelity; all critical text inside the exact safe area; no unsupported foil or embossing claim.

### 22. `audiobook_producer` — Narration and Audio Producer

- **Department / MCP:** Production / `production_quality`.
- **Mission:** Render approved text into licensed synthetic narration with correct pronunciation, chaptering and accessible playback assets.
- **Inputs:** Approved manuscript, locale, licensed model/voice card, pronunciation glossary and audio profile.
- **Outputs:** Audio files, transcript, chapter manifest, voice/model licence record and audio QA report.
- **Knowledge sources:** MOSS-TTS-Nano or Piper model cards and licences; EBU R 128 loudness guidance; audiobook chapter metadata standards; WCAG media accessibility guidance.
- **KPIs:** 100% text/audio version match; no unlicensed voice cloning; pronunciation defect rate tracked; transcript available for every audio edition; audio playback and download checks pass.

### 23. `mockup_renderer` — Product Mockup Artist

- **Department / MCP:** Production / `production_quality`.
- **Mission:** Create realistic but clearly labelled digital product mockups from approved covers and sample interior pages.
- **Inputs:** Approved cover PDF, page renders, 3D model, lighting direction and mockup disclosure status.
- **Outputs:** WebP/PNG mockups, scene files, render metadata and synthetic-asset manifest.
- **Knowledge sources:** Blender manual; Three.js documentation; product photography composition; colour-management workflow; internal visual brand system.
- **KPIs:** All digital mockups labelled until physical photography exists; zero fake customer locations or endorsements; image dimensions match platform requirements; source asset provenance recorded.

### 24. `qa_face_similarity` — Adult-Only Optional Likeness QA

- **Department / MCP:** Quality / `production_quality`.
- **Mission:** If separately approved for a lawful adult-personalised product, assess adult likeness consistency under an independently reviewed biometric policy. This agent is disabled for minors.
- **Inputs:** Adult-only explicit consent, approved reference, provider/model licence evidence and temporary comparison assets.
- **Outputs:** Adult likeness QA report, failure reason and immediate deletion request for temporary biometric data.
- **Knowledge sources:** InsightFace code and model licences; biometric privacy guidance; NIST face-recognition evaluation literature; internal DPIA and risk decision.
- **KPIs:** 0 minor biometric processing; 100% adult path has separate consent and licence evidence; measured error rates documented; no biometric output becomes a marketing asset.

### 25. `qa_text_fidelity` — Text and Proper-Name Auditor

- **Department / MCP:** Quality / `production_quality`.
- **Mission:** Compare approved manuscript with rendered pages and catch missing, reordered, duplicated or altered content.
- **Inputs:** Source text, page mapping, OCR/rendered text and approved name list.
- **Outputs:** Text diff, proper-name report, page mismatch list and QA score.
- **Knowledge sources:** OCR evaluation literature; Unicode text processing; multilingual spell-checking; *The Chicago Manual of Style*; internal proper-name criticality policy.
- **KPIs:** 100% of proper names matched; zero missing page text; text fidelity score ≥0.98 for exact content segments; all OCR uncertainty routed for direct visual inspection.

### 26. `qa_print_fitness` — Print File Preflight Auditor

- **Department / MCP:** Quality / `production_quality`.
- **Mission:** Verify final print package against the exact POD SKU, profile and submitted order constraints.
- **Inputs:** Interior PDF, cover PDF, printer template, embedded-font report, effective image PPI and colour profile.
- **Outputs:** Pass/fail preflight, defects, printer-template version and report hash.
- **Knowledge sources:** PDF Association PDF/X guidance; Ghent Workgroup specifications; ICC colour management; printer API requirements; Typst PDF output documentation.
- **KPIs:** Zero critical preflight errors; 100% files match a live supplier template; zero unembedded required fonts; physical proof defects tracked and classified.

### 27. `qa_safety_second_opinion` — Independent Safety Reviewer

- **Department / MCP:** Quality / `production_quality`.
- **Mission:** Independently re-review content safety, privacy leakage and image suitability after the primary safety guard.
- **Inputs:** Manuscript, artwork summary, first safety report and audience policy.
- **Outputs:** Independent vote, severity notes and disagreement flag.
- **Knowledge sources:** NIST AI RMF; OWASP LLM Top 10; child-safety content standards; internal policy taxonomy and red-team fixture set.
- **KPIs:** 100% high-severity disagreement blocks release; evaluator disagreement measured; 0 page released with unresolved critical flag; regression set grows after every confirmed defect.

### 28. `consensus_judge` — QA Consensus and Critical Page Extractor

- **Department / MCP:** Quality / `production_quality`.
- **Mission:** Apply the defined 3-of-4 independent review rule, minimum mean score and critical-page threshold; never convert low confidence into automatic approval.
- **Inputs:** Four independent QA votes, critical dimensions and page metadata.
- **Outputs:** Consensus verdict, failed dimensions, page indexes requiring founder review and consensus report digest.
- **Knowledge sources:** Multi-rater reliability; calibration and inter-rater agreement; evaluation design; internal release policy.
- **KPIs:** Exactly four distinct voters; at least three pass votes; mean score ≥0.85; any critical note below 0.92 is surfaced; 0 unreviewed critical dimensions.

### 29. `fulfilment_dispatcher` — POD Order Dispatcher

- **Department / MCP:** Fulfilment / `fulfilment_operations`.
- **Mission:** Submit the approved print package only when payment, customer proof, founder signature and live quote all match.
- **Inputs:** Final artifact hash, live quote ID, payment receipt, founder approval, destination, SKU and print template.
- **Outputs:** Provider order ID, exact submitted payload hash, provider response and dispatch receipt.
- **Knowledge sources:** Gelato API documentation; Lulu Print API; provider product catalogues; payment and print reconciliation patterns; shipping and customs basics.
- **KPIs:** 100% dispatched orders have all prerequisites; zero double-print side effects; supplier cost variance tracked; 100% external actions have durable idempotency keys.

### 30. `shipment_tracker` — Delivery Status Agent

- **Department / MCP:** Fulfilment / `fulfilment_operations`.
- **Mission:** Convert supplier and carrier status events into a clean customer timeline and flag stalled, lost or damaged parcels.
- **Inputs:** POD order ID, carrier tracking ID, provider webhooks and delivery destination.
- **Outputs:** Normalised status, delivery evidence, exception ticket and notification event.
- **Knowledge sources:** Gelato order and webhook documentation; Lulu order status APIs; carrier event standards; customer service recovery practices.
- **KPIs:** Every shipment has a current state or explicit “tracking unavailable”; duplicate status events do not duplicate messages; delivery exceptions escalated within policy; address data not written to public vault.

### 31. `cmo_marketing_strategist` — Chief Marketing Strategist

- **Department / MCP:** Marketing / `growth_b2b`.
- **Mission:** Define positioning, message hierarchy, content themes and measurable acquisition experiments using only substantiated product claims.
- **Inputs:** Brand strategy, customer objections, verified product assets, organic analytics and approved budget.
- **Outputs:** Campaign brief, channel plan, message tests and brand-safety checklist.
- **Knowledge sources:** *Positioning* by Al Ries and Jack Trout; *How Brands Grow* by Byron Sharp; customer-based brand equity; jobs-to-be-done; consent-aware marketing requirements.
- **KPIs:** Qualified enquiry rate, paid conversion, customer acquisition cost, contribution after acquisition and substantiated-claim compliance; no vanity metric substitutes for paid demand.

### 32. `social_media_publisher` — Approved Social Publisher

- **Department / MCP:** Marketing / `growth_b2b`.
- **Mission:** Publish only founder-approved synthetic brand assets through authorised platform accounts and APIs.
- **Inputs:** Approved asset manifest, exact social copy, account identity, OAuth scope and founder publish approval.
- **Outputs:** Platform post ID, publish receipt, URL and error status.
- **Knowledge sources:** Meta Graph API documentation; TikTok Content Posting API and audit rules; LinkedIn Posts API; platform community and branded-content policies.
- **KPIs:** 100% posts have founder approval and synthetic-asset manifest; zero child likeness or private customer assets; API errors and rejected scopes tracked; platform terms rechecked before each connector release.

### 33. `viral_video_scripter` — Short-Form Story Scriptwriter

- **Department / MCP:** Marketing / `growth_b2b`.
- **Mission:** Write short scripts that show the making of a sample book, editorial decisions and physical materials without featuring real children or fabricated buyer reactions.
- **Inputs:** Synthetic portfolio asset, approved brand story, video length, platform format and claims whitelist.
- **Outputs:** Hook, shot list, voiceover, caption, disclosure and accessibility text.
- **Knowledge sources:** Narrative hook design; platform video format guidance; accessible captioning; consumer advertising substantiation principles; internal creative performance tests.
- **KPIs:** 100% scripts map to approved assets; zero child likeness references; caption accuracy 100%; measure watch-through and qualified click-through without promising virality.

### 34. `performance_ads_manager` — Paid Media Draft and Control Agent

- **Department / MCP:** Marketing / `growth_b2b`.
- **Mission:** Prepare paid campaign drafts only after the cumulative verified net-profit threshold is reached; never release spend without a founder signature.
- **Inputs:** Profit evidence, approved campaign brief, audience, landing page, creative manifest and spend cap.
- **Outputs:** Draft campaign, forecast assumptions, risk note and approval request.
- **Knowledge sources:** Platform ad policies; *Lean Analytics*; incrementality and attribution basics; CAC/LTV economics; privacy and sensitive-data advertising restrictions.
- **KPIs:** Tool remains locked below USD 10,000 verified cumulative net profit; zero live spend without founder approval; daily spend cap checked; reporting separates attributed from incremental outcomes.

### 35. `outbound_lead_hunter` — Ethical Prospect Researcher

- **Department / MCP:** Acquisition & Growth / `growth_b2b`.
- **Mission:** Research public business prospects and adult enquiries with a lawful, relevant contact route; do not profile parents or children.
- **Inputs:** Target industry, public organisation information, country, contact permission and suppression list.
- **Outputs:** Verified business lead, source URL, relevance note, lawful-contact check and do-not-contact status.
- **Knowledge sources:** Public business registry and institution directories; GDPR direct-marketing guidance; UK PECR and CAN-SPAM basics where applicable; professional B2B prospecting ethics.
- **KPIs:** 100% lead records carry source and use-purpose; 0 child/parent profiling; 100% opt-outs suppressed; qualified reply rate and meeting rate measured.

### 36. `seo_factory` — Search Experience and SEO Editor

- **Department / MCP:** Acquisition & Growth / `growth_b2b`.
- **Mission:** Create genuinely useful, original, localised pages tied to a real offer, customer question and supporting evidence.
- **Inputs:** Search intent, keyword group, verified service facts, sample assets and language brief.
- **Outputs:** Page draft, internal links, title/meta, schema markup and originality report.
- **Knowledge sources:** Google Search Central helpful-content and spam policies; technical SEO; structured data documentation; multilingual SEO and hreflang; editorial fact checking.
- **KPIs:** 100% pages satisfy a distinct user need; no bulk thin-page publishing; crawl/index and qualified-enquiry metrics tracked; zero fabricated local claims or competitor comparisons.

### 37. `vault_publisher` — Public Edition Record Publisher

- **Department / MCP:** Acquisition & Growth / `growth_b2b`.
- **Mission:** Publish a redacted edition record only after separate customer-publication permission and founder approval.
- **Inputs:** Serial, approved public projection, exact artifact hash, customer publication choice and founder approval.
- **Outputs:** Public vault record, public metadata digest and cache invalidation receipt.
- **Knowledge sources:** OWASP API Security; object-level authorisation; privacy-by-design; search engine index controls; cryptographic integrity principles.
- **KPIs:** Zero private manuscript or image exposure; 100% public records have consent evidence; serial enumeration blocked by rate limits; depublication requests verified.

### 38. `referral_loop` — Permission-Based Referral Manager

- **Department / MCP:** Acquisition & Growth / `growth_b2b`.
- **Mission:** Invite a buyer to share the brand after delivery using optional, non-coercive referral mechanics.
- **Inputs:** Delivery receipt, customer marketing preference, referral campaign rules and abuse signals.
- **Outputs:** Referral invitation, trackable code and attribution event.
- **Knowledge sources:** Referral marketing research; double-sided incentive design; fraud prevention; email and consumer marketing rules.
- **KPIs:** 100% referrals opt-in; abuse and self-referral rates tracked; incremental referred orders measured; referral rewards never exceed approved contribution margin.

### 39. `b2b_hotel_school_scout` — Hospitality and School Prospect Analyst

- **Department / MCP:** B2B Enterprise / `growth_b2b`.
- **Mission:** Identify organisations whose guest, alumni, family or learning experience could support a small bespoke publishing pilot.
- **Inputs:** Public hotel/school directory, region, prospect relevance and buying-role map.
- **Outputs:** Account brief, probable sponsor role, procurement path, personalisation risks and pilot hypothesis.
- **Knowledge sources:** Public hotel operator reports; tourism ministry data; school authority and KHDA/MOE datasets; procurement frameworks; safeguarding and student-data guidance.
- **KPIs:** Every prospect has source and relevance; 0 unverified claims of partnership; qualified pilot introductions tracked; no student data collected during prospecting.

### 40. `b2b_account_closer` — Enterprise Proposal and Account Agent

- **Department / MCP:** B2B Enterprise / `growth_b2b`.
- **Mission:** Draft scoped proposals, service descriptions, rights schedules, pilot statements of work and renewal economics; it does not execute legal contracts.
- **Inputs:** Prospect brief, pilot scope, procurement rules, cost quote, licence need and buyer authority.
- **Outputs:** Proposal draft, cost sheet, approval checklist and negotiation issues.
- **Knowledge sources:** *The Challenger Sale*; enterprise procurement basics; statement-of-work design; licensing and IP ownership principles; hospitality guest-experience frameworks.
- **KPIs:** 100% proposals include scope, volume, rights, exclusions, supplier quote validity and acceptance criteria; zero contract execution without authorised signer; pilot margin tracked.

### 41. `support_agent` — Multilingual Customer Support Drafter

- **Department / MCP:** Support / `intake_support`.
- **Mission:** Draft accurate Arabic, English or French responses using order status and policy; refund or reprint actions remain constrained by approved policy.
- **Inputs:** Customer ticket, order timeline, approved policy, language and case evidence.
- **Outputs:** Reply draft, case category, severity and escalation requirement.
- **Knowledge sources:** ITIL incident and request management; service recovery literature; plain-language writing; FOLIAVERE refund, correction and shipping policy.
- **KPIs:** Response correctness; first-contact resolution; reopened-ticket rate; 100% severe privacy or safety tickets escalated; 0 unauthorised refund or reprint commitments.

### 42. `nps_feedback_collector` — Post-Delivery Feedback Analyst

- **Department / MCP:** Support / `intake_support`.
- **Mission:** Invite voluntary feedback after delivery and separate NPS from product-quality questions and review publication consent.
- **Inputs:** Verified delivery, communication preference, survey version and customer opt-in.
- **Outputs:** Feedback record, NPS category, quality issue flag and permission status.
- **Knowledge sources:** Bain NPS methodology; survey design basics; response-bias research; privacy and testimonial permission rules.
- **KPIs:** Survey invitation only after confirmed delivery; response rate; NPS distribution with sample size; 100% public testimonial use has explicit publication approval.

### 43. `seasonal_trend_scout` — Trend Intelligence and Prompt Optimisation Owner

- **Department / MCP:** Innovation & R&D / `creative_rnd`.
- **Mission:** Track cultural occasions and customer themes and use aggregate QA findings to propose prompt revisions. The `prompt_self_optimizer` label is a capability alias within this role.
- **Inputs:** Public trend sources, aggregate anonymised QA, search questions and product defect taxonomy.
- **Outputs:** Trend report, content opportunity, prompt revision proposal and regression test set.
- **Knowledge sources:** Google Trends documentation; public cultural calendars; search trend research; prompt evaluation methods; experiment design and version control.
- **KPIs:** Every prompt change passes the full regression set; no customer story or personal data used for trend analysis; defect recurrence reduced against measured baseline; trend proposals linked to verified buyer demand.

### 44. `finance_ledger` — Financial Controller

- **Department / MCP:** Finance / `commerce_finance`.
- **Mission:** Reconcile customer payments, refunds, supplier costs, FX, reserves, fees, taxes and operating expenditure to calculate verified cumulative net profit.
- **Inputs:** Payment receipts, supplier invoices, bank settlements, refunds, chargebacks, tax liabilities and cost quotes.
- **Outputs:** Transaction ledger, unit economics, monthly close report, cash forecast and upgrade eligibility.
- **Knowledge sources:** Double-entry bookkeeping; IFRS concepts where applicable; management accounting; cash-flow and working-capital analysis; Paymob settlement and bank statements.
- **KPIs:** Every money value uses Decimal; every order reconciles payment to supplier cost; reprint reserve ≥2%; profit evidence excludes taxes and customer funds owed; no upgrade unlocks from revenue alone.

### 45. `ops_sentinel` — Reliability, Security and Recovery Monitor

- **Department / MCP:** Operations / `fulfilment_operations`.
- **Mission:** Monitor API health, worker queues, backup integrity, security alerts and restore drills, excluding biometric source data from backups.
- **Inputs:** Health checks, logs, backup manifests, restore receipts, adapter error budgets and security policy.
- **Outputs:** Operational alert, recovery report, incident record and signed evidence bundle.
- **Knowledge sources:** Google SRE; NIST Cybersecurity Framework; OWASP ASVS; PostgreSQL backup/restore documentation; provider status pages and incident response playbooks.
- **KPIs:** RPO ≤15 minutes and RTO ≤60 minutes only after measured restore evidence; 100% backups encrypted; 0 prohibited biometric records in backup; failed health checks generate an incident; 0 secrets in logs.

## 4. Handoff map

```text
Customer / adult buyer
  -> intake_concierge
  -> spec_compiler
  -> consent_auditor + legal_scribe + dpa_compliance_monitor
  -> payment_gatekeeper + tax_router + pricing_optimizer
  -> pedagogy_architect (children's scope) / story_architect (other scope)
  -> story_writer
  -> translator_ar_fr (when locale requires)
  -> character_keeper -> illustrator -> upscaler
  -> safety_guard
  -> typesetter + cover_designer + audiobook_producer + mockup_renderer
  -> qa_text_fidelity + qa_print_fitness + qa_safety_second_opinion
  -> consensus_judge
  -> founder_screen
  -> fulfilment_dispatcher
  -> shipment_tracker
  -> support_agent + nps_feedback_collector
  -> finance_ledger
  -> ops_sentinel
```

Parallel company-level flows:

```text
cmo_marketing_strategist -> viral_video_scripter -> founder_screen -> social_media_publisher
b2b_hotel_school_scout -> b2b_account_closer -> founder_screen -> paid micro-pilot
seo_factory -> human editorial review -> founder_screen -> vault_publisher (redacted records only)
seasonal_trend_scout -> prompt regression -> story_architect / story_writer
finance_ledger -> upgrade evidence -> founder_screen
outbound_lead_hunter -> public business prospects or opted-in adult enquiries only
referral_loop -> confirmed delivery + separate customer opt-in
performance_ads_manager -> USD 10,000 verified net-profit lock + explicit founder approval
```

## 5. One customer order — end-to-end reference journey

**Example:** an adult customer commissions an Arabic Heirloom sample for a family member. The initial release uses written names and a fictional protagonist profile. No child photo is uploaded.

| Step / event | Agents | MCP actions | Evidence / state transition | Failure path |
|---:|---|---|---|---|
| 1. `intake.request.received` | `asma_chief_orchestrator`, `intake_concierge` | `intake.brief.create`, `exec.status.read` | Normalised brief, tenant/subject context | Missing or excessive data → ask adult buyer to revise; no generation |
| 2. `intake.brief.normalized` | `spec_compiler` | `intake.spec.compile` | Validated BookSpec + canonical digest | Invalid age, language, price or page count → stop and return field errors |
| 3. `compliance.precheck` | `consent_auditor`, `legal_scribe`, `dpa_compliance_monitor`, `safety_guard` | `compliance.consent.audit`, `compliance.authorship.record`, `compliance.dpa.audit`, `compliance.content.scan` | Consent/rights/policy evidence | Any missing permission or provider clearance → block personal-data use |
| 4. `commerce.payment.requested` | `tax_router`, `pricing_optimizer`, `payment_gatekeeper`, `finance_ledger` | `commerce.tax.route`, `commerce.price.quote`, hosted checkout, `commerce.payment.verify` | Verified payment receipt and ledger event | Callback signature invalid, amount mismatch, duplicate event or uncertain tax → reject/hold/manual review |
| 5. `creative.book.requested` | `pedagogy_architect`, `story_architect`, `story_writer` | `creative.pedagogy.build`, `creative.story.plan`, `creative.story.write` | Approved objective, outline and manuscript hash | Unsupported claim, unsafe theme or source-fact conflict → block and request revision |
| 6. `creative.localisation.requested` | `translator_ar_fr` | `creative.translate.ar_fr` | Localised Arabic/English/French text | Name transliteration uncertainty → mark critical and request customer confirmation |
| 7. `creative.images.requested` | `character_keeper`, `illustrator`, `upscaler` | `creative.character.prepare`, `creative.illustrate`, `production.upscale` | Synthetic character guide, page assets and hashes | Asset rights or prompt policy failure → reject asset and regenerate within bounded retry budget |
| 8. `production.package.requested` | `typesetter`, `cover_designer`, `audiobook_producer`, `mockup_renderer` | `production.typeset`, `production.cover.design`, `production.audio.render`, `production.mockup.render` | Print PDF, cover, optional audio, digital mockups | Fonts, RTL or audio licence failure → hold; do not send to POD |
| 9. `quality.review.requested` | `qa_text_fidelity`, `qa_print_fitness`, `qa_safety_second_opinion`, `consensus_judge` | `quality.text_fidelity`, `quality.print_fitness`, `quality.safety.second_opinion`, `quality.consensus` | 4 independent votes, score and critical pages | Fewer than 3 pass votes, mean <0.85 or critical policy issue → return to bounded correction |
| 10. `founder.approval.requested` | `founder_screen`, `asma_chief_orchestrator` | `exec.founder_approval.request`, `exec.founder_approval.record` | One-time HMAC approval tied to exact file and quote hashes | File or quote changes → prior signature invalid; new approval required |
| 11. `fulfilment.dispatch.requested` | `fulfilment_dispatcher` | `fulfilment.print.dispatch` | Provider order ID and request hash | Supplier rejection, SKU mismatch or quote expiry → stop and request new quote/approval |
| 12. `fulfilment.shipment.updated` | `shipment_tracker`, `support_agent` | `fulfilment.shipment.track`, `support.reply.draft` | Tracking timeline, customer notice | Lost/damaged/stalled shipment → exception case; no false delivery claim |
| 13. `fulfilment.delivery.confirmed` | `support_agent`, `nps_feedback_collector`, `referral_loop` | `support.reply.draft`, `support.nps.record`, `growth.referral.issue` | Delivery feedback, opt-in referral state | No consent → no marketing invitation; dissatisfied customer → service-recovery path |
| 14. `finance.order.closed` | `finance_ledger`, `ops_sentinel` | `finance.ledger.reconcile`, `operations.health.inspect`, `operations.backup.verify` | Reconciled order margin, backup and audit receipts | Supplier invoice variance or payment reversal → hold profit evidence and upgrade unlock |
| 15. `vault.publish.requested` (optional) | `vault_publisher`, `founder_screen` | `growth.vault.publish` | Redacted public record and approval | No explicit public metadata permission → no public record |
| 16. `marketing.content.requested` (optional) | `cmo_marketing_strategist`, `viral_video_scripter`, `social_media_publisher` | `marketing.strategy.plan`, `marketing.video.script`, `marketing.social.publish` | Synthetic brand campaign and publish receipt | Any private/customer/child likeness or missing founder approval → reject |

**Not activated in this consumer order:** `b2b_hotel_school_scout` and `b2b_account_closer` are activated only by an institutional prospect; `performance_ads_manager` remains locked until profit threshold and founder approval; the trend scout runs only on aggregate, non-identifying data. This is a deliberate separation, not an omitted control.

## 6. Founder's operating rhythm and workload truth

The system targets a single decision surface, not a fictional three-minute universal review. The founder's work is divided into:

- **Routine approval:** inspect only critical page thumbnails, exact proper names, final proof, quote and file hash.
- **Commercial decisions:** pricing, refunds outside policy, B2B proposals, supplier change, legal entity, trademark and paid spend.
- **Exception handling:** payment mismatches, delayed shipments, supplier failures, privacy requests, QA disagreement and customer complaints.
- **System governance:** approve prompts, model changes, provider changes, schema migrations and security-policy changes.

The workload target is under two hours per operating day only after measurement of a representative order cohort. The actual formula is:

`Founder hours = orders × median review minutes / 60 + exceptions × median exception minutes / 60 + fixed governance hours`.

At 500 orders per month, a three-minute screen alone requires 1,500 minutes, or 25 hours per month, before all exceptions, marketing, bookkeeping, procurement and customer disputes. The business must not promise 500 monthly orders as a solo-operated outcome until this load is measured and a lawful external service-provider arrangement is funded.

## 7. Decision Log

| Decision | Owner | Why |
|---|---|---|
| Keep exactly 45 agent identities | CEO + Head of AI Agent Engineering | Preserves the required org chart while treating the prompt optimiser as a skill. |
| Use shared runtimes and eight MCP toolsets | CTO | Avoids 45 independent services, duplicated secrets and excess operating cost. |
| No child image or biometric handling in v1 | Legal + CPO | Minimises risk until contracts, consent, deletion and security are proved. |
| Keep print, publication and spend founder-gated | CEO + CTO | Autonomous drafting must not become autonomous external commitment. |
| Treat two-hour founder day as a measured target | Head of Operations | Workload must be calculated from real order and exception data. |

**Sign-off:** Head of AI Agent Engineering — role and workflow design; CTO — gateway and event architecture; Head of Operations — workload model; Chief Legal & Compliance Officer — privacy and consent controls.
