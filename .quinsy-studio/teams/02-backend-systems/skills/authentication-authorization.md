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

### 1. Payload auth

```markdown
The Users collection is the only login.
  - Sign in: POST /api/users/login
  - Current user: GET /api/users/me
  - Cookie: payload-token (HttpOnly; secure because production is HTTPS)
  - Access: named on every collection
  - First admin: created in /admin

Do not add Supabase Auth, Clerk, NextAuth, or a second user table.
Do not pull studio-library/packages/auth. That folder is the old module.
The product form is auth-login. It posts to the Payload routes above.
```

### 1a. Payload auth settings (name each on the receipt)

| Setting | Rule |
|---|---|
| `auth.maxLoginAttempts` / `auth.lockTime` | Set on every auth collection. The template uses 5 attempts and 10 minutes. Add a per-IP limit at the proxy or route too, because the lock is per account and an attacker can lock out a known email. |
| `auth.tokenExpiration` | Short (the default is 2 hours). Longer only with a reason in the architecture doc. |
| Sessions and revocation | When the installed Payload version supports `auth.useSessions`, keep it on: logout, password change and admin "log out everywhere" then end server sessions. Without it a JWT stays valid until it expires; keep `tokenExpiration` short and say so in the threat model (PE-005). |
| `saveToJWT: true` on `role` | Lets access functions read the role without a DB call. A role change takes effect at the next token; on demotion, revoke sessions. Never put personal data or secrets in the JWT. |
| Field access on `role` | `create` and `update` are admin-only (`FieldAccess`). A user can never set their own role, through REST, GraphQL or a hook. |
| First user | The template's `beforeChange` hook makes the first user `admin`. Create that user in `/admin` (create-first-user) before the app is reachable from the internet. |
| `access.create` on `users` | `() => true` means public signup. Keep it only if the PRD has self-signup; otherwise admin-only. With self-signup, turn on `auth.verify` (email verification). |
| `access.admin` | Admin panel only for `role === 'admin'` (or the roles the PRD names). |
| `csrf` and `cors` in the Payload config | List the exact production origins. No `*`. |
| `auth.useAPIKey` | Only for machine clients named in the architecture doc; one key per client, scoped by role. |

### 2. RBAC (role-based access control)

```markdown
Hierarchy (example; ship only the roles the PRD needs, default user + admin):
  owner > admin > moderator > user > guest

Permission check:
  1. Does the user have the role?
  2. Does the role have the permission?
  3. Does the resource belong to the user? (data level)

Where the check lives:
  - Payload collection `access` (read/create/update/delete) and field `access`
  - Route handlers: `payload.auth({ headers })` then the same helper the access function uses
  - Local API from user-driven code: `overrideAccess: false` and pass `user`
    (the default is `true`, which skips every rule)
```

### 2a. Identity and access rules

- **Least privilege.** Start every role with no access and add what the PRD needs. Default roles: `user` and `admin`; add more only when a ticket names the difference. The app's Postgres user is not a superuser.
- **The server decides.** Hiding a button is UX. Every operation is checked on the server, every time.
- **Ownership from the session.** User ID and tenant ID come from `req.user`, never from a request parameter or body. Access returns a `where` query (`{ owner: { equals: user.id } }`) so lists filter too.
- **Revocation is real.** Deactivating a user, changing a password or demoting a role ends that user's sessions (see 1a). Test it: an old cookie gets `401` after the change.
- **No enumeration.** Login, signup and forgot-password answer the same way for known and unknown emails.
- **Audit auth events.** Log login failure, lockout, password reset, role change and API-key creation with user ID, IP and `request_id`. Never the password, token or reset link.
- **Recovery is a login path.** Reset tokens are single-use and expire (Payload `auth.forgotPassword.expiration`). A password reset ends other sessions.

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
  - Social or SSO login is an ADR. It signs users into the Payload `users`
    collection (plugin or custom strategy), never into a second user store.
  - Authorization code + PKCE; `state` checked on every callback; `nonce` for OIDC
  - Exact-match redirect URI allowlist
  - Verify ID token issuer, audience and an allowlisted `alg`
  - No tokens in URLs
  - Linking an SSO email to an existing password account needs the user to prove both
