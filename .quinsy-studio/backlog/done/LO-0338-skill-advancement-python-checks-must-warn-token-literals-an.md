---
id: LO-0338
title: Skill-advancement Python checks must warn token literals and native selects and require Eval on AI receipts
type: studio-evolution
status: done
phase: 6
priority: P1
estimate: L
assignee_role: Studio Automation Engineer (Director)
team: 09-studio-operations-evolution
skills: [SO-001, FE-001, FE-002, AI-004]
dependencies: [LO-0334, LO-0335, LO-0337]
files: [.quinsy-studio/studio-tools/]
sprint: HQ-SKILL-06
epic: HQ-SKILL
signal: tooling-gap
source: studio-hq
infusion_kind: tooling
infusion_path: process/hq-skill-advancement-sprints.md
train_skills: [SO-001]
created: 2026-09-24
---

## Target
Python checkers enforce distilled rules: token-literal warn (LO-0334), native `<select>` / missing kit-peer warn (FE-001), AI implement receipts require an Eval heading when skills include AI-001/AI-004.

## Scope
New `studio_skill_checks.py` + tests. Wire warn into `run_qa_gate.py` level 5. `move … done` may **warn** then, after tests, **refuse** AI receipts missing Eval (match receipt skill-QA pattern). Allowlists documented. IA CLI is LO-0333. Epic: process/hq-skill-advancement-sprints.md.

## AC
- unit tests for hex scan, select scan, eval heading
- gate 5 prints warnings; AI receipt rule documented in GETTING_STARTED via LO-0339
- CHANGELOG

## Out of scope
Failing entire gate 5 red on all hex matches day one. Scraping Figma.
