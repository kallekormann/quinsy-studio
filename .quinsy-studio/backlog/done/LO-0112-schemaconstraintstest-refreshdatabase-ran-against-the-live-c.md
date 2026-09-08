---
id: LO-0112
title: SchemaConstraintsTest `RefreshDatabase` ran against the live Compose Postgres an
type: studio-evolution
status: done
phase: 6
priority: P1
estimate: S
assignee_role: Database Specialist (Director)
team: 02-backend-systems
skills: [BE-002]
dependencies: []
files: [.quinsy-studio/knowledge-base/local-first-sync-playbook.md, .quinsy-studio/CHANGELOG.md]
signal: knowledge-gap
source: affiliate-platform
infusion_kind: database
infusion_path: knowledge-base/local-first-sync-playbook.md
train_skills: [BE-002]
created: 2026-09-08
---

## Target
General rule lives in `knowledge-base/local-first-sync-playbook.md` so the next project cannot repeat this. No client / product names in studio HQ titles or infused body (provenance `--source` / CHANGELOG only).

## Scope
Kind `database`. Promote or author in `knowledge-base/local-first-sync-playbook.md` using `knowledge-base/backend_playbook.md`. Principle title must stay product-agnostic. Train skills: ['BE-002']. Observation (provenance): SchemaConstraintsTest `RefreshDatabase` ran against the live Compose Postgres and wiped the operator domain/kit; it had to be restored by hand.

## AC
- Inbox item LO-0112 generalized into `knowledge-base/local-first-sync-playbook.md` (or matching playbook/skill/package)
- Infused text passes portability gate (no project folder names outside provenance)
- CHANGELOG.md updated
- LO moved to backlog/done/

## Status Change
- **From:** open
- **To:** done
- **Date:** 2026-09-08
- **Reason:** Infused into backend_playbook.md (PHPUnit vs operator database).
