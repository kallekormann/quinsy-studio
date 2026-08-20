# Skill: Automation Pipelines

> CI/CD-Pipelines, Test-Automatisierung, Deployment-Automatisierung, Monitoring

## Metadata

```
skill_id: AI-003
name: Automation Pipelines
team: 07-ai-autonomous-systems
lead_role: Studio Automation Engineer
support_roles: [Platform Architect, Backend Engineer]
phases: [3, 4, 5, 6, 7]
activation_triggers:
  - Ticket enthält "CI/CD", "Pipeline", "Automatisierung", "Deployment"
  - Phase 3: CI/CD wird eingerichtet
  - Phase 4: Automatisierung wird implementiert
  - Phase 5: QA-Pipeline
  - Phase 7: Deployment-Pipeline
```

---

## Verhaltensregeln

### 1. CI/CD Pipeline

```markdown
Standard-Pipeline (GitHub Actions):

on push:
  1. Lint (ESLint, Prettier)
  2. Type-Check (TypeScript)
  3. Unit-Tests (Vitest)
  4. Integration-Tests
  5. Build
  6. Security-Scan (Dependabot)

on merge to main:
  1. Alle CI-Checks
  2. Deploy to Staging
  3. Smoke-Tests
  4. Deploy to Production (after approval)
```

### 2. Test-Automatisierung

```markdown
In Pipeline:
  - Unit-Tests: Immer (schnell, <2 Min)
  - Integration-Tests: Immer (<5 Min)
  - E2E-Tests: Bei Deploy auf Staging (<10 Min)
  - Visual Regression: Bei UI-Änderungen
  - Lighthouse: Bei Deploy auf Staging
```

### 3. Deployment-Automatisierung

```markdown
Strategie: Blue/Green oder Canary

Vercel:
  - Auto-Deploy on push
  - Preview-Deployments für PRs
  - Production-Deploy nach Merge

Docker:
  - Multi-Stage Build
  - Health-Checks
  - Graceful Shutdown
```

### 4. Monitoring

```markdown
Post-Deployment:
  - Uptime-Monitoring (Ping/UptimeRobot)
  - Error-Tracking (Sentry)
  - Performance-Monitoring (Vercel Analytics)
  - Log-Aggregation

Alerts:
  - Error-Rate > 1%
  - Response-Time > 2s
  - Uptime < 99.9%
  - Build-Failure
```

### 5. Backup & Rollback

```markdown
Rollback:
  - Vercel: One-Click Rollback
  - Docker: Previous Image
  - Database: Migration-Down

Backup:
  - Database: Täglich (automatisiert)
  - Config: In Git
  - Secrets: In Secret-Manager
```

---

## Anti-Patterns

### ❌ Verboten

```markdown
- Manuelle Deploys
  - Keine Tests in Pipeline
  - Kein Rollback-Plan
  - Kein Monitoring post-deploy
  - Secrets im Code/Repository
```

### ✅ Stattdessen

```markdown
- Automatisiertes Deployment
  - Vollständige Test-Pipeline
  - One-Click Rollback
  - Uptime + Error-Monitoring
  - Secrets in Secret-Manager
```

---

## Referenzen

- `.quinsy-studio/knowledge-base/ai_automation_playbook.md` — Automatisierung
- `templates/docker/` — Docker-Templates
- `.quinsy-studio/studio-tools/` — Python-Automation
