# Skill: UX Design (UX-002)

> Owns how a surface behaves: every state (empty, loading, error, success), the interaction pattern, the form and label rules, the microcopy, and the motion that carries a state change. Loads on forms, dialogs, settings, canvas chrome, and any flow with more than one state. The bar: a state matrix with no blank cell and copy that passes the error rubric.

## Metadata

```
skill_id: UX-002
name: UX Design
team: 10-product-design-experience
lead_role: UX Designer
support_roles: [Product Designer, UI/Visual Designer]
phases: [3, 4]
activation_triggers:
  - ticket_type: ui-new-component, ui-composition, workflow-explainer
  - Phrases: "form", "modal", "dialog", "settings", "error state", "empty state", "toast", "notification"
pairs_with: [UX-001, UX-005, FE-004, BE-004, UX-009]
```

Default verdict: a surface with an unspecified state is unfinished.

## When to load

- Any design-track ticket with user input, async work, or more than one state.
- Reviewing a flow for delight (empty / wait / first success / hard-work-done / buy).
- Not for: pure visual restyle of a signed, single-state surface.

## Rules

### 1. The state matrix is complete

Rest, hover, pressed, disabled, focus; open/closed for menus; empty/loading/error/success for surfaces. Every cell names copy and motion. `design_mocks_states_error` fails the packet otherwise.

### 2. Errors answer three questions

What happened (user's words), why (if known), what to do next (one action, with the control). See the rubric below; the same text rules apply to API `message` fields (BE-004). FE-004 covers how errors are announced.

### 3. Forms follow Wroblewski

Top-aligned labels, smart defaults, inline validation after blur, never lose typed input, one primary action. External: `ux-form-design`, `ux-interaction-patterns`.

### 4. Motion carries state

§2d names the transition for each state change with tokens and a reduced-motion path. No decorative motion. The `motion` and `flow` push-back codes land here.

### 5. Notifications respect the person

One notification, one next step, an off switch where it arrives, opt-in for marketing, no dark patterns, no inferred special-category data. Full list below.

### 6. Delight is audited, not added

Audit empty / wait / milestone moments with `delight-micro-interactions.md`. No joke loaders, no confetti on save.

## Workflow

1. Read §1 from UX-001, the catalog topics `interaction.md`, `craft.md`, and the push-back log for the surface.
2. Write the state matrix; write copy for each cell with the error rubric.
3. Write §2d motion with UX-005.
4. Check the real-UI mock renders every state; name the missing ones for the capture list.
5. Cite the catalog in §7b.

## Deliverables

- State matrix and interaction notes in the design spec.
- Form/label notes; error copy per field or action.
- §2d Motion (or `motion: off` from HITL).
- Delight audit table when reviewing a flow.

## Done evidence

```markdown
## Design skill
- UX-002: state matrix complete — docs/design-specs/<TICKET>.md
- UX-002: error copy passes rubric — docs/design-specs/<TICKET>.md §<n>
- UX-002: §2d motion + reduced-motion — docs/design-specs/<TICKET>.md
```

## Anti-patterns

- `Something went wrong` with no next step.
- A loading state that was never designed because "it is fast".
- Toasts for errors that belong next to a field.
- Confetti, joke loaders, guilt streaks, fake urgency.

## Handoff

- **To UX-005:** the state list that needs visual treatment.
- **To FE-001 / FE-004:** copy and announcements per state.
- **To BE-004:** error `message` text that follows the rubric.

## Deltas

- Studio addition: push-back codes `flow` and `motion` open lesson candidates that land as PB- bullets in `design-science-playbook.md`; the source methods assume a designer who remembers.

## Error-message rubric

Every error state in a spec and in shipped copy answers three things:

1. **What happened**, in the user's words. "Your card was declined", not "Payment error".
2. **Why**, when we know. "The card has expired." If we do not know, say so.
3. **What to do next.** One concrete action, with the control to do it. "Use another card" next to the card field.

Fail lines:

- A code or status alone (`Error 401`, `422`, `Something went wrong`). A code may follow the message for support.
- Blame ("You entered an invalid email"). Name the fix instead: "Enter an email like name@example.com".
- A message far from the field or action that caused it.
- Input lost after the error. Keep what the user typed.
- A dead end. Every error offers a way forward or a way back.

## Notification rules

Applies to in-app notices, toasts, email and push that the product sends.

- One notification, one actionable next step. No bare counts like "You have 14 unread items".
- The user picks channel and frequency. Respect quiet hours. When someone stops responding, send less, not on a louder channel.
- Every notification has an off switch where it arrives (unsubscribe link, settings link).
- Marketing email and push need prior opt-in consent (UWG §7, DSGVO). Transactional notices stay transactional.
- No dark patterns: no confirmshaming ("No thanks, I like losing money"), no fake urgency or countdowns, no guilt streaks, no pre-ticked boxes, no nagging after a "no".
- No variable-reward loops built to keep people checking.
- Do not infer health or other special-category data (ADHD, mood, stress, "overwhelmed") from behaviour to tune messages. That is Art. 9 DSGVO data. Adapt only to preferences the user set.
- Offer an exit with every prompt to continue ("Do another five, or stop for today?").

## References

- [interaction-ux-playbook.md](../../../knowledge-base/interaction-ux-playbook.md) · [delight-playbook.md](../../../knowledge-base/delight-playbook.md)
- [motion-transitions.md](../../../knowledge-base/skill-extensions/motion-transitions.md) · [figma-token-handoff.md](../../../knowledge-base/skill-extensions/figma-token-handoff.md) · [delight-micro-interactions.md](../../../knowledge-base/skill-extensions/delight-micro-interactions.md)
- External (optional): `ux-interaction-patterns`, `ux-form-design`
