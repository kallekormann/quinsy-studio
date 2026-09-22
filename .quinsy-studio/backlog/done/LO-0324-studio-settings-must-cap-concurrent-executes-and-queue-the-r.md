---
id: LO-0324
title: Studio settings must cap concurrent executes and queue the rest
type: studio-evolution
status: done
phase: 6
priority: P1
estimate: M
assignee_role: Studio Automation Engineer (Director)
team: 09-studio-operations-evolution
skills: [SO-001, SO-002]
dependencies: []
files: [.quinsy-studio/studio-tools/studio_settings.py, .quinsy-studio/studio.settings.yaml, .quinsy-studio/studio-tools/studio.py]
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
parallel.max_projects (default 5) in HQ settings. A sixth ./studio execute prints queued and does not rewrite isolation for a new product.

## Scope
File-based lease under .quinsy-studio/.cache/execute-leases/. Settings key documented. Sprint `HQ-ISO-04`. Epic: process/hq-isolation-sprints.md.

## AC
- Sixth concurrent execute is refused or queued with a clear message
- Releasing a lease (execute HITL idle / explicit stop) allows the next project
- studio.settings.yaml documents the key; CHANGELOG

## Out of scope
Product features. Morning-brief dashboards. Reading env values into the agent transcript.
