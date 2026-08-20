# Skill: Authentication & Authorization

> JWT, RBAC, OAuth 2.0, Sessions, Password-Hashing, CSRF-Schutz

## Metadata

```
skill_id: BE-003
name: Authentication & Authorization
team: 02-backend-systems
lead_role: Backend Security Engineer
support_roles: [Backend Architect, Backend Engineer]
phases: [2, 3, 4, 5]
activation_triggers:
  - Ticket enthält "Auth", "Login", "JWT", "Session", "RBAC"
  - Phase 2: Auth-Architektur wird definiert
  - Phase 4: Auth wird implementiert
  - Security-Check in Phase 5
```

---

## Verhaltensregeln

### 1. JWT-Strategie

```markdown
Access Token:
  - Ablaufzeit: 15 Minuten
  - Enthält: user_id, roles, permissions
  - Signiert mit RS256 (asymmetrisch)
  - Immer über HTTPS

Refresh Token:
  - Ablaufzeit: 7 Tage
  - Stored in HttpOnly Cookie (nicht localStorage!)
  - Rotation bei jedem Use
  - Server-seitig invalidierbar

Token-Format:
{
  "sub": "user-uuid",
  "roles": ["user", "admin"],
  "permissions": ["read", "write"],
  "iat": 1640995200,
  "exp": 1640996100
}
```

### 2. RBAC (Role-Based Access Control)

```markdown
Hierarchie:
  owner > admin > moderator > user > guest

Permission-Check:
  1. User hat Role?
  2. Role hat Permission?
  3. Resource gehört User? (Data-Level)

Middleware:
  requireAuth()     → Mindestens eingeloggt
  requireRole('admin') → Bestimmte Rolle
  requirePermission('write') → Bestimmte Berechtigung
```

### 3. OAuth 2.0

```markdown
Flows:
  - Authorization Code (+ PKCE) für Web-Apps
  - Client Credentials für Server-to-Server

Provider:
  - Google (für Consumer)
  - GitHub (für Developer)
  - Custom (für Enterprise)

Regeln:
  - State-Parameter gegen CSRF
  - PKCE für Public Clients
  - Tokens nicht in URLs
  - Redirect-URIs whitelisten
```

### 4. Password-Sicherheit

```markdown
Hashing:
  - bcrypt (cost factor 12) ODER argon2id
  - KEIN MD5/SHA1/SHA256!
  - Salt ist automatisch (bcrypt)

Validierung:
  - Min. 8 Zeichen
  - Groß-/Kleinbuchstaben
  - Zahlen
  - Sonderzeichen
  - Kein Passwort-Reuse (letzte 5)

Reset:
  - Token mit Ablaufzeit (1 Stunde)
  - Token single-use
  - E-Mail-Benötigung
```

### 5. Session-Management

```markdown
Cookie-Settings:
  - HttpOnly: true (kein JS-Zugriff)
  - Secure: true (nur HTTPS)
  - SameSite: Strict (CSRF-Schutz)
  - Path: /
  - Max-Age: 7 Tage

Session-Speicherung:
  - Redis (Production)
  - In-Memory (Development)
  - Timeout: 30 Minuten Inaktivität
```

### 6. CSRF-Schutz

```markdown
Strategien:
  - SameSite Cookie (primär)
  - CSRF-Token für State-Changing-Requests
  - Custom Headers (X-Requested-With)

Für SPA:
  - Token in HttpOnly Cookie (automatisch mitgesendet)
  - Additional Header für API-Calls
```

---

## Anti-Patterns

### ❌ Verboten

```markdown
- JWT in localStorage (XSS-Angriff!)
- Secrets im Code
- MD5/SHA für Passwörter
- JWT ohne Ablaufzeit
- Kein CSRF-Schutz
- Session-IDs in URLs
- Kein Rate-Limiting bei Login
- Passwort in URL-Parametern
```

### ✅ Stattdessen

```markdown
- JWT in HttpOnly Cookie
- Secrets in Environment Variables
- bcrypt/argon2 für Hashing
- Kurze Ablaufzeiten + Refresh
- SameSite Cookies + CSRF-Token
- Cookies-only für Sessions
- Rate-Limiting bei Auth-Endpoints
- HTTPS überall
```

---

## Referenzen

- `.quinsy-studio/knowledge-base/backend_playbook.md` — Backend-Regeln
- `.quinsy-studio/knowledge-base/compliance_playbook.md` — DSGVO
- `studio-library/packages/auth/` — Auth-Package
