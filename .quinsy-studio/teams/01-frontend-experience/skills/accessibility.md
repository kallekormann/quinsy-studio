# Skill: Accessibility (FE-004)

> Shipped UI that people can use with a keyboard, a screen reader, zoom and reduced motion. The target is WCAG 2.2 Level AA on every changed route. German and EU law sets the floor: the BFSG and the harmonised standard EN 301 549. Team 10 owns the semantics in the spec; this skill implements and proves them. An automated scan is necessary and not enough.

## Metadata

```
skill_id: FE-004
name: Accessibility
team: 01-frontend-experience
lead_role: QA Specialist
support_roles: [Frontend Architect, UX Designer]
phases: [4, 5]
activation_triggers:
  - Ticket contains "a11y", "Accessibility", "WCAG", "Screenreader", "BFSG", "Barrierefreiheit"
  - Any UI ticket before MOVE_DONE (receipt ## A11y)
  - New or changed form, dialog, menu, tabs, combobox or toast
pairs_with: [FE-006, FE-001, UX-002, UX-009, CL-003]
```

## When to load

- Every UI ticket in an implementation phase.
- When a design packet adds a custom widget. Check the spec names its keyboard pattern.
- When a commercial or consumer-facing product launches. CL-003 decides whether the BFSG applies.

## Rules

### 1. Know the standard and do not overstate it

- **BFSG** (Barrierefreiheitsstärkungsgesetz, obligations apply since 28 June 2025) covers consumer-facing services such as e-commerce and banking, with a micro-enterprise exemption for services. Whether it applies to a product is a CL-003 decision, recorded in the PRD.
- **EN 301 549** is the harmonised standard behind the BFSG and the EU Accessibility Act. Its web chapter incorporates WCAG 2.1 AA.
- **We build to WCAG 2.2 AA.** It contains 2.1 AA and adds focus-not-obscured, target size, dragging alternatives, consistent help, redundant entry and accessible authentication.
- A BFSG service publishes how it meets the requirements (an accessibility statement). CL-003 places it.

Never claim "conformant" from a scan. Write PASS, FAIL or NOT TESTED per check.

### 2. Native HTML first, studio-library for the rest

Use `<button>`, `<a href>`, `<label>`, `<fieldset>`, `<table>` and landmarks before ARIA. For dialogs, menus, listboxes, comboboxes, tabs and disclosures, pull the studio-library Headless primitive. It already implements the WAI-ARIA Authoring Practices pattern. Do not hand-roll one. No `div` with `onClick`. No ARIA that repeats what the element already says.

### 3. Keyboard walk on every changed flow

Unplug the mouse. Tab through the changed route from the top:

- Every control is reachable and works with Enter or Space.
- Tab order follows the visual order.
- Focus is always visible (2.4.7) and not hidden under a sticky header or a cookie banner (2.4.11).
- Escape closes dialogs, menus and popovers. Focus returns to the trigger.
- No keyboard trap, except a modal dialog, which releases on close.
- A skip link reaches `<main>`.

### 4. Contrast and colour

- Text at least 4.5:1, large text at least 3:1 (1.4.3).
- Controls, focus rings and meaningful icons at least 3:1 against their neighbours (1.4.11).
- Colour is never the only signal for an error, a status or a required field (1.4.1).

Check the project token pairs, not single hex values. A failing pair is a token fix in the project, not an inline override.

### 5. Forms and errors

- Every input has a visible `<label>`. A placeholder is not a label.
- Hints and errors link with `aria-describedby`. Required fields say so in text.
- On submit with errors, focus moves to an error summary or the first invalid field, and the message is announced.
- Status messages ("Saved") use a polite live region (4.1.3).
- Sign-in allows paste and password managers. No puzzle without an alternative (3.3.8).
- Do not ask for the same data twice in one flow (3.3.7).

Error copy follows the UX-002 error-message rubric.

### 6. Targets, zoom and reflow

- Pointer targets at least 24 × 24 CSS px, or enough spacing (2.5.8).
- Content reflows at 320 CSS px wide with no two-way scrolling (1.4.10). The 390 capture is not this test; zoom to 400 % at 1280.
- Text spacing overrides do not clip text (1.4.12).
- Anything done by dragging has a single-pointer alternative (2.5.7).

### 7. Motion

