# 12 Deliverables Traceability

This register maps the approved source package to current code and validation. The detailed source documents remain authoritative; this file does not replace them. `docs/README.md` was stale at audit time and references deleted `catalog.ts` and routes.

| # | Deliverable / source | Requirement groups | Current implementation | Validation / evidence | Gap / next action |
|---:|---|---|---|---|---|
| 1 | Board Audit — `docs/00_board_audit.md` | scope, risks, decision gates, launch constraints | audit document only | source inspection; earlier audit evidence | keep register current; close high risks before release |
| 2 | Name & Domain — `docs/01_name_and_domains.md` | naming, trademark/domain research, provisional choice | source document; `brand/brand_system.yaml` | static cross-reference | FOLIAVERE provisional; actual clearance requires founder/legal action |
| 3 | Consumer Psychology — `docs/02_consumer_psychology.md` | ethical value proposition, trust, buyer research | research source only | source review | conduct consented customer interviews; no outcomes claimed |
| 4 | Brand Story & Voice — `docs/03_brand_story_and_voice.md` | voice, messaging, localization | source document; current page copy is inconsistent | source/runtime comparison | implement approved bilingual copy and review translations |
| 5 | Brand System — `brand/brand_system.yaml`, `brand/brand_system.md`, `apps/storefront/src/styles/tokens.css` | identity, design tokens, logo/type/color rules | tokens exist but active layout bypasses them | YAML parse passed; runtime import absent | connect tokens and ensure fonts are licensed/available |
| 6 | Visual Identity 2027 — `docs/04_visual_identity_2027.md` | visual system, accessibility, RTL/LTR | design guidance and partial CSS only | no rendered accessibility test | implement component system and run contrast/keyboard checks |
| 7 | Portfolio & Unboxing — `docs/05_portfolio_and_unboxing.md` | SKU scope, sample artifacts, packaging journey | source document; prior `catalog.ts` deleted | route/file inventory | restore only validated, visibly synthetic sample catalog; obtain quotes |
| 8 | Complete Website — `docs/06_website_complete.md` | customer pages, onboarding, trust, support, legal, SEO | single Arabic static `/` page | Astro build required; route inventory confirms omissions | implement route set and nonfunctional-flow guards |
| 9 | Agent Workforce Bible — `docs/07_agent_workforce_bible.md` | 45 roles, departments, inputs/outputs, governance | detailed role documentation; five generic agent classes | role count from source; no role ACL runtime | define manifest and permissions; implement one workflow first |
| 10 | Market Intelligence — `docs/08_market_intelligence.md` | market evidence, competitor context, assumptions | dated research source only | sources not refreshed in this pass | verify primary facts with access dates; no TAM/customer claims |
| 11 | Growth Engine — `docs/09_growth_engine.md` | ethical acquisition, content, approval boundary | source only; CLI calls missing SEO module | code/source inventory | implement drafts only; founder approval before publication |
| 12 | Finance, Execution & Quality — `docs/10_finance_execution_quality.md` | costs, margin, operating gates, privacy, QA | assumptions/model/service and tests | formula/test validation pending | replace estimates with dated quotes and actual cohort evidence |

## Evidence vocabulary

`DOCUMENTED` means a requirement is described. `IMPLEMENTED` means code exists. `TESTED` means a named test actually passed on the stated revision. `LOCAL_OPERATIONAL` means a local flow was exercised end to end. `PRODUCTION_OPERATIONAL`, `COMMERCIALLY_VERIFIED`, and `LEGALLY_APPROVED` require independent evidence and are not inferred from repository code.
