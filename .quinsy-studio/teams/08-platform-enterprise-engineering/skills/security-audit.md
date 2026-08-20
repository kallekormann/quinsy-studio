# Skill: Security Audit

> OWASP Top 10, Dependency Scanning, Secrets Management, Penetration Testing

## Metadata

```
skill_id: PE-003
name: Security Audit
team: 08-platform-enterprise-engineering
lead_role: Backend Security Engineer
support_roles: [Platform Architect, QA Specialist]
phases: [2, 4, 5]
activation_triggers:
  - Ticket contains "Security", "OWASP", "Penetration", "Vulnerability"
  - Phase 2: Security architecture
  - Phase 4: Security implementation
  - Phase 5: Security audit (mandatory)
```

---

## Behavioral Rules

### 1. OWASP Top 10

```markdown
A01: Broken Access Control
  - RBAC correctly implemented
  - Server-side validation
  - No IDOR (Insecure Direct Object References)

A02: Cryptographic Failures
  - TLS everywhere
  - bcrypt/argon2 for passwords
  - No hardcoded secrets

A03: Injection
  - Parameterized queries (no SQL string concatenation!)
  - Input validation
  - Output encoding

A05: Security Misconfiguration
  - Change default passwords
  - Error messages not internal
  - Security headers (CSP, HSTS, X-Frame-Options)

A07: XSS
  - Output encoding
  - Content Security Policy
  - HTTPOnly cookies
```

### 2. Dependency Scanning

```markdown
Tools:
  - Dependabot (GitHub)
  - Snyk (optional)
  - npm audit

Process:
  - Daily scans
  - Critical fixes: immediately
  - High fixes: within 7 days
  - Medium/Low: next sprint
```

### 3. Secrets Management

```markdown
Rules:
  - No secrets in code (verifiable!)
  - No secrets in Git
  - Environment variables for local development
  - Secret manager for production

Where to store secrets:
  - Vercel: Environment Variables
  - GitHub: Secrets
  - Docker: Docker Secrets / .env (not committed!)
  - AWS: Secrets Manager / Parameter Store
```

### 4. Security Headers

```markdown
Mandatory headers:
  - Strict-Transport-Security: max-age=31536000; includeSubDomains
  - Content-Security-Policy: default-src 'self'; ...
  - X-Content-Type-Options: nosniff
  - X-Frame-Options: DENY
  - Referrer-Policy: strict-origin-when-cross-origin
  - Permissions-Policy: camera=(), microphone=(), geolocation=()
```

### 5. Penetration Testing

```markdown
Before every release:
  - Automated scans (OWASP ZAP)
  - Manual testing of critical paths
  - Auth bypass attempts
  - IDOR tests
  - XSS/SQL injection attempts

Findings:
  - Critical: Fix immediately, no release
  - High: Fix before release
  - Medium: Fix in next sprint
```

---

## Anti-Patterns

### ❌ Prohibited

```markdown
- Secrets in code/repository
  - SQL string concatenation
  - No security headers
  - No HTTPS
  - XSS-vulnerable outputs
  - Default passwords in production
```

### ✅ Instead

```markdown
- Secrets in Secret Manager
  - Parameterized queries
  - Complete security headers
  - HTTPS everywhere
  - Output encoding / CSP
  - Strong passwords + MFA
```

---

## External Skill Support

> Before implementation, load the imported best-in-class skills (`./studio update-skills`):

- **`all_domains/security/security-audit`** — Comprehensive security audit workflow. **Primary reference.**
- **`all_domains/security/threat-modeling`** — Threat modeling before architecture
- **`all_domains/security/dependency-scanning`** — Vulnerabilities in dependencies
- **`all_domains/security/static-application-security-testing`** — SAST in CI
- **`all_domains/security/dynamic-application-security-testing`** — DAST for running apps

Workflow: Threat modeling (Phase 2) → SAST/DAST in CI (Phase 4) → Security audit (Phase 5).

## References

- `.quinsy-studio/knowledge-base/backend_playbook.md` — Backend rules
- `.quinsy-studio/knowledge-base/compliance_playbook.md` — Compliance
- `.quinsy-studio/process/gates.md` — Security in Gate 5
