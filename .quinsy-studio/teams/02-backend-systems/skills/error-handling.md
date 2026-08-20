# Skill: Error Handling

> Fehlerbehandlung, Logging, Retry mit Backoff, Circuit Breaker

## Metadata

```
skill_id: BE-004
name: Error Handling & Resilience
team: 02-backend-systems
lead_role: Backend Architect
support_roles: [Backend Engineer, Platform Architect]
phases: [3, 4, 5]
activation_triggers:
  - Ticket enthält "Error", "Exception", "Fehlerbehandlung", "Retry"
  - Phase 3: Error-Handling-Strategie wird definiert
  - Phase 4: Error-Handling wird implementiert
  - Phase 5: QA prüft Error-Handling
```

---

## Verhaltensregeln

### 1. Error-Response-Format

```markdown
Standardisierte Error-Response:
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Ungültige Eingabe",
    "details": [
      { "field": "email", "code": "INVALID_FORMAT", "message": "Keine gültige E-Mail" }
    ],
    "request_id": "req-abc-123",
    "timestamp": "2026-08-20T10:30:00Z"
  }
}

Error-Codes (konsistent):
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
Log-Levels:
  ERROR   → Systemfehler, braucht Aufmerksamkeit
  WARN    → Unerwartet aber nicht kritisch
  INFO    → Wichtige Operationen
  DEBUG   → Detaillierte Infos (nur Dev)

Log-Format:
{
  "level": "error",
  "message": "Payment failed",
  "context": { "user_id": "uuid", "order_id": "uuid" },
  "error": { "name": "PaymentError", "message": "...", "stack": "..." },
  "request_id": "req-abc-123",
  "timestamp": "2026-08-20T10:30:00Z"
}

Was loggen:
  - Alle Error-Level auf alle Channels
  - Auth-Events (Login, Logout, Failed)
  - Datenbank-Operationen (bei Fehlern)
  - External API Calls (Response-Time, Errors)
  - Security-Events (CSRF, Rate-Limit)

Was NICHT loggen:
  - Passwörter, Tokens, Secrets
  - Vollständige User-Inputs (DSGVO!)
  - Unnötige Debug-Infos in Production
```

### 3. Retry mit Backoff

```markdown
Strategie: Exponential Backoff + Jitter

Base Delay: 1s
Max Retries: 3
Backoff: base * 2^attempt + random_jitter

Attempt 1: ~1s
Attempt 2: ~2-3s
Attempt 3: ~4-8s

Wann retry:
  - 5xx Server Errors
  - Network Timeout
  - Rate Limit (mit Retry-After Header)

Kein retry bei:
  - 4xx Client Errors (außer 429)
  - Auth-Fehler
  - Validierungs-Fehler
```

### 4. Circuit Breaker

```markdown
Für External Services:

States:
  CLOSED     → Normaler Betrieb, alle Requests durchlassen
  OPEN       → Fehler-Limit erreicht, alle Requests werden abgelehnt
  HALF-OPEN  → Test-Request wird durchgelassen

Schwellenwerte:
  - Fehler-Limit: 5 fehlgeschlagene Requests
  - Timeout: 30 Sekunden
  - Successes für HALF-OPEN → CLOSED: 3

Funktion:
  1. Bei 5 Fehlern in Folge → OPEN
  2. Nach 30s → HALF-OPEN
  3. Test-Request → Erfolg: CLOSED / Fehler: OPEN
```

### 5. Graceful Degradation

```markdown
Wenn ein Service ausfällt:
  1. Feature deaktivieren (nicht Crashed)
  2. Fallback-Daten anzeigen (wenn möglich)
  3. User informieren (klare Meldung)
  4. Monitoring alarmieren
  5. automatik Wiederherstellung versuchen

Beispiele:
  - Payment-Service down → "Zahlung momentan nicht möglich"
  - Search-Service down → Fallback auf DB-Query
  - Analytics-Service down → Events puffern
```

---

## Anti-Patterns

### ❌ Verboten

```markdown
- catch {} (stiller Fehler)
- Error Messages die interne Details zeigen
- Kein Logging bei Fehlern
- Infinite Retry ohne Backoff
- Kein Circuit Breaker für External Services
- Exception-Propagation ohne Kontext
```

### ✅ Stattdessen

```markdown
- Spezifisches Error-Handling pro Fehler-Typ
- Generische User-Messages (kein Stack-Trace)
- Strukturiertes Logging mit Kontext
- Exponential Backoff mit Jitter
- Circuit Breaker für alle External Services
- Error-Messages mit request_id für Tracing
```

---

## Referenzen

- `.quinsy-studio/knowledge-base/backend_playbook.md` — Backend-Regeln
- `.quinsy-studio/process/gates.md` — Error-Handling im QA-Gate
