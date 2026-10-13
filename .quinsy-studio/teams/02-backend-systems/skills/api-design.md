# Skill: API Design

> RESTful APIs, OpenAPI specification, versioning, rate limiting, pagination

**Playbook:** [backend_playbook.md](../../../knowledge-base/backend_playbook.md) (API spine). Do not rewrite this file wholesale — `./studio infusion-delta`.

## Metadata

```
skill_id: BE-001
name: API Design
team: 02-backend-systems
lead_role: Backend Architect
support_roles: [Senior Fullstack Architect, Backend Engineer]
phases: [2, 3, 4]
activation_triggers:
  - Ticket contains "API", "endpoint", "REST", "GraphQL"
  - Phase 2: API contracts are defined
  - Phase 4: API implementation
  - New backend feature that needs an endpoint
```

---

## Behavior rules

### 0. Payload first

Payload already serves REST at `/api/<collection>` and the Local API on the server. Use them for CRUD; the collection `access` rules are the authorization. Write a custom endpoint (Payload `endpoints` or a Next route handler) only for operations that are not CRUD on one collection: webhooks, checkout, exports, multi-step actions. Rules 1–7 apply to custom endpoints. Payload's built-in routes keep Payload's own error format (`{ "errors": [{ "message": … }] }`); do not wrap them.

### 1. RESTful resources

```markdown
Naming:
  - Nouns (not verbs): /users, /orders, /products
  - Plural: /user → /users
  - Nested: /users/:id/orders
  - No file extensions: /users (not /users.json)

HTTP methods:
  GET    /users          → retrieve list
  GET    /users/:id      → retrieve single element
  POST   /users          → create
  PUT    /users/:id      → full update
  PATCH  /users/:id      → partial update
  DELETE /users/:id      → delete

Sub-resources:
  GET /users/:id/orders → orders of a user
  POST /orders/:id/items → add item to an order
```

### 2. Response format

```markdown
Standard response:
{
  "data": { ... },           // single object
  "meta": {
    "page": 1,
    "per_page": 20,
    "total": 150,
    "total_pages": 8
  }
}

For lists:
{
  "data": [ ... ],
  "meta": { ... }
}

For errors — the one studio error shape (same as BE-004):
{
  "code": "VALIDATION_ERROR",
  "message": "Email is invalid",
  "details": [
    { "field": "email", "code": "INVALID_FORMAT", "message": "Must be a valid email address" }
  ],
  "request_id": "req_7f3a9c"
}
```

- `code`: stable UPPER_SNAKE string from the BE-004 list. Clients branch on it, never on `message`.
- `message`: one sentence for a developer. The UI shows its own catalog text for `code` (FE-008), not this string.
- `details`: array, empty when there is nothing to add. Field errors use `field`.
- `request_id`: also sent as the `X-Request-Id` response header and written to every log line.
- The HTTP status carries the class; the body never says `200` with an error inside.

### 3. Status codes

```markdown
2xx success:
  200 OK                  → standard success
  201 Created             → resource created
  204 No Content          → success without response body (e.g. DELETE)
  202 Accepted            → async operation started

3xx redirect:
  301 Moved Permanently    → URL changed
  304 Not Modified        → cache valid

4xx client errors:
  400 Bad Request         → invalid input data
  401 Unauthorized        → not authenticated
  403 Forbidden           → no permission
  404 Not Found           → resource not found
  409 Conflict            → conflict (e.g. duplicate)
  422 Unprocessable       → validation error
  429 Too Many Requests   → rate limit

5xx server errors:
  500 Internal Error      → unexpected error
  502 Bad Gateway         → upstream problem
  503 Service Unavailable → maintenance mode
```

### 4. Pagination

```markdown
Offset-based:
  GET /users?page=3&per_page=20

Cursor-based (for large datasets):
  GET /users?cursor=abc123&limit=20

Response with pagination meta:
{
  "data": [...],
  "meta": {
    "page": 3,
    "per_page": 20,
    "total": 150,
    "has_next": true,
    "has_prev": true
  }
}
```

### 5. Versioning

