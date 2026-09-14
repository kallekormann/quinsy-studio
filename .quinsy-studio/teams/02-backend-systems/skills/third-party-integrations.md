# Skill: Third-Party Integrations

> API integration, webhooks, queues, payment, email, analytics

**Playbook:** [backend_playbook.md](../../../knowledge-base/backend_playbook.md) (Integrations).

## Metadata

```
skill_id: BE-005
name: Third-Party Integrations
team: 02-backend-systems
lead_role: Backend Architect
support_roles: [Backend Engineer, Data Engineer]
phases: [3, 4, 5]
activation_triggers:
  - Ticket contains "integration", "API", "webhook", "Stripe", "SendGrid"
  - Phase 3: external services are planned
  - Phase 4: integrations are implemented
  - Payment, email, analytics features
```

---

## Behavior rules

### 1. Integration checklist

```markdown
Before every integration:
  [ ] read the API documentation
  [ ] note the rate limits
  [ ] understand the auth method
  [ ] document the error codes
  [ ] understand the webhook events
  [ ] define the fallback strategy
  [ ] set up monitoring
  [ ] secrets in environment variables
```

### 2. Payment (Stripe)

```markdown
Architecture:
  - Frontend: Stripe.js / Stripe Elements (PCI compliant)
  - Backend: Stripe SDK for server side
  - Webhooks for payment events

Events we handle:
  payment_intent.succeeded   → confirm the order
  payment_intent.failed      → inform the user
  subscription.created       → activate access
  subscription.deleted       → deactivate access
  invoice.payment_failed     → payment reminder

Security:
  - Verify the webhook signature
  - Idempotency keys for mappings
  - No secrets in the frontend
```

### 3. Email (SendGrid/Resend)

```markdown
Architecture:
  - Transactional emails: server side
  - Marketing: third-party (don't build it yourself)

Templates:
  - Welcome
  - Password reset
  - Email verification
  - Payment confirmation
  - Newsletter

Rules:
  - Always track with the user ID
  - Unsubscribe link always included
  - Configure SPF/DKIM/DMARC
```

### 4. Webhooks

```markdown
Incoming webhooks:
  - Signature verification (always!)
  - Idempotency check (event ID)
  - Queue for processing
  - Retry with backoff
  - Logging of all events

Outgoing webhooks:
  - User can configure the URL
  - Signature with secret
  - Retry on 5xx/timeout
  - Event history for debugging
```

### 5. Queue system

```markdown
When to use queues:
  - Long-running operations (>5s)
  - Email sending
  - PDF generation
  - Bulk operations
  - Webhook processing

Implementation:
  - Redis/RabbitMQ/Inngest
  - Dead-letter queue for failed jobs
  - Retry with backoff
  - Job monitoring
```

### 6. Fallback strategies

```markdown
When a service fails:
  1. Try an alternative (e.g. another payment provider)
  2. Disable the feature gracefully
  3. Inform the user clearly
  4. Buffer all requests
  5. Alert monitoring

Example:
  Stripe down → "Payment currently unavailable. Please try later."
  SendGrid down → email queue → will be sent as soon as the service is back
```

---

## Anti-patterns

### ❌ Forbidden

```markdown
- Secrets in code/repository
- No webhook signature verification
- Synchronous API call in the request handler (>5s)
- No retry/backoff
- No fallback on service failure
- API tokens in URLs
```

### ✅ Instead

```markdown
- Secrets in environment variables
- Always signature verification
- Asynchronous via queue
- Exponential backoff with max retries
- Graceful degradation + user message
- Tokens in headers
```

---

## References

- `.quinsy-studio/knowledge-base/backend_playbook.md` — backend rules
- `studio-library/packages/billing/` — billing package
- `studio-library/packages/feature-gating/` — feature gating
