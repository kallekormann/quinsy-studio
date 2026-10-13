# Design spec template (Team 10)

Path: `projects/<project>/docs/design-specs/<TICKET-ID>.md`

Load before writing: [contextual-ia-playbook.md](contextual-ia-playbook.md), [workflow-definition-playbook.md](workflow-definition-playbook.md), [interaction-ux-playbook.md](interaction-ux-playbook.md), [product-ux-playbook.md](product-ux-playbook.md), [design-system-compliance-checklist.md](design-system-compliance-checklist.md).

> **Mandatory:** The spec file and mocks must **exist on disk** before anyone is asked to review or `./studio approve-design`. Pointing at `docs/design-specs/<TICKET>.md` that was never written is a process fail. A stub created at ticket time is not a spec.

> **LO-0038:** A large set of mocks does **not** satisfy `approve-design` by itself. Fill **§2 Context & placement** and **§2c Experienceable in-context mocks** (with real shell / asset paths / **all states** / anti-orphan) as soon as the first composed mock exists — preferably before the catalog is "done."

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

> **Gate:** `./studio approve-design` **blocks** if this section is missing, the spec file is a stub, the mock routes are missing, a mock draws its own UI, screenshots are missing or older than the mock code, or required states are not shown.
>
> **Real UI only.** The human signs a mock only when it looks exactly like the implemented app, with the design task and its solution woven into it. A mock is a **route in the product app** that renders the app's own views, layouts, and components:
>
> - App: `apps/web` (Payload), else a Next app at the project root (adopted projects), else the gate-2b kit in `design/prototype` before any app exists.
> - Route: `app/(design-mocks)/design-mocks/<TICKET>/page.tsx`. `(design-mocks)/layout.tsx` calls `notFound()` in production, so mocks never ship.
> - **The mock is an interactive prototype, not a set of static frames.** One `'use client'` `page.tsx` at the ticket root — never `<TICKET>/<state>/page.tsx`. Wire handlers: hover, open/close, selection, and flow steps work when the human uses it. Pull `mock-scenario-panel` and mount it on that page so every related state is a click (`?state=`). `scenarios` must list every name in **States shown** and every screenshot stem. Transitions named in §2d are wired in the mock exactly as the product will move. Folder-per-state packets fail `./studio mock` / `approve-design`.
> - The page imports the real shell or view the feature ships in (the `(app)` or `(marketing)` layout, the page view) and the real components. A part that does not exist yet is built as a real component in the app (library-first) and imported. Nothing is redrawn: no `<style>`, no `style={{…}}`, no hex colours, no arbitrary colour classes, no standalone HTML.
> - Screenshots of every state, captured from the running route at 1440 and 390 wide, go in `docs/design-specs/mocks/<TICKET>/`, named by state (`hover-1440.png`, `open-390.png`). They must be newer than the mock code. **Screenshots are the record; the running route is the review surface.**
>
> Capture example: `npx playwright screenshot --viewport-size=1440,900 "http://localhost:3000/design-mocks/<TICKET>/?state=hover" docs/design-specs/mocks/<TICKET>/hover-1440.png`. For hover, focus, and pressed, drive the real component with Playwright (`hover()`, `focus()`, mouse down) or a `?state=` scenario the harness exposes. Verify the whole packet with `./studio mock <project> <TICKET>`.

| Field | Value |
|-------|-------|
| **Shell / surface** | Exact route and the real layout or view the mock renders (e.g. `/commands` list in the `(app)` layout) |
| **Mock route** | `app/(design-mocks)/design-mocks/<TICKET>/` in the product app (required) |
| **Mock assets** | `docs/design-specs/mocks/<TICKET>/*.png`, one per state and width, captured from the route (required) |
| **Real parts used** | Layout, view, and component imports the mock renders; new components built for this ticket |
| **States shown** | List **every** required state (see below) |
| **Anti-orphan check** | Confirm chrome, nav, or neighboring UI is visible in the screenshots |

**Wrong:** Modal or button alone on grey/white. A hand-built HTML page that imitates the app.
**Right:** The real app route, with its real shell, nav, and neighbouring panels, and the new control rendered from real components inside it.

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

Put states in this table **and** in the panel `scenarios` list and screenshot names (`?state=<id>`, one screenshot per state). One rest-state frame is not approval. Folder-per-state routes are not approval.

## 2d. Motion (required)

