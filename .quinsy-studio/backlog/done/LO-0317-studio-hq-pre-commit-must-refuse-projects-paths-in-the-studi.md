---
id: LO-0317
title: Studio HQ pre-commit must refuse projects paths in the studio index
type: studio-evolution
status: done
phase: 6
priority: P1
estimate: S
assignee_role: Studio Automation Engineer (Director)
team: 09-studio-operations-evolution
skills: [SO-001, SO-002]
dependencies: []
files: [.quinsy-studio/studio-tools/, .gitignore]
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
A studio-root commit that stages projects/ or a product tree aborts. verify-worlds remains the audit; the hook is the gate.

## Scope
Install via ./studio install. Do not require core.hooksPath if a committed hook sample + install copy is simpler. Sprint `HQ-ISO-02`. Epic: process/hq-isolation-sprints.md.

## AC
- Staging a fake projects/foo file fails the HQ pre-commit in a test or documented hook script
- ./studio install (or documented path) installs the hook
- CHANGELOG

## Out of scope
Product features. Morning-brief dashboards. Reading env values into the agent transcript.
