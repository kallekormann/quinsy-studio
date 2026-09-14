---
id: LO-0254
title: QA Prettier must ignore generated session usage JSON
type: studio-evolution
status: done
phase: 6
priority: P1
estimate: S
assignee_role: Studio Automation Engineer (Director)
team: 09-studio-operations-evolution
skills: [SO-001]
dependencies: []
files: [.quinsy-studio/studio-tools/run_qa_gate.py, .quinsy-studio/studio-tools/studio_settings.py, .quinsy-studio/CHANGELOG.md]
signal: tooling-gap
source: affiliate-platform
infusion_kind: tooling
infusion_path: studio-tools/
train_skills: [SO-001]
created: 2026-09-14
completed: 2026-09-14
---

## Target
General rule lives in `studio-tools/` so the next project cannot repeat this. No client / product names in studio HQ titles or infused body (provenance `--source` / CHANGELOG only).

## Infused
`ensure_prettierignore_cost_lines` plus gate Prettier `--ignore-path .prettierignore`. Skill SO-001: do not format the estimate ledger as a ticket fix. PB-20260914-002 on `process/gates.md`.

## AC
- [x] Inbox item LO-0254 generalized into `studio-tools/`
- [x] Infused text passes portability gate (no project folder names outside provenance)
- [x] CHANGELOG.md updated
- [x] LO moved to backlog/done/
