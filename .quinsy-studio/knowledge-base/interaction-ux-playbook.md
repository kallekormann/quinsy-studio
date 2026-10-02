# Interaction UX playbook (UX-002)

Interaction, forms, states, microcopy. Distilled from Cooper *About Face*, Nielsen’s 10 usability heuristics ([NN/g](https://www.nngroup.com/articles/ten-usability-heuristics/) — credit Jakob Nielsen), Wroblewski *Web Form Design*, Krug *Don't Make Me Think*, Apple HIG / Material *foundations* as **grammar** (not a visual clone), Laws of UX as a psychology index. UI writing: [anti-slop-design-ux.md](anti-slop-design-ux.md).

Checkout / paid forms also use [growth-mechanics-playbook.md](growth-mechanics-playbook.md). Delight (empty, wait, peak–end): [delight-playbook.md](delight-playbook.md) — not a substitute for these rules.

## Always

**Do**

- Show **system status** (idle, loading, success, error) in the control or its region — not only a toast on another page (Nielsen: visibility).
- **Recognition over recall:** choices visible (select, list, chips), not “remember the code.”
- **User control:** cancel, back, and escape from a transient UI; don’t trap focus in a fake modal.
- Match **user language** on labels (Krug: self-evident). Literal verbs: Save, Add, Delete — not “Let’s go.”
- Mock **rest, hover, pressed, disabled, focus**; disclosure **open/closed**; surfaces **empty/loading/error**.
- **Motion is on** unless the spec says `motion: off`. Open is an invitation (about 250ms); close gets out of the way (about 150ms). Name it in §2d. Extension: [skill-extensions/motion-transitions.md](skill-extensions/motion-transitions.md).
- After a hard job, **peak–end**: show what was made + next step (delight-playbook). Joke loaders are forbidden.

**Don’t**

- Hand-roll focus traps, Escape, or portals — studio-library / Headless / Radix.
- Disable the primary button with no explanation.
- Use placeholder text as the only label (Wroblewski).
- Animate through information the user needs to compare (Laws of UX: don’t hide cost of choice).
- **Scroll hijack** (take over wheel/touch), hide copy behind motion, or desktop-only parallax as the only way to read the story (`scroll-experience`). Prefer CSS `animation-timeline: view()`; GSAP/Lenis only via ADR. Honor `prefers-reduced-motion`.

**Spec / mock fail**

- Interactive control with only a rest frame.
- Interactive UI with no §2d Motion and no `motion: off`.
- Error copy that says “Something went wrong” with no field or next step (Nielsen: recover).
- Form that reloads blank after a validation error.
- Marketing/story scroll that cannot be read with reduced motion or without a pointer wheel.

## Nielsen — fail lines (credit Nielsen / NN/g)

| Heuristic | Fail the spec/mock when |
|----------|-------------------------|
| Visibility of status | Submit with no pending/success state |
| Match the real world | Labels are schema names (`user_uuid`) |
| User control | No cancel/back on a multi-step |
| Consistency | Two different buttons for the same action |
| Error prevention | Destructive with no confirm when undo is impossible |
| Recognition | Required format only in a tooltip after fail |
| Flexibility | Power path blocked (no keyboard on a dense tool) |
| Minimalism | Three competing primary CTAs |
| Error recovery | Error not next to the field that failed |
| Help | Complex legal/billing choice with zero in-context explanation |

## Forms (Wroblewski)

**Do:** Visible label; mark optional (or required) consistently; group related fields; primary action one; defaults that match the common case; keep typed input on error; mobile: correct `inputmode` / type.

**Don’t:** Reset the form on error. Multi-column labels that don’t line up with fields. “Confirm email” unless the cost of a typo is high.

**Fail:** Label missing. Password rules only after submit. Address fields that don’t match how the user would write them (over-split).

## Cooper — interaction

**Do:** Excise work the computer should do (don’t ask for data you already have). Posture-appropriate density. Disabled *with* a reason. Selection then action (or obvious default action).

**Don’t:** Implementation-model dialogs (“Update join table”). Mixing view and edit without a clear mode.

**Fail:** Empty state with no path to the first object (see also LO-0179 in design-science).

## Platform grammar (HIG / Material foundations)

**Do:** Use platform-standard patterns for back, sheets vs dialogs, destructive emphasis. Touch targets ≥44px (see design-science).

**Don’t:** iOS-only chrome on a dense desktop sovereign app, or vice versa, without a reason in §4 Platform.

## UI writing (with anti-slop)

**Do:** Name the object and the action. Errors: what happened + how to fix. Empty states: why it’s empty + the next control.

**Don’t:** Motivational fluff, “delight” copy that hides the action, joke errors.

**Fail:** CTA that does not match the result (“Learn more” that submits payment).
