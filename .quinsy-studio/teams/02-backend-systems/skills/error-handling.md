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

```markdown
Standardized error response:
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Invalid input",
    "details": [
      { "field": "email", "code": "INVALID_FORMAT", "message": "Not a valid email" }
    ],
    "request_id": "req-abc-123",
    "timestamp": "2026-08-20T10:30:00Z"
  }
}

Error codes (consistent):
  VALIDATION_ERROR      → 422
  AUTH_REQUIRED         → 401
  FORBIDDEN             → 403
  NOT_FOUND             → 404
  CONFLICT              → 409
  RATE_LIMITED          → 429
  INTERNAL_ERROR        → 500
  SERVICE_UNAVAILABLE   → 503
```

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
```

### 4. Circuit breaker

```markdown
For external services:

States:
  CLOSED     → normal operation, all requests pass through
  OPEN       → error limit reached, all requests are rejected
  HALF-OPEN  → a test request is let through

Thresholds:
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
```

### ✅ Instead

```markdown
- Specific error handling per error type
- Generic user messages (no stack trace)
- Structured logging with context
- Exponential backoff with jitter
- Circuit breaker for all external services
- Error messages with request_id for tracing
```

---

## Toolbox (trained — LO-0146)

### Missing operator queue

- If the product has no admin idea queue, do not silently take a chat paste as the system of record. Fail closed: ticket the queue, keep markdown as a briefing seed only.

---

## References

- `.quinsy-studio/knowledge-base/backend_playbook.md` — backend rules
- `.quinsy-studio/process/gates.md` — error handling in the QA gate
