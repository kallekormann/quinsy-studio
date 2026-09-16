---
id: LO-0294
title: Write the architecture packet before implement when `needs_architecture` is true
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
Kind `process`. Promote or author in `process/` using `process/learning-loop.md`. Principle title must stay product-agnostic. Train skills: none (playbook-only). Observation (provenance): Write the architecture packet before implement when `needs_architecture` is true.

## AC
- Inbox item LO-0294 generalized into `process/` (or matching playbook/skill/package)
- Infused text passes portability gate (no project folder names outside provenance)
- CHANGELOG.md updated
- LO moved to backlog/done/
## Done
Architecture packet before implement (`PB-20260916-003` ticket-workflow, `PB-20260916-004` HITL).
