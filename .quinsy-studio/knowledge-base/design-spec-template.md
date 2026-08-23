# Design spec template (Team 10)

Path: `projects/<project>/docs/design-specs/<TICKET-ID>.md`

## 1. Summary

One paragraph: user problem, solution, success metric.

## 2. Atomic inventory

| Level | Name | Library source | New? |
|-------|------|----------------|------|
| primitive | Dialog | pull: dialog | no |
| atom | Button | pull: button | no |
| molecule | … | compose: … | yes → studio-library first |

## 3. Design rationale

### Gestalt grouping

What reads as one unit (proximity, similarity, closure).

### Proportion & type

- Base size: __px
- Scale: φ (1.618) or modular ratio __
- Show calculated steps: __ → __ → __

### Color & contrast

| Foreground | Background | Ratio | WCAG AA |
|------------|------------|-------|---------|
| #___ | #___ | _._ | pass/fail |

60-30-10 allocation: dominant __ / secondary __ / accent __

### IA (if navigation changes)

- Top-level items: __ (target ≤7)
- Max depth: __ (target ≤3)

### Platform

- [ ] Desktop  - [ ] Mobile web  - [ ] Webapp  - [ ] Extension

## 3b. Aesthetic preset (Team 10 — required)

| Field | Value |
|-------|-------|
| **Preset slug** | e.g. `stripe-like-ui` or `project-brand-only` |
| **SKILL path** | `.quinsy-studio/knowledge-base/aesthetic-presets/<slug>/SKILL.md` |
| **Rationale** | Why this preset fits audience + surface |
| **Token mapping** | Preset colors → project token names |
| **Motion / Headless UI** | Transitions, focus, active states from preset |

Catalog: `knowledge-base/aesthetic-presets/README.md`

## 4. Storyboard (UX-007 — marketing / workflow)

| Step | Visual | Copy | CTA |
|------|--------|------|-----|
| 1 | Hero | … | … |

Narrative arc: setup → tension → resolution.

## 5. Handoff to Team 01

- Library pulls: `./studio library pull <project> …`
- Page type: `ui/page-types/…` or compose organisms
- Dark mode: required surfaces listed
