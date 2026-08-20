# Skill: CI/CD Pipelines

> GitHub Actions, automatisches Testing, Security-Scanning, Deployment

## Metadata

```
skill_id: PE-002
name: CI/CD Pipelines
team: 08-platform-enterprise-engineering
lead_role: DevOps Engineer
support_roles: [Platform Architect, Backend Engineer]
phases: [3, 4, 5, 7]
activation_triggers:
  - Ticket enthält "CI/CD", "Pipeline", "GitHub Actions"
  - Phase 3: CI/CD wird eingerichtet
  - Phase 4: Pipeline wird implementiert
  - Phase 5: QA-Pipeline
  - Phase 7: Deployment-Pipeline
```

---

## Verhaltensregeln

### 1. GitHub Actions Standard

```markdown
Pipeline-Struktur:

name: CI/CD

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  ci:
    - Checkout
    - Setup Node.js
    - Install Dependencies
    - Lint (ESLint)
    - Type-Check (TypeScript)
    - Unit-Tests (Vitest)
    - Build
    - Security-Scan (Dependabot)

  deploy-staging:
    needs: ci
    if: github.ref == 'refs/heads/main'
    - Deploy to Vercel (Staging)
    - Smoke-Tests

  deploy-production:
    needs: deploy-staging
    - Deploy to Vercel (Production)
    - Health-Check
```

### 2. Testing in Pipeline

```markdown
Stufen:
  1. Lint: <30s
  2. Type-Check: <1 Min
  3. Unit-Tests: <2 Min
  4. Integration-Tests: <5 Min
  5. Build: <3 Min

Bei Fehler: Pipeline stoppt, PR kann nicht gemerget werden
```

### 3. Security-Scanning

```markdown
Automatisiert:
  - Dependabot: Dependency-Updates
  - CodeQL: Code-Security-Analyse
  - npm audit: Known Vulnerabilities

Bei kritischen CVEs:
  - Sofortiges Update
  - PR erstellen
  - Auto-Merge wenn CI grün
```

### 4. Deployment

```markdown
Vercel:
  - Auto-Deploy on push to main
  - Preview-Deployments für PRs
  - Production nach Approval

Docker:
  - Build Image
  - Push to Registry
  - Pull + Deploy auf Server
  - Health-Check
  - Traffic umschalten
```

### 5. Rollback

```markdown
Vercel: One-Click Rollback (im Dashboard)
Docker: Previous Image deployen
Database: Migration-Down ausführen

Automatisiert:
  - Bei Health-Check-Failure
  - Bei Error-Rate > 5%
  - Manuell jederzeit möglich
```

---

## Anti-Patterns

### ❌ Verboten

```markdown
- Keine Pipeline (manuelles Deployment)
  - Tests in Pipeline überspringen
  - Kein Security-Scan
  - Kein Rollback-Plan
  - Secrets in GitHub Actions (nicht im Secret-Store)
```

### ✅ Stattdessen

```markdown
- Vollständige CI/CD-Pipeline
  - Alle Tests als Pflicht
  - Security-Scan automatisiert
  - One-Click Rollback
  - Secrets in GitHub Secrets / Secret-Manager
```

---

## Referenzen

- `.quinsy-studio/knowledge-base/ai_automation_playbook.md` — Automatisierung
- `.quinsy-studio/teams/07-ai-autonomous-systems/skills/automation-pipelines.md` — Automation Skills
