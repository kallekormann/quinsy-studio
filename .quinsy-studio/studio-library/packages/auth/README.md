# Auth package — Supabase + Next.js App Router

> Boilerplate from **Moody M2** (MOOD-0004). Pull into projects and adapt branding + protected routes.

## Pull

```bash
./studio library pull <project> auth
# aliases: supabase-auth, supabase
```

Peer dependencies in the project: `@supabase/ssr`, `@supabase/supabase-js`, `next`. Optional: `resend` for welcome emails.

## Env vars (critical)

| Variable | Source |
|----------|--------|
| `NEXT_PUBLIC_SUPABASE_URL` | `supabase status -o env` → `API_URL` |
| `NEXT_PUBLIC_SUPABASE_ANON_KEY` | `ANON_KEY` (JWT `eyJ…`) — **not** the status table “Publishable” label |

```bash
npx supabase start
node packages/auth/scripts/sync-supabase-env.mjs   # or npm run supabase:env
npm run dev   # restart after env change
```

## Next.js wiring

```typescript
// src/lib/supabase/client.ts
export { createBrowserSupabaseClient as createClient, isSupabaseConfigured } from '@packages/auth/next/client';

// src/middleware.ts
import { updateSession } from '@packages/auth/next/middleware';
export async function middleware(request) {
  return updateSession(request);
}

// app/auth/callback/route.ts
import { handleAuthCallback } from '@packages/auth/next/callback';
export async function GET(request: Request) {
  return handleAuthCallback(request, { defaultNext: '/settings' });
}
```

Custom protected routes:

```typescript
import { createSessionMiddleware } from '@packages/auth/next/middleware';
export const updateSession = createSessionMiddleware({
  protectedPathPrefixes: ['/settings', '/dashboard', '/api/account'],
});
```

## Flows

| Flow | Implementation |
|------|----------------|
| Sign up / sign in | Supabase client `signUp` / `signInWithPassword` |
| Magic link | `signInWithOtp` → `/auth/callback` |
| Welcome email | `sendWelcomeEmail()` via Resend (separate from magic link SMTP) |
| Local magic link inbox | Mailpit in project Docker + Supabase SMTP → `host.docker.internal:54325` |
| RBAC | `getUserRoles`, `hasPermission` from `./rbac` |

## Templates

- `supabase/config.local.toml.template` — local Supabase + Mailpit SMTP
- `supabase/migrations/profile_on_signup.sql.template` — profile row on register
- `scripts/sync-supabase-env.mjs` — CLI → `.env.local`

## UI

Generic login form molecule: `./studio library pull <project> auth-login` → `ui/components/auth-login/`
