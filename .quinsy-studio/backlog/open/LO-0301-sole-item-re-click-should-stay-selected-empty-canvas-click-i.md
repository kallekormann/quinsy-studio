---
id: LO-0301
title: Sole-item re-click should stay selected; empty-canvas click is what clears
type: studio-evolution
status: open
phase: 6
priority: P1
estimate: S
assignee_role: Studio Automation Engineer (Director)
team: 09-studio-operations-evolution
skills: [SO-001]
dependencies: []
files: [.quinsy-studio/studio-tools/, .quinsy-studio/CHANGELOG.md]
signal: tooling-gap
source: moody
infusion_kind: tooling
infusion_path: studio-tools/
train_skills: [SO-001]
created: 2026-09-16
---

## Target
General rule lives in `studio-tools/` so the next project cannot repeat this. No client / product names in studio HQ titles or infused body (provenance `--source` / CHANGELOG only).

## Scope
Kind `tooling`. Promote or author in `studio-tools/` using `process/gates.md`. Principle title must stay product-agnostic. Train skills: ['SO-001']. Observation (provenance): Sole-item re-click should stay selected; empty-canvas click is what clears.

## AC
- Inbox item LO-0301 generalized into `studio-tools/` (or matching playbook/skill/package)
- Infused text passes portability gate (no project folder names outside provenance)
- CHANGELOG.md updated
- LO moved to backlog/done/
