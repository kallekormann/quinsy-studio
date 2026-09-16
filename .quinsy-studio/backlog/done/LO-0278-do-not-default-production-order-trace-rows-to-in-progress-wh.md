---
id: LO-0278
title: Do not default production-order trace rows to `in_progress` when the pipeline is
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
source: affiliate-platform
infusion_kind: process
infusion_path: process/
train_skills: []
created: 2026-09-16
---

## Target
General rule lives in `process/` so the next project cannot repeat this. No client / product names in studio HQ titles or infused body (provenance `--source` / CHANGELOG only).

## Scope
Kind `process`. Promote or author in `process/` using `process/learning-loop.md`. Principle title must stay product-agnostic. Train skills: none (playbook-only). Observation (provenance): Do not default production-order trace rows to `in_progress` when the pipeline is empty.

## AC
- Inbox item LO-0278 generalized into `process/` (or matching playbook/skill/package)
- Infused text passes portability gate (no project folder names outside provenance)
- CHANGELOG.md updated
- LO moved to backlog/done/

## Done
Infused `PB-20260916-001` on `knowledge-base/backend_playbook.md`.
