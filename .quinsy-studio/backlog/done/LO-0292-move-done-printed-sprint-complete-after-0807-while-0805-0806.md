---
id: LO-0292
title: MOVE_DONE printed “sprint complete” after 0807 while 0805/0806/0808 were still o
type: studio-evolution
status: done
phase: 6
priority: P1
estimate: S
assignee_role: Process Guard (Director)
team: 09-studio-operations-evolution
skills: [SO-002]
dependencies: []
files: [.quinsy-studio/process/, .quinsy-studio/CHANGELOG.md]
signal: process-gap
source: moody
infusion_kind: process
infusion_path: process/
train_skills: []
created: 2026-09-16
---

## Target
General rule lives in `process/` so the next project cannot repeat this. No client / product names in studio HQ titles or infused body (provenance `--source` / CHANGELOG only).

## Scope
Kind `process`. Promote or author in `process/` using `process/learning-loop.md`. Principle title must stay product-agnostic. Train skills: none (playbook-only). Observation (provenance): MOVE_DONE printed “sprint complete” after 0807 while 0805/0806/0808 were still open; execute still picked the next ticket, but the message is misleading.

## AC
- Inbox item LO-0292 generalized into `process/` (or matching playbook/skill/package)
- Infused text passes portability gate (no project folder names outside provenance)
- CHANGELOG.md updated
- LO moved to backlog/done/

## Done
MOVE_DONE prints remaining-ticket continue-execute copy until the sprint is empty (`PB-20260916-003` HITL).
