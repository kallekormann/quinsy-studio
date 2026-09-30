# backend / data

Portable studio principles (not project incidents).
Matching playbook/skill: `knowledge-base/backend_playbook.md`.

## Principles

- **LO-0362** 2026-09-29 :: Do not run `supabase start` beside an existing Compose Postgres in the same working copy.
  - One working copy, one Postgres. If Compose already publishes Postgres, do not start a second Supabase CLI database next to it. Issue the local session from the product API and store `auth_user_id` as the hook for the Auth `sub` that the hosted GoTrue later signs.
- **PB-20260927-001** helpful=12 harmful=0 :: When a requirement needs a fact the schema cannot store, architecture must add that column instead of shipping the schema alone.
- **LO-0354** 2026-09-26 :: When a requirement needs a fact the schema cannot store, architecture must add that column instead of shipping the schem
  - When a requirement needs a fact the schema cannot store, architecture must add that column instead of shipping the schema alone.
