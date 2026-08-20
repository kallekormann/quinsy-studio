# Skill: Monitoring & Observability

> Application Monitoring, Error-Tracking, Uptime-Monitoring, Alerting

## Metadata

```
skill_id: PE-004
name: Monitoring & Observability
team: 08-platform-enterprise-engineering
lead_role: Platform Architect
support_roles: [DevOps Engineer, Backend Engineer]
phases: [5, 6, 7]
activation_triggers:
  - Ticket enthält "Monitoring", "Alerting", "Uptime", "Sentry"
  - Phase 5: Monitoring wird eingerichtet
  - Phase 6: Monitoring nach Deploy
  - Phase 7: Monitoring-Pflege
```

---

## Verhaltensregeln

### 1. Error-Tracking (Sentry)

```markdown
Integration:
  - Frontend: Sentry Browser SDK
  - Backend: Sentry Node/Python SDK
  - Source Maps hochladen

Konfiguration:
  - environment: production / staging
  - sampleRate: 1.0 (alle Fehler)
  - tracesSampleRate: 0.2 (20% der Transaktionen)
  - beforeSend: PII filtern
```

### 2. Uptime-Monitoring

```markdown
Tools: UptimeRobot / BetterStack / Vercel Analytics

Was monitoren:
  - HTTP-Endpoints (alle 5 Min)
  - API-Response-Time
  - SSL-Zertifikat-Ablauf
  - DNS-Änderungen

Alerts:
  - Down: Sofort (E-Mail + SMS)
  - Slow (>2s): Innerhalb 5 Min
  - SSL ablauft: 30 Tage vorher
```

### 3. Application Performance Monitoring

```markdown
Metriken:
  - Response Time (p50, p95, p99)
  - Error Rate
  - Throughput (Requests/sec)
  - Database Query Time
  - Memory/CPU Usage

Tools:
  - Vercel Analytics (Frontend)
  - Sentry Performance (Backend)
  - Custom Metrics (bei Bedarf)
```

### 4. Logging

```markdown
Strukturiertes Logging:
{
  "level": "info",
  "message": "User logged in",
  "userId": "uuid",
  "requestId": "req-abc",
  "timestamp": "2026-08-20T10:30:00Z"
}

Log-Aggregation:
  - Vercel Logs
  - Sentry Logs
  - stdout für Docker
```

### 5. Alerting

```markdown
Alert-Kanäle:
  - E-Mail: Wichtige Alerts
  - Slack/Discord: Team-Alerts
  - SMS: Kritische Alerts (nur für On-Call)

Alert-Regeln:
  - Error-Rate > 1% → E-Mail
  - Error-Rate > 5% → SMS
  - Response-Time p95 > 3s → Slack
  - Uptime < 99.9% → SMS
```

---

## Anti-Patterns

### ❌ Verboten

```markdown
- Kein Error-Tracking
  - Kein Uptime-Monitoring
  - Keine Alerts
  - Logs ohne Struktur
  - PII in Logs
```

### ✅ Stattdessen

```markdown
- Sentry für Error-Tracking
  - UptimeRobot für Uptime
  - Mehrstufiges Alerting
  - Strukturiertes Logging
  - Anonymisierte Logs
```

---

## Referenzen

- `.quinsy-studio/knowledge-base/backend_playbook.md` — Backend-Regeln
- `.quinsy-studio/process/gates.md` — Monitoring im Gate 5