Honour `prefers-reduced-motion`: same content and layout, durations at 0 ms (spec §2d). Nothing flashes more than three times a second (2.3.1). Auto-moving content has a pause control (2.2.2).

### 8. Names, titles and route changes

Each page sets a unique `title` through Next.js metadata. The App Router announces route changes from it. One `<h1>` per page and no skipped heading levels. Images that carry meaning have alt text that says the purpose; decorative ones have `alt=""`. Icon-only buttons have an accessible name.

### 9. axe via Playwright on every changed route

Run `@axe-core/playwright` in the e2e suite on each changed route and each state the ticket adds (open dialog, error state):

```typescript
import AxeBuilder from '@axe-core/playwright';

const results = await new AxeBuilder({ page })
  .withTags(['wcag2a', 'wcag2aa', 'wcag21a', 'wcag21aa', 'wcag22aa'])
  .analyze();
expect(results.violations.filter((v) => ['critical', 'serious'].includes(v.impact ?? ''))).toEqual([]);
```

The planned gate check `a11y_axe` fails on `critical` or `serious` violations. List `moderate` and `minor` on the receipt.

### 10. Screen reader spot check

On a new custom widget, form or dialog, run VoiceOver (macOS Safari) through the changed flow. Check that role, name and state are announced and that errors are read. Record what you heard. NVDA with Firefox when a Windows machine is available.

### 11. No overlays

Third-party accessibility toolbars and overlay scripts do not fix the source and often break assistive technology. Fix the HTML, CSS and ARIA.

## Workflow

1. Read the spec states and the keyboard pattern for each new control.
2. Build with native elements and pulled Headless primitives.
3. Add the axe check to the ticket's Playwright spec.
4. Do the keyboard walk at 1440. Zoom to 400 % and check reflow.
5. Do the screen reader spot check when rule 10 applies.
6. Check reduced motion.
7. Fill the receipt `## A11y`.

## Deliverables

- An axe assertion in the e2e spec for each changed route and state.
- Token pairs that pass contrast, fixed in the project token file.
- Receipt `## A11y`.

## Done evidence (receipt)

```markdown
## A11y
- Standard: WCAG 2.2 AA (BFSG applies: yes | no | CL-003 open)
- axe (wcag2a…wcag22aa) on /settings, /settings#dialog-open · PASS (0 critical/serious; 1 moderate: <rule>)
- Keyboard walk /settings · PASS — order, visible focus, Esc returns focus
- Contrast: token pairs text/surface 7.1:1, focus/surface 3.4:1 · PASS
- Reflow 400 % at 1280 · PASS
- Reduced motion · PASS
- Screen reader (VoiceOver + Safari): dialog announced "Rename project, dialog"; error read · PASS | NOT TESTED (reason)
```

Results are PASS, FAIL or NOT TESTED. A NOT TESTED line names the reason.

## Anti-patterns

- A green Lighthouse or axe score offered as "accessible".
- A placeholder used as the only label.
- `outline: none` with no replacement focus style.
- A hand-rolled modal or dropdown next to the library primitive.
- `aria-hidden="true"` on a focusable element.
- Errors shown only in red.
- An overlay widget.
- Telling a client the BFSG requires something it does not, or skipping it because "we are small" without a CL-003 decision.

## Handoff

- **To UX-009:** focus and error states captured at both widths.
- **To SO-005:** the axe check runs on the journey routes on dev.
- **To Team 10:** a contrast or target-size failure in a token or kit component becomes a design-track ticket.
- **To CL-003:** the accessibility statement content.

## References

- [WCAG 2.2](https://www.w3.org/TR/WCAG22/) · [WAI-ARIA Authoring Practices](https://www.w3.org/WAI/ARIA/apg/)
- [EN 301 549](https://www.etsi.org/standards) · BFSG (Barrierefreiheitsstärkungsgesetz)
- [axe-core tags](https://github.com/dequelabs/axe-core/blob/develop/doc/API.md#axe-core-tags)
- [frontend_playbook.md](../../../knowledge-base/frontend_playbook.md) · [qa-gate-playbook.md](../../../knowledge-base/qa-gate-playbook.md) · [headless-ui-playbook.md](../../../knowledge-base/headless-ui-playbook.md)
- Source: msitarzewski/agency-agents `testing/testing-accessibility-auditor.md`, `engineering/engineering-section-508-specialist.md` (MIT), reframed from Section 508 to BFSG / EN 301 549
