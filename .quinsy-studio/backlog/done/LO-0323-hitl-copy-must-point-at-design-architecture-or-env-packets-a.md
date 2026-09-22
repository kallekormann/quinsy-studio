---
id: LO-0323
title: HITL copy must point at design, architecture, or env packets and must not invent a morning-brief UX
type: studio-evolution
status: done
phase: 6
priority: P1
estimate: S
assignee_role: Studio Automation Engineer (Director)
team: 09-studio-operations-evolution
skills: [SO-001, SO-002]
dependencies: []
files: [.quinsy-studio/process/human-in-the-loop.md, .quinsy-studio/studio-tools/studio_execute.py]
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
Execute HITL commands name the file to review (spec/mocks, architecture packet, or env --approve intent). No ops morning-brief dashboard.

## Scope
Process + CARD strings only. Product UX sign-off stays approve-design. Sprint `HQ-ISO-03`. Epic: process/hq-isolation-sprints.md.

## AC
- human-in-the-loop.md states packet HITL and forbids a morning brief as the sign-off
- HITL execute lines for design/arch still cite the packet path
- CHANGELOG

## Out of scope
Product features. Morning-brief dashboards. Reading env values into the agent transcript.
