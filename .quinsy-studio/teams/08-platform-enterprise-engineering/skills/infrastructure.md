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
  - Never assume 5432, 6379, 3000, or 54321–54323 are free
  - Bind via project env (${POSTGRES_HOST_PORT}:5432), document in RUNBOOK.md
  - Published database ports are for local Compose only; production publishes none (§6 item 4)
  - See knowledge-base/host-port-allocation.md (LO-0066)

Services:
  - app (Next.js / Laravel)
  - db (PostgreSQL)
  - redis (cache/queue)
  - worker (background jobs)

Production shape (same pair locally and on the VPS):
  - docker/docker-compose.yml + docker/compose.prod.yml (template copied by `./studio env <p> init`)
  - The overlay resets every data port, sets restart + bounded logging, runs the app
    from a built image with NODE_ENV=production and `migrate` before `start`
  - `./studio ops <p> readiness` lists PASS/FAIL per rule; `./studio ship <p> --to main` refuses on a FAIL
  - Boot the production shape on the desktop before the first main ship:
    docker compose -f docker-compose.yml -f compose.prod.yml up -d
```

**Agent operations on the VPS (LO-0404).** Access comes from names the human fills in `projects/<p>/.env.local` (`./studio env <p> prod --explain` lists them: `VPS_SSH_*`, `VPS_COMPOSE_DIR`, `COOLIFY_*`, `PROD_DATABASE_URL`). You run `./studio ops <p> deploy | logs | status | db | cleanup` yourself and INFORM; each run is one line in `docs/ops/ops-log.md`. Only `migrate --prod --approve`, `db --reset`, and `cleanup --prune-volumes` wait for the human. Never read `.env.local` values into chat; the command passes the file to `ssh`/`curl` through the environment.

### 2. Cloud Selection

```markdown
Default:
  - Coolify on a VPS → Next.js + Payload
  - Coolify Postgres → the app database
  - Cloudflare R2 → production uploads

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
  - Cloudflare in front of Coolify
  - Images: Cloudflare R2, served through the same adapter as local MinIO

Caching strategy:
  - Static assets: immutable, 1 year
  - API: stale-while-revalidate
  - HTML: short cache + revalidation
```

### 4. SSL/TLS & DNS

```markdown
SSL:
  - Coolify terminates HTTPS
  - Cloudflare in front when the blueprint says so
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
  - Coolify (production)

Rules:
  - Everything versioned in Git
  - No manual changes in production
  - State backend for Terraform
  - Plan before apply
  - Desired state is the Compose file or the project IaC. A console-only change is drift: write it back or revert it.
  - Every long-running service has a health check.
  - Temp and upload directories have an owner and a cleanup.
```

### 6. VPS + Coolify Posture Checklist

Run before the first `./studio ship <p> --to main`, after any server change, and when the human asks for a posture review. Mark each line PASS / FAIL / N/A with the command output or a screenshot path. A FAIL on items 1–6 blocks the main ship.

```markdown
Access
  1. SSH keys only: sshd_config has PasswordAuthentication no and KbdInteractiveAuthentication no.
     Root: PermitRootLogin prohibit-password (Coolify connects to its own host as root with a key; do not set "no" unless Coolify uses a sudo user).
     Check: sshd -T | grep -Ei 'passwordauthentication|permitrootlogin|kbdinteractive'
  2. Coolify dashboard behind HTTPS on its own domain, strong admin password, 2FA on, registration disabled after the first user.

Network
  3. Host firewall default deny inbound; allow 22 (or the moved SSH port), 80, 443 only.
     Docker-published ports bypass ufw rules. Do not rely on ufw to hide a container port; do not publish it.
  4. Database ports not published: production Postgres (and Redis) have no public port mapping and no "Make it publicly available" toggle in Coolify.
     Check from outside the VPS: nc -vz <host> 5432 → must fail. On the host: ss -tlnp shows no 0.0.0.0:5432.
  5. Coolify internal ports (8000 dashboard, 6001/6002 realtime) not reachable directly once the dashboard has a domain.

TLS
  6. Every public domain served over HTTPS by the Coolify proxy with automatic certificates; HTTP redirects to HTTPS; HSTS header set (PE-003 §4).
     Check: curl -sI http://<domain> → 301/308 to https; curl -sI https://<domain> | grep -i strict-transport

Data
  7. Encryption in transit to managed services (R2, external Postgres if any) uses TLS endpoints.
  8. Backups off-host: Coolify scheduled Postgres backups go to S3-compatible storage at another provider or account, EU region. Not only on the VPS disk.
  9. Restore drill done: latest backup restored into a scratch Postgres, app smoke passed. Date, backup age and restore time recorded in docs/ops/incident-runbook.md (PE-007).
 10. Uploads live in R2 (or MinIO locally), not on the container disk; bucket is private unless it serves public marketing media.

Host
 11. Unattended security updates on (Ubuntu: unattended-upgrades) and a reboot plan.
 12. Containers run as non-root where the image allows (the Payload Dockerfile uses the nextjs user).
 13. Server and backup storage in the EU; provider DPA (AVV) on file (CL-001).
```

Record results in `docs/ops/vps-posture.md` with the date. Re-run after changes. `./studio ops <p> status` gives you items 3–5 and the disk line without leaving the chat.

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
  - Postgres or Redis port published on the production VPS
  - Password SSH login
  - Backups only on the same VPS as the database
```

### ✅ Instead

```markdown
- Infrastructure as Code
  - Docker Compose for everyone
  - Probe and pin unique host ports per project (host-port-allocation.md)
  - Secrets in gitignored .env (local) and Coolify variables (production) — PE-006
  - SSL everywhere
  - EU servers for EU users
  - Database reachable only on the internal Docker network
  - SSH keys only, firewall default deny
  - Off-host backups with a recorded restore drill (PE-007)
```

---

## Done Evidence (receipt)

Infra tickets that change the server, Compose or Coolify setup: receipt `## Risk & rollback` names what changed, how to undo it, and the posture checklist items re-run (PASS / FAIL / N/A, with `docs/ops/vps-posture.md` date).

---

## References

- `.quinsy-studio/knowledge-base/backend_playbook.md` — Backend rules
- `.quinsy-studio/knowledge-base/host-port-allocation.md` — Probe host ports before Compose publish
- `templates/docker/` — Docker templates
- `.quinsy-studio/process/project-archetypes.md` — Stack recommendations
- PE-006 Secrets hygiene, PE-007 Incident and breach response (backups, restore drill)
- Posture checklist source: agency-agents `security/security-cloud-security-architect.md` (MIT), rewritten for a single VPS with Coolify
