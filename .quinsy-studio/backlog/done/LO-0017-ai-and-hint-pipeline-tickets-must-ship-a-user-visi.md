---
id: LO-0017
title: AI and hint-pipeline tickets must ship a user-visible surface in the same sprint — adapter/API alone fails review
type: studio-evolution
status: done
phase: 6
priority: P2
estimate: M
assignee_role: Process Guard (Director)
team: 09-studio-operations-evolution
skills: ['SO-002']
dependencies: []
created: 2026-08-26
---

# LO-0017 — AI and hint-pipeline tickets must ship a user-visible surface in the same sprint — adapter/API alone fails review

## 1. Context & Value
- **Current state:** Observation: AI and hint-pipeline tickets must ship a user-visible surface in the same sprint — adapter/API alone fails review (signal: process-gap, source: moody)
- **Target state:** The studio is improved so this signal does not recur.
- **Value:** The studio learns from projects (dual loop) and improves process, skills, or tooling.

## 2. Technical Constraints
- **Modification scope:** .quinsy-studio/process/, .quinsy-studio/studio-tools/, .quinsy-studio/teams/
- **Rule:** No changes to client projects (studio HQ only)
- **Rule:** Every change → CHANGELOG.md entry
- **Rule:** After implementation: skill-matching test + QA gate green
- **Rule:** Signal: process-gap — Source: moody
- **Playbook:** `process/learning-loop.md` (mandatory)
- **Anti-slop:** No AI clichés, no unnecessary external packages without an ADR

## 3. Acceptance Criteria (BDD)
**Scenario 1:** Studio improvement works
- **Given:** The learning signal (process-gap) occurs again
- **When:** The improved process/skill/tool is applied
- **Then:** The signal no longer occurs or is handled correctly

## 4. Definition of Done
- [x] Discussed in meta retro (SPRINT-42)
- [x] Implemented (CHANGELOG.md entry)
- [x] Skill-matching test green (n/a docs)
- [x] QA gate green (n/a docs)

## Skills
- SO-002