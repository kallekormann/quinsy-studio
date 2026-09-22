---
id: LO-0321
title: Product execute must INFORM open HQ learning counts and must not switch to STUDIO_LO mid-project
type: studio-evolution
status: done
phase: 6
priority: P1
estimate: S
assignee_role: Studio Automation Engineer (Director)
team: 09-studio-operations-evolution
skills: [SO-001, SO-002]
dependencies: []
files: [.quinsy-studio/studio-tools/studio_execute.py, .quinsy-studio/process/learning-loop.md]
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
While a product ticket is in flight, execute stays IMPLEMENT/PRODUCTION/HITL and INFORM: N portable LOs — open a HQ train session. STUDIO_LO only when the product loop is idle.

## Scope
Matches isolated HQ learning epic. Do not infuse playbooks from the product chat. Sprint `HQ-ISO-03`. Epic: process/hq-isolation-sprints.md.

## AC
- In-flight product execute output contains INFORM with an open-LO count when LOs exist
- decide_next_action does not return STUDIO_LO when implementation_in_flight is true
- CHANGELOG + learning-loop.md one paragraph

## Out of scope
Product features. Morning-brief dashboards. Reading env values into the agent transcript.
