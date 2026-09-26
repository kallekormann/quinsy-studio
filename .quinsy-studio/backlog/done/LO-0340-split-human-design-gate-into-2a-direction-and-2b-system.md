---
id: LO-0340
title: Split human design gate into 2a direction HITL and 2b system HITL
type: studio-evolution
status: done
phase: 6
priority: P0
estimate: L
assignee_role: Process Guard (Director)
team: 09-studio-operations-evolution
skills: [SO-002, UX-001]
dependencies: []
files: [.quinsy-studio/studio-tools/pre_impl_workflow.py, .quinsy-studio/studio-tools/studio.py, .quinsy-studio/studio-tools/studio_execute.py]
sprint: HQ-DESIGN-GATES-01
epic: HQ-DESIGN-GATES
signal: process-gap
source: studio-hq
infusion_kind: process
infusion_path: knowledge-base/design-direction-playbook.md
train_skills: [SO-002]
created: 2026-09-26
---

## Target
Human design is two signed packets. `./studio approve --gate 2` refuses. Sequential: 0 → 1 → 2a → 2b. Legacy `human_gates.2` approved still counts as design-complete.

## Scope
CLI parse 2a/2b. Execute HITL after each packet is ready. Sprint only after 2b (or legacy 2).

## AC
- `--gate 2` prints use 2a then 2b
- 2b requires 2a; 2a requires 1
- CHANGELOG
