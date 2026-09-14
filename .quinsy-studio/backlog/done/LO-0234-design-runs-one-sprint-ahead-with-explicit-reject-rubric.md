---
id: LO-0234
title: Design runs one sprint ahead of UI implementation, with an explicit written reject rubric
type: studio-evolution
status: open
phase: 6
priority: P1
estimate: S
assignee_role: UX Designer (Director)
team: 10-product-design-experience
skills: [UX-002, UX-006, SO-002]
dependencies: []
files: [.quinsy-studio/knowledge-base/design_playbook.md, .quinsy-studio/process/human-in-the-loop.md, .quinsy-studio/CHANGELOG.md]
signal: design-gap
source: affiliate-platform
infusion_kind: process
infusion_path: knowledge-base/design_playbook.md
train_skills: [UX-002, UX-006]
created: 2026-09-12
---

## Target
Two sprint-planning rules for design quality. (1) Lead time: any sprint containing UI implementation requires its design specs approved in the previous sprint — design blocks are scheduled sprint items, not preambles inside implement tickets; a multi-surface design block starts two sprints early. (2) Reject rubric written before design starts: automatic-reject triggers agreed with the human up front (mock not in-context; lorem ipsum/fake data; hand-rolled control where a primitive exists; rate without sample size; no empty state — at early product stages the empty state IS the primary state; no loading/error state; surface displays data the backend cannot supply; off-token-scale type/spacing; contrast/target-size failure; two metaphors for one concept). Cheaper to reject at spec review than at sprint review.

## Scope
Kind `process`. Add both rules to `knowledge-base/design_playbook.md`; reference from sprint-planning guidance in `process/human-in-the-loop.md`. Complements the existing §2/§2c lock rule (LO-0213/0218/0220/0222) — this adds the scheduling rule and the pre-agreed rubric.

## AC
- Lead-time rule and rubric template in design_playbook.md, product-agnostic
- Sprint planning checklist gains "design specs for next sprint's UI approved this sprint"
- Portability gate passes; CHANGELOG updated; LO moved to done
