---
id: LO-0362
title: Do not run `supabase start` beside an existing Compose Postgres in the same work
type: studio-evolution
status: done
phase: 6
priority: P1
estimate: S
assignee_role: Database Specialist (Director)
team: 02-backend-systems
skills: [BE-002]
dependencies: []
files: [.quinsy-studio/knowledge-base/learnings/backend/data.md, .quinsy-studio/CHANGELOG.md]
signal: knowledge-gap
source: arthur
infusion_kind: database
infusion_path: knowledge-base/learnings/backend/data.md
train_skills: [BE-002]
created: 2026-09-29
---

## Target
General rule lives in `knowledge-base/learnings/backend/data.md` so the next project cannot repeat this. No client / product names in studio HQ titles or infused body (provenance `--source` / CHANGELOG only).

## Scope
Kind `database`. Promote or author in `knowledge-base/learnings/backend/data.md` using `knowledge-base/backend_playbook.md`. Principle title must stay product-agnostic. Train skills: ['BE-002']. Observation (provenance): Do not run `supabase start` beside an existing Compose Postgres in the same working copy. Keep GoTrue for the host that already owns Auth; locally issue the cookie from the product API and store `auth_user_id` as the hook.

## AC
- Inbox item LO-0362 generalized into `knowledge-base/learnings/backend/data.md` (or matching playbook/skill/package)
- Infused text passes portability gate (no project folder names outside provenance)
- CHANGELOG.md updated
- LO moved to backlog/done/
