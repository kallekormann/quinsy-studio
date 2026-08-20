# Skill: CI/CD Pipelines

> GitHub Actions, automated testing, security scanning, deployment

## Metadata

```
skill_id: PE-002
name: CI/CD Pipelines
team: 08-platform-enterprise-engineering
lead_role: DevOps Engineer
support_roles: [Platform Architect, Backend Engineer]
phases: [3, 4, 5, 7]
activation_triggers:
  - Ticket contains "CI/CD", "Pipeline", "GitHub Actions"
  - Phase 3: CI/CD is being set up
  - Phase 4: Pipeline is being implemented
  - Phase 5: QA pipeline
  - Phase 7: Deployment pipeline
```

---

## Behavioral Rules

### 1. GitHub Actions Standard

```markdown
Pipeline structure:

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
    - Unit Tests (Vitest)
    - Build
    - Security Scan (Dependabot)

  deploy-staging:
    needs: ci
    if: github.ref == 'refs/heads/main'
    - Deploy to Vercel (Staging)
    - Smoke tests

  deploy-production:
    needs: deploy-staging
    - Deploy to Vercel (Production)
    - Health Check
```

### 2. Testing in Pipeline

```markdown
Stages:
  1. Lint: <30s
  2. Type-Check: <1 min
  3. Unit tests: <2 min
  4. Integration tests: <5 min
  5. Build: <3 min

On error: Pipeline stops, PR cannot be merged
```

### 3. Security Scanning

```markdown
Automated:
  - Dependabot: Dependency updates
  - CodeQL: Code security analysis
  - npm audit: Known vulnerabilities

On critical CVEs:
  - Immediate update
  - Create PR
  - Auto-merge when CI is green
```

### 4. Deployment

```markdown
Vercel:
  - Auto-deploy on push to main
  - Preview deployments for PRs
  - Production after approval

Docker:
  - Build image
  - Push to registry
  - Pull + deploy on server
  - Health check
  - Switch traffic
```

### 5. Rollback

```markdown
Vercel: One-click rollback (in dashboard)
Docker: Deploy previous image
Database: Run migration down

Automated:
  - On health check failure
  - On error rate > 5%
  - Manual anytime possible
```

---

## Anti-Patterns

### ❌ Prohibited

```markdown
- No pipeline (manual deployment)
  - Skipping tests in pipeline
  - No security scan
  - No rollback plan
  - Secrets in GitHub Actions (not in Secret Store)
```

### ✅ Instead

```markdown
- Complete CI/CD pipeline
  - All tests mandatory
  - Security scan automated
  - One-click rollback
  - Secrets in GitHub Secrets / Secret Manager
```

---

## References

- `.quinsy-studio/knowledge-base/ai_automation_playbook.md` — Automation
- `.quinsy-studio/teams/07-ai-autonomous-systems/skills/automation-pipelines.md` — Automation Skills
