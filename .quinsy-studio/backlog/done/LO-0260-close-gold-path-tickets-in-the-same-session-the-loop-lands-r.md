---
id: LO-0260
title: Close gold-path tickets in the same session the loop lands (receipt + gate + `MO
type: studio-evolution
status: done
phase: 6
priority: P1
estimate: S
assignee_role: Studio Automation Engineer (Director)
team: 09-studio-operations-evolution
skills: [SO-001, BE-001]
dependencies: []
files: [.quinsy-studio/studio-library/packages/, .quinsy-studio/CHANGELOG.md]
signal: library-gap
source: affiliate-platform
infusion_kind: package
infusion_path: studio-library/packages/
train_skills: [SO-001, BE-001]
created: 2026-09-15
---

## Target
General rule lives in `studio-library/packages/` so the next project cannot repeat this. No client / product names in studio HQ titles or infused body (provenance `--source` / CHANGELOG only).

## Scope
Kind `package`. Promote or author in `studio-library/packages/` using `studio-library/library_registry.md`. Principle title must stay product-agnostic. Train skills: ['SO-001', 'BE-001']. Observation (provenance): Close gold-path tickets in the same session the loop lands (receipt + gate + `MOVE_DONE`) so website-package notes can drain into SPRINT-41 instead of stacking.

## AC
- Inbox item LO-0260 generalized into `studio-library/packages/` (or matching playbook/skill/package)
- Infused text passes portability gate (no project folder names outside provenance)
- CHANGELOG.md updated
- LO moved to backlog/done/
