# Billing Package

> Subscription, metering, and payment processing for SaaS applications.

## Features

- Subscription management (Free/Pro/Enterprise)
- Metering and usage-based pricing
- Payment processing (Stripe, Lemon Squeezy)
- Invoice generation
- Webhook handling
- Entitlement management

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

## Usage

```typescript
import { billing, subscription, metering } from '@studio/billing';

// Check subscription
const sub = await subscription.get(userId);
if (sub.plan === 'pro') {
  // Allow pro features
}

// Track usage
await metering.track(userId, 'api_calls', 1);

// Get usage
const usage = await metering.getUsage(userId, 'api_calls');
```

## Webhooks

```typescript
// Handle Stripe webhooks
app.post('/webhooks/stripe', async (req, res) => {
  const event = stripe.webhooks.constructEvent(
    req.body,
    req.headers['stripe-signature'],
    process.env.STRIPE_WEBHOOK_SECRET
  );

  switch (event.type) {
    case 'customer.subscription.created':
      await billing.handleSubscriptionCreated(event.data.object);
      break;
    case 'invoice.payment_succeeded':
      await billing.handlePaymentSucceeded(event.data.object);
      break;
  }

  res.json({ received: true });
});
```
