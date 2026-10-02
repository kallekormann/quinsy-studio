---
id: LO-0367
title: After architecture sign-off in a mixed sprint, do not run `--phase` if it untags
type: studio-evolution
status: done
phase: 6
priority: P1
estimate: S
assignee_role: Process Guard (Director)
team: 09-studio-operations-evolution
skills: [SO-002]
dependencies: []
files: [.quinsy-studio/knowledge-base/learnings/process/workflow.md, .quinsy-studio/CHANGELOG.md]
signal: process-gap
source: arthur
infusion_kind: process
infusion_path: knowledge-base/learnings/process/workflow.md
train_skills: []
created: 2026-09-30
---

## Target
General rule lives in `knowledge-base/learnings/process/workflow.md` so the next project cannot repeat this. No client / product names in studio HQ titles or infused body (provenance `--source` / CHANGELOG only).

## Scope
Kind `process`. Promote or author in `knowledge-base/learnings/process/workflow.md` using `process/learning-loop.md`. Principle title must stay product-agnostic. Train skills: none (playbook-only). Observation (provenance): After architecture sign-off in a mixed sprint, do not run `--phase` if it untags implementation work; keep the sprint tag until MOVE_DONE of the last ticket.

## AC
- Inbox item LO-0367 generalized into `knowledge-base/learnings/process/workflow.md` (or matching playbook/skill/package)
- Infused text passes portability gate (no project folder names outside provenance)
- CHANGELOG.md updated
- LO moved to backlog/done/
