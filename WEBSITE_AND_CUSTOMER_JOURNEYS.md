# Website and Customer Journeys

## Current verified state

Astro contains one active route, `/`, rendered in Arabic RTL using `BrandLayout.astro`. It shows three unverified tier prices/material promises and contains no checkout, contact form, locale switch, or product order action. The former catalog and localized/vault routes are absent. The React founder screen is separate and is not a customer journey.

## Required safe journey

1. Discovery page explains the provisional brand, intended product and what is a demo.
2. Customer views a synthetic sample clearly labeled “demonstration; no customer data”.
3. Intake is disabled until secure storage, consent, age/privacy boundaries, deletion and support process are implemented.
4. Product configuration and quote use a dated supplier quote; estimated prices are visibly labeled until verified.
5. Payment and fulfillment remain unavailable in local/demo mode; never show order success without a verified provider response.
6. Production proof goes through QA and customer review; founder approval binds to artifact and quote hashes.
7. Order status, support, refund, retention and deletion instructions are available before launch.

## Route plan to implement

`/` home; `/en/` and `/ar/` locale entry; `/editions/`; `/portfolio/`; `/how-it-works/`; `/trust/`; `/faq/`; `/contact/`; `/policies/privacy/`, `/policies/terms/`, `/policies/returns/`; `/for-organisations/` only if source scope supports it. Vault serial pages require a privacy-safe publication model and explicit approval. Checkout must be feature-disabled until backend readiness.

## UI acceptance checklist

- English and Arabic content are reviewed, with correct `lang`, `dir`, locale links and stable layout direction.
- Keyboard navigation, visible focus, semantic headings/forms, contrast, reduced motion, screen-reader names and mobile breakpoints are tested.
- Buttons either perform a real action or are clearly disabled; no fake “live” or “complete” states.
- SEO metadata is accurate, canonical URLs do not claim an unverified domain, and structured data contains no fabricated reviews.
- Use tokens from the approved brand system; avoid remote fonts if offline/resilience or license policy requires packaged fonts.
