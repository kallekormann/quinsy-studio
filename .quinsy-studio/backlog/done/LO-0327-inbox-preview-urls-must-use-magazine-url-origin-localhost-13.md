---
id: LO-0327
title: Inbox preview URLs must use MAGAZINE_URL origin (localhost:13000 on Compose). Property chrome is host= query, not {prope
type: studio-evolution
status: done
phase: 6
priority: P1
estimate: S
assignee_role: UX Designer (Director)
team: 10-product-design-experience
skills: [UX-003, FE-002]
dependencies: []
files: [.quinsy-studio/knowledge-base/learnings/design/inbox.md, .quinsy-studio/CHANGELOG.md]
signal: process-gap
source: affiliate-platform
infusion_kind: layout
infusion_path: knowledge-base/learnings/design/inbox.md
train_skills: [UX-003, FE-002]
created: 2026-09-23
---

## Target
General rule lives in `knowledge-base/learnings/design/inbox.md` so the next project cannot repeat this. No client / product names in studio HQ titles or infused body (provenance `--source` / CHANGELOG only).

## Scope
Kind `layout`. Promote or author in `knowledge-base/learnings/design/inbox.md` using `knowledge-base/design_playbook.md`. Principle title must stay product-agnostic. Train skills: ['UX-003', 'FE-002']. Observation (provenance): Inbox preview URLs must use MAGAZINE_URL origin (localhost:13000 on Compose). Property chrome is host= query, not {property.host}:port — that hostname does not resolve locally.

## AC
- Inbox item LO-0327 generalized into `knowledge-base/learnings/design/inbox.md` (or matching playbook/skill/package)
- Infused text passes portability gate (no project folder names outside provenance)
- CHANGELOG.md updated
- LO moved to backlog/done/
