---
id: LO-0368
title: Do not rewrite existing `text-[12px]` classNames on the send button — added line
type: studio-evolution
status: done
phase: 6
priority: P1
estimate: S
assignee_role: UI/Interaction Designer (Director)
team: 10-product-design-experience
skills: [UX-005, FE-002, SO-001]
dependencies: []
files: [.quinsy-studio/knowledge-base/learnings/library/components.md, .quinsy-studio/CHANGELOG.md]
signal: library-gap
source: arthur
infusion_kind: ui-component
infusion_path: knowledge-base/learnings/library/components.md
train_skills: [UX-005, FE-002, SO-001]
created: 2026-10-01
---

## Target
General rule lives in `knowledge-base/learnings/library/components.md` so the next project cannot repeat this. No client / product names in studio HQ titles or infused body (provenance `--source` / CHANGELOG only).

## Scope
Kind `ui-component`. Promote or author in `knowledge-base/learnings/library/components.md` using `knowledge-base/atomic-design-playbook.md`. Principle title must stay product-agnostic. Train skills: ['UX-005', 'FE-002', 'SO-001']. Observation (provenance): Do not rewrite existing `text-[12px]` classNames on the send button — added lines fail the token check.

## AC
- Inbox item LO-0368 generalized into `knowledge-base/learnings/library/components.md` (or matching playbook/skill/package)
- Infused text passes portability gate (no project folder names outside provenance)
- CHANGELOG.md updated
- LO moved to backlog/done/
