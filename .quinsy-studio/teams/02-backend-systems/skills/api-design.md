# Skill: API Design

> RESTful APIs, OpenAPI-Spezifikation, Versionierung, Rate-Limiting, Pagination

## Metadata

```
skill_id: BE-001
name: API Design
team: 02-backend-systems
lead_role: Backend Architect
support_roles: [Senior Fullstack Architect, Backend Engineer]
phases: [2, 3, 4]
activation_triggers:
  - Ticket enthält "API", "Endpoint", "REST", "GraphQL"
  - Phase 2: API-Kontrakte werden definiert
  - Phase 4: API-Implementierung
  - Neues Backend-Feature das einen Endpoint braucht
```

---

## Verhaltensregeln

### 1. RESTful Ressourcen

```markdown
Naming:
  - Nomen (nicht Verben): /users, /orders, /products
  - Plural: /user → /users
  - Verschachtelt: /users/:id/orders
  - Keine Datei-Endungen: /users (nicht /users.json)

HTTP-Methods:
  GET    /users          → Liste abrufen
  GET    /users/:id      → Einzelnes Element
  POST   /users          → Erstellen
  PUT    /users/:id      → Vollständig aktualisieren
  PATCH  /users/:id      → Teilaktualisierung
  DELETE /users/:id      → Löschen

Sub-Ressourcen:
  GET /users/:id/orders → Bestellungen eines Users
  POST /orders/:id/items → Item zu Bestellung hinzufügen
```

### 2. Response-Format

```markdown
Standard-Response:
{
  "data": { ... },           // Einzelnes Objekt
  "meta": {
    "page": 1,
    "per_page": 20,
    "total": 150,
    "total_pages": 8
  }
}

Für Listen:
{
  "data": [ ... ],
  "meta": { ... }
}

Für Fehler:
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Email ist ungültig",
    "details": [
      { "field": "email", "message": "Muss eine gültige E-Mail-Adresse sein" }
    ]
  }
}
```

### 3. Status-Codes

```markdown
2xx Erfolg:
  200 OK                  → Standard-Erfolg
  201 Created             → Resource erstellt
  204 No Content          → Erfolg ohne Response-Body (z.B. DELETE)
  202 Accepted            → Async-Operation gestartet

3xx Redirect:
  301 Moved Permanently    → URL geändert
  304 Not Modified        → Cache gültig

4xx Client-Fehler:
  400 Bad Request         → Ungültige Input-Daten
  401 Unauthorized        → Nicht authentifiziert
  403 Forbidden           → Keine Berechtigung
  404 Not Found           → Resource nicht gefunden
  409 Conflict            → Konflikt (z.B. Duplicate)
  422 Unprocessable       → Validierungsfehler
  429 Too Many Requests   → Rate Limit

5xx Server-Fehler:
  500 Internal Error      → Unerwarteter Fehler
  502 Bad Gateway         → Upstream-Problem
  503 Service Unavailable → Wartungsmodus
```

### 4. Pagination

```markdown
Offset-basiert:
  GET /users?page=3&per_page=20

Cursor-basiert (für große Datensätze):
  GET /users?cursor=abc123&limit=20

Response mit Pagination-Meta:
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

### 5. Versionierung

```markdown
Strategie: URL-basiert
  /api/v1/users
  /api/v2/users

Regeln:
  - Alte Versionen mindestens 6 Monate supported
  - Breaking Changes nur in neuer Version
  - Deprecation-Header bei alten Endpoints
  - Changelog für API-Änderungen
```

### 6. Rate-Limiting

```markdown
Headers:
  X-RateLimit-Limit: 100
  X-RateLimit-Remaining: 95
  X-RateLimit-Reset: 1640995200

Bei Limit:
  429 Too Many Requests
  Retry-After: 60

Limits:
  - Auth-Endpoints: 10/min
  - Standard-Endpoints: 100/min
  - Read-Heavy: 1000/min
```

---

## Anti-Patterns

### ❌ Verboten

```markdown
- Verben in URLs: /getUser, /createOrder
- POST /delete-user/123
- Status 200 bei Fehlern
- Kein Error-Handling
- HTTP 500 mit internem Stack-Trace
- Keine Pagination bei Listen
- GET /users mit POST zum Filtern
```

### ✅ Stattdessen

```markdown
- Ressourcen-basierte URLs
- Korrekte HTTP-Methods
- Korrekte Status-Codes
- Strukturierte Error-Responses
- Generic Error-Messages (kein Stack-Trace)
- Immer Pagination bei Listen
- Query-Parameter für Filter
```

---

## Referenzen

- `.quinsy-studio/process/adr-policy.md` — ADR für API-Entscheidungen
- `.quinsy-studio/knowledge-base/backend_playbook.md` — Backend-Regeln
- `studio-library/packages/` — Wiederverwendbare Packages
