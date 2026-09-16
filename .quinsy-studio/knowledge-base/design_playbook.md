# Design Playbook

> UX heuristics, cognitive load theory, 8pt grid, typography — the global design standards.

## Core principle

```
Design is not how it looks.
Design is how it works.
— Steve Jobs
```

## Spec and mocks are mandatory (before HITL)

Do not ask a human to `./studio approve-design` until:

1. `projects/<p>/docs/design-specs/<TICKET>.md` **exists and is filled** (a ticket stub is not enough)
2. HTML mocks live in `docs/design-specs/mocks/<TICKET>/` and **import this project's CSS tokens**
3. The mock is **in the product view** the work ships in (chrome/nav/neighbors — not an orphan artboard)
4. **Every state** is shown: rest/up, hover, pressed/down, disabled/inactive, focus; plus open/closed for menus; empty/loading/error for surfaces

Missing a state means implement will hallucinate it. The CLI rejects incomplete packets.

---

## UX heuristics (Nielsen/Norman)

| # | Heuristic | Description | Implementation |
|---|-----------|-------------|----------------|
| 1 | **Visibility of system status** | user always knows what is happening | loading states, feedback |
| 2 | **Match with the real world** | language of the user, not of technology | clear labels, icons |
| 3 | **User control** | undo, back, cancel | always possible |
| 4 | **Consistency & standards** | expected behavior | design system |
| 5 | **Error prevention** | design prevents errors | guards, confirmations |
| 6 | **Recognition over recall** | visible options | dropdowns > free text |
| 7 | **Flexibility & efficiency** | keyboard shortcuts for power users | accelerators |
| 8 | **Aesthetic & minimalism** | less is more | progressive disclosure |
| 9 | **Error detection & recovery** | clear error messages | specific messages |
| 10 | **Help & documentation** | help readily available | tooltips, context help |

---

## Cognitive load theory

### Three types of cognitive load

| Type | Description | Reduction |
|------|-------------|-----------|
| **Intrinsic** | difficulty of the task itself | simplify, step by step |
| **Extraneous** | bad design | clear structure, avoid redundancy |
| **Germane** | learning and understanding process | patterns, consistency, feedback |

### Implementation

```
✅ progressive disclosure (not everything at once)
✅ chunking (group information)
✅ visual hierarchy (important things first)
✅ whitespace (let it breathe)
✅ consistent patterns (recognition)
```

---

## 8pt grid system

```
Base unit: 8px

Spacing scale:
  xs:  4px   (0.5 × 8)
  sm:  8px   (1 × 8)
  md:  16px  (2 × 8)
  lg:  24px  (3 × 8)
  xl:  32px  (4 × 8)
  2xl: 48px  (6 × 8)
  3xl: 64px  (8 × 8)
```

### Application

- **Padding:** always a multiple of 8
- **Margin:** always a multiple of 8
- **Icon sizes:** 16, 24, 32, 48
- **Border radius:** 4, 8, 12, 16, 999 (pill)
- **Font size:** not on the grid, but line-height: 1.5 (body), 1.2 (headings)

---

## Typography system

### Scale

```css
--text-xs:   0.75rem;   /* 12px */
--text-sm:   0.875rem;  /* 14px */
--text-base: 1rem;      /* 16px */
--text-lg:   1.125rem;  /* 18px */
--text-xl:   1.25rem;   /* 20px */
--text-2xl:  1.5rem;    /* 24px */
--text-3xl:  1.875rem;  /* 30px */
--text-4xl:  2.25rem;   /* 36px */
--text-5xl:  3rem;      /* 48px */
```

### Font stack

```css
--font-sans: 'Inter', system-ui, -apple-system, sans-serif;
--font-mono: 'JetBrains Mono', 'Fira Code', monospace;
```

### Hierarchy

| Element | Size | Weight | Line height |
|---------|------|--------|-------------|
| Display | 48px | 800 | 1.1 |
| H1 | 36px | 700 | 1.2 |
| H2 | 24px | 600 | 1.3 |
| H3 | 20px | 600 | 1.4 |
| Body | 16px | 400 | 1.5 |
| Small | 14px | 400 | 1.5 |
| Caption | 12px | 400 | 1.5 |

---

## Color system

### Principle

