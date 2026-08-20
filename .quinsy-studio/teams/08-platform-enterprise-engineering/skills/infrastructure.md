# Skill: Infrastructure

> Docker, Cloud-Auswahl, CDN, SSL/TLS, DNS, IaC

## Metadata

```
skill_id: PE-001
name: Infrastructure Design
team: 08-platform-enterprise-engineering
lead_role: Platform Architect
support_roles: [Backend Security Engineer, DevOps Engineer]
phases: [1, 2, 3, 4, 6, 7]
activation_triggers:
  - Ticket enthält "Infrastructure", "Docker", "Cloud", "Deploy"
  - Phase 1: Cloud-Evaluierung
  - Phase 2: Infrastruktur-Architektur
  - Phase 3: Docker-Setup
  - Phase 6/7: Deployment
```

---

## Verhaltensregeln

### 1. Docker

```markdown
Standard-Setup:
  - docker-compose.yml für lokale Entwicklung
  - Multi-Stage Builds für Produktion
  - Health-Checks für jeden Service
  - Volumes für persistente Daten
  - Networks für Service-Isolation

Services:
  - app (Next.js / Laravel)
  - db (PostgreSQL)
  - redis (Cache/Queue)
  - worker (Background-Jobs)
```

### 2. Cloud-Auswahl

```markdown
Standard:
  - Vercel → Next.js Hosting (einfach, schnell)
  - Supabase → Database + Auth + Storage
  - Railway / Fly.io → Backend-Services

Enterprise:
  - AWS → Volle Kontrolle
  - GCP → ML/AI-Workloads
  - Azure → Microsoft-Ökosystem

Entscheidungskriterien:
  - Kosten
  - Skalierbarkeit
  - Region (EU-Datenschutz!)
  - Managed Services
  - Team-Kompetenz
```

### 3. CDN & Caching

```markdown
CDN:
  - Vercel Edge Network (automatisch)
  - Cloudflare (bei Bedarf)
  - Bilder: Image-CDN (Vercel/Image Optimization)

Caching-Strategie:
  - Static Assets: immutable, 1 year
  - API: stale-while-revalidate
  - HTML: short-cache + revalidation
```

### 4. SSL/TLS & DNS

```markdown
SSL:
  - Automatisch via Vercel/Cloudflare
  - Let's Encrypt für selbst-gehostete
  - HSTS-Header aktivieren

DNS:
  - Cloudflare oder Route53
  - DNS-SEC aktivieren
  - MX für E-Mail
  - CNAME für WWW
```

### 5. Infrastructure as Code

```markdown
Tools:
  - Terraform (bei AWS/GCP)
  - Pulumi (programmatisch)
  - Docker Compose (lokal)
  - Vercel/Supabase (managed)

Regeln:
  - Alles in Git versioniert
  - Keine manuellen Änderungen in Production
  - State-Backend für Terraform
  - Plan before apply
```

---

## Anti-Patterns

### ❌ Verboten

```markdown
- Manuelle Server-Konfiguration
  - Kein Docker für lokale Entwicklung
  - Secrets im Code
  - Kein SSL
  - US-Server für EU-User (DSGVO!)
```

### ✅ Stattdessen

```markdown
- Infrastructure as Code
  - Docker-Compose für alle
  - Secrets in Secret-Manager
  - SSL überall
  - EU-Server für EU-User
```

---

## Referenzen

- `.quinsy-studio/knowledge-base/backend_playbook.md` — Backend-Regeln
- `templates/docker/` — Docker-Templates
- `.quinsy-studio/process/project-archetypes.md` — Stack-Empfehlungen
