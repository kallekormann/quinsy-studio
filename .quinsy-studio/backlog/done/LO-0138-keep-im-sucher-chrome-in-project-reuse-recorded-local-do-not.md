---
id: LO-0138
title: Keep Im Sucher chrome in-project (reuse recorded local); do not promote magazine
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
created: 2026-09-08
---

## Target
General rule lives in `studio-library/packages/` so the next project cannot repeat this. No client / product names in studio HQ titles or infused body (provenance `--source` / CHANGELOG only).

## Scope
Kind `package`. Promote or author in `studio-library/packages/` using `studio-library/library_registry.md`. Principle title must stay product-agnostic. Train skills: ['SO-001', 'BE-001']. Observation (provenance): Keep Im Sucher chrome in-project (reuse recorded local); do not promote magazine packages.

## AC
- Inbox item LO-0138 generalized into `studio-library/packages/` (or matching playbook/skill/package)
- Infused text passes portability gate (no project folder names outside provenance)
- CHANGELOG.md updated
- LO moved to backlog/done/