> **Gate:** `./studio approve-design` blocks when this section is missing, unless the spec or the ticket says `motion: off`.
> Motion is the default. Skill: `knowledge-base/skill-extensions/motion-transitions.md`.
> `prefers-reduced-motion` still shows the same content with durations at `0ms`.

| Surface | Enter | Leave | Scale | Token |
|---------|-------|-------|-------|-------|
| e.g. filter menu | 250ms, ease smooth-out | 150ms, same ease | open 0.97, close 0.99 | `--motion-scale-medium` / `--motion-scale-tiny` |

The mock route renders the real component closed and open. The open frame transitions opacity and transform with the tokens above. A dialog uses `--motion-scale-large` and `transform-origin: center`. A menu originates at its trigger.

- Reduced motion: same layout and copy, durations at `0ms`.
- Kit components already animate. Name a field shake, text swap, icon swap, number update, skeleton reveal, or success mark here only when this screen needs it. Use the tokens in the skill. Do not add a second transition catalog.

HITL opt-out (the only off switch):

```
motion: off
```

That line means the project token file sets every `--motion-duration-*` to `0ms`. It does not mean a hand-rolled static fork of Dialog or Button.

## 2e. Interaction walkthrough (required)

> **Gate:** `./studio approve-design` blocks when this section is missing or has fewer than 3 steps.
> This is the review script: the human runs the mock route and follows it. `./studio mock <project> <TICKET>` prints it next to the route URLs. Each step is "do X → expect Y", and names the §2d transition where one fires.

**Mock route:** `http://localhost:3000/design-mocks/<TICKET>/` (states via `?state=`)

| # | Do | Expect (incl. motion) |
|---|----|------------------------|
| 1 | Hover the primary control | Expect hover tint, 150ms ease |
| 2 | Click to open the menu | Expect panel opens from trigger, 250ms, scale 0.97 → 1 |
| 3 | Switch `?state=empty` in the panel | Expect empty view with its CTA, no layout shift |

Cover the happy path, one failure path, and every scenario state the mock exposes. The implementation sprint ports this behavior from the mock code — the walkthrough is also its acceptance script.

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

## 5. Story (required — marketing-page, workflow-explainer, commercial ui-composition)

> Arc is setup, tension, resolution, and one CTA. Copy is literal. Name what moves and what stays. The still uses real product chrome (LO-0054). Scroll may reveal. It may not hijack.

- **Setup:** _fill_
- **Tension:** _fill_
- **Resolution:** _fill_
- **CTA:** _fill_
- **Motion:** what moves, what stays. Reduced-motion path: _fill_

### Imagery

> UX-007. One row per image, or the line `imagery: none`. Product screens are captures of the running app, never generated. No generated person is presented as a customer. Log source, licence or model, and the AI label in `docs/design-specs/imagery.md`.

| Fold | Job | Brief (subject · setting · light · framing · ratio) | Exclude | Alt |
|------|-----|-----------------------------------------------------|---------|-----|
| _fill_ | _fill_ | _fill_ | _fill_ | _fill_ |

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

### Five-second test

> Every packet (GD-003). Look at the first screen of the mock for five seconds as a PRD persona. Commercial packets also append `## Appendix — Persona walkthrough (GD-003)` at the end of this file.

| Question | 390 | 1440 |
|----------|-----|------|
| What is this? | _fill_ | _fill_ |
| Is it for me? | _fill_ | _fill_ |
| What do I do next? | _fill_ | _fill_ |

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

## 7b. Catalog applied (required)

Proof that Team 10 read the design playbooks and UX skills before drawing. One line per entry: the PB- id, and where in this spec it lands. LO- ids are local tickets and do not count. Sources: `knowledge-base/design_playbook.md` and the other design playbooks (PB-ids), `teams/10-*/skills/` (PB-ids), and the product's `docs/design-specs/pushback-log.md` (codes from earlier rejections on this surface).

- PB-YYYYMMDD-NNN — applied in §<n>: <one clause>
- LO-NNNN — applied in §<n>: <one clause>
- push-back `<code>` on <ticket> — answered in §<n>: <one clause>

If nothing matched, write `catalog: none` and the reason in one sentence.

## 8. Handoff to Team 01

- Library pulls: `./studio library pull <project> …`
- Page type: `ui/page-types/…` or compose organisms
- Dark mode: required surfaces listed
