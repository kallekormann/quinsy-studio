# Motion transitions (UX-002, UX-005, FE-001, FE-002)

Small, purposeful motion is the default on product UI. A control that snaps open, a hover that pops, or a number that replaces itself in one frame reads as unfinished.

**HITL opt-out is the only off switch.** A human command in the ticket or spec, written as `motion: off`, sets every `--motion-duration-*` to `0ms` in the **project** token file. Do not strip the kit classes. Do not invent a second static kit.

`prefers-reduced-motion` is always on. Same content. Durations collapse to `0ms` through the tokens.

Tokens live in `studio-library/ui/tokens/design-tokens.css`. Match **usage**, not the nearest number. A 300ms modal close is still `--motion-duration-quick` (150ms) because it is a close.

## Default (no new skill ID)

| Surface | When | Open | Close | Scale | Easing |
|---------|------|------|-------|-------|--------|
| Button, badge, toggle, tabs, nav item | Hover, press, selected | 250ms | same | none | `--motion-ease-smooth-out` |
| Tooltip | Hint over a trigger | 150ms after 80ms | 150ms, no delay | `--motion-scale-small` (0.98) | `--motion-ease-out` |
| Menu, popover, select, combobox, hover card | Grows from its trigger | 250ms | 150ms | open `--motion-scale-medium` (0.97), close `--motion-scale-tiny` (0.99) | `--motion-ease-smooth-out` |
| Dialog, alert dialog | Centered, on top of the page | 250ms | 150ms | `--motion-scale-large` (0.96) both ways | `--motion-ease-smooth-out` |
| Sheet / panel | Slides into a region | 400ms | 350ms | none; travel on enter | `--motion-ease-smooth-out` |
| Accordion | Height grows and shrinks | 250ms | 250ms | none | `--motion-ease-smooth-out` |
| Switch thumb | Thumb travels | 250ms | same | none | `--motion-ease-bounce` |
| Checkbox mark | Check appears | 150ms | — | short scale-in | `--motion-ease-in-out` |
| Skeleton | Placeholder, then content | pulse, linear | reveal 400ms | none | `--motion-ease-linear` then `--motion-ease-in-out` |
| Toast | Notice from the edge | 400ms | 350ms | none | `--motion-ease-smooth-out` |

Origin for a menu or tooltip is the trigger (`transform-origin` from the kit). A dialog originates at its center. Close is faster than open, except accordion, tabs, icon swap, and text swap, which are one reversible motion. Never bounce a close. Never delay a close. A tooltip delay exists so a passing cursor does not fire it.

Color, background, shadow, and transform only. Not `transition: all`.

## Mock (Team 10)

The HTML mock imports the project token file and shows the closed frame and the open frame. The open frame uses the real transition. A screenshot of one resting frame is not the motion.

```html
<link rel="stylesheet" href="ui/tokens/design-tokens.css">
<div data-state="closed">Menu closed</div>
<div
  data-state="open"
  style="
    transform-origin: top center;
    opacity: 1;
    transform: scale(1);
    transition:
      opacity var(--motion-duration-fast) var(--motion-ease-smooth-out),
      transform var(--motion-duration-fast) var(--motion-ease-smooth-out);
  "
>
  Menu open
</div>
```

The closed frame starts at `opacity: 0` and `scale(var(--motion-scale-medium))`, and its transition duration is `--motion-duration-quick`. A dialog uses `--motion-scale-large` and `transform-origin: center`. Reduced motion: same markup, durations at `0ms`, copy still readable.

## Spec (Team 10)

Every design-track spec has **§2d Motion** before `./studio approve-design`. Name the surface, the open, the close (or the symmetric duration), the scale when there is one, and the reduced-motion path. `motion: off` skips the section.

**Spec-fail:** interactive UI with no §2d and no `motion: off`. Content that appears only after a tween finishes. A page-wide enter on every route. Desktop-only motion as the only way to read the screen.

## Named behaviors (only when §2d asks)

These are not extra kit components. Implement them with the tokens when the spec names the behavior.

| Behavior | What it does |
|----------|----------------|
| Field shake | The invalid field shifts on X by `--motion-distance-small`, then `--motion-distance-base`, in steps of `--motion-duration-micro`, then rests. The border returns to neutral. |
| Text swap | Outgoing text rises `--motion-distance-micro` and softens by `--motion-blur-small`. Incoming text rises into the same slot. Duration `--motion-duration-quick`, same both ways. |
| Icon swap | Two icons share one slot. They cross-fade with a small scale and `--motion-blur-small`. Duration `--motion-duration-fast`, same both ways. |
| Number update | Each changed digit re-enters with a short slide and `--motion-blur-small`. Stagger is `--motion-duration-stagger`. Cap the total stagger near 300ms. |
| Skeleton reveal | The placeholder pulses on `--motion-ease-linear`. Content then fades in over `--motion-duration-slow` as blur falls from `--motion-blur-small` to 0. |
| Success mark | One check fades and rises `--motion-distance-base` over `--motion-duration-very-slow`. Use it on a completed action. Never on a failure. It does not cover the page. |

## Implement (Team 01)

Pull the kit. The motion is already on Button, Dialog, Alert Dialog, Dropdown Menu, Popover, Select, Combobox, Context Menu, Menubar, Navigation Menu, Hover Card, Tooltip, Sheet, Drawer overlay, Accordion, Tabs, Switch, Checkbox, Toggle, Badge, Skeleton, Progress, and Sonner.

Overlays set `--tw-enter-scale` and `--tw-exit-scale` from the motion scale tokens so the existing enter/exit animation keeps its translate. Do not put a second fade on top.

**Implement-fail:** a second duration scale (`duration-100` on a new overlay, a hand-rolled modal fade, Framer or GSAP added to re-do the kit). A named behavior above that ignores the tokens.

## Don’t

- Page-wide enter animations as the default. Content stays readable at once.
- 3D card tilt, scroll hijack, or hiding copy behind a blur until the tween ends.
- `transition: all`, or animating `width` / `top` / `box-shadow` when transform and opacity will do.
- Confetti, a bounce on close, or a success motion on a failed action.