```
60-30-10 rule:
  60% — dominant color (background)
  30% — secondary color (text, borders)
  10% — accent color (CTAs, highlights)
```

### Contrasts

| Element | Minimum contrast |
|---------|------------------|
| Normal text | 4.5:1 (WCAG AA) |
| Large text | 3:1 (WCAG AA) |
| UI components | 3:1 (WCAG AA) |
| Focus indicators | 3:1 (WCAG AA) |

---

## Responsive breakpoints

| Breakpoint | Width | Layout |
|------------|-------|--------|
| Mobile | < 640px | single column, full width |
| Tablet | 640-1024px | 2 columns |
| Desktop | > 1024px | centered content (max-width: 640-800px) |

### Mobile-first

```css
/* Base: mobile */
.element { padding: 16px; }

/* Tablet */
@media (min-width: 640px) {
  .element { padding: 24px; }
}

/* Desktop */
@media (min-width: 1024px) {
  .element { padding: 32px; max-width: 640px; margin: 0 auto; }
}
```

---

## Animation principles

### 12 principles of animation (Disney)

1. **Squash & stretch** — weight and inertia
2. **Anticipation** — preparation for movement
3. **Staging** — direct attention
4. **Straight ahead & pose to pose** — timing
5. **Follow through & overlapping action** — follow-through
6. **Slow in & slow out** — ease
7. **Arcs** — natural movements
8. **Secondary action** — accompanying movement
9. **Timing** — speed
10. **Exaggeration** — emphasis
11. **Solid drawing** — 3D in 2D
12. **Appeal** — likability

### CSS equivalents

```css
/* Spring physics */
transition: transform 0.3s cubic-bezier(0.68, -0.55, 0.265, 1.55);

/* Smooth ease */
transition: opacity 0.2s ease-in-out;

/* GPU-accelerated */
transform: translateZ(0); /* or will-change: transform */
```

### Sticky scroll stages — avoid SoftCard decks (LO-0117)

When a marketing scroll story advances stages (copy + illustration), **do not default to white SoftCard chrome + scale-recess stacking**. That reads as a card deck, not a continuous product story. Prefer **blur/opacity crossfade** (or bare stages on the page surface) while keeping sticky scroll motion. SoftCards stay for interactive pricing/FAQ — not for every scroll beat.

**Throw-on / cover numbers in the spec (LO-0126):** Design specs must list concrete start values (blur radius, opacity, scale) and end tilt degrees — and sticky **cover-range px** when using progress-driven stages — so IMPLEMENT does not invent them.

---

## Dual-surface delete consistency (LO-0158)

When the same user objects appear in **two clients** of one product (e.g. companion capture list and cloud inbox rail), **delete must mean the same thing on both**. Local-only delete while the cloud rail keeps the row (or the reverse) fails usability review — testers experience “it came back” / “two inboxes.” Prefer bidirectional delete (or an explicit “local draft only” label) before calling the surface ready.

## Accessibility (a11y)

### WCAG 2.1 AA

- [ ] All interactions keyboard-navigable
- [ ] Focus indicators visible
- [ ] Color contrasts at least 4.5:1
- [ ] All images have alt texts
- [ ] Forms have labels
- [ ] Error messages are specific
- [ ] Skip links present
- [ ] ARIA labels where needed

---

## Imagery mosaics — per-cell pixel budgets (LO-0068 / LO-0070 / LO-0073)

Editorial **bento** or solid-fill mosaics fail review when a low-resolution source occupies the **lead** (largest) cell — visible pixelation undermines mood. Placement by **selection order** (first picked → hero cell) is wrong when sources have mixed resolutions.

### Resolution budget (before layout is “done”)

1. **Measure each cell’s display budget** in CSS pixels at render size (width × height; account for `devicePixelRatio` when choosing source URLs).
2. **Assign a minimum pixel requirement per cell** — lead cell highest, corner accents lowest. Example heuristic: `minPixels = cellCssW × cellCssH × dpr²` (tune per product; document the constant in the ticket).
3. **Sort candidates by usable resolution** (short edge or area of the chosen rendition URL), not by pick order.
4. **Greedy assign** highest-res sources to highest-budget cells; overflow low-res items to small cells or solid-fill / duotone fallbacks — never upscale a thumbnail into the hero slot.
5. **DoD gate:** no cell may render a source whose native rendition is below its budget; smoke with at least one deliberately small Openverse thumb in the set.

