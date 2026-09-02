---
id: LO-0018
title: Gemini model defaults go stale — pin Flash-Lite GA in ADR and smoke live Analyze before sprint review
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

# LO-0018 — Gemini model defaults go stale — pin Flash-Lite GA in ADR and smoke live Analyze before sprint review

## 1. Context & Value
- **Current state:** Observation: Gemini model defaults go stale — pin Flash-Lite GA in ADR and smoke live Analyze before sprint review (signal: process-gap, source: moody)
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
- [ ] Discussed in meta retro
- [ ] Implemented (CHANGELOG.md entry)
- [ ] Skill-matching test green
- [ ] QA gate green

## Skills
- SO-002