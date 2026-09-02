# Design spec template (Team 10)

Path: `projects/<project>/docs/design-specs/<TICKET-ID>.md`

Load before writing: [contextual-ia-playbook.md](contextual-ia-playbook.md), [workflow-definition-playbook.md](workflow-definition-playbook.md), [design-system-compliance-checklist.md](design-system-compliance-checklist.md).

> **LO-0038:** A large mock HTML pack does **not** satisfy `approve-design` by itself. Fill **§2 Context & placement** and **§2c Experienceable in-context mocks** (with real shell / asset paths / states / anti-orphan) as soon as the first composed mock exists — preferably before the catalog is "done."


## 1. Summary

One paragraph: user problem, solution, success metric.

## 2. Context & placement (required)

> **Gate:** `./studio approve-design` warns if this section is missing.  
> Playbook: `knowledge-base/contextual-ia-playbook.md`

### User intent & surface

| Field | Value |
|-------|-------|
| **Primary intent** | What is the user trying to do? |
| **Home surface** | Where this capability lives (route/dialog/panel) |
| **Why not elsewhere** | Reject alternate surfaces (e.g. "not Share — presentation context") |

### Cross-surface map (if 2+ surfaces touched)

| Capability | Home surface | Not on |
|------------|--------------|--------|
| | | |

### Workflow reference

Link to `docs/design-specs/<TICKET-ID>-workflow.md` or embed §2b below for short flows.

## 2b. Workflow map (required if multi-surface)

| Step | User action | Surface |
|------|-------------|---------|
| 1 | | |

## 2c. Experienceable in-context mocks (required — AM-007)

> **Gate:** `./studio approve-design` **blocks** if this section is missing or placeholder-only.  
> Mocks must show the component/workflow **embedded in the real UI shell** where it will ship — not an orphan artboard on a blank canvas.

| Field | Value |
|-------|-------|
| **Shell / surface** | e.g. board chrome, extension popup, presentation builder |
| **Mock assets** | Paths under `docs/design-specs/mocks/<TICKET>/` or linked frames |
| **States shown** | empty / loading / success / error (list which) |
| **Anti-orphan check** | Confirm chrome, nav, or neighboring UI is visible in the mock |

**Wrong:** Modal alone on grey background.  
**Right:** Modal drawn inside board / popup / builder chrome with real surrounding UI.

## 3. Atomic inventory

| Level | Name | Library source | New? |
|-------|------|----------------|------|
| primitive | Dialog | pull: dialog | no |
| atom | Button | pull: button | no |
| molecule | … | compose: … | yes → studio-library first |

## 4. Design rationale

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

### Navigation IA (only if nav chrome changes)

- Top-level items: __ (target ≤7)
- Max depth: __ (target ≤3)

### Platform

- [ ] Desktop  - [ ] Mobile web  - [ ] Webapp  - [ ] Extension

## 4b. Aesthetic preset (Team 10 — required)

| Field | Value |
|-------|-------|
| **Preset slug** | e.g. `stripe-like-ui` or `project-brand-only` |
| **SKILL path** | `.quinsy-studio/knowledge-base/aesthetic-presets/<slug>/SKILL.md` |
| **Rationale** | Why this preset fits audience + surface |
| **Token mapping** | Preset colors → project token names |
| **Motion / Headless UI** | Transitions, focus, active states from preset |

Catalog: `knowledge-base/aesthetic-presets/README.md`

## 5. Storyboard (UX-007 — marketing / workflow)

| Step | Visual | Copy | CTA |
|------|--------|------|-----|
| 1 | Hero | … | … |

Narrative arc: setup → tension → resolution.

## 6. Design system compliance

Self-check against `design-system-compliance-checklist.md` and **`anti-slop-design-ux.md`** (utilitarian layout, literal microcopy, no fluff vocabulary) — library pulls, tokens, no hallucinated primitives.

Agent contract (design-track): paste the block from `anti-slop-design-ux.md` § Agent contract into the ticket or spec header.

## 7. Handoff to Team 01

- Library pulls: `./studio library pull <project> …`
- Page type: `ui/page-types/…` or compose organisms
- Dark mode: required surfaces listed
