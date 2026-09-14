# Skill: Authentication & Authorization

> JWT, RBAC, OAuth 2.0, sessions, password hashing, CSRF protection

**Playbook:** [backend_playbook.md](../../../knowledge-base/backend_playbook.md) (Auth).

## Metadata

```
skill_id: BE-003
name: Authentication & Authorization
team: 02-backend-systems
lead_role: Backend Security Engineer
support_roles: [Backend Architect, Backend Engineer]
phases: [2, 3, 4, 5]
activation_triggers:
  - Ticket contains "auth", "login", "JWT", "session", "RBAC"
  - Phase 2: auth architecture is defined
  - Phase 4: auth is implemented
  - Security check in phase 5
```

---

## Behavior rules

### 1. JWT strategy

```markdown
Access token:
  - Expiry: 15 minutes
  - Contains: user_id, roles, permissions
  - Signed with RS256 (asymmetric)
  - Always over HTTPS

Refresh token:
  - Expiry: 7 days
  - Stored in an HttpOnly cookie (not localStorage!)
  - Rotated on every use
  - Server-side invalidatable

Token format:
{
  "sub": "user-uuid",
  "roles": ["user", "admin"],
  "permissions": ["read", "write"],
  "iat": 1640995200,
  "exp": 1640996100
}
```

### 2. RBAC (role-based access control)

```markdown
Hierarchy:
  owner > admin > moderator > user > guest

Permission check:
  1. Does the user have the role?
  2. Does the role have the permission?
  3. Does the resource belong to the user? (data level)

Middleware:
  requireAuth()     → at least logged in
  requireRole('admin') → specific role
  requirePermission('write') → specific permission
```

### 3. OAuth 2.0

```markdown
Flows:
  - Authorization code (+ PKCE) for web apps
  - Client credentials for server-to-server

Providers:
  - Google (for consumer)
  - GitHub (for developers)
  - Custom (for enterprise)

Rules:
  - State parameter against CSRF
  - PKCE for public clients
  - No tokens in URLs
  - Whitelist redirect URIs
```

### 4. Password security

```markdown
Hashing:
  - bcrypt (cost factor 12) OR argon2id
  - NO MD5/SHA1/SHA256!
  - Salt is automatic (bcrypt)

Validation:
  - Min. 8 characters
  - Upper/lowercase letters
  - Numbers
  - Special characters
  - No password reuse (last 5)

Reset:
  - Token with expiry (1 hour)
  - Token single-use
  - Email required
```

### 5. Session management

```markdown
Cookie settings:
  - HttpOnly: true (no JS access)
  - Secure: true (HTTPS only)
  - SameSite: Strict (CSRF protection)
  - Path: /
  - Max-Age: 7 days

Session storage:
  - Redis (production)
  - In-memory (development)
  - Timeout: 30 minutes of inactivity
```

### 6. CSRF protection

```markdown
Strategies:
  - SameSite cookie (primary)
  - CSRF token for state-changing requests
  - Custom headers (X-Requested-With)

For SPA:
  - Token in HttpOnly cookie (sent automatically)
  - Additional header for API calls
```

---

## Anti-patterns

### ❌ Forbidden

```markdown
- JWT in localStorage (XSS attack!)
- Secrets in code
- MD5/SHA for passwords
- JWT without expiry
- No CSRF protection
- Session IDs in URLs
- No rate limiting on login
- Password in URL parameters
```

### ✅ Instead

```markdown
- JWT in HttpOnly cookie
- Secrets in environment variables
- bcrypt/argon2 for hashing
- Short expiries + refresh
- SameSite cookies + CSRF token
- Cookies-only for sessions
- Rate limiting on auth endpoints
- HTTPS everywhere
```

---

## References

- `.quinsy-studio/knowledge-base/backend_playbook.md` — backend rules
- `.quinsy-studio/knowledge-base/compliance_playbook.md` — GDPR
- `studio-library/packages/auth/` — auth package
