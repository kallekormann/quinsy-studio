---
id: LO-0171
title: Prefer `--record local` early for brand-specific `ui/` atoms so reuse does not b
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
created: 2026-09-10
---

## Target
General rule lives in `studio-library/ui/components/` so the next project cannot repeat this. No client / product names in studio HQ titles or infused body (provenance `--source` / CHANGELOG only).

## Scope
Kind `ui-component`. Promote or author in `studio-library/ui/components/` using `knowledge-base/atomic-design-playbook.md`. Principle title must stay product-agnostic. Train skills: ['UX-005', 'FE-002', 'SO-001']. Observation (provenance): Prefer `--record local` early for brand-specific `ui/` atoms so reuse does not block retro.

## AC
- Inbox item LO-0171 generalized into `studio-library/ui/components/` (or matching playbook/skill/package)
- Infused text passes portability gate (no project folder names outside provenance)
- CHANGELOG.md updated
- LO moved to backlog/done/


## Status Change
- **From:** open
- **To:** done
- **Date:** 2026-09-10
- **Reason:** Infused into HQ playbooks/tools
