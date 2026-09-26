---
id: LO-0342
title: Gate 2b must require project CSS kit and must not promote product look to studio-library
type: studio-evolution
status: done
phase: 6
priority: P0
estimate: M
assignee_role: UI/Visual Designer (Director)
team: 10-product-design-experience
skills: [UX-005, FE-002, SO-001]
dependencies: [LO-0340, LO-0341]
files: [.quinsy-studio/studio-tools/pre_impl_workflow.py, .quinsy-studio/studio-tools/studio.py, .quinsy-studio/studio-tools/library_manager.py]
sprint: HQ-DESIGN-GATES-01
epic: HQ-DESIGN-GATES
signal: process-gap
source: studio-hq
infusion_kind: process
infusion_path: knowledge-base/atomic-design-playbook.md
train_skills: [UX-005]
created: 2026-09-26
---

## Target
2b handoff is project-owned: CSS tokens, Tailwind mapped to variables, coded atoms/molecules/organisms, sticker sheet with inventory children (not titles only), mocks on those tokens. Approving 2b does not merge product look into studio-library.

## AC
- 2b validator refuses title-only sticker and indigo scaffold
- `approve --gate 2b` generates tickets, does not call promote_design_to_library
- CHANGELOG
