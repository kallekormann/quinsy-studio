# Skill: Error Handling

> Error handling, logging, retry with backoff, circuit breaker

**Playbook:** [backend_playbook.md](../../../knowledge-base/backend_playbook.md) (Errors).

## Metadata

```
skill_id: BE-004
name: Error Handling & Resilience
team: 02-backend-systems
lead_role: Backend Architect
support_roles: [Backend Engineer, Platform Architect]
phases: [3, 4, 5]
activation_triggers:
  - Ticket contains "error", "exception", "retry"
  - Phase 3: error-handling strategy is defined
  - Phase 4: error handling is implemented
  - Phase 5: QA checks error handling
```

---

## Behavior rules

### 1. Error response format

One shape for every custom endpoint and route handler. BE-001 uses the same shape. Payload's built-in REST routes keep Payload's own format.

```markdown
Error response body:
{
  "code": "VALIDATION_ERROR",
  "message": "Invalid input",
  "details": [
    { "field": "email", "code": "INVALID_FORMAT", "message": "Not a valid email" }
  ],
  "request_id": "req_7f3a9c"
}

  code        stable UPPER_SNAKE, from the list below; clients branch on it
  message     one sentence for a developer; never a stack trace or SQL
  details     array, may be empty
  request_id  same value in the X-Request-Id header and every log line
  (no timestamp in the body; the log line has it)

Error codes (consistent):
  VALIDATION_ERROR      → 422
  AUTH_REQUIRED         → 401
  FORBIDDEN             → 403
  NOT_FOUND             → 404
  CONFLICT              → 409
  RATE_LIMITED          → 429
  INTERNAL_ERROR        → 500
  UPSTREAM_ERROR        → 502
  SERVICE_UNAVAILABLE   → 503
  UPSTREAM_TIMEOUT      → 504
```

Build it in one helper (`apiError(code, message, details?)`) that reads the request ID from `x-request-id` or creates one. No route builds error JSON by hand.

### 1a. User-facing error messages

The UI never shows `message` from the API. It maps `code` to a catalog string (FE-008). Each string answers three questions:

| Part | Question | Example |
|---|---|---|
| What happened | What failed, in the user's words | "Your payment did not go through." |
| Why | The cause, if known and safe to say | "The bank declined the card." |
| What next | One action the user can take | "Try another card or contact your bank." |

- No blame ("You entered…"), no jargon, no error codes in the main text. Show `request_id` in small print on unexpected errors so support can find the log.
- Validation errors sit next to the field, not only in a toast.
- Login and reset errors never reveal whether an account exists (BE-003).

### 2. Logging

```markdown
Log levels:
  ERROR   → system errors, needs attention
  WARN    → unexpected but not critical
  INFO    → important operations
  DEBUG   → detailed info (dev only)

Log format:
{
  "level": "error",
  "message": "Payment failed",
  "context": { "user_id": "uuid", "order_id": "uuid" },
  "error": { "name": "PaymentError", "message": "...", "stack": "..." },
  "request_id": "req-abc-123",
  "timestamp": "2026-08-20T10:30:00Z"
}

What to log:
  - All error levels on all channels
  - Auth events (login, logout, failed)
  - Database operations (on errors)
  - External API calls (response time, errors)
  - Security events (CSRF, rate limit)

What NOT to log:
  - Passwords, tokens, secrets
  - Full user inputs (GDPR!)
  - Unnecessary debug info in production
```

### 3. Retry with backoff

```markdown
Strategy: exponential backoff + jitter

Base delay: 1s
Max retries: 3
Backoff: base * 2^attempt + random_jitter

Attempt 1: ~1s
Attempt 2: ~2-3s
Attempt 3: ~4-8s

When to retry:
  - 5xx server errors
  - Network timeout
  - Rate limit (with Retry-After header)

No retry for:
  - 4xx client errors (except 429)
  - Auth errors
  - Validation errors
  - Non-idempotent writes without an idempotency key
```

### 3a. Timeout and retry budgets

```markdown
Every outbound call has an explicit timeout:
  fetch(url, { signal: AbortSignal.timeout(ms) })
  No call relies on a library or OS default.

Budget per request:
  - The architecture doc names each dependency's timeout and retry count.
  - Sum of (attempts × timeout) + backoff must fit inside the caller's own timeout,
    with room to answer. If it does not fit, retry less or move the work to a job (BE-006).
  - Retry at one layer only. A retrying client over a retrying SDK over a retrying
    proxy multiplies load on a failing service.
  - Honor Retry-After on 429 and 503; it overrides the backoff formula.
  - When the budget runs out, return UPSTREAM_TIMEOUT (504) or UPSTREAM_ERROR (502),
    not INTERNAL_ERROR.

Background jobs:
  - Bounded attempts, then dead-letter (failed status you can inspect).
  - Each attempt has its own timeout; a stuck attempt does not hold the queue.
```

### 4. Circuit breaker

```markdown
For external services:

States:
  CLOSED     → normal operation, all requests pass through
  OPEN       → error limit reached, all requests are rejected
  HALF-OPEN  → a test request is let through

Thresholds (starting values; set per dependency in the architecture doc):
  - Error limit: 5 failed requests
  - Timeout: 30 seconds
  - Successes for HALF-OPEN → CLOSED: 3

Function:
  1. After 5 consecutive errors → OPEN
  2. After 30s → HALF-OPEN
  3. Test request → success: CLOSED / error: OPEN
```

### 5. Graceful degradation

```markdown
When a service fails:
  1. Disable the feature (don't crash)
  2. Show fallback data (if possible)
  3. Inform the user (clear message)
  4. Alert monitoring
  5. Try automatic recovery

Examples:
  - Payment service down → "Payment currently unavailable"
  - Search service down → fallback to DB query
  - Analytics service down → buffer events
```

---

## Anti-patterns

### ❌ Forbidden

```markdown
- catch {} (silent error)
- Error messages that show internal details
- No logging on errors
- Infinite retry without backoff
- No circuit breaker for external services
- Exception propagation without context
- Outbound fetch without a timeout
- Retries at several layers for the same call
- A second error shape (e.g. `{ "error": { … } }`) next to the studio shape
- Showing the API `message` to end users
```

### ✅ Instead

```markdown
- Specific error handling per error type
- Generic user messages (no stack trace)
- Structured logging with context
- Exponential backoff with jitter
- Circuit breaker for all external services
- Error messages with request_id for tracing
- One `apiError` helper; UI copy from the catalog by `code`
```

## Done evidence (receipt)

On tickets that add an outbound call or a user-facing error path, the receipt lists:

- Each new dependency with its timeout and retry count
- One error response sample in the studio shape (or point to `## API proof`)
- The catalog key and text for each new user-facing error, checked against the three-part rubric

---

## Toolbox (trained — LO-0146)

### Missing operator queue

- If the product has no admin idea queue, do not silently take a chat paste as the system of record. Fail closed: ticket the queue, keep markdown as a briefing seed only.

---

## References

- `.quinsy-studio/knowledge-base/backend_playbook.md` — backend rules
- `.quinsy-studio/process/gates.md` — error handling in the QA gate
- BE-001 API design (same error shape), BE-006 jobs (dead-letter), FE-008 catalogs

## Deltas

- **PB-20260925-001** helpful=0 harmful=0 :: Open HQ LOs are not a product execute failure. INFORM the count and keep IMPLEMENT. Infuse in a HQ session. STUDIO_LO only when the product loop is idle. Do not steal an in-flight product chat.
