---
id: LO-0319
title: Abstraction verify must scan every real project folder name, not one hardcoded product
type: studio-evolution
status: done
phase: 6
priority: P1
estimate: S
assignee_role: Studio Automation Engineer (Director)
team: 09-studio-operations-evolution
skills: [SO-001, SO-002]
dependencies: []
files: [.quinsy-studio/studio-tools/studio_context.py, .quinsy-studio/studio-tools/test_verify_worlds.py]
sprint: HQ-ISO-02
epic: HQ-ISO
signal: tooling-gap
source: studio-hq
infusion_kind: tooling
infusion_path: process/hq-isolation-sprints.md
train_skills: []
created: 2026-09-22
---

## Target
./studio verify-abstraction flags any projects/<name> token in HQ body text the same way portability already lists project names.

## Scope
Replace Moody-only regex in verify_studio_abstraction with list_project_names(). Provenance allowlist stays. Sprint `HQ-ISO-02`. Epic: process/hq-isolation-sprints.md.

## AC
- A HQ fixture line naming a listed project folder fails verify-abstraction
- Provenance/source lines still pass
- CHANGELOG

## Out of scope
Product features. Morning-brief dashboards. Reading env values into the agent transcript.
