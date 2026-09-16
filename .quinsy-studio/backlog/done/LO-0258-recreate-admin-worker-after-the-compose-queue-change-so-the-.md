---
id: LO-0258
title: Recreate the queue worker after Compose `--queue` changes
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
YAML worker-command / `--queue` edits require recreating that service (LO-0156 class). PB-20260914-003 on `backend_playbook.md`.

## AC
- [x] Generalized into `backend_playbook.md`
- [x] Infused text passes portability gate
- [x] CHANGELOG.md updated
- [x] LO moved to backlog/done/
