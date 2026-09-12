# Delight playbook (Teams 10 + 11)

Users remember how a product **felt** after the job: software, a site, or a buy. Delight is not a feature and **not a new ticket type**. It is a layer on craft we already own.

**No new skill ID.** A `UX-009 Delight` router would only fire when someone tagged it — so most specs would skip it, and “delight tickets” would ship confetti on broken flows. Load this playbook from UX-001/002/003/007 and GD-002. Subordinate to [anti-slop-design-ux.md](anti-slop-design-ux.md).

Sources (distilled): Don Norman *Emotional Design* (visceral / behavioral / reflective); NN/g [Three pillars of user delight](https://www.nngroup.com/articles/pillars-user-delight/); Kano (basic → performance → excitement; delighters **decay** into expectations — Jared Spool / Noriaki Kano); Peak–end rule (the end of a hard job is what people keep); *Good Services* (the service tells the truth).

The old extension `skill-extensions/delight-micro-interactions.md` is an **audit checklist** only. It must not recommend winky icons, joke loaders, or confetti on every save.

## Rule zero (Kano)

Meet **basic expectations** first: the control works, status is visible, the thing is findable, the price is honest. Extra polish on a failing job is **contempt**, not delight.

Then **performance** (faster, clearer, fewer steps). Then **excitement** (small, cheap, unexpected help) — which becomes expected later, so keep it cheap to maintain.

## Three levels (Norman / NN/g)

| Level | What people feel | Craft owner | Example that is allowed |
|-------|------------------|-------------|-------------------------|
| **Visceral** | It looks and moves like it was made on purpose | UX-005, UX-007, UX-006 | Spring on a drawer; preset motion; not a second palette |
| **Behavioral** | It was easy; I stayed in flow | UX-002, UX-001 | Keyboard in a sovereign tool; field error that names the fix |
| **Reflective** | I felt competent / this brand is for me | UX-001, UX-003, UX-007, Team 11 | First success named; receipt matches the promise |

**Deep delight** (NN/g): remove friction, enable flow, match aspiration. **Surface delight**: a moment (motion, line of copy, a well-timed empty state). Surface without behavioral competence is slop.

## Where to place a moment (not everywhere)

| Moment | Job | Delight that earns its place |
|--------|------|------------------------------|
| **Empty → first object** | Start | Name the gap + one control; optional quiet illustration from brand, not a joke |
| **Wait** | Loading | Determinate progress or skeleton of the *real* layout; `prefers-reduced-motion` |
| **Hard work done** (peak–end) | Submit, export, pay, publish | Status + what happened + next step. Optional *one* restrained success motion |
| **First success** | Aha | “You made X” with the artifact visible — not a tour overlay that blocks it |
| **Recovery** | Error | Specific, calm, reversible. Wit never hides the fix |
| **Buy / commit** | Checkout, plan, PDP add | Trust and completion (see below). No fake urgency |

**Don’t** sprinkle easter eggs on settings, legal, or destructive confirms.

## UI level (UX-002 / UX-005 / UX-008)

**Do**

- Feedback that the action *took* (checked state, count, new row) within ~100ms perceived.
- Motion that explains (open, close, what’s new) — 150–250ms, interruptible, reduced-motion alternative.
- Hover/focus that clarifies the target (library states), not a character that performs.

**Don’t**

- Confetti on Save, “Reticulating splines,” wink icons, emoji chrome (LO-0037).
- Blocking celebration that delays the next click.
- Personality copy that fails anti-slop (banned fluff, “Let’s go!”).

**Fail:** Success animation on a failed payment. Loader copy that lies about what is happening. Empty state with only humor and no CTA.

## Information architecture (UX-003)

IA delight is **feeling oriented and smart** — not a mascot in the sidebar.

**Do:** The capability lives where the task lives. Labels the user would say. “You are here” (title, selected nav). Search/filter when the list is long. The panoramic “I see the whole” on enter (wayfinding): structure is readable without a legend.

**Don’t:** Surprise nav that rearranges itself as a “delight.” Hidden gestures as the only path. Cute names that fail wayfinding (`Magic`, `Nexus`).

**Fail:** User cannot name where they are. Duplicate homes for one job. First-run delight overlay that covers the map they need.

## Service design (UX-001 + Team 11)

Buying and multi-touch journeys: delight is **the service keeping its word**.

**Do**

- Same next step in UI, email, and ops (*Good Services*).
- Peak–end: after pay/publish, show the artifact (order, plan, file) and the one next useful action.
- Anticipate a need without a new dark pattern (remember the cart, show total early, guest checkout).
- If a human must still do something, **name it** — a fake “you’re done” is the opposite of delight.

**Don’t:** Confetti that hides a pending review, delayed charge, or “we’ll email you.” Fake scarcity as excitement (Kano excitement ≠ deception).

**Fail:** Confirmation that doesn’t match cart. Success page with no receipt/total. Marketing promise the product UI cannot keep (Team 10+05).

## Spec (when it is required)

Add **Delight layer** (one table) when the ticket includes empty, wait, first success, hard-work-done, or a commercial end:

| Field | Value |
|-------|--------|
| **Kano** | Basic met? (yes/no — if no, no excitement) |
| **Level** | visceral / behavioral / reflective |
| **Moment** | empty / wait / peak-end / first success / recovery / buy |
| **What we add** | One concrete thing, or “none — basics only” |
| **Reduced motion / a11y** | How it degrades |

**Fail `approve-design` on commercial / marketing-page** if Growth intent has a success end-state with no peak–end (what they see after pay/submit). Other tickets: CARD + this playbook; do not block a settings spec for missing confetti.

## Team 11

Treat delight as **performance and excitement on a working funnel**, not a variant of “add sparkle.” Hypotheses may test a calmer success page vs a louder one — one change, still no dark patterns.
