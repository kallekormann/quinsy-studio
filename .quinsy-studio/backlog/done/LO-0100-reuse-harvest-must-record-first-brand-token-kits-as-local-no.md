---
id: LO-0100
title: Reuse harvest must record first-brand token kits as local, not auto-open studio-library package LOs
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
signal: process-gap
source: affiliate-platform
infusion_kind: package
infusion_path: studio-library/packages/
train_skills: [SO-001, BE-001]
created: 2026-09-07
---

## Target
General rule lives in `studio-library/packages/` so the next project cannot repeat this. No client / product names in studio HQ titles or infused body (provenance `--source` / CHANGELOG only).

## Scope
Kind `package`. Promote or author in `studio-library/packages/` using `studio-library/library_registry.md`. Principle title must stay product-agnostic. Train skills: ['SO-001', 'BE-001']. Observation (provenance): Reuse harvest must record first-brand token kits as local, not auto-open studio-library package LOs

## AC
- Inbox item LO-0100 generalized into `studio-library/packages/` (or matching playbook/skill/package)
- Infused text passes portability gate (no project folder names outside provenance)
- CHANGELOG.md updated
- LO moved to backlog/done/

## Status Change
- **From:** open
- **To:** done
- **Date:** 2026-09-07
- **Reason:** Infused: harvest_reuse_items skips token kits / project UI; registry generic packages only.
