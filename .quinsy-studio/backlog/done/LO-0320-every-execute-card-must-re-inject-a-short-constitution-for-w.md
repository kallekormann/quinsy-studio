---
id: LO-0320
title: Every execute CARD must re-inject a short constitution for worlds, secrets, and HITL packets
type: studio-evolution
status: done
phase: 6
priority: P1
estimate: S
assignee_role: Studio Automation Engineer (Director)
team: 09-studio-operations-evolution
skills: [SO-001, SO-002]
dependencies: []
files: [.quinsy-studio/studio-tools/studio_execute.py, .quinsy-studio/studio-tools/test_studio_execute.py]
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
format_execute_step always prints a compact CONSTITUTION so long chats cannot rely on session-start AGENTS.md alone.

## Scope
Worlds, no sibling Read, no env values, HITL is spec/mocks or arch or env --approve — not a morning brief. Sprint `HQ-ISO-03`. Epic: process/hq-isolation-sprints.md.

## AC
- test_studio_execute asserts CONSTITUTION (or equivalent heading) in format_execute_step
- Lines mention secrets-as-names and packet HITL
- CHANGELOG

## Out of scope
Product features. Morning-brief dashboards. Reading env values into the agent transcript.
