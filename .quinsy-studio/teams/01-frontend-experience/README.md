# Team 01 — Frontend Experience

Owns **shipping** UI after Team 10 (and Team 11 on commercial surfaces). Compose the gate-2 design system and studio-library. Do **not** invent IA, visual language, SEO programs, or experiment backlogs.

## Split

| Craft | Owner |
|-------|--------|
| What / why / states / brand / atomic | Team 10 |
| Hypothesis / commercial mechanics | Team 11 |
| SEO / AEO / campaign copy | Team 05 |
| Implementation (React, kit, a11y, perf, tests) | **Team 01** |

## Director-level roles

| Role | Level | Responsibilities |
|------|-------|------------------|
| **Frontend Architect** | Director | app shell, SSR/ISR, Core Web Vitals, PWA |
| **Frontend Engineer** | Lead | React, Tailwind, studio-library / Radix kit |
| **Frontend Security Engineer** | — | XSS/CSRF, token handling in the client |
| **QA Specialist** | Director | FE-006 + QA level 5; default-flow proof — **not** a separate Team 12 |

## Skills

| ID | Skill | Lead role | File |
|----|-------|-----------|------|
| FE-001 | UI Component Design | Frontend Engineer | `skills/ui-component-design.md` |
| FE-002 | Design System | Frontend Engineer (tokens already approved) | `skills/design-system.md` |
| FE-003 | Performance Optimization | Frontend Architect | `skills/performance-optimization.md` |
| FE-004 | Accessibility (a11y) | QA Specialist | `skills/accessibility.md` |
| FE-005 | PWA Implementation | Frontend Architect | `skills/pwa-implementation.md` |
| FE-006 | Frontend Testing | QA Specialist | `skills/frontend-testing.md` |
| FE-007 | Client Security | Frontend Security Engineer | `skills/client-security.md` |

Canon: [frontend-team-canon-ledger.md](../../knowledge-base/frontend-team-canon-ledger.md). Playbook: [frontend_playbook.md](../../knowledge-base/frontend_playbook.md). QA rubric: [qa-gate-playbook.md](../../knowledge-base/qa-gate-playbook.md).

## Phase participation

| Slice | Lead | Support |
|-------|-------|---------|
| Gate 0–1 | — | Frontend Architect (feasibility) |
| Gate 2 | — | FE-002 (tokens already from design track) |
| Implement | Frontend Engineer | FE-004, FE-006 |
| QA level 5 | QA Specialist | Frontend Engineer |

## Workflow

1. Design-track: wait for `design_status: approved` (spec + mocks exist).
2. `./studio library list` → `suggest` → `pull`. Confirm kit peers in `docs/setup/ui-kit.md`.
3. Stay on project tokens. Missing atom → design-track ticket, not a one-off CSS control.
4. Receipt + `./studio gate --level 5` before `move … done`.

## References

- `.quinsy-studio/process/ticket-team-allocation.md`
- `.quinsy-studio/studio-library/ui/`
- `./studio library pull <project> …`