### Adaptive bento

| Signal | Layout response |
|--------|-----------------|
| All sources high-res | Full mosaic; lead cell gets largest asset |
| Mixed resolutions | Re-rank placement; demote low-res to 1×1 tiles |
| All low-res | Prefer fewer, larger cells or solid-fill band — do not fake a dense grid |

### Anti-pattern

```
❌ images[0] → leadCell, images[1] → cell2, …  // selection order
✅ sortBy(resolution) → assignTo(cellsByDescendingBudget)
```

Pair with [contextual-ia-playbook.md](contextual-ia-playbook.md) — imagery epics need presentation placement DoD, not rail-only (LO-0065).

---

## Scrollbar gutter on public chrome (LO-0172)

When switching public sections, filters, or rubric chips, **content width must not shift** because a classic vertical scrollbar appears or disappears.

- Put `scrollbar-gutter: stable` on the **scrolling root** (`html`, or the well that actually scrolls).
- Treat reserved gutter as an AC on public layout / chrome tickets — not a follow-up nit.
- Overlay OS scrollbars still must not shove the masthead; classic gutters always reserve the slot.

```
❌ short page vs long page moves the well sideways
✅ same content box whether the bar is painted or not
```

---

## Plugin / extension cold-open chrome (LO-0182)

Signed-out first paint must show the **primary Login / connect** control — never a disabled refresh icon or empty soft button that only reveals login after click. Auth chrome and icon refresh polish belong in the **same** ticket when both ship in one review cycle (see LO-0185).

```
❌ Cold open → white/soft refresh → click → Login appears
✅ Cold open → Login (correct button style); after auth → tabs + icon refresh
```

## Dimmed icon chrome (LO-0187 / LO-0190 / LO-0193)

Toolbar / card **icon buttons** (sign-out, refresh, open-external) default to **dimmed / outline** controls that respect light and dark surfaces — not soft white (or coral-wash) discs that read as off-brand “white buttons.” Match outline/secondary chrome used for secondary actions; keep one clear primary CTA where needed. Host-plugin HTML (Figma, etc.) must use the same rule: `outline`/`ghost` + token ink/border — never `soft` accent-wash on icon-only controls.

```
❌ Soft white / wash disc icon buttons in plugin or dock chrome
✅ Dimmed outline icon buttons in light and dark; primary reserved for the main action
```

## Moving exports between rails (LO-0186)

When kit exports (brief, tokens, PDF) move from one rail to another, the **source rail must drop leftover helper cards and “go elsewhere” copy** in the same ticket. Icon-row polish on the destination rail is incomplete if the old rail still teases the moved actions.

```
❌ Destination gets icons; source still shows “Export from X…” card
✅ Destination owns actions; source list has no orphan deep-link card or hub helper line
```

## Export chrome copy (LO-0226)

Export / download tooltips and labels name the **deliverable** (filename and format: `theme.css`, `@theme`, `tokens.json`). Do not put framework names or version numbers in that chrome.

## List/detail titles (LO-0229)

Mail / inbox / library **list and detail titles truncate by default** (ellipsis). Do not wrap long titles onto extra rows as the default. Responsive mail (folders off-canvas, list/detail drawer under the project’s tablet breakpoint) belongs in AC when the ticket ships that chrome.

## Public index smoke (LO-0205)

Tickets that change public chrome (masthead, home feature, heroes, measure) must be smoked on **`/` at the RUNBOOK public host port** with published inventory — not only on an article slug. An empty index with a working inner route is a default-flow miss (LO-0203).

## Selected palette drives screen and print (LO-0201)

The **operator-selected** color set (token rail, brand MD, kit palette id) must be the same source for **on-canvas presentation and PDF/print**. Fixing fills only in a design-tool file (or a one-off CSS dump) is not done if the live surface still uses a default/inverted/fallback palette.

```
❌ Plugin/file colors look right; presentation + PDF still use the default kit
✅ One selected palette id → screen tokens and print/PDF colors
```

See also frontend WYSIWYG type stack (LO-0032).

## Zone-sourced kit rails (LO-0290)

When a canvas zone is the source of truth for a kit or inspector rail, reassemble from **current** zone children on add or delete. Do not rematch a stale stored palette that still contains removed items (`PB-20260916-003`).

