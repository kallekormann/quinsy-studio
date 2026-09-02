---
id: LO-0029
title: Anti-slop magic-number 100 and sequential-await rules blocked Moody export PDF sprint mid-gate; document in frontend DoD and consider test-file exemptions or named-const guidance in validate_anti_slop docs
type: studio-evolution
status: done
phase: 6
priority: P2
estimate: M
assignee_role: Process Guard (Director)
team: 09-studio-operations-evolution
skills: ['SO-002']
dependencies: []
created: 2026-08-28
---

# LO-0029 — Anti-slop magic-number 100 and sequential-await rules blocked Moody export PDF sprint mid-gate; document in frontend DoD and consider test-file exemptions or named-const guidance in validate_anti_slop docs

## 1. Context & Value
- **Current state:** Observation: Anti-slop magic-number 100 and sequential-await rules blocked Moody export PDF sprint mid-gate; document in frontend DoD and consider test-file exemptions or named-const guidance in validate_anti_slop docs (signal: process-gap, source: moody)
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

## Infusion (2026-08-28)
- Documented S8/S9 + named-const / await-chain guidance in `process/anti-slop.md`
- Export/PDF DoD: non-empty file size + anti-slop on export paths in `frontend_playbook.md`
- Clearer messages in `validate_anti_slop.py` (no test-file exemption)
- CHANGELOG entry
