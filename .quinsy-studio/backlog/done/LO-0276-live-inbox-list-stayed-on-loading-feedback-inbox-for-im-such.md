---
id: LO-0276
title: Live Inbox list stayed on “Loading feedback inbox…” for im-sucher.com during bro
type: studio-evolution
status: done
phase: 6
priority: P1
estimate: S
assignee_role: Studio Automation Engineer (Director)
team: 09-studio-operations-evolution
skills: [SO-001]
dependencies: []
files: [.quinsy-studio/studio-tools/, .quinsy-studio/CHANGELOG.md]
signal: tooling-gap
source: affiliate-platform
infusion_kind: tooling
infusion_path: studio-tools/
train_skills: [SO-001]
created: 2026-09-16
---

## Target
General rule lives in `studio-tools/` so the next project cannot repeat this. No client / product names in studio HQ titles or infused body (provenance `--source` / CHANGELOG only).

## Scope
Kind `tooling`. Promote or author in `studio-tools/` using `process/gates.md`. Principle title must stay product-agnostic. Train skills: ['SO-001']. Observation (provenance): Live Inbox list stayed on “Loading feedback inbox…” for im-sucher.com during browser checks, so some AC was proven by tests rather than a full click-through of the message pane.

## AC
- Inbox item LO-0276 generalized into `studio-tools/` (or matching playbook/skill/package)
- Infused text passes portability gate (no project folder names outside provenance)
- CHANGELOG.md updated
- LO moved to backlog/done/

## Done
Infused `PB-20260916-001` on `process/gates.md`; receipt stub + SO-001 toolbox; qa-gate-playbook Don't.
