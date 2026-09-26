---
id: LO-0341
title: Design-direction discovery must block prototype scaffold until gate 2a
type: studio-evolution
status: done
phase: 6
priority: P0
estimate: M
assignee_role: Product Designer (Director)
team: 10-product-design-experience
skills: [UX-004, UX-006, UX-008, SO-001]
dependencies: [LO-0340]
files: [.quinsy-studio/studio-tools/studio_design_discovery.py, .quinsy-studio/studio-tools/pre_impl_workflow.py]
sprint: HQ-DESIGN-GATES-01
epic: HQ-DESIGN-GATES
signal: process-gap
source: studio-hq
infusion_kind: process
infusion_path: knowledge-base/design-direction-playbook.md
train_skills: [UX-004]
created: 2026-09-26
---

## Target
After gate 1 the agent writes unanswered questions to `docs/design/discovery.md` and fills `design/DESIGN.md` from human answers. It does not scaffold `design/prototype` or indigo tokens until 2a is approved.

## AC
- validate 2a fails on stub DESIGN.md, unanswered discovery, default indigo, missing uniqueness
- `./studio design` refuses until 2a approved
- tests
