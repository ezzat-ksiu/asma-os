# Agent Workforce Status

The Workforce Bible defines **45 logical roles** in 15 departments, not 45 separate hosted processes. Current code has generic Base/Gateway/Execution/Planning/Review agents and a plan/execute/review workflow. No role-specific identity, permission registry, deployment, or real business execution was verified. The historical `agents/manifest.yaml` is absent on current `main`.

## Runtime status

| Status level | Current finding |
|---|---|
| Documented | 45 role definitions in `docs/07_agent_workforce_bible.md` |
| Manifest | Missing at current HEAD |
| Generic runtime | Implemented locally; prior tests exist |
| Role-specific runtime | None verified |
| Permissions/ACL | Shared toolsets and boundaries are documented; enforcement not connected to API |
| Tested business execution | No complete customer-to-delivery flow verified |
| Deployed/real work | Not verified |

## 45-role inventory

`asma_chief_orchestrator`, `founder_screen`, `intake_concierge`, `spec_compiler`, `payment_gatekeeper`, `tax_router`, `pricing_optimizer`, `consent_auditor`, `safety_guard`, `privacy_purger`, `legal_scribe`, `dpa_compliance_monitor`, `pedagogy_architect`, `story_architect`, `story_writer`, `translator_ar_fr`, `character_keeper`, `illustrator`, `upscaler`, `typesetter`, `cover_designer`, `audiobook_producer`, `mockup_renderer`, `qa_face_similarity`, `qa_text_fidelity`, `qa_print_fitness`, `qa_safety_second_opinion`, `consensus_judge`, `fulfilment_dispatcher`, `shipment_tracker`, `cmo_marketing_strategist`, `social_media_publisher`, `viral_video_scripter`, `performance_ads_manager`, `outbound_lead_hunter`, `seo_factory`, `vault_publisher`, `referral_loop`, `b2b_hotel_school_scout`, `b2b_account_closer`, `support_agent`, `nps_feedback_collector`, `seasonal_trend_scout`, `finance_ledger`, `ops_sentinel`.

The Bible gives each role a mission, input/output, knowledge sources and KPIs. Build a machine-readable manifest from that source with explicit tool allowlists, data classifications, approval requirements, audit events, failure behavior, and acceptance tests. Do not imply role existence from an ID in a document. `prompt_self_optimizer` is an alias/skill of `seasonal_trend_scout`, not an extra identity.

## Initial workflow recommendation

Implement one bounded internal workflow: synthetic request → validated spec → deterministic plan → no-op/simulated production preparation → QA result → founder review record. External publishing, payment, supplier orders, refunds and contracts remain human-approved and disabled absent verified auth, evidence, and credentials.
