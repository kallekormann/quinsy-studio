# Skill: Payments and Billing

> Takes money exactly once and keeps the product's view of every subscription equal to the provider's. Uses the studio `billing` package (Stripe or Lemon Squeezy) through hosted checkout. Webhooks are the source of truth. The subscription state lives in a Payload collection. Prices, VAT and German price display are decided on the server and proven in test mode on the receipt.

## Metadata

```
skill_id: BE-008
name: Payments and Billing
team: 02-backend-systems
lead_role: Backend Architect
support_roles: [Backend Engineer, Backend Security Engineer, Compliance Lead]
phases: [2, 3, 4, 5]
activation_triggers:
  - Ticket adds checkout, a plan, a subscription, a refund, a coupon or a webhook from a payment provider
  - Blueprint names Stripe or Lemon Squeezy, or the archetype is SaaS with paid plans or a shop
  - Ticket words: checkout, subscription, billing, invoice, refund, dunning, VAT, pricing page
pairs_with: [BE-006, BE-007, BE-009, PE-005, PE-006, CL-003, GD-002]
```

## When to load

- Gate 1: when the PRD has paid plans. The architecture doc names the provider and the tax model (rule 8).
- Architecture phase: every ticket that touches money, plans, entitlements or provider webhooks.
- Implementation: same tickets. Pricing-page copy and layout stay with GD-002; this skill owns the numbers on it.

## Rules

### 1. Pull the studio package. Do not write a second client.

`./studio library pull <p> billing`. It gives a `BillingProvider` with `createCheckout(planId, email, userId)` and `handleWebhook(rawBody, signature)` for `stripe` and `lemon-squeezy`. Adapt it in the project. When you add a generic fix, promote it with `./studio library promote <p> packages/billing --ticket <ID>`. Do not pull `feature-gating`; entitlements are built in the project (rule 5).

### 2. Hosted checkout only. No card data on our servers.

Use Stripe Checkout or the Lemon Squeezy checkout URL. Card fields never render in our DOM, so the product stays in PCI DSS SAQ A. Stripe Elements needs an ADR. A form that posts card numbers to our server is refused.

### 3. The client never sends a price

The browser sends a plan key (`pro-monthly`). The server maps it to the provider price or variant ID from config. Amounts are integers in minor units with an ISO 4217 code (`1900`, `EUR`). No floats. Display price and charged price come from the same server function. Pass the Payload user ID into the checkout so the webhook can link it: Stripe `client_reference_id` and `metadata[user_id]`, Lemon Squeezy `checkout_data.custom.user_id`. The package sets these when you pass `userId`; always pass it.

### 4. Webhooks: verify the raw body, store, then acknowledge

- Route: a Payload root endpoint or a Next route handler. Read `await req.text()` before any JSON parse. Parsed-then-restringified JSON fails the signature.
- Verify with `provider.handleWebhook(raw, signature)`. Stripe header `stripe-signature`; Lemon Squeezy header `X-Signature`. Bad or missing signature returns `400` and changes nothing.
- Stripe: the package rejects a `t=` timestamp more than 300 seconds off (the Stripe SDK default tolerance) and accepts any `v1` value, so secret rotation works. Keep both if you adapt it.
- Insert the verified event into a `billing-events` collection: `eventId` (unique index), `provider`, `type`, `payload` (json), `status` (`pending` | `done` | `failed`), `attempts`. `eventId` is the provider event ID (`evt_…`) or a SHA-256 of the raw body when the provider sends none.
- Return `200` after the insert commits. A duplicate `eventId` also returns `200`. A storage failure returns `503` so the provider retries.
- Process in a Payload job (BE-006). Mark `done` only after the side effects commit. Failed jobs retry with backoff and end in `failed` for inspection.
- Never fulfil on the success redirect. The redirect only shows "processing" until the webhook lands.

### 5. Subscription state is a Payload collection

`subscriptions`: `user` (relationship), `provider`, `providerCustomerId`, `providerSubscriptionId` (unique), `plan`, `status`, `currentPeriodEnd`, `cancelAtPeriodEnd`, `lastEventAt`. Access: `read` is admin or owner; `create`, `update`, `delete` are `false` for every user. Only the webhook job writes, through the Local API with `overrideAccess: true` and no `user`.

| From | Event | To | The system must |
|---|---|---|---|
| none | checkout completed | `trialing` or `active` | Create the row, grant entitlements |
| `trialing` | trial ends, payment ok | `active` | Keep access |
| `active` | renewal payment fails | `past_due` | Keep access for the grace window in config, send the dunning mail |
| `past_due` | payment recovers | `active` | Restore silently |
| `past_due` | retries exhausted | `canceled` | Revoke entitlements, keep data |
| `active` | user cancels | `active` + `cancelAtPeriodEnd` | Access until `currentPeriodEnd`, then `canceled` |
| any | plan change | same status, new `plan` | Provider prorates; we only mirror |

Out-of-order events: ignore an event older than `lastEventAt`, or re-fetch the subscription from the provider and write its current state. Entitlement checks read `status` and `plan` only, in one server helper.

### 6. Refunds, disputes and dunning

- Refunds go through the provider API with an idempotency key derived from the business operation (`refund-<orderId>-<n>`), never a random UUID per call. Partial refunds are normal.
- Orders, payments and refunds are never deleted. They change status.
- Dunning uses the provider's retry schedule (Stripe Smart Retries, Lemon Squeezy dunning). We send the "update your card" mail with a link to the provider's customer portal.
- A dispute event freezes the order and notifies the admin. Dispute deadlines are the provider's; show the date in admin.

