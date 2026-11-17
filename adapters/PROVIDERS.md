# Provider adapter configuration

Adapters make no network requests when imported. Configure credentials in the hosting secret manager and invoke the corresponding client method explicitly. Keep production credentials out of source control and browser bundles.

| Adapter | Required environment variables | Notes |
| --- | --- | --- |
| Cloudflare R2 | `CLOUDFLARE_R2_ACCOUNT_ID`, `CLOUDFLARE_R2_ACCESS_KEY_ID`, `CLOUDFLARE_R2_SECRET_ACCESS_KEY` | Requires optional `boto3`; objects are private by default. |
| Auth0 | `AUTH0_DOMAIN`, `AUTH0_AUDIENCE`; `AUTH0_CLIENT_ID`, `AUTH0_CLIENT_SECRET` for M2M | Requires optional `PyJWT[crypto]` to validate RS256 tokens. |
| Gelato | `GELATO_API_KEY` | Quotes and orders are explicit API calls. |
| Lulu | `LULU_CLIENT_KEY`, `LULU_CLIENT_SECRET` | Defaults to the sandbox host; opt into production deliberately. |
| Paymob | `PAYMOB_SECRET_KEY`, `PAYMOB_HMAC_SECRET` | Intent amounts are minor currency units. Callback deduplication in this adapter is process-local; production deployments should persist event IDs with a database unique constraint. |
| Resend | `RESEND_API_KEY` | Pass an event-derived idempotency key for each transactional message. |

See `.env.example` in each frontend directory for the non-secret UI configuration. Never prefix server credentials with `VITE_`; Vite embeds those values in browser assets.
