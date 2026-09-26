# Design spec template (Team 10)

Path: `projects/<project>/docs/design-specs/<TICKET-ID>.md`

Load before writing: [contextual-ia-playbook.md](contextual-ia-playbook.md), [workflow-definition-playbook.md](workflow-definition-playbook.md), [interaction-ux-playbook.md](interaction-ux-playbook.md), [product-ux-playbook.md](product-ux-playbook.md), [design-system-compliance-checklist.md](design-system-compliance-checklist.md).

> **Mandatory:** The spec file and mocks must **exist on disk** before anyone is asked to review or `./studio approve-design`. Pointing at `docs/design-specs/<TICKET>.md` that was never written is a process fail. A stub created at ticket time is not a spec.

> **LO-0038:** A large mock HTML pack does **not** satisfy `approve-design` by itself. Fill **§2 Context & placement** and **§2c Experienceable in-context mocks** (with real shell / asset paths / **all states** / anti-orphan) as soon as the first composed mock exists — preferably before the catalog is "done."

> **Mocks are implementation contracts.** If a state is not mocked, implement will guess. Incomplete state coverage **fails** `approve-design`.


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

> **Gate:** `./studio approve-design` **blocks** if this section is missing, the spec file is a stub, mock HTML is missing, mocks ignore project tokens, or required states are not shown.  
> Mocks must show the component/workflow **embedded in the real product view** where it will ship — not an orphan artboard on a blank canvas.  
> Style mocks with **this project's** `ui/tokens` (CSS variables). Do not invent a parallel palette.

| Field | Value |
|-------|-------|
| **Shell / surface** | Exact route or chrome (e.g. `/commands` list + app sidebar) |
| **Mock assets** | `docs/design-specs/mocks/<TICKET>/*.html` (required). Screenshots optional. |
| **Project tokens** | Path to project `ui/tokens/design-tokens.css` (or equivalent) used in the HTML |
| **States shown** | List **every** required state (see below) |
| **Anti-orphan check** | Confirm chrome, nav, or neighboring UI is visible in the mock |

**Wrong:** Modal or button alone on grey/white.  
**Right:** Same control drawn inside the actual app shell (nav, sidebar, neighboring panels) with real surrounding UI.

### Required mock states (mandatory)

Interactive controls (button, input, dropdown, select, switch, checkbox, toggle, tabs):

| State | Also called | Must mock |
|-------|-------------|-----------|
| Rest | up, default, idle | Yes |
| Hover | | Yes |
| Pressed | down, `:active` | Yes |
| Disabled | inactive | Yes |
| Focus | `:focus-visible` | Yes |

Disclosure controls (dropdown, menu, select, combobox, popover): **open** and **closed**, each with the interaction states that apply.

Surfaces / compositions (lists, boards, settings, marketing, IA): **empty**, **loading**, **error** (plus populated/success when there is a happy path).

Put states in this table **and** in the mock files (separate HTML, headings, or `data-state="hover"`). One rest-state frame is not approval.

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

```
ia_nav: { top: __, depth: __ }
```

- Top-level items: __ (target ≤7)
- Max depth: __ (target ≤3)
- Tool: `./studio ia-audit <project> <TICKET>` before `approve-design`

### Platform

- [ ] Desktop  - [ ] Mobile web  - [ ] Webapp  - [ ] Extension

## 4b. Aesthetic preset (Team 10 — optional footnote)

> Not required. Signed `design/DESIGN.md` uniqueness is the source of truth. If you use a catalog slug, map it onto project tokens.

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

## 6. Growth intent (Team 11 — required on commercial surfaces)

> Landing, pricing, checkout, PLP, PDP. Playbook: `knowledge-base/growth-mechanics-playbook.md`.  
> `./studio approve-design` fails on these surfaces if this section is missing. A/B is optional; the **claim** is not.

| Field | Value |
|-------|--------|
| **Surface class** | commercial-web / product-app |
| **Job** | What the person is trying to finish |
| **Claim** | One falsifiable sentence |
| **Change vs control** | One primary difference (or “control only”) |
| **Metric or stand-in** | Named event, or what we would count if analytics are missing |
| **Stop / not testing** | What would kill a variant; what is out of scope |
| **Peak–end** | After pay/submit/signup: what they see (artifact + next step). Playbook: `delight-playbook.md` |

Team 05 (SEO/AEO) only if this URL is public — not a substitute for this table.

## 6b. Delight layer (empty / wait / first success / hard-work-done / buy)

> Required when this ticket includes those moments. [delight-playbook.md](delight-playbook.md). **Kano:** if basics fail, write “none — basics only.” Confetti on Save is a fail.

| Field | Value |
|-------|--------|
| **Kano** | Basics met? yes/no |
| **Level** | visceral / behavioral / reflective |
| **Moment** | empty / wait / peak-end / first success / recovery / buy / none |
| **What we add** | One thing, or none |
| **Reduced motion** | How it degrades |

## 7. Design system compliance

Self-check against `design-system-compliance-checklist.md` and **`anti-slop-design-ux.md`** (utilitarian layout, literal microcopy, no fluff vocabulary) — library pulls, tokens, no hallucinated primitives.

Agent contract (design-track): paste the block from `anti-slop-design-ux.md` § Agent contract into the ticket or spec header.

## 8. Handoff to Team 01

- Library pulls: `./studio library pull <project> …`
- Page type: `ui/page-types/…` or compose organisms
- Dark mode: required surfaces listed
