---
id: LO-0256
title: Derived graph mentions use persisted entity ids, never display names
type: studio-evolution
status: done
phase: 6
priority: P1
estimate: S
assignee_role: Process Guard (Director)
team: 09-studio-operations-evolution
skills: [SO-002]
dependencies: []
files: [.quinsy-studio/knowledge-base/backend_playbook.md, .quinsy-studio/CHANGELOG.md]
signal: process-gap
source: affiliate-platform
infusion_kind: process
infusion_path: knowledge-base/backend_playbook.md
train_skills: []
created: 2026-09-14
completed: 2026-09-14
---

## Target
General rule lives in the matching backend playbook so the next project cannot repeat this.

## Infused
If content blocks have no entity foreign key, mention-edge count stays 0. Do not mint entities from labels. PB-20260914-002 on `backend_playbook.md`.

## AC
- [x] Generalized into `backend_playbook.md` (matching playbook)
- [x] Infused text passes portability gate
- [x] CHANGELOG.md updated
- [x] LO moved to backlog/done/
