---
id: LO-0235
title: Every sprint ships a proof surface; truth before polish when surfaces display invented data
type: studio-evolution
status: open
phase: 6
priority: P2
estimate: S
assignee_role: Process Director
team: 09-studio-ops
skills: [SO-002, PS-002]
dependencies: []
files: [.quinsy-studio/knowledge-base/sprint-planning-playbook.md, .quinsy-studio/CHANGELOG.md]
signal: process-gap
source: affiliate-platform
infusion_kind: process
infusion_path: knowledge-base/sprint-planning-playbook.md
train_skills: [SO-002]
created: 2026-09-12
---

## Target
Two sprint-scoping rules. (1) Proof surface: no sprint is purely internal — infrastructure sprints ship an observable artifact (a smoke test that defines "the product works", a receipt, a minimal honest view) so progress is verifiable rather than asserted; the loop-closure smoke test pattern (action → assert the full chain of effects) doubles as the product's definition of working. (2) Truth before polish: where an existing surface displays invented/placeholder data, the honest (often emptier) version ships before any refinement, and the human is told in advance that it will look like a regression — with designed empty states so honesty reads as intentional. Also: two parallel tickets in one sprint must have disjoint file lists.

## Scope
Kind `process`. Author or extend `knowledge-base/sprint-planning-playbook.md` with both rules plus the disjoint-files rule. Product-agnostic; provenance in CHANGELOG only.

## AC
- Rules in the playbook; sprint proposal template gains a "proof surface" line
- Portability gate passes; CHANGELOG updated; LO moved to done
