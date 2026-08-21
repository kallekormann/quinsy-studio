---
id: LO-0001
title: Extract Supabase auth boilerplate from Moody into studio-library packages/auth
type: studio-evolution
status: done
phase: 6
priority: P1
estimate: M
assignee_role: Process Guard (Director)
team: 09-studio-operations-evolution
skills: ['SO-002']
dependencies: []
created: 2026-08-21
completed: 2026-08-21
source: moody SPRINT-08 MOOD-0004
---

# LO-0001 — Extract Supabase auth boilerplate from Moody into studio-library

## 1. Context & Value

- **Signal:** library-gap — Moody rebuilt Supabase auth in `src/lib/supabase/` because `packages/auth` was a JWT stub.
- **Target state:** Reusable `packages/auth` v2 + `auth-login` UI molecule; projects pull via `./studio library pull`.
- **Value:** Next SaaS project gets sign-up/login/magic-link/Mailpit/Resend patterns without re-discovery.

## 2. Delivered

- `packages/auth/next/*` — client, server, middleware, callback, env helpers
- `packages/auth/rbac.ts`, email welcome + Resend helper
- `packages/auth/scripts/sync-supabase-env.mjs`
- Supabase + profile migration templates
- `ui/components/auth-login/AuthLoginForm.tsx`
- Manifest v2.0.0, registry aliases `supabase-auth`, CHANGELOG 1.9.2

## 3. Definition of Done

- [x] Implemented in `.quinsy-studio/studio-library/`
- [x] CHANGELOG.md entry
- [x] Registry + manifest updated
