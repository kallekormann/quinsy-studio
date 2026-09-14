---
id: LO-0246
title: Commit each product ticket; push origin/dev before review; main is HITL
type: studio-evolution
status: done
phase: 6
priority: P1
estimate: S
assignee_role: Process Guard (Director)
team: 09-studio-operations-evolution
skills: [SO-002]
dependencies: []
files: [.quinsy-studio/process/, .quinsy-studio/studio-tools/, .quinsy-studio/CHANGELOG.md]
signal: process-gap
source: studio
infusion_kind: process
infusion_path: process/
train_skills: []
created: 2026-09-14
completed: 2026-09-14
---

## Target
General rule lives in `process/` so the next project cannot repeat this. No client / product names in studio HQ titles or infused body.

## Infused
Product git is one commit per `MOVE_DONE`. Cadence review may push `origin/dev` only. Production/`main` requires HITL `--approve`. No Docker-vs-VPS heuristic — branch policy is enough.

## AC
- Inbox item LO-0246 generalized into `process/` (or matching playbook/skill/package)
- Infused text passes portability gate (no project folder names outside provenance)
- CHANGELOG.md updated
- LO moved to backlog/done/
