# Skill: Infrastructure

> Docker, Cloud Selection, CDN, SSL/TLS, DNS, IaC

## Metadata

```
skill_id: PE-001
name: Infrastructure Design
team: 08-platform-enterprise-engineering
lead_role: Platform Architect
support_roles: [Backend Security Engineer, DevOps Engineer]
phases: [1, 2, 3, 4, 6, 7]
activation_triggers:
  - Ticket contains "Infrastructure", "Docker", "Cloud", "Deploy"
  - Phase 1: Cloud evaluation
  - Phase 2: Infrastructure architecture
  - Phase 3: Docker setup
  - Phase 6/7: Deployment
```

---

## Behavioral Rules

### 1. Docker

```markdown
Standard setup:
  - docker-compose.yml for local development
  - Multi-stage builds for production
  - Health checks for every service
  - Volumes for persistent data
  - Networks for service isolation
  - Unique Compose `name:` / container_name per project

Host ports:
  - Probe before pinning (docker ps published ports, then lsof listeners)
  - Never assume 5432, 6379, 3000, or Supabase 54321–54323 are free
  - Bind via project env (${POSTGRES_HOST_PORT}:5432), document in RUNBOOK.md
  - See knowledge-base/host-port-allocation.md (LO-0066)

Services:
  - app (Next.js / Laravel)
  - db (PostgreSQL)
  - redis (cache/queue)
  - worker (background jobs)
```

### 2. Cloud Selection

```markdown
Default:
  - Vercel → Next.js hosting (simple, fast)
  - Supabase → Database + Auth + Storage
  - Railway / Fly.io → Backend services

Enterprise:
  - AWS → Full control
  - GCP → ML/AI workloads
  - Azure → Microsoft ecosystem

Decision criteria:
  - Cost
  - Scalability
  - Region (EU data protection!)
  - Managed services
  - Team expertise
```

### 3. CDN & Caching

```markdown
CDN:
  - Vercel Edge Network (automatic)
  - Cloudflare (if needed)
  - Images: Image CDN (Vercel/Image Optimization)

Caching strategy:
  - Static assets: immutable, 1 year
  - API: stale-while-revalidate
  - HTML: short cache + revalidation
```

### 4. SSL/TLS & DNS

```markdown
SSL:
  - Automatic via Vercel/Cloudflare
  - Let's Encrypt for self-hosted
  - Enable HSTS header

DNS:
  - Cloudflare or Route53
  - Enable DNSSEC
  - MX for email
  - CNAME for WWW
```

### 5. Infrastructure as Code

```markdown
Tools:
  - Terraform (for AWS/GCP)
  - Pulumi (programmatic)
  - Docker Compose (local)
  - Vercel/Supabase (managed)

Rules:
  - Everything versioned in Git
  - No manual changes in production
  - State backend for Terraform
  - Plan before apply
```

---

## Anti-Patterns

### ❌ Prohibited

```markdown
- Manual server configuration
  - No Docker for local development
  - Hardcoded host ports 5432 / 6379 / 3000 on a machine that already runs another stack
  - Secrets in code
  - No SSL
  - US servers for EU users (GDPR!)
```

### ✅ Instead

```markdown
- Infrastructure as Code
  - Docker Compose for everyone
  - Probe and pin unique host ports per project (host-port-allocation.md)
  - Secrets in Secret Manager
  - SSL everywhere
  - EU servers for EU users
```

---

## References

- `.quinsy-studio/knowledge-base/backend_playbook.md` — Backend rules
- `.quinsy-studio/knowledge-base/host-port-allocation.md` — Probe host ports before Compose publish
- `templates/docker/` — Docker templates
- `.quinsy-studio/process/project-archetypes.md` — Stack recommendations
