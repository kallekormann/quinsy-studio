# Skill: Security Audit

> OWASP Top 10, Dependency Scanning, Secrets Management. **Defensive** — no pentest/Metasploit catalogs. Prompt-injection and LLM output sinks: **AI-005** (AI-code security audit). Threat model and per-ticket threat delta: **PE-005**. Secrets lifecycle: **PE-006**.

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

Full rules, inventory and leak response: **PE-006 Secrets hygiene**.

```markdown
Rules:
  - No secrets in code (gate check secret_scan)
  - No secrets in Git history (history scan before ship --to main)
  - Names only in env.schema.json and .env.example
  - Fail loudly when a secret is missing; no || '' fallbacks (except during next build)
  - No secret behind NEXT_PUBLIC_; no secret as a Docker build arg

Where values live:
  - Local: gitignored projects/<p>/.env, injected by ./studio env <p> up|migrate|dev --approve
  - Production: Coolify environment variables (runtime, not "Build Variable")
  - CI: GitHub Actions secrets, only if a workflow needs one
  - Inventory (names, owner, rotation, location — never values): docs/security/secrets-inventory.md
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

### 6. Pattern Catalog (PASS / FAIL / N/A)

Run over the diff (ticket) or the whole app (phase 5). Every line gets PASS, FAIL or N/A with a file path or a reason. A FAIL on a Critical or High item blocks `MOVE_DONE` and `ship --to main`. Severity is the default; raise it when the data is personal or financial.

| # | Pattern | Look for | Severity |
|---|---|---|---|
| P1 | Hardcoded secret | `password = "`, `API_KEY = "`, `sk_live_`, `-----BEGIN .* PRIVATE KEY-----`, `postgres://user:pass@` in source | Critical |
| P2 | Insecure env fallback | `process.env.X \|\| '...'`, `?? '...'`, `os.getenv("X", "...")` on a secret name | Critical |
| P3 | Secret in client | `NEXT_PUBLIC_*SECRET\|KEY\|TOKEN`, server module imported in `"use client"` file | Critical |
| P4 | Missing Payload access | Collection without `access`, `() => true` on `update` / `delete` (details AI-005) | Critical |
| P5 | Local API access bypass | `overrideAccess: true`, or `payload.*` call with user input and no `overrideAccess: false` | Critical |
| P6 | Unsigned webhook | Webhook route without `constructEvent` / HMAC check on the raw body | Critical |
| P7 | SQL injection | String-built SQL, `sql.raw(` with input, template literals into `db.execute` | Critical |
| P8 | Custom JWT without pinned algorithm | `jwt.verify(token, key)` with no `algorithms`, `jwt.decode` used for auth. Prefer Payload auth; do not hand-roll | Critical |
| P9 | Sensitive data in logs | `console.log(token)`, logging `req.headers`, `req.cookies`, whole bodies, full emails | High |
| P10 | Token in browser storage | `localStorage.setItem('token'`, tokens in JS-readable cookies. Payload's `payload-token` cookie stays HttpOnly | High |
| P11 | Stack or internals in responses | `err.stack` or `err.message` from the DB sent to the client in production | High |
| P12 | Permissive CORS / CSRF | Payload `cors: '*'` or missing `csrf` allowlist with cookie auth; `Access-Control-Allow-Origin: *` on authenticated routes | High |
| P13 | Unsafe HTML | `dangerouslySetInnerHTML` with user or CMS data not sanitized; rich text rendered without the Lexical serializer | High |
| P14 | Personal data or tokens in URLs | Email, ids of other people, reset tokens in query strings that reach logs or analytics | High |
| P15 | No brute-force limit | Auth collection without `maxLoginAttempts` / `lockTime`; reset and signup without a rate limit (proxy or app level) | Medium |
| P16 | Missing security headers | See §4; check with `curl -sI` against the deployed URL | Medium |
| P17 | Over-fetch | No `maxDepth` / `defaultDepth` limits on public collections; GraphQL on with no client and no `maxComplexity` | Medium |
| P18 | Vulnerable dependency | `npm audit --omit=dev` High or Critical with a fix available | High |

### 7. Gate checks (planned: sprint S2 in `process/hq-agency-agents-integration.md`)

These checks move the catalog from prose into `run_qa_gate.py`. Until a check ships, the agent runs the pattern by hand and records the result in the receipt.

| Check | Level | Covers |
|---|---|---|
| `secret_scan` | 2 | P1 |
| `client_env_leak` | 2 | P3 |
| `insecure_env_fallback` | 2 | P2 |
| `docker_secret_leak` | 2 | Secrets in `ARG` / `ENV` / `COPY .env` (PE-006) |
| `payload_access` | 5 | P4 |
| `local_api_override` | 5 | P5 |
| `webhook_signature` | 5 | P6 |
| `npm_audit_policy` | 5 | P18 |
| `llm_sink`, `sensitive_log`, `security_headers` | warning | AI-005 rule 8, P9, P16 |

---

## Done Evidence (receipt)

Receipt section `## Security`: one line per catalog item in scope, PASS / FAIL / N/A with file path or reason, plus the gate check names that ran. Phase-5 audits also list open findings with severity and the ticket that will fix each one.

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
- Secrets in gitignored .env (local) and Coolify variables (production) — PE-006
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

---

## Studio skill extensions

**Frontend (XSS, CSP, client tokens, CSRF):**  
[knowledge-base/skill-extensions/frontend-security-auditor.md](../../../knowledge-base/skill-extensions/frontend-security-auditor.md)

**Backend (BOLA, injection, SSRF, mass assignment, rate limits):**  
[knowledge-base/skill-extensions/backend-security-auditor.md](../../../knowledge-base/skill-extensions/backend-security-auditor.md)

**Adds to PE-003:**
- Codebase search patterns per layer (FE vs BE)
- Structured vulnerability report tables with remediation snippets
- Client-side logic bypass checks (UI-only permission gates)
- Consent/schema cross-checks when audit spans privacy + security

## References

- `.quinsy-studio/knowledge-base/backend_playbook.md` — Backend rules
- `.quinsy-studio/knowledge-base/compliance_playbook.md` — Compliance
- `.quinsy-studio/process/gates.md` — Security in Gate 5
- `teams/08-platform-enterprise-engineering/skills/threat-modeling.md` (PE-005), `secrets-hygiene.md` (PE-006), `incident-response.md` (PE-007)
- `teams/07-ai-autonomous-systems/skills/ai-code-security-audit.md` (AI-005) — Payload access, prompt injection, LLM sinks
- Pattern catalog source: agency-agents `security/security-senior-secops.md` (MIT), rewritten for Payload and Coolify
