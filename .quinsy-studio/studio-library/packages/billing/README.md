# Billing Package

> Subscription, metering, and payment processing for SaaS applications.

## Features

- Checkout sessions (Stripe, Lemon Squeezy), linked to the Payload user
- Webhook signature verification (Stripe: timestamp tolerance, key rotation)
- Plan, subscription, entitlement and metering models are project code in Payload (BE-008); invoices are BE-009

## Architecture

```
┌─────────────────────────────────────────────────────────┐
│                   BILLING FLOW                          │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  1. Subscription                                        │
│     └─▶ User selects plan                              │
│     └─▶ Checkout session created                       │
│     └─▶ Payment processed                              │
│     └─▶ Subscription activated                         │
│                                                         │
│  2. Metering                                            │
│     └─▶ Track usage (API calls, storage, etc.)         │
│     └─▶ Aggregate metrics                              │
│     └─▶ Apply to subscription                          │
│                                                         │
│  3. Billing Cycle                                       │
│     └─▶ Generate invoice                               │
│     └─▶ Process payment                                │
│     └─▶ Send receipt                                   │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

## Configuration

```typescript
// billing.config.ts
export const billingConfig = {
  provider: 'stripe', // or 'lemon-squeezy'
  plans: {
    free: {
      name: 'Free',
      price: 0,
      features: ['basic-features'],
    },
    pro: {
      name: 'Pro',
      price: 1900, // cents
      interval: 'month',
      features: ['basic-features', 'advanced-features'],
    },
    enterprise: {
      name: 'Enterprise',
      price: 9900,
      interval: 'month',
      features: ['basic-features', 'advanced-features', 'enterprise-features'],
    },
  },
  metering: {
    enabled: true,
    metrics: ['api_calls', 'storage_gb', 'seats'],
  },
};
```

## What the package ships

The package is two providers behind one interface (`types.ts`). Subscription state, entitlements and metering live in the project as Payload collections (skill BE-008); the package does not store anything.

```typescript
import { stripeProvider } from './providers/stripe'

// Server action or route handler; userId is the Payload user id
const session = await stripeProvider.createCheckout(priceId, user.email, String(user.id))
redirect(session.url)
```

`userId` is sent as `client_reference_id` and `metadata.user_id` (Stripe) or `checkout_data.custom.user_id` (Lemon Squeezy), so the webhook can find the subscriber.

## Webhooks

Pass the **raw** request body; parsed JSON breaks the signature.

```typescript
// app/(payload)/api/webhooks/stripe/route.ts
export async function POST(req: Request) {
  const raw = await req.text()
  await stripeProvider.handleWebhook(raw, req.headers.get('stripe-signature') ?? '')
  const event = JSON.parse(raw)
  // Idempotency: store event.id in a Payload collection; skip if already processed.
  // Update the subscription collection from event.type, never from client input.
  return Response.json({ received: true })
}
```

`handleWebhook` throws on a bad signature. Stripe signatures older than 5 minutes are refused (replay protection), and every `v1` value is checked so secret rotation keeps working.
