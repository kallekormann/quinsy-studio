---
id: LO-0314
title: Secret values must live outside agent-readable trees; schema files list names only
type: studio-evolution
status: done
phase: 6
priority: P0
estimate: M
assignee_role: Studio Automation Engineer (Director)
team: 09-studio-operations-evolution
skills: [SO-001, SO-002]
dependencies: []
files: [.cursorignore, .quinsy-studio/studio-tools/studio_isolation.py, .quinsy-studio/process/hq-isolation-sprints.md]
sprint: HQ-ISO-01
epic: HQ-ISO
signal: tooling-gap
source: studio-hq
infusion_kind: tooling
infusion_path: process/hq-isolation-sprints.md
train_skills: []
created: 2026-09-22
---

## Target
Agents can name env keys from env.example / env.schema.json. Values never appear in Cursor Read, Grep, or ticket receipts.

## Scope
Ignore/deny host secret dir and all projects/*/.env (including focused project). Keep names in committed schema. Do not invent a product brand. Cite process/hq-isolation-sprints.md. Sprint `HQ-ISO-01`. Epic: process/hq-isolation-sprints.md.

## AC
- Focused and sibling .env / secret-store paths are in Cursor deny/ignore so Read/Grep cannot open values
- Committed env.schema.json or .env.example documents names and purpose only
- A unit or fixture test proves schema has keys and no password-shaped values
- CHANGELOG records the rule

## Out of scope
Product features. Morning-brief dashboards. Reading env values into the agent transcript.