```

### 4. Password security (NIST SP 800-63B)

```markdown
Hashing:
  - Payload hashes passwords (salted PBKDF2). Do not hash passwords yourself
    and do not store a second hash anywhere.

Length, not composition (SP 800-63B-4, 2025):
  - Minimum 15 characters when the password is the only factor;
    minimum 8 when it is one factor of MFA
  - Accept at least 64 characters, spaces and all Unicode; do not truncate
  - NO composition rules (no "one upper, one digit, one symbol")
  - NO forced periodic rotation; force a change only on evidence of compromise
  - NO password-reuse history, NO hints, NO security questions
  - Allow paste and password managers; offer "show password"

Blocklist (required):
  - Reject passwords found in breach corpora, dictionary words, and context
    words (product name, the user's email)
  - Breach check: Have I Been Pwned range API (k-anonymity: send only the first
    5 hex chars of the SHA-1). If the API is down, fall back to a local list of
    common passwords and log a warning
  - Tell the user why it was rejected ("This password appears in a known breach")

Where to check:
  - Every path that sets a password: signup, change, reset
  - Test all three. If one path skips the check (e.g. a built-in Payload route),
    send it through a custom endpoint that checks first

Throttling:
  - SP 800-63B caps consecutive failures at 100 per account; Payload's
    maxLoginAttempts is stricter, which is fine

Reset:
  - Single-use token with expiry
  - Same response for known and unknown emails
  - Reset ends other sessions
```

### 5. Session management

```markdown
Payload sets the session cookie. Do not invent a second session store.
  - HttpOnly
  - Secure in production
  - SameSite as Payload configures it
Redis is not the session store. Payload jobs and this cookie do not need it.
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
- Own password hashing next to Payload's
- Composition rules, forced rotation, reuse history
- JWT without expiry
- No CSRF protection
- Session IDs in URLs
- No rate limiting on login
- Password in URL parameters
- Local API calls from user-driven code without `overrideAccess: false`
- Role field writable by the user
- User or tenant ID read from the request body
```

### ✅ Instead

```markdown
- Payload `payload-token` HttpOnly cookie
- Secret names in env.schema.json; values via ./studio env … --approve
- Payload's built-in hashing
- Length + breached-password blocklist
- Short tokenExpiration; sessions revoked on change
- SameSite cookies + Payload `csrf` allowlist
- Cookies-only for sessions
- maxLoginAttempts + per-IP limit
- HTTPS everywhere (Coolify)
- `overrideAccess: false` + `user`
- Admin-only field access on `role`
- IDs from `req.user`
```

---

## Done evidence (receipt)

`## API proof` (shared with BE-001) on auth tickets, PASS / FAIL / NOT TESTED:

- Login as `user` and as `admin`; `/api/users/me` response trimmed
- Authz negative: `user` reads another user's document → `403` or empty list; `user` PATCHes own `role` → refused
- Lockout after `maxLoginAttempts` wrong passwords (status and message)
- Short password and a known-breached password are refused on signup, change and reset
- Old cookie after password change or demotion → `401` (or NOT TESTED with the reason, if sessions are not on)
- Payload auth settings from 1a listed with their values

---

## References

- `.quinsy-studio/knowledge-base/backend_playbook.md` — backend rules
- `.quinsy-studio/knowledge-base/compliance_playbook.md` — GDPR
- `knowledge-base/payload-playbook.md` — Users collection is the login
- `studio-templates/payload/app/src/collections/Users.ts` — template access, role field, first-user hook
- `studio-library/ui/components/auth-login/` — the product form
- NIST SP 800-63B-4 (2025), sections on memorized secrets / passwords
- Payload docs: Authentication (config, operations, cookies, API keys)
- PE-005 threat modeling, AI-005 AI-code security audit (Payload access checks)
