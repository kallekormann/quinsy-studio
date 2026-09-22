---
id: LO-0318
title: Infusion and learn commits must abort on product nouns and serialize HQ JSON with a lock
type: studio-evolution
status: done
phase: 6
priority: P1
estimate: M
assignee_role: Studio Automation Engineer (Director)
team: 09-studio-operations-evolution
skills: [SO-001, SO-002]
dependencies: []
files: [.quinsy-studio/studio-tools/studio_infusion_delta.py, .quinsy-studio/studio-tools/studio_learnings_store.py, .quinsy-studio/studio-tools/studio_train.py]
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
infusion-delta, commit_principle, train-queue, inbox, and library registry refuse product folder names outside provenance and use a file lock so five chats cannot interleave writes.

## Scope
Reuse studio_portability.find_product_nouns. Lockfile under .quinsy-studio/.cache or similar gitignored path. Sprint `HQ-ISO-02`. Epic: process/hq-isolation-sprints.md.

## AC
- infusion-delta add with a project folder name in the body raises and does not write
- Concurrent-safe lock around train-queue.json and inbox.md (test or documented flock)
- CHANGELOG

## Out of scope
Product features. Morning-brief dashboards. Reading env values into the agent transcript.