```markdown
Strategy: URL-based
  /api/v1/users
  /api/v2/users

Rules:
  - Version only endpoints that outside clients call (extension, mobile, partner).
    Same-origin routes used only by our Next app change together with the app.
  - Breaking changes only in a new version (see compatibility table)
  - Old version kept for the window named in the architecture doc
  - `Deprecation` (RFC 9745) and `Sunset` (RFC 8594) headers on old endpoints
  - Changelog for API changes
```

### 5a. Compatibility table

| Safe within a version | Breaking: needs a new version |
|---|---|
| Add an endpoint | Remove or rename an endpoint or field |
| Add an optional response field | Change a field's type, format or unit |
| Add an optional request parameter | Make an optional parameter required |
| Add an error `code` inside the same shape | Change the error shape or a status code's meaning |
| Add an enum value, if clients are documented to ignore unknown values | Remove an enum value or change a default |
| Relax a validation rule | Tighten a validation rule |
| Add a Payload field with `access.read` limited to admin | Expose or hide a field by changing `access.read` on a public collection |

A Payload collection that a client reads over REST is a public contract too: renaming a field is breaking.

### 6. Rate limiting

```markdown
Headers:
  X-RateLimit-Limit: 100
  X-RateLimit-Remaining: 95
  X-RateLimit-Reset: 1640995200

On limit:
  429 Too Many Requests
  Retry-After: <seconds>
  body: { "code": "RATE_LIMITED", "message": "…", "details": [], "request_id": "…" }

Limits:
  - Set per endpoint class in the architecture doc (auth, write, read)
  - Auth: Payload `maxLoginAttempts` / `lockTime` per account (BE-003),
    plus a per-IP limit at the proxy or route
  - Webhooks are not rate-limited by us; they are verified (BE-008)
```

### 7. Idempotent writes

Creates that a client may retry (checkout, order, send) accept an `Idempotency-Key` header. Store key plus response for the retry window; a repeat returns the stored response. Derive server-side keys from the business operation (`order-<id>-attempt-<n>`), not a random value per call.

---

## Anti-patterns

### ❌ Forbidden

```markdown
- Verbs in URLs: /getUser, /createOrder
- POST /delete-user/123
- Status 200 on errors
- No error handling
- HTTP 500 with internal stack trace
- No pagination for lists
- GET /users with POST for filtering
```

### ✅ Instead

```markdown
- Resource-based URLs
- Correct HTTP methods
- Correct status codes
- Structured error responses
- Generic error messages (no stack trace)
- Always pagination for lists
- Query parameters for filters
```

---

## Done evidence (receipt)

`## API proof` on every BE-001 ticket, PASS / FAIL / NOT TESTED per line:

- One request and response sample per new or changed endpoint (method, path, status, body trimmed), from a real call (`curl` or test log), not hand-written
- **Authz negative case:** the same call as a user without access, or anonymous, returns `401` / `403` (or a filtered empty list for Payload `read`). Name the user and the status
- One error sample in the studio error shape, with `request_id`
- Compatibility: "additive only" or the new version and its `Sunset` date
- For Payload collections: the `access` function names per operation

---

## Toolbox (trained — LO-0146)

### Operator idea queues

- When operators must feed a writer or synthesis loop, the idea queue is a **product admin resource**, not IDE chat.
- Markdown briefing files may seed a first corpus; they are not the ongoing operator inbox. Ticket the admin surface; do not invent topics from chat mid-sprint.

---

## References

- `.quinsy-studio/process/adr-policy.md` — ADR for API decisions
- `.quinsy-studio/knowledge-base/backend_playbook.md` — backend rules
- `.quinsy-studio/knowledge-base/payload-playbook.md` — Payload REST and Local API
- BE-004 error handling (error codes, timeouts), BE-003 auth, BE-008 webhooks
- `studio-library/packages/` — reusable packages

## Deltas

- **PB-20260925-001** helpful=0 harmful=0 :: HQ skill-catalog work is a separate queue from product sprint notes. Do not enqueue HQ LOs on the product sprint inbox. Product execute INFORM the open HQ LO count; the HQ session consumes those jobs.
