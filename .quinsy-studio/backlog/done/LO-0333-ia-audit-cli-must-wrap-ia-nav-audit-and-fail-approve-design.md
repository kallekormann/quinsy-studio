---
id: LO-0333
title: IA audit CLI must wrap ia_nav_audit and fail approve-design when nav counts are missing or over limit
type: studio-evolution
status: done
phase: 6
priority: P1
estimate: M
assignee_role: Studio Automation Engineer (Director)
team: 10-product-design-experience
skills: [UX-003, SO-001]
dependencies: []
files: [.quinsy-studio/studio-tools/design_math.py, .quinsy-studio/studio-tools/design_ticket_helpers.py, .quinsy-studio/teams/10-product-design-experience/skills/information-architecture.md]
sprint: HQ-SKILL-02
epic: HQ-SKILL
signal: tooling-gap
source: studio-hq
infusion_kind: tooling
infusion_path: knowledge-base/contextual-ia-playbook.md
train_skills: [UX-003]
created: 2026-09-24
---

## Target
Catalog has no real IA skill. Studio already has `ia_nav_audit`. Agents must run it. `approve-design` on `ia-navigation` tickets fails when spec omits top-level count / max depth or audit returns findings.

## Scope
`./studio ia-audit <project> <TICKET>` prints findings. Wire into approve-design for `ia-navigation` (and spec §2 nav tables when present). Tests. UX-003 skill points at the CLI. Epic: process/hq-skill-advancement-sprints.md.

## AC
- CLI exists and uses `design_math.ia_nav_audit`
- approve-design red when ia-navigation spec lacks counts or exceeds ≤7 / depth ≤3
- unit tests; CHANGELOG

## Out of scope
Rewriting contextual-ia-playbook wholesale. Product information architecture.
