# Skill: API Design

> RESTful APIs, OpenAPI specification, versioning, rate limiting, pagination

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

For errors:
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Email is invalid",
    "details": [
      { "field": "email", "message": "Must be a valid email address" }
    ]
  }
}
```

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
  - Old versions supported for at least 6 months
  - Breaking changes only in a new version
  - Deprecation header on old endpoints
  - Changelog for API changes
```

### 6. Rate limiting

```markdown
Headers:
  X-RateLimit-Limit: 100
  X-RateLimit-Remaining: 95
  X-RateLimit-Reset: 1640995200

On limit:
  429 Too Many Requests
  Retry-After: 60

Limits:
  - Auth endpoints: 10/min
  - Standard endpoints: 100/min
  - Read-heavy: 1000/min
```

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

## References

- `.quinsy-studio/process/adr-policy.md` — ADR for API decisions
- `.quinsy-studio/knowledge-base/backend_playbook.md` — backend rules
- `studio-library/packages/` — reusable packages
