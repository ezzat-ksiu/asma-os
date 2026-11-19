# Test and Validation Report

## Baseline from forensic audit (before this branch's API changes)

- `pytest --collect-only`: 88 tests collected.
- CI-target `test_e2e_gates.py`: 4 passed, 2 failed. Failures: missing `/api/health.gates_total`; missing `/api/payments/paymob/initiate` (404 expected 503). The test also required all gates to be PENDING, contrary to the old hard-coded PASSED response.
- Python AST parse: 58 source files, zero syntax errors.
- YAML parser accepted `brand/brand_system.yaml` and `.github/workflows/ci.yml`.
- Full suite not run in audit because one test writes a tracked invoice PDF; use a disposable checkout/temp output before full validation.
- Prior commit `5378e73a` historically reported 85 passed, 3 skipped and successful app builds. Not evidence for current HEAD.

## Current branch validation log

| Date | Command / check | Result |
|---|---|---|
| 2026-11-19 | `.venv\Scripts\python.exe -B -m pytest -p no:cacheprovider -v` | **94 passed, 3 skipped** (97 collected, 2.19s); full suite exited 0 |
| 2026-11-19 | Storefront `npm run build` | **Passed**; Astro built 21 static pages including Arabic/English concept routes |
| 2026-11-19 | Founder console `npm run build` | **Passed**; Vite production build completed |
| 2026-11-19 | Branch API regressions | Covered by full suite; health/gates pending, payment/invoice fail-closed, CORS default deny |
| 2026-11-19 | Python AST with UTF-8-SIG | 60 files parsed, 0 syntax errors |

The Typst test generated a tracked demonstration PDF during execution. Its bytes were restored from branch `HEAD` in a `finally` block after each full run. The frontend build touched a tracked generated `dist/index.html`; it is restored to the branch baseline after build verification.

Never mark a check passed unless the command completed and output was observed. Current revision's Python suite and both frontend builds passed. Production tests, accessibility, live providers, deployment, legal and financial checks remain unverified.
