---
id: LO-0268
title: Cache-busting that must happen after a write belongs on the plane that has the s
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
source: affiliate-platform
infusion_kind: process
infusion_path: process/
train_skills: []
created: 2026-09-15
---

## Target
General rule lives in `process/` so the next project cannot repeat this. No client / product names in studio HQ titles or infused body (provenance `--source` / CHANGELOG only).

## Scope
Kind `process`. Promote or author in `process/` using `process/learning-loop.md`. Principle title must stay product-agnostic. Train skills: none (playbook-only). Observation (provenance): Cache-busting that must happen after a write belongs on the plane that has the secret (Laravel/admin), not a browser fetch of internal env.

## AC
- Inbox item LO-0268 generalized into `process/` (or matching playbook/skill/package)
- Infused text passes portability gate (no project folder names outside provenance)
- CHANGELOG.md updated
- LO moved to backlog/done/

## Done
Infused `PB-20260915-003` on `process/human-in-the-loop.md`. Package already in `studio-library/packages/write-side-revalidate/` (LO-0266).
