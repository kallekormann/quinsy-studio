# Skill: Automation Pipelines

> CI/CD pipelines, test automation, deployment automation, monitoring

## Metadata

```
skill_id: AI-003
name: Automation Pipelines
team: 07-ai-autonomous-systems
lead_role: Studio Automation Engineer
support_roles: [Platform Architect, Backend Engineer]
phases: [3, 4, 5, 6, 7]
activation_triggers:
  - Ticket contains "CI/CD", "pipeline", "automation", "deployment"
  - Phase 3: CI/CD is set up
  - Phase 4: automation is implemented
  - Phase 5: QA pipeline
  - Phase 7: deployment pipeline
```

---

## Behavior rules

### 1. CI/CD pipeline

```markdown
Standard pipeline (GitHub Actions):

on push:
  1. Lint (ESLint, Prettier)
  2. Type check (TypeScript)
  3. Unit tests (Vitest)
  4. Integration tests
  5. Build
  6. Security scan (Dependabot)

on merge to main:
  1. All CI checks
  2. Deploy to staging
  3. Smoke tests
  4. Deploy to production (after approval)
```

### 2. Test automation

```markdown
In pipeline:
  - Unit tests: always (fast, <2 min)
  - Integration tests: always (<5 min)
  - E2E tests: on deploy to staging (<10 min)
  - Visual regression: on UI changes
  - Lighthouse: on deploy to staging
```

### 3. Deployment automation

```markdown
Strategy: blue/green or canary

Vercel:
  - Auto-deploy on push
  - Preview deployments for PRs
  - Production deploy after merge

Docker:
  - Multi-stage build
  - Health checks
  - Graceful shutdown
```

### 4. Monitoring

```markdown
Post-deployment:
  - Uptime monitoring (ping/UptimeRobot)
  - Error tracking (Sentry)
  - Performance monitoring (Vercel Analytics)
  - Log aggregation

Alerts:
  - Error rate > 1%
  - Response time > 2s
  - Uptime < 99.9%
  - Build failure
```

### 5. Backup & rollback

```markdown
Rollback:
  - Vercel: one-click rollback
  - Docker: previous image
  - Database: migration down

Backup:
  - Database: daily (automated)
  - Config: in git
  - Secrets: in secret manager
```

---

## Anti-patterns

### ❌ Forbidden

```markdown
- Manual deploys
- No tests in the pipeline
- No rollback plan
- No post-deploy monitoring
- Secrets in code/repository
```

### ✅ Instead

```markdown
- Automated deployment
- Complete test pipeline
- One-click rollback
- Uptime + error monitoring
- Secrets in secret manager
```

---

## References

- `.quinsy-studio/knowledge-base/ai_automation_playbook.md` — automation
- `templates/docker/` — docker templates
- `.quinsy-studio/studio-tools/` — python automation
