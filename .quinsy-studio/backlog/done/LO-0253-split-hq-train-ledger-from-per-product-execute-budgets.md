---
id: LO-0253
title: Split HQ train studio-load ledger from per-product execute budgets
type: studio-evolution
status: done
phase: 6
priority: P1
estimate: M
assignee_role: Process Guard (Director)
team: 09-studio-operations-evolution
skills: [SO-002]
dependencies: []
files: [.quinsy-studio/studio-tools/studio_settings.py, .quinsy-studio/studio.settings.yaml, .quinsy-studio/CHANGELOG.md]
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
Studio HQ settings pay for train/infusion. Each product repo has `docs/studio.settings.yaml` for execute session/step caps. Existing trees `./studio settings <p> --init`. Usage files stay gitignored, not in retro.

## AC
- Inbox item LO-0253 generalized into `process/` (or matching playbook/skill/package)
- Infused text passes portability gate (no project folder names outside provenance)
- CHANGELOG.md updated
- LO moved to backlog/done/
