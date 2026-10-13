# backend / data

Portable studio principles (not project incidents).
Matching playbook/skill: `knowledge-base/backend_playbook.md`.

## Principles

- **LO-0362** 2026-09-29 :: One working copy, one Postgres. Do not start a second database beside Compose.
  - Login is the Payload Users collection. Do not add a second auth service next to that Postgres.
- **PB-20260927-001** helpful=12 harmful=0 :: When a requirement needs a fact the schema cannot store, architecture must add that column instead of shipping the schema alone.
- **LO-0354** 2026-09-26 :: When a requirement needs a fact the schema cannot store, architecture must add that column instead of shipping the schem
  - When a requirement needs a fact the schema cannot store, architecture must add that column instead of shipping the schema alone.
