---
id: LO-0326
title: Guides must state Docker is required, one chat per product, and HQ train in a separate session
type: studio-evolution
status: done
phase: 6
priority: P1
estimate: S
assignee_role: Studio Automation Engineer (Director)
team: 09-studio-operations-evolution
skills: [SO-001, SO-002]
dependencies: [LO-0316, LO-0321, LO-0324]
files: [AGENTS.md, .quinsy-studio/GETTING_STARTED.md, README.md]
sprint: HQ-ISO-04
epic: HQ-ISO
signal: tooling-gap
source: studio-hq
infusion_kind: tooling
infusion_path: process/hq-isolation-sprints.md
train_skills: []
created: 2026-09-22
---

## Target
AGENTS.md, GETTING_STARTED, and README quality rules match the shipped CLI: Docker, secrets-as-names, INFORM learnings, packet HITL.

## Scope
Docs only after CLI from earlier sprints exists. Link process/hq-isolation-sprints.md. Sprint `HQ-ISO-04`. Epic: process/hq-isolation-sprints.md.

## AC
- AGENTS.md session start mentions Docker and no env values
- README quality rule for isolation/cost/learnings updated
- CHANGELOG

## Out of scope
Product features. Morning-brief dashboards. Reading env values into the agent transcript.
