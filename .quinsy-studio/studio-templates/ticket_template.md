---
id: [PROJ-NNNN | LO-NNNN]
title: [Concise action instruction, e.g. "Enforce hash generation for tickets"]
type: [feature | bug | studio-evolution]
status: open
phase: [N]
priority: [P0/P1/P2/P3]
estimate: [S/M/L/XL]
assignee_role: [Director role, e.g. "Studio Automation Engineer (Director)"]
team: [Team folder, e.g. "09-studio-operations-evolution"]
skills: [Skill IDs, e.g. ["SO-001"]]
dependencies: [Ticket IDs, e.g. ["LO-0001"]]
created: [YYYY-MM-DD]
---

# [ID] — [Title]

## 1. Context & Value

> Unique context: current state vs. target state, so scope and goal are precise.

- **Current state:** [What is the case today? Concrete, e.g. "Ticket IDs are assigned manually, which leads to duplicates."]
- **Target state:** [What should apply after implementation? Measurable, e.g. "A script strictly generates unique IDs."]
- **Value:** [Why is this important? What loss/delay does it prevent?]

## 2. Technical Constraints

> Hard guardrails. The agent must NOT take the path of least resistance.

- **Modification scope:** [Exact paths, e.g. `studio-tools/generate_ticket_manifest.py` — ONLY here]
- **Rule:** [e.g. "Use the native Python `uuid` library. Do not install external packages."]
- **Rule:** [Further restrictions, e.g. "No changes to client projects."]
- **Playbook:** [`knowledge-base/backend_playbook.md` — mandatory]
- **Anti-Slop:** No AI clichés, no unnecessary external packages without an ADR.

## 3. Acceptance Criteria (BDD)

> Machine-testable behavior instead of implementation description.

- **Scenario 1:** [Name, e.g. "Creating a new ticket"]
  - **Given:** [Initial state, e.g. "The agent runs the intake script."]
  - **When:** [Action, e.g. "A new ticket is generated."]
  - **Then:** [Measurable result, e.g. "The ID starts with `LO-` followed by an 8-character alphanumeric hash and is unique."]

- **Scenario 2:** [Optional — further case]
  - **Given:** ...
  - **When:** ...
  - **Then:** ...

## 4. Definition of Done

- [ ] [e.g. "`run_qa_gate.py` runs without errors."]
- [ ] [e.g. "A test run provably produces no duplicates."]
- [ ] [e.g. "CHANGELOG.md is updated with the new ID logic."]
- [ ] QA gate green (`./studio gate <project> --level 5`)
- [ ] Anti-Slop audit: 0 violations

## Dependencies

- [Other tickets that must be finished first]

## Skills

- [Skill IDs to activate — for the agent's role/knowledge mapping]

## History

- [YYYY-MM-DD]: Ticket created (status: open)
