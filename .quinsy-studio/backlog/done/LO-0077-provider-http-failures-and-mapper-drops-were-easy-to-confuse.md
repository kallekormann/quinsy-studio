---
id: LO-0077
title: Provider HTTP failures and mapper drops were easy to confuse as the same empty S
type: studio-evolution
status: done
phase: 6
priority: P1
estimate: S
assignee_role: Process Guard (Director)
team: 09-studio-operations-evolution
skills: [SO-002]
dependencies: []
files: [.quinsy-studio/process/, .quinsy-studio/CHANGELOG.md]
signal: process-gap
source: moody
infusion_kind: process
infusion_path: process/
train_skills: []
created: 2026-09-07
---

## Target
General rule lives in `process/` so the next project cannot repeat this. No client / product names in studio HQ titles or infused body (provenance `--source` / CHANGELOG only).

## Scope
Kind `process`. Promote or author in `process/` using `process/learning-loop.md`. Principle title must stay product-agnostic. Train skills: none (playbook-only). Observation (provenance): Provider HTTP failures and mapper drops were easy to confuse as the same empty Suggested state before reason plumbing

## AC
- Inbox item LO-0077 generalized into `process/` (or matching playbook/skill/package)
- Infused text passes portability gate (no project folder names outside provenance)
- CHANGELOG.md updated
- LO moved to backlog/done/

## Status Change
- **From:** open
- **To:** done
- **Date:** 2026-09-07
- **Reason:** Duplicate of LO-0069/0074 — degraded copy outage vs filter-empty already in human-in-the-loop.md
