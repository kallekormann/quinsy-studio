---
id: LO-0257
title: Keep the Compose worker `--queue` list aligned with topology
type: studio-evolution
status: done
phase: 6
priority: P1
estimate: S
assignee_role: Backend Architect (Director)
team: 02-backend-systems
skills: [BE-001, BE-004]
dependencies: []
files: [.quinsy-studio/knowledge-base/backend_playbook.md, .quinsy-studio/CHANGELOG.md]
signal: knowledge-gap
source: affiliate-platform
infusion_kind: backend
infusion_path: knowledge-base/backend_playbook.md
train_skills: [BE-001, BE-004]
created: 2026-09-14
completed: 2026-09-14
---

## Target
General rule lives in `knowledge-base/backend_playbook.md` so the next project cannot repeat this.

## Infused
Worker `--queue=` must list every topology queue jobs are dispatched on. PB-20260914-004 on `backend_playbook.md`.

## AC
- [x] Generalized into `backend_playbook.md`
- [x] Infused text passes portability gate
- [x] CHANGELOG.md updated
- [x] LO moved to backlog/done/
