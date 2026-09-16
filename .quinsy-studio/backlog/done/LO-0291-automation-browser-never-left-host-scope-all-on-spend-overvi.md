---
id: LO-0291
title: Automation browser never left host-scope `all` on Spend/Overview (same hang clas
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
Kind `tooling`. Promote or author in `studio-tools/` using `process/gates.md`. Principle title must stay product-agnostic. Train skills: ['SO-001']. Observation (provenance): Automation browser never left host-scope `all` on Spend/Overview (same hang class as live Inbox), so default-flow proof is PHPUnit + curl, not a click-through.

## AC
- Inbox item LO-0291 generalized into `studio-tools/` (or matching playbook/skill/package)
- Infused text passes portability gate (no project folder names outside provenance)
- CHANGELOG.md updated
- LO moved to backlog/done/

## Done
Infused gates/QA: host-scope hang is not API proof; HOST_ONLY_PATHS restores `?host=`.
