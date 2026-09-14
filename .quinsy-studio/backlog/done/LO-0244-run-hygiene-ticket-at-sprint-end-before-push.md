---
id: LO-0244
title: Run hygiene ticket at sprint end before push
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
created: 2026-09-13
completed: 2026-09-14
---

## Target
General rule lives in `process/` so the next project cannot repeat this. No client / product names in studio HQ titles or infused body (provenance `--source` / CHANGELOG only).

## Infused
Hygiene is a **sprint kind**, not a drive-by at the end of an implementation sprint: `./studio sprint <p> --kind hygiene`. Implementation batches use skill QA on the receipt; cadence review is every N implementation sprints. Production packets (`ACTION: PRODUCTION`, `approve-design` / `approve-arch`) keep unsigned work off the implementation board so hygiene and feature work do not starve each other.

## AC
- Inbox item LO-0244 generalized into `process/` (or matching playbook/skill/package)
- Infused text passes portability gate (no project folder names outside provenance)
- CHANGELOG.md updated
- LO moved to backlog/done/
