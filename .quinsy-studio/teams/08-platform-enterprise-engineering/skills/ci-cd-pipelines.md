# Skill: CI/CD Pipelines

> GitHub Actions, automated testing, security scanning, deployment.  
> Durable **agent** jobs are **AI-003**. Product queues are **BE-006**.

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
    - ./studio ship <project> --to dev
    - Coolify builds that branch
    - Smoke tests

  deploy-production:
    needs: deploy-staging
    - Git-history secret scan + secrets inventory complete (PE-006)
    - ./studio ship <project> --to main --approve
    - Coolify runs payload migrate, then node server.js
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
Coolify:
  - Builds the branch ./studio ship pushed
  - Runs payload migrate, then node server.js
  - Production only after --approve on main

Docker:
  - Build image
  - Push to registry
  - Pull + deploy on server
  - Health check
  - Switch traffic
```

### 5. Rollback

```markdown
App: redeploy the previous image
  - Coolify: Deployments → pick the last good deployment → Redeploy / Rollback
  - Plain Docker: run the previous image tag (tags are immutable; never reuse "latest" as the only tag)

Database: forward-fix, never "migration down" in production
  - payload migrate:down drops data written since the up migration
  - A broken migration is repaired by a new forward migration, tested on a restored copy first (PE-007)
  - Restoring a backup is the last resort and loses writes since the backup — HITL

Automated:
  - Coolify health check fails → the new container never takes traffic; the old one keeps serving
  - Manual previous-image redeploy any time, if the schema is still compatible (see §6)
```

### 6. Migrations: Expand / Contract (Payload)

Coolify runs `payload migrate` before the new container serves traffic, so the **old app runs against the new schema** for a while, and a previous-image rollback runs against it too. Every migration must keep the previous release working.

```markdown
Expand (release N):
  - Add new tables, nullable columns, or columns with a default
  - New code writes both old and new fields where needed
  - Backfill in batches (Payload job or a separate migration), not inside one long lock

Switch (release N+1):
  - Reads move to the new field
  - Add NOT NULL / unique constraints only after the backfill is verified

Contract (release N+2 or later):
  - Drop the old column/table only when no deployed image reads it

Payload specifics:
  - Create with payload migrate:create <name>; review the generated SQL before commit
  - A renamed field or collection is generated as drop + add → data loss. Hand-edit to a rename or split into expand/contract
  - A changed select/enum option or a new required field on a filled table needs a default or a backfill step
  - Production sets push: false; schema changes reach production only through committed migrations
  - Check payload migrate:status in the ticket; run migrations locally via ./studio env <p> migrate --approve

Receipt: ## Risk & rollback names the migration file, which phase it is (expand / switch / contract),
and confirms the previous image still works against the new schema.
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
  - payload migrate:down against production data
  - Dropping or renaming a column in the same release that stops using it
  - Secrets passed as Docker build args or Coolify "Build Variable" (PE-006)
```

### ✅ Instead

```markdown
- Complete CI/CD pipeline
  - All tests mandatory
  - Security scan automated
  - One-click previous-image redeploy + forward-fix migrations
  - Expand / contract migrations across releases
  - Secrets in Coolify runtime variables; GitHub Secrets only for CI that needs them
```

---

## References

- `.quinsy-studio/knowledge-base/ai_automation_playbook.md` — Automation
- `.quinsy-studio/teams/07-ai-autonomous-systems/skills/automation-pipelines.md` — Automation Skills
- `.quinsy-studio/knowledge-base/payload-playbook.md` — `push: false` in production, migrate in Coolify
- PE-007 Incident and breach response (forward-fix, restore drill), PE-006 Secrets hygiene (history scan before main)
