---
id: LO-0316
title: Gate, migrate, and product boot must require Docker and must not print secret values
type: studio-evolution
status: done
phase: 6
priority: P0
estimate: M
assignee_role: Studio Automation Engineer (Director)
team: 09-studio-operations-evolution
skills: [SO-001, SO-002]
dependencies: [LO-0315]
files: [.quinsy-studio/studio-tools/run_qa_gate.py, .quinsy-studio/GETTING_STARTED.md]
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
If Docker is missing, execute/gate/env stop with an install hint. Runtime uses the project Compose stack, not host-exported secrets in the agent transcript.

## Scope
Detect docker compose. Fail closed. Do not skip by reading .env into the chat. Sprint `HQ-ISO-01`. Epic: process/hq-isolation-sprints.md.

## AC
- No Docker → command fails with install instructions, not a host fallback that cats .env
- gate/migrate/dev documented as Docker-backed
- Smoke/gate output redacts values matching secret patterns
- CHANGELOG + GETTING_STARTED one-liner

## Out of scope
Product features. Morning-brief dashboards. Reading env values into the agent transcript.
