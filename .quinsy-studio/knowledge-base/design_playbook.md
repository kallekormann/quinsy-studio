# Design Playbook

> UX heuristics, cognitive load theory, 8pt grid, typography — the global design standards.

## Core principle

```
Design is not how it looks.
Design is how it works.
— Steve Jobs
```

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

## References

- `.quinsy-studio/process/lifecycle.md` — phase 2 (design blueprinting)
- `.quinsy-studio/knowledge-base/anti_ai_slop_protocol.md` — UI slop rules
- `.quinsy-studio/studio-library/ui/tokens/` — design tokens
