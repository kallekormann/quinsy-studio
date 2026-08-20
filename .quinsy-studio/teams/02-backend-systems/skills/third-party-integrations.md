# Skill: Third-Party Integrations

> API-Integration, Webhooks, Queues, Payment, Email, Analytics

## Metadata

```
skill_id: BE-005
name: Third-Party Integrations
team: 02-backend-systems
lead_role: Backend Architect
support_roles: [Backend Engineer, Data Engineer]
phases: [3, 4, 5]
activation_triggers:
  - Ticket enthält "Integration", "API", "Webhook", "Stripe", "SendGrid"
  - Phase 3: Externe Services werden geplant
  - Phase 4: Integrationen werden implementiert
  - Payment, Email, Analytics Features
```

---

## Verhaltensregeln

### 1. Integration-Checkliste

```markdown
Vor jeder Integration:
  [ ] API-Dokumentation gelesen
  [ ] Rate Limits notiert
  [ ] Auth-Methode verstanden
  [ ] Error-Codes dokumentiert
  [ ] Webhook-Events verstanden
  [ ] Fallback-Strategie definiert
  [ ] Monitoring eingerichtet
  [ ] Secrets in Environment Variables
```

### 2. Payment (Stripe)

```markdown
Architektur:
  - Frontend: Stripe.js / Stripe Elements (PCI-konform)
  - Backend: Stripe SDK für Server-Side
  - Webhooks für Payment-Events

Events die wir handlen:
  payment_intent.succeeded   → Order bestätigen
  payment_intent.failed      → User informieren
  subscription.created       → Zugang aktivieren
  subscription.deleted       → Zugang deaktivieren
  invoice.payment_failed     → Zahlungserinnerung

Sicherheit:
  - Webhook-Signatur verifizieren
  - Idempotency Keys für Mappings
  - Keine Secrets im Frontend
```

### 3. Email (SendGrid/Resend)

```markdown
Architektur:
  - Transaktionale E-Mails: Server-Side
  - Marketing: Third-Party (nicht selbst bauen)

Templates:
  - Willkommen
  - Passwort-Reset
  - E-Mail-Verifizierung
  - Zahlungs-Bestätigung
  - Newsletter

Regeln:
  - Immer mit User-ID tracken
  - Unsubscribe-Link immer dabei
  - SPF/DKIM/DMARC konfigurieren
```

### 4. Webhooks

```markdown
Eingehende Webhooks:
  - Signatur-Verifizierung (immer!)
  - Idempotency-Check (Event-ID)
  - Queue für Verarbeitung
  - Retry mit Backoff
  - Logging aller Events

Ausgehende Webhooks:
  - User kann URL konfigurieren
  - Signatur mit Secret
  - Retry bei 5xx/Timeout
  - Event-History für Debugging
```

### 5. Queue-System

```markdown
Wann Queues nutzen:
  - Langlaufende Operationen (>5s)
  - E-Mail-Versand
  - PDF-Generierung
  - Bulk-Operationen
  - Webhook-Verarbeitung

Implementierung:
  - Redis/RabbitMQ/Inngest
  - Dead-Letter-Queue für fehlgeschlagene Jobs
  - Retry mit Backoff
  - Job-Monitoring
```

### 6. Fallback-Strategien

```markdown
Wenn Service ausfällt:
  1. Versuche Alternative (z.B. anderes Payment-Provider)
  2. Deaktiviere Feature graceful
  3. User informiere klar
  4. Alle Anfragen pufere
  5. Monitoring alarmiere

Beispiel:
  Stripe down → "Zahlung momentan nicht möglich. Bitte später versuchen."
  SendGrid down → E-Mail-Queue → wird versendet sobald Service wieder da
```

---

## Anti-Patterns

### ❌ Verboten

```markdown
- Secrets im Code/Repository
- Keine Webhook-Signatur-Verifizierung
- Synchroner API-Call in Request-Handler (>5s)
- Kein Retry/Backoff
- Kein Fallback bei Service-Ausfall
- API-Tokens in URLs
```

### ✅ Stattdessen

```markdown
- Secrets in Environment Variables
- Immer Signatur-Verifizierung
- Asynchron via Queue
- Exponential Backoff mit Max Retries
- Graceful Degradation + User-Meldung
- Tokens in Headers
```

---

## Referenzen

- `.quinsy-studio/knowledge-base/backend_playbook.md` — Backend-Regeln
- `studio-library/packages/billing/` — Billing-Package
- `studio-library/packages/feature-gating/` — Feature-Gating
