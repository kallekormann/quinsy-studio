---
id: LO-0255
title: Pin QUEUE_CONNECTION=sync in PHPUnit TestCase when Compose injects redis
type: studio-evolution
status: done
phase: 6
priority: P1
estimate: S
assignee_role: Backend Systems Director
team: 02-backend-systems
skills: [BE-001]
dependencies: []
files: [.quinsy-studio/knowledge-base/backend_playbook.md, .quinsy-studio/CHANGELOG.md]
signal: process-gap
source: affiliate-platform
infusion_kind: backend
infusion_path: knowledge-base/backend_playbook.md
train_skills: [SO-001]
created: 2026-09-14
completed: 2026-09-14
---

## Target
General rule lives in `knowledge-base/backend_playbook.md` so the next project cannot repeat this.

## Infused
Same env-leak class as `DB_DATABASE`: TestCase must pin `QUEUE_CONNECTION=sync` or `ShouldQueue` tests no-op into Redis. Harvest had classified this as IA; routed to backend playbook. PB-20260914-001.

## AC
- [x] Generalized into `backend_playbook.md` (matching playbook; not IA)
- [x] Infused text passes portability gate
- [x] CHANGELOG.md updated
- [x] LO moved to backlog/done/
