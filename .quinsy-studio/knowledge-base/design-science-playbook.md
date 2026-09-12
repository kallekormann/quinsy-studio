# Design science playbook

Theory-backed, **calculable** visual decisions for Team 10 (UX-005). Interaction/forms: [interaction-ux-playbook.md](interaction-ux-playbook.md). Product layers: [product-ux-playbook.md](product-ux-playbook.md).

## Visual hierarchy and layout (Do / Don’t / fail)

**Do**

- One dominant element per view (60–30–10: dominant surface, secondary chrome, accent for the one action).
- Type scale from a stated base × ratio (φ or modular) — write the steps in spec §4.
- Contrast: body text ≥4.5:1, large UI / large type ≥3:1 (WCAG). Fill the contrast table before `approve-design`.
- Line length ~45–75 characters for reading blocks. Touch/click ≥44×44px.
- Gestalt: proximity for related controls; same action = same button variant; figure vs ground (canvas vs chrome).

**Don’t**

- Equal-weight headings, cards, and CTAs (no hierarchy).
- Hardcoded hex in components when project tokens exist (UX-006).
- Decorative type smaller than the WCAG large-text cutoff used as body copy.

**Spec / mock fail**

- Contrast table empty or “pass” with no ratio.
- Marketing F-pattern claim with a centered wall of equal type.
- Accent color used on five competing actions.

---

## Gestalt (perception)

| Principle | Application |
|-----------|-------------|
| Proximity | Related controls share spacing group (8pt multiples) |
| Similarity | Same action = same button variant |
| Closure | Cards/containers imply boundaries |
| Continuity | Eye path follows F/Z pattern on marketing pages |
| Figure-ground | Canvas vs chrome contrast |

## Calculable rules

| Domain | Rule | Tool |
|--------|------|------|
| Contrast | Text ≥4.5:1, large UI ≥3:1 | `design_math.contrast_ratio` |
| Type scale | base × φ^n | `design_math.golden_scale` |
| Palette | 60-30-10 split | `design_math.palette_60_30_10` |
| IA | ≤7 top-level nav, depth ≤3 | `design_math.ia_nav_audit` |
| Touch | ≥44×44px targets | spec checklist |
| Measure | 45–75 characters line length | typography spec |

## Usability

Nielsen heuristics (see `design_playbook.md`): visibility, match, control, consistency, error prevention, recognition, flexibility, minimalism, error recovery, help.

**Empty states that depend on a prior step (LO-0179):** Name that step in the copy and provide a control that opens it. Do not hide the next action (create/start) only because the list is empty — show the empty state plus the path to fill it; reveal the next action once the dependency exists.

## Accessibility

WCAG 2.1 AA — load FE-004 + `ux-accessibility` external skill at implement.

Run `./studio approve-design` only after contrast table is filled with calculated ratios.

## Marketing scroll stories (LO-0118 / LO-0119)

**Lock the motion model in the design spec before implement** — sticky stack vs scroll-scrub vs discrete chapters. Changing mid-flight burns review patience and produces laggy or “stuck” feels.

DoD defaults for scroll-story / illustration tickets:

| Default | Why |
|---------|-----|
| **Fixed illustration height** (shared px/`dvh` across stages) | Stage swaps must not reflow the page |
| **No page-wide enter cascades** (`translateY` reveals on every section/frame) | One hero rise is enough; cascading rises make the page flip |
| **Native 1:1 scroll on sticky pins** | Smooth-scroll lerp / scrub lag fights sticky and feels stuck |
| **`prefers-reduced-motion`** | Opacity-only or static end pose |

Name the chosen model in §2c of the design spec; do not invent a second model during IMPLEMENT.

**Appear / throw-on DoD (LO-0123):** Design specs for scroll-enter illustrations must name **start state** (blur, opacity, scale) and **end tilt degrees** (and side rule) before IMPLEMENT — not “add a little tilt” alone.

**Sticky motion smoke (LO-0125):** Before marking sticky-stage motion tickets done, prototype cover progress on **one** section (current sharp → next blur-in → previous fade) and record the cover-range px in the design spec.