```
❌ Operator deletes a zone swatch; the rail still shows that hex from last persist
✅ Zone children change → Color / type / imagery / mood reassemble from what is in the zone now
```

---

## References

- `.quinsy-studio/process/lifecycle.md` — phase 2 (design blueprinting)
- `.quinsy-studio/knowledge-base/anti_ai_slop_protocol.md` — UI slop rules
- `.quinsy-studio/studio-library/ui/tokens/` — design tokens

## Design runs one sprint ahead (LO-0234)

- **PB-20260914-001** helpful=0 harmful=0 :: **Lead-time rule:** any sprint containing UI implementation requires its design specs approved in the **previous** sprint. Design blocks are scheduled sprint items, not preambles inside implement tickets. A multi-surface design block starts **two** sprints early.

**Reject rubric before design starts:** agree automatic-reject triggers with the human up front — cheaper to reject at spec review than at sprint review. Rubric template:

- Mock not in-context (not embedded in the real product view)
- Lorem ipsum / fake data
- Hand-rolled control where a primitive exists
- Rate shown without sample size
- No empty state — at early product stages the empty state IS the primary state
- No loading/error state
- Surface displays data the backend cannot supply
- Off-token-scale type/spacing
- Contrast or target-size failure
- Two metaphors for one concept

Complements the §2/§2c lock rule (LO-0213/0218/0220/0222): this adds the scheduling rule and the pre-agreed rubric.

## Symlinked file layouts must stay complete (LO-0247)

- **PB-20260914-002** helpful=0 harmful=0 :: When a repo mirrors files via symlinks (e.g. root config/entry files pointing into an app subtree), any file **referenced by** a symlinked file must also be reachable from the symlink's location. Adding a sibling module without its matching symlink breaks type-checking/builds at the root while the subtree stays green. Rule: when adding a file next to a symlink target, add the mirror symlink in the same change — or better, remove the mirror layout.

## Gold-path chrome matches live chrome (LO-0293)

When a ticket removes an operator control, update gold-path tests in the **same** change. Do not leave the suite asserting a control operators no longer see (`PB-20260916-004`).

```
❌ Chrome ticket removes Trash; gold-path still expects a trash control until a later pin ticket
✅ Gold-path asserts the chrome that shipped — remove or rewrite the assertion with the control
```

## Deltas

- **PB-20260916-006** helpful=1 harmful=0 :: Canvas or other non-DOM paint must use the same dark/light ink as html.dark CSS, never a hardcoded light-theme hex. CSS variables do not reach canvas/Konva fills unless resolved to hex first.
- **PB-20260916-005** helpful=0 harmful=0 :: When a chrome ticket removes or rewires a control, update the gold-path source test in the same change. Do not leave the suite asserting the old button.
- **PB-20260916-004** helpful=2 harmful=0 :: Gold-path tests for operator chrome must match the live chrome. When a ticket removes a control, update the gold path in the same change; do not leave the suite asserting a control operators no longer see.
- **PB-20260916-003** helpful=0 harmful=0 :: When a canvas zone is the source of truth for a kit or inspector rail, reassemble from current zone children on add or delete. Do not rematch a stale stored palette that still contains removed items.
- **PB-20260916-002** helpful=0 harmful=0 :: Left-rail demo profiles and app-chrome identity are separate surfaces. When the operator asks to remove all hardcoded profiles, ticket both the column and the shell chip.
- **PB-20260916-001** helpful=0 harmful=0 :: A sprint that ships operator chrome or identity is not backend-only. Cadence review stays on the UI path; do not skip review because ticket_type is feature.
- **PB-20260915-004** helpful=0 harmful=0 :: Host helpers for chrome and for catalog or page lookup must share one tenant key. Two resolvers for the same property split masthead from inventory.
- **PB-20260915-003** helpful=0 harmful=0 :: Chrome and page lookup must share one host resolver. Do not trust the raw Host header on a preview origin when chrome already resolved the public hostname — layout and Start will disagree.
- **PB-20260915-002** helpful=0 harmful=0 :: Close a canvas-chrome sprint when those tickets are done; keep export/MD deliverable work in a later sprint.
- **PB-20260915-001** helpful=1 harmful=0 :: Do not mix canvas chrome with long export/MD deliverable tickets in one implementation sprint; finish gold-path product bugs first.
