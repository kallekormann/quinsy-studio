---
id: LO-0210
title: Add HTML sticker integrity test (style closes before body) in gate — already add
type: studio-evolution
status: done
phase: 6
priority: P1
estimate: S
assignee_role: UI/Interaction Designer (Director)
team: 10-product-design-experience
skills: [UX-005, FE-002, SO-001]
dependencies: []
files: [.quinsy-studio/studio-library/ui/components/, .quinsy-studio/CHANGELOG.md]
signal: library-gap
source: moody
infusion_kind: ui-component
infusion_path: studio-library/ui/components/
train_skills: [UX-005, FE-002, SO-001]
created: 2026-09-12
---

## Target
General rule lives in `studio-library/ui/components/` so the next project cannot repeat this. No client / product names in studio HQ titles or infused body (provenance `--source` / CHANGELOG only).

## Scope
Kind `ui-component`. Promote or author in `studio-library/ui/components/` using `knowledge-base/atomic-design-playbook.md`. Principle title must stay product-agnostic. Train skills: ['UX-005', 'FE-002', 'SO-001']. Observation (provenance): Add HTML sticker integrity test (style closes before body) in gate — already added MOOD-0755 test; keep for full A/M/O expansion.

## AC
- Inbox item LO-0210 generalized into `studio-library/ui/components/` (or matching playbook/skill/package)
- Infused text passes portability gate (no project folder names outside provenance)
- CHANGELOG.md updated
- LO moved to backlog/done/
