---
id: LO-0325
title: Focus must not clobber another live chat isolation; one product tree per session
type: studio-evolution
status: done
phase: 6
priority: P1
estimate: M
assignee_role: Studio Automation Engineer (Director)
team: 09-studio-operations-evolution
skills: [SO-001, SO-002]
dependencies: [LO-0324]
files: [.quinsy-studio/studio-tools/studio_isolation.py, .quinsy-studio/studio-tools/studio.py]
sprint: HQ-ISO-04
epic: HQ-ISO
signal: tooling-gap
source: studio-hq
infusion_kind: tooling
infusion_path: process/hq-isolation-sprints.md
train_skills: []
created: 2026-09-22
---

## Target
A second ./studio focus while another project holds an execute lease warns and does not rewrite .cursorignore unless --force. Default remains one product visible per IDE window.

## Scope
Leases from LO-0324. Document: five products = five chats/windows, not one ignore list. Sprint `HQ-ISO-04`. Epic: process/hq-isolation-sprints.md.

## AC
- focus on B while A is leased prints the conflict and leaves A's isolation unless --force
- GETTING_STARTED states one chat per product
- CHANGELOG

## Out of scope
Product features. Morning-brief dashboards. Reading env values into the agent transcript.
