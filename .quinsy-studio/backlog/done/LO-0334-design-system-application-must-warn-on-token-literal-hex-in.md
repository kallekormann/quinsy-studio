---
id: LO-0334
title: Design-system application must warn on token-literal hex in product UI and must not treat shadcn as the kit
type: studio-evolution
status: done
phase: 6
priority: P1
estimate: M
assignee_role: Frontend Architect (Director)
team: 01-frontend-experience
skills: [FE-002, UX-005, SO-001]
dependencies: [LO-0332]
files: [.quinsy-studio/knowledge-base/frontend_playbook.md, .quinsy-studio/studio-tools/run_qa_gate.py, .quinsy-studio/teams/01-frontend-experience/skills/design-system.md]
sprint: HQ-SKILL-03
epic: HQ-SKILL
signal: tooling-gap
source: studio-hq
infusion_kind: playbook
infusion_path: knowledge-base/frontend_playbook.md
train_skills: [FE-002]
created: 2026-09-24
---

## Target
FE-002 stays “apply approved tokens.” Catalog `ui-design-system` / `tailwind-patterns` distill into the frontend playbook. Gate 5 **warns** on hardcoded color literals in app UI. `shadcn` is not a studio-library substitute.

## Scope
Playbook Don’t: second palette; shadcn as source of truth. Optional allowlist for canvas engines that paint from CSS variables. Warn-only first (false positives). Epic: process/hq-skill-advancement-sprints.md.

## AC
- FE-002 skill points at new playbook bullets
- gate 5 reports token-literal warnings (documented allowlist)
- conflict matrix / registry: shadcn not pullable as kit
- CHANGELOG

## Out of scope
Failing gate 5 red on first ship. Rewriting studio-library components.
