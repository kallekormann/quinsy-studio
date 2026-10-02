---
id: LO-0369
title: UI specs and the studio kit use motion unless HITL turns it off
type: studio-evolution
status: done
phase: 6
priority: P1
estimate: M
assignee_role: UI/Interaction Designer (Director)
team: 10-product-design-experience
skills: [UX-002, UX-005, FE-001, FE-002]
dependencies: []
files:
  - .quinsy-studio/knowledge-base/skill-extensions/motion-transitions.md
  - .quinsy-studio/studio-library/ui/tokens/design-tokens.css
  - .quinsy-studio/skill-dependencies.json
signal: library-gap
source: hq
infusion_kind: ui-component
infusion_path: knowledge-base/skill-extensions/motion-transitions.md
train_skills: [UX-002, UX-005, FE-001, FE-002]
created: 2026-10-02
---

## Target

Small transitions are part of a finished UI. Team 10 names them in every design spec. Team 01 inherits them from the studio kit. A human can turn motion off with one line.

## Scope

- Subscribe `Jakubantalik/transitions.dev` (`transitions-dev`, `transitions-polish`). Distill. Do not republish the `t-*` catalog.
- `--motion-*` tokens and kit components use the scale.
- `approve-design` requires §2d Motion unless `motion: off`.

## Done when

- Extension, registry, conflict matrix, and playbook pointers exist.
- Core kit controls reference the tokens.
- `design_spec_motion_error` tests pass.
