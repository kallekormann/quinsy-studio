---
id: LO-0360
title: Keep the project UI kit in the product repo. Do not promote it into studio-libra
type: studio-evolution
status: done
phase: 6
priority: P1
estimate: S
assignee_role: Studio Automation Engineer (Director)
team: 09-studio-operations-evolution
skills: [SO-001, BE-001]
dependencies: []
files: [.quinsy-studio/knowledge-base/learnings/library/packages.md, .quinsy-studio/CHANGELOG.md]
signal: library-gap
source: craftos
infusion_kind: package
infusion_path: knowledge-base/learnings/library/packages.md
train_skills: [SO-001, BE-001]
created: 2026-09-27
---

## Target
General rule lives in `knowledge-base/learnings/library/packages.md` so the next project cannot repeat this. No client / product names in studio HQ titles or infused body (provenance `--source` / CHANGELOG only).

## Scope
Kind `package`. Promote or author in `knowledge-base/learnings/library/packages.md` using `studio-library/library_registry.md`. Principle title must stay product-agnostic. Train skills: ['SO-001', 'BE-001']. Observation (provenance): Keep the project UI kit in the product repo. Do not promote it into studio-library from this sprint.

## AC
- Inbox item LO-0360 generalized into `knowledge-base/learnings/library/packages.md` (or matching playbook/skill/package)
- Infused text passes portability gate (no project folder names outside provenance)
- CHANGELOG.md updated
- LO moved to backlog/done/
