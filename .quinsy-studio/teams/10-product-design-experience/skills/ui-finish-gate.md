# Skill: UI Finish Gate

> The last design check before `MOVE_DONE` on a UI ticket. Capture the shipped screen at 1440 and 390 in every state the signed real-UI mock shows, put each one next to the signed mock screenshot, and return PASS or HOLD. The human signed mocks that look exactly like the app; this gate makes sure the app still looks exactly like the mocks. HOLD counts as a QA fail on the same retry counter. It is not a new human stop.

## Metadata

```
skill_id: UX-009
name: UI Finish Gate
team: 10-product-design-experience
lead_role: Design QA Reviewer
support_roles: [UX Designer, Brand Guardian, QA Specialist]
phases: [4, 5]
activation_triggers:
  - UI ticket with design_status approved reaches a green gate 5, before MOVE_DONE
  - UI ticket with design_status n/a that changes a screen in the gate-2b baseline
  - Phrases: "finish gate", "matches the mock", "mock fidelity", "shipped vs signed"
pairs_with: [UX-002, UX-006, UX-008, FE-001, FE-004, FE-006]
```

Default verdict: HOLD until a shipped screenshot exists for every signed state at both widths.

## When to load

- After gate level 5 is green on a UI ticket and before `MOVE_DONE`.
- After each fix of an earlier HOLD.
- Not during a design phase. Mocks are signed with `approve-design`; this gate checks the build against them.
- Not for backend-only tickets.

## Rules

### 1. The signed packet is the contract

Compare against `docs/design-specs/<TICKET>.md` (§2c states, §2d motion, §2e walkthrough), the signed mock **route** under `app/(design-mocks)/design-mocks/<TICKET>/` (reference behavior) and the screenshots in `docs/design-specs/mocks/<TICKET>/`. Do not write a new design contract. Do not judge taste. A ticket with `design_status: n/a` compares against the gate-2b baseline screen and the project tokens.

### 2. Same states, same widths, same names

Capture the shipped route for every state file in the mock folder, at 1440 and at 390. Use the same file names in `sprints/SPRINT-NN/qa/<TICKET>-finish/` (`hover-1440.png`, `open-390.png`). Drive hover, focus and pressed with Playwright (`hover()`, `focus()`, mouse down), not with CSS overrides. A missing state is a HOLD.

### 3. Audit in this order

1. **First read.** The object and the primary action the spec names are visible in the first viewport at both widths.
2. **Placement.** The control lives on the home surface from spec §2, inside the real shell, with the same neighbours as the mock.
3. **Hierarchy.** Visual weight follows the mock: heading, key signal, controls, supporting text.
4. **States.** Rest, hover, pressed, disabled and focus on controls. Open and closed on disclosures. Empty, loading and error on surfaces. Each one matches its mock.
5. **Narrow layout.** At 390 the job survives. Status and next action are not pushed below stacked desktop cards.
6. **Fidelity.** Project tokens, pulled studio-library components and literal spec copy. No hex values, no arbitrary colour classes, no hand-rolled modal or menu.
7. **Motion.** Enter and leave follow §2d tokens. With `prefers-reduced-motion` the same content shows with 0 ms durations. Skip only when the spec says `motion: off`.
8. **Behavior.** Run every §2e walkthrough step on the shipped surface and side by side on the signed mock route. Each interaction, transition and scenario state must behave the same; one row per step in the `## Behavior` table. A step that cannot be reproduced is a HOLD.

### 4. A difference is a HOLD unless it is recorded

Any visible difference from the signed mock is a HOLD, including one that looks better. A deliberate departure needs a reason on the receipt. A real design change is a design-track ticket for the next design phase. It is not a fix inside this ticket.

### 5. Every HOLD item is checkable

Name the state, the width and what differs. Name how to verify the fix. "Feels off" or "make it more polished" is not a finding. Do not invent findings to fill the report. Zero findings with complete captures is a PASS.

### 6. Keep list

List the decisions that already match the mock and must not regress during the fix: spacing rhythm, a focus ring, the empty-state copy, the 390 order. The next attempt re-checks the Keep list first.

