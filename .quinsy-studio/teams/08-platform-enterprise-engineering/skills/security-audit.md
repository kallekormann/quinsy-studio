# Skill: Security Audit

> OWASP Top 10, Dependency-Scanning, Secrets-Management, Penetration Testing

## Metadata

```
skill_id: PE-003
name: Security Audit
team: 08-platform-enterprise-engineering
lead_role: Backend Security Engineer
support_roles: [Platform Architect, QA Specialist]
phases: [2, 4, 5]
activation_triggers:
  - Ticket enthält "Security", "OWASP", "Penetration", "Vulnerability"
  - Phase 2: Sicherheits-Architektur
  - Phase 4: Security-Implementation
  - Phase 5: Security-Audit (Pflicht)
```

---

## Verhaltensregeln

### 1. OWASP Top 10

```markdown
A01: Broken Access Control
  - RBAC korrekt implementiert
  - Server-side Validierung
  - Keine IDOR (Insecure Direct Object References)

A02: Cryptographic Failures
  - TLS überall
  - bcrypt/argon2 für Passwörter
  - Keine Hardcoded Secrets

A03: Injection
  - Parameterized Queries (kein SQL String Concat!)
  - Input Validation
  - Output Encoding

A05: Security Misconfiguration
  - Standard-Passwörter ändern
  - Error-Messages nicht intern
  - Security-Headers (CSP, HSTS, X-Frame-Options)

A07: XSS
  - Output Encoding
  - Content Security Policy
  - HTTPOnly Cookies
```

### 2. Dependency-Scanning

```markdown
Tools:
  - Dependabot (GitHub)
  - Snyk (optional)
  - npm audit

Prozess:
  - Tägliche Scans
  - Kritische Fixes: sofort
  - High Fixes: innerhalb 7 Tage
  - Medium/Low: beim nächsten Sprint
```

### 3. Secrets-Management

```markdown
Regeln:
  - Keine Secrets im Code (nachweisbar!)
  - Keine Secrets in Git
  - Environment Variables für lokale Entwicklung
  - Secret-Manager für Production

Wo Secrets speichern:
  - Vercel: Environment Variables
  - GitHub: Secrets
  - Docker: Docker Secrets / .env (nicht committed!)
  - AWS: Secrets Manager / Parameter Store
```

### 4. Security-Headers

```markdown
Pflicht-Header:
  - Strict-Transport-Security: max-age=31536000; includeSubDomains
  - Content-Security-Policy: default-src 'self'; ...
  - X-Content-Type-Options: nosniff
  - X-Frame-Options: DENY
  - Referrer-Policy: strict-origin-when-cross-origin
  - Permissions-Policy: camera=(), microphone=(), geolocation=()
```

### 5. Penetration Testing

```markdown
Vor jedem Release:
  - Automatisierte Scans (OWASP ZAP)
  - Manuelle Prüfung der kritischen Pfade
  - Auth-Bypass-Versuche
  - IDOR-Tests
  - XSS/SQL-Injection-Versuche

Funden:
  - Kritisch: Sofort fixen, kein Release
  - Hoch: Fixen vor Release
  - Mittel: Fixen im nächsten Sprint
```

---

## Anti-Patterns

### ❌ Verboten

```markdown
- Secrets im Code/Repository
  - SQL String Concatenation
  - Keine Security-Headers
  - Kein HTTPS
  - XSS-anfällige Outputs
  - Standard-Passwörter in Production
```

### ✅ Stattdessen

```markdown
- Secrets in Secret-Manager
  - Parameterized Queries
  - Vollständige Security-Headers
  - HTTPS überall
  - Output Encoding / CSP
  - Starke Passwörter + MFA
```

---

## Externe Skill-Unterstützung

> Vor der Umsetzung die importierten Best-in-Class-Skills laden (`./studio update-skills`):

- **`all_domains/security/security-audit`** — umfassender Security-Audit-Workflow. **Primäre Referenz.**
- **`all_domains/security/threat-modeling`** — Bedrohungsmodellierung vor Architektur
- **`all_domains/security/dependency-scanning`** — Vulnerabilities in Dependencies
- **`all_domains/security/static-application-security-testing`** — SAST im CI
- **`all_domains/security/dynamic-application-security-testing`** — DAST für laufende Apps

Ablauf: Threat-Modeling (Phase 2) → SAST/DAST im CI (Phase 4) → Security-Audit (Phase 5).

## Referenzen

- `.quinsy-studio/knowledge-base/backend_playbook.md` — Backend-Regeln
- `.quinsy-studio/knowledge-base/compliance_playbook.md` — Compliance
- `.quinsy-studio/process/gates.md` — Security im Gate 5
