---
id: LO-0322
title: Approve gate N must refuse unless the previous human gate is already approved
type: studio-evolution
status: done
phase: 6
priority: P1
estimate: S
assignee_role: Studio Automation Engineer (Director)
team: 09-studio-operations-evolution
skills: [SO-001, SO-002]
dependencies: []
files: [.quinsy-studio/studio-tools/studio.py, .quinsy-studio/studio-tools/pre_impl_workflow.py]
sprint: HQ-ISO-03
epic: HQ-ISO
signal: tooling-gap
source: studio-hq
infusion_kind: tooling
infusion_path: process/hq-isolation-sprints.md
train_skills: []
created: 2026-09-22
---

## Target
./studio approve --gate 1 fails if gate 0 is not approved; gate 2 fails if gate 1 is not. Artifact validation still runs.

## Scope
Close the cmd_approve skip that execute already sequences. Sprint `HQ-ISO-03`. Epic: process/hq-isolation-sprints.md.

## AC
- Unit or CLI test: approve gate 1 with gate 0 pending returns False
- Re-approve of an already-approved gate still allowed
- CHANGELOG

## Out of scope
Product features. Morning-brief dashboards. Reading env values into the agent transcript.
