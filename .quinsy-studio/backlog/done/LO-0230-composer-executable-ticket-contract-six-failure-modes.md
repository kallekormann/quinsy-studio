---
id: LO-0230
title: Ticket contract for small-model execution — six failure modes, each with a ticket-level antidote
type: studio-evolution
status: done
phase: 6
priority: P0
estimate: M
assignee_role: Process Director
team: 09-studio-ops
skills: [SO-002, PS-002]
dependencies: []
files: [.quinsy-studio/knowledge-base/ticket-authoring-playbook.md, .quinsy-studio/CHANGELOG.md]
signal: process-gap
source: affiliate-platform
infusion_kind: process
infusion_path: knowledge-base/ticket-authoring-playbook.md
train_skills: [SO-002, PS-002]
created: 2026-09-12
---

## Target
A studio-wide ticket-authoring playbook so tickets are executable by small/fast models without invention. Small models fail in six predictable ways; each is preventable by something the ticket author writes or omits: (F1) invention under ambiguity → verbatim artifacts (literal DDL/signatures/enums, never described); (F2) wrong location → exact paths per step; (F3) declaring done without verifying → literal Verify commands with expected output; (F4) scope drift → explicit Do-not-touch list naming files owned by parallel tickets; (F5) context loss → size cap (≤8 files, ≤400 lines, no XL — split instead); (F6) silent assumption → Stop-and-ask-if triggers converting assumptions into escalations.

## Scope
Kind `process`. Author `knowledge-base/ticket-authoring-playbook.md` with the six-failure-mode table, required ticket sections (Target / Read first ≤5 files / Plan one-step-per-file / Verbatim artifacts / Verify / AC / Do not touch / Stop and ask if / Out of scope), the sizing table, and the rule "if two tickets must agree on a name, the earlier writes it verbatim and the later quotes it." Add `executable_by: composer|opus|human` to the ticket frontmatter convention. Provenance: derived from scoping a 66-ticket programme for small-model execution (source project in CHANGELOG only).

## AC
- Playbook exists in `knowledge-base/` and is referenced from `process/ticket-team-allocation.md`
- Groom checklist gains: no XL tickets; Verify commands literal; verbatim-artifact rule
- Portability gate passes (no project names outside provenance)
- CHANGELOG updated; LO moved to done

## Status Change
- **From:** open
- **To:** done
- **Date:** 2026-09-12 23:50
- **Reason:** Infused ticket-authoring-playbook.md; groom checklist + ticket-workflow pointers; CHANGELOG provenance
