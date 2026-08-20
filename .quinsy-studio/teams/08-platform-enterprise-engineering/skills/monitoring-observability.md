# Skill: Monitoring & Observability

> Application monitoring, error tracking, uptime monitoring, alerting

## Metadata

```
skill_id: PE-004
name: Monitoring & Observability
team: 08-platform-enterprise-engineering
lead_role: Platform Architect
support_roles: [DevOps Engineer, Backend Engineer]
phases: [5, 6, 7]
activation_triggers:
  - Ticket contains "Monitoring", "Alerting", "Uptime", "Sentry"
  - Phase 5: Monitoring is being set up
  - Phase 6: Monitoring after deploy
  - Phase 7: Monitoring maintenance
```

---

## Behavioral Rules

### 1. Error Tracking (Sentry)

```markdown
Integration:
  - Frontend: Sentry Browser SDK
  - Backend: Sentry Node/Python SDK
  - Upload source maps

Configuration:
  - environment: production / staging
  - sampleRate: 1.0 (all errors)
  - tracesSampleRate: 0.2 (20% of transactions)
  - beforeSend: Filter PII
```

### 2. Uptime Monitoring

```markdown
Tools: UptimeRobot / BetterStack / Vercel Analytics

What to monitor:
  - HTTP endpoints (every 5 min)
  - API response time
  - SSL certificate expiry
  - DNS changes

Alerts:
  - Down: Immediate (email + SMS)
  - Slow (>2s): Within 5 min
  - SSL expiring: 30 days before
```

### 3. Application Performance Monitoring

```markdown
Metrics:
  - Response time (p50, p95, p99)
  - Error rate
  - Throughput (requests/sec)
  - Database query time
  - Memory/CPU usage

Tools:
  - Vercel Analytics (frontend)
  - Sentry Performance (backend)
  - Custom metrics (if needed)
```

### 4. Logging

```markdown
Structured logging:
{
  "level": "info",
  "message": "User logged in",
  "userId": "uuid",
  "requestId": "req-abc",
  "timestamp": "2026-08-20T10:30:00Z"
}

Log aggregation:
  - Vercel Logs
  - Sentry Logs
  - stdout for Docker
```

### 5. Alerting

```markdown
Alert channels:
  - Email: Important alerts
  - Slack/Discord: Team alerts
  - SMS: Critical alerts (on-call only)

Alert rules:
  - Error rate > 1% → Email
  - Error rate > 5% → SMS
  - Response time p95 > 3s → Slack
  - Uptime < 99.9% → SMS
```

---

## Anti-Patterns

### ❌ Prohibited

```markdown
- No error tracking
  - No uptime monitoring
  - No alerts
  - Logs without structure
  - PII in logs
```

### ✅ Instead

```markdown
- Sentry for error tracking
  - UptimeRobot for uptime
  - Multi-level alerting
  - Structured logging
  - Anonymized logs
```

---

## References

- `.quinsy-studio/knowledge-base/backend_playbook.md` — Backend rules
- `.quinsy-studio/process/gates.md` — Monitoring in Gate 5