### 7. Reconcile, do not assume

A scheduled Payload job compares the provider's active subscriptions with the `subscriptions` rows (ID, status, plan). Any drift is logged as an error with both values and alerts the admin. Ship the job with the first billing ticket, not later.

### 8. Tax and German price law

- Pick the tax model at gate 1. **Lemon Squeezy** is the merchant of record: it charges VAT, issues the invoice and files OSS. **Stripe** makes us the seller: we charge VAT (Stripe Tax or our own table), issue §14 UStG invoices (BE-009) and file OSS.
- With Stripe: B2C digital services to other EU states are taxed where the customer lives (§3a Abs. 5 UStG), declared through OSS (§18j UStG). B2B in another EU state with a valid USt-IdNr. (checked against VIES) is reverse charge (§13b UStG); the invoice says "Steuerschuldnerschaft des Leistungsempfängers". Kleinunternehmer (§19 UStG) charge no VAT and say so on the invoice.
- B2C prices are shown as the total including VAT (§3 PAngV). Subscriptions show the price per period and the term. A struck-through "was" price must be the lowest price of the last 30 days (§11 PAngV).
- The order button reads "zahlungspflichtig bestellen" or an equally clear phrase (§312j Abs. 3 BGB). Consumer subscriptions sold online need a cancellation button ("Verträge hier kündigen", §312k BGB). AGB and withdrawal text are CL-003.

### 9. Test mode and live mode never cross

Local `.env` and Compose use test keys. Coolify holds live keys. The app logs `billing mode: test` or `live` at boot from the key prefix, never the key. Env names: `STRIPE_SECRET_KEY`, `STRIPE_WEBHOOK_SECRET`, `STRIPE_SUCCESS_URL`, `STRIPE_CANCEL_URL`, `LEMONSQUEEZY_API_KEY`, `LEMONSQUEEZY_STORE_ID`, `LEMONSQUEEZY_WEBHOOK_SECRET`. Add them to `env.schema.json`; inject with `./studio env <p> … --approve`.

### 10. Shop rules (only when there is a cart)

- Stock goes down when payment succeeds, not at add-to-cart, with one atomic update (`UPDATE … SET stock = stock - 1 WHERE id = $1 AND stock > 0`). Zero rows updated means sold out.
- Coupon stacking is written down and tested with sale price plus VAT.
- Cart, checkout and account pages are never cached by the CDN or Next (`dynamic = 'force-dynamic'` or `no-store`).

## Workflow

1. Map the money: who pays, one-time or recurring, currencies, B2C or B2B, refund policy, tax model. Write it in the architecture doc.
2. Pull `billing`. Add plan config (keys to provider IDs) on the server.
3. Build `billing-events` and `subscriptions` with access rules, then the webhook route, then the job. UI comes last.
4. Wire entitlements through one helper. Wire the pricing page numbers to the same plan config.
5. Test the failure catalog in test mode (Done evidence). Add the reconciliation job.
6. Promote package fixes. Update `docs/library-usage.json`.

## Deliverables

- `billing-events` and `subscriptions` collections with named access
- Webhook route and processing job, idempotent by `eventId`
- Server plan config and one entitlement helper
- Reconciliation job with an alert
- Architecture doc section "Billing": provider, tax model, state table, grace window, env names

## Done evidence (receipt)

`## Billing proof` with results PASS / FAIL / NOT TESTED:

- Test-mode checkout completes; the `subscriptions` row appears with the right `plan` and `status`
- The same event delivered twice: one `billing-events` row, one state change (Stripe: `stripe events resend <evt_id>`)
- Bad signature: `400`, no row written
- Decline card `4000 0000 0000 0002` and 3DS card `4000 0027 6000 3184` (Stripe test cards), or the Lemon Squeezy test-mode equivalent
- Refund in test mode; the order shows `refunded`, nothing deleted
- Pricing page shows gross prices and the period; the order button text is quoted
- Boot log line shows `billing mode: test`

Stripe local forwarding: `stripe listen --forward-to localhost:3000/<webhook path>` and `stripe trigger <event>`.

## Anti-patterns

- Fulfilling or granting access on the success redirect
- Amount or price ID taken from the request body
- JSON-parsing the body before signature verification
- Marking an event `done` in a `finally` block
- Deleting an order, payment or subscription row to "fix" it
- A second subscription table outside Payload, or `plan` stored on the user record as the source of truth
- Live keys in local `.env`, test keys in Coolify
- Net prices on a B2C pricing page

## Handoff

- **Consumes:** architecture doc tax model, plan list from the PRD, GD-002 pricing-page spec.
- **Produces:** entitlement helper for FE tickets; invoice data for BE-009 (Stripe model only); webhook boundary for PE-005; env names for PE-006.

## References

- `studio-library/packages/billing/` (README, `types.ts`, `providers/`)
- `knowledge-base/payload-playbook.md`, `knowledge-base/backend_playbook.md`
- BE-006 jobs, BE-007 Payload, BE-009 document generation, CL-003 Impressum/AGB, GD-002 commercial surfaces
- Stripe docs: webhooks, testing; Lemon Squeezy docs: webhooks, test mode
- UStG §§3a, 13b, 14, 18j, 19; PAngV §§3, 11; BGB §§312j, 312k
