---
id: LO-0156
title: After compose queue/volume/env changes, recreate `admin-worker` and `web` so `
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
created: 2026-09-09
---

## Target
General rule lives in `knowledge-base/backend_playbook.md` so the next project cannot repeat this. No client / product names in studio HQ titles or infused body (provenance `--source` / CHANGELOG only).

## Scope
Kind `backend`. Promote or author in `knowledge-base/backend_playbook.md` using `knowledge-base/backend_playbook.md`. Principle title must stay product-agnostic. Train skills: ['BE-001', 'BE-004']. Observation (provenance): After compose queue/volume/env changes, recreate `admin-worker` and `web` so `--queue=synthesis,default` and the revalidate secret are live.

## AC
- Inbox item LO-0156 generalized into `knowledge-base/backend_playbook.md` (or matching playbook/skill/package)
- Infused text passes portability gate (no project folder names outside provenance)
- CHANGELOG.md updated
- LO moved to backlog/done/
