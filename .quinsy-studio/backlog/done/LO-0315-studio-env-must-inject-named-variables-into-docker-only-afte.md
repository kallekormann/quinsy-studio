---
id: LO-0315
title: Studio env must inject named variables into Docker only after HITL approve
type: studio-evolution
status: done
phase: 6
priority: P0
estimate: L
assignee_role: Studio Automation Engineer (Director)
team: 09-studio-operations-evolution
skills: [SO-001, SO-002]
dependencies: [LO-0314]
files: [.quinsy-studio/studio-tools/studio.py, .quinsy-studio/studio-tools/init_project_env.py]
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
./studio env up|migrate|dev <project> --approve copies names to container env from the host secret store. Without --approve the command refuses.

## Scope
HITL is the approve flag plus a one-line intent (no values). Docker Compose for that project receives the env. Logs print key names only. Sprint `HQ-ISO-01`. Epic: process/hq-isolation-sprints.md.

## AC
- Missing --approve exits non-zero and prints the HITL command
- With --approve, Compose/container sees the named variables; stdout/stderr never contain secret values
- Tests cover refuse-without-approve and redaction
- CHANGELOG records the command

## Out of scope
Product features. Morning-brief dashboards. Reading env values into the agent transcript.