### 7. HOLD is a QA fail, not a human stop

HOLD writes `sprints/SPRINT-NN/debug/<TICKET>.md` in Issue / Expected / Actual / Evidence / Fix / Files form and counts toward the same 3 attempts as a red gate. At 3 fails the ticket goes to `blocked` through the normal escalation. Never ask the human to re-sign a mock to make a HOLD pass.

### 8. Accessibility and states are part of finished

A missing focus state, an unlabeled control or an error state that shows no message is a HOLD here, even when the axe check (FE-004) is green.

## Workflow

1. Read the spec §1, §2, §2c, §2d and §2e. List every mock screenshot file.
2. Start the app with `./studio env <p> dev --approve` if it is not running. Capture and audit on the shipped route; use the `(design-mocks)` route only as the reference to compare behavior against.
3. Capture every state at 1440 and 390 into `sprints/SPRINT-NN/qa/<TICKET>-finish/`.
4. Put each pair side by side. Walk the audit order (rule 3), including the §2e behavior steps.
5. Write the Keep list and the HOLD items.
6. Write the verdict file and the receipt `## Evidence` lines.
7. PASS: continue to `MOVE_DONE`. HOLD: write the debug file and return to implement.

## Deliverables

`sprints/SPRINT-NN/qa/<TICKET>-finish-gate.md`:

```markdown
# UI finish gate — <TICKET>

Decision: PASS | HOLD
Attempt: 1/3
Spec: docs/design-specs/<TICKET>.md
Mock: docs/design-specs/mocks/<TICKET>/
Shipped: sprints/SPRINT-NN/qa/<TICKET>-finish/

## Comparison
| State | Width | Mock | Shipped | Result |
|-------|-------|------|---------|--------|
| rest  | 1440  | rest-1440.png | rest-1440.png | PASS |
| open  | 390   | open-390.png  | open-390.png  | HOLD |

## Required before PASS
1. open-390: menu covers the primary action → anchor menu to trigger per mock. Verify: open-390.png shows "Save" visible.

## Keep
- 8px rhythm between list rows (matches rest-1440)
- Focus ring token on the trigger

## Not compared
- <state, reason>
```

## Done evidence (receipt)

Receipt `## Evidence` on every UI ticket:

```markdown
## Evidence
- Finish gate: PASS (sprints/SPRINT-NN/qa/<TICKET>-finish-gate.md)
- Shipped states: sprints/SPRINT-NN/qa/<TICKET>-finish/*.png (n files, 1440 + 390)
- Departures from mock: none | <state: reason>
```

Every path must exist on disk. A state with no capture is NOT TESTED, which blocks PASS.

## Anti-patterns

- Comparing the `(design-mocks)` route with itself instead of the shipped route.
- Capturing only the rest state at 1440.
- Calling a difference "close enough" without recording it.
- A taste redesign during the gate.
- Inventing HOLD items to look thorough.
- Treating HOLD as a reason to ask the human for approval.
- Fixing a HOLD with inline styles or hex values that the gate-5 checks then warn about.

## Handoff

- **PASS → Team 01:** `MOVE_DONE` with the receipt `## Evidence` filled.
- **HOLD → Team 01:** the debug file and the Keep list; fix only the listed items.
- **Design gap → Team 10:** a design-track ticket when the signed mock cannot be built as drawn (`approve-arch --reject` path in the next cycle).
- **To SO-005:** the finish-gate file is evidence for the release reality check.

## References

- [design-spec-template.md](../../../knowledge-base/design-spec-template.md) — §2c real-UI mocks, §2d motion
- [design-system-compliance-checklist.md](../../../knowledge-base/design-system-compliance-checklist.md)
- [anti-slop-design-ux.md](../../../knowledge-base/anti-slop-design-ux.md)
- [motion-transitions.md](../../../knowledge-base/skill-extensions/motion-transitions.md)
- [hq-agency-agents-integration.md](../../../process/hq-agency-agents-integration.md) — L9
- Source: msitarzewski/agency-agents `design/design-ui-finish-gate-reviewer.md` (MIT), rewritten for real-UI mocks
