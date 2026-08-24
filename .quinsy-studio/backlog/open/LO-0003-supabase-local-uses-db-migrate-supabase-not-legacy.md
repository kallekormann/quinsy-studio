---
id: LO-0003
title: Supabase local uses db:migrate:supabase not legacy db:migrate on port 54320
type: studio-evolution
status: open
phase: 6
priority: P2
estimate: M
assignee_role: Studio Automation Engineer (Director)
team: 09-studio-operations-evolution
skills: ['SO-001']
dependencies: []
created: 2026-08-24
---

# LO-0003 — Supabase local uses db:migrate:supabase not legacy db:migrate on port 54320

## 1. Context & Value
- **Current state:** Observation: Supabase local uses db:migrate:supabase not legacy db:migrate on port 54320 (signal: tooling-gap, source: moody)
- **Target state:** The studio is improved so this signal does not recur.
- **Value:** The studio learns from projects (dual loop) and improves process, skills, or tooling.

## 2. Technical Constraints
- **Modification scope:** .quinsy-studio/process/, .quinsy-studio/studio-tools/, .quinsy-studio/teams/
- **Rule:** No changes to client projects (studio HQ only)
- **Rule:** Every change → CHANGELOG.md entry
- **Rule:** After implementation: skill-matching test + QA gate green
- **Rule:** Signal: tooling-gap — Source: moody
- **Playbook:** `process/learning-loop.md` (mandatory)
- **Anti-slop:** No AI clichés, no unnecessary external packages without an ADR

## 3. Acceptance Criteria (BDD)
**Scenario 1:** Studio improvement works
- **Given:** The learning signal (tooling-gap) occurs again
- **When:** The improved process/skill/tool is applied
- **Then:** The signal no longer occurs or is handled correctly

## 4. Definition of Done
- [ ] Discussed in meta retro
- [ ] Implemented (CHANGELOG.md entry)
- [ ] Skill-matching test green
- [ ] QA gate green

## Skills
- SO-001