# Team 10 — Product Design & Experience

Owns **what** and **why** for UI/UX. Team 01 implements after the **project kit** is signed (gates **2a → 2b**) and, in later cycles, after the design phase is signed with `./studio approve-design <project> --phase`.

## Director roles

| Skill | Role |
|-------|------|
| UX-001 | Product Designer |
| UX-002 | UX Designer |
| UX-003 | Information Architect |
| UX-004 | UX Researcher |
| UX-005 | UI / Visual Designer |
| UX-006 | Brand Guardian |
| UX-007 | Visual Storyteller |
| UX-008 | Anti-Slop Design & UX |
| UX-009 | UI Finish Gate — shipped screen vs signed real-UI mock, PASS / HOLD |

## Anti-slop (mandatory)

All design specs, mocks, and microcopy follow [anti-slop-design-ux.md](../../knowledge-base/anti-slop-design-ux.md). Skill: [skills/anti-slop-design-ux.md](skills/anti-slop-design-ux.md). Default SaaS indigo is a process fail (U-C2).

## Aesthetic presets (craft substrate)

The catalog locks type, elevation, motion, and density. It is not the product identity.

- Catalog: [knowledge-base/aesthetic-presets/README.md](../../knowledge-base/aesthetic-presets/README.md)
- Skill: [skills/aesthetic-presets.md](skills/aesthetic-presets.md)

`design/DESIGN.md` names one preset slug and a product delta. UX-008 then writes `design/DIRECTION-CRITIQUE.md`. Gate 2a HITL waits until every rubric line is PASS.

## Workflow

**Start of a product (before any sprint):**

1. **2a** — CARD: UX-001, UX-004, UX-006, UX-008. Unanswered questions in `docs/design/discovery.md`. HITL until the human answers. Fill `design/DESIGN.md` (preset substrate, product delta, token names). UX-008 writes `design/DIRECTION-CRITIQUE.md` in a second pass. `./studio approve --gate 2a` only after every critique line is PASS. Do **not** scaffold `design/prototype`. Playbook: [design-direction-playbook.md](../../knowledge-base/design-direction-playbook.md)
2. **2b** — CARD: UX-005, UX-002, UX-003, UX-006, UX-008, FE-002. `./studio design` pulls the library base kit. Style it with project CSS tokens. Shell routes (marketing when the archetype is public, sign-in, register, app shell, settings, empty/loading/error) plus the PRD journey. Sticker sheet renders the pulled controls in all states. `./studio revise --gate 2b` until `./studio approve --gate 2b`, which copies the prototype into the product app and leaves `design/prototype/` as the baseline. Do **not** promote this product’s look into studio-library.

**After gate 2b (the phase train):**

1. A **design phase** holds experience tickets whose `design_status` is `pending`. Polish on the signed kit stays `n/a` and stays out of this phase.
2. Team 10 **fills** every spec (remove the stub banner) and builds **real-UI mocks**: routes in the product app at `app/(design-mocks)/design-mocks/<TICKET>/` that render the app's own layouts, views, and components with the design solution woven in. A missing part is built as a real component and imported; nothing is redrawn in HTML or inline styles. Screenshots of **all states** at 1440 and 390 go in `docs/design-specs/mocks/<TICKET>/`. The human only signs mocks that look exactly like the implemented app. Each ticket states `architecture delta: none` or names the architecture ticket. **§2d Motion** is required. The only skip is the line `motion: off` from HITL.
3. Human → `./studio approve-design <project> --phase` once, after every packet in the phase is written.
4. An **architecture phase** signs the deltas and any boundary tickets. `./studio approve-arch <project> <TICKET> --reject` sends an infeasible design to the next design cycle.
5. An **implementation phase** builds only tickets whose design and architecture are `approved` or `n/a`. Team 01 styles the pulled kit and this baseline; do not redraw popover, tooltip, dropdown, or dialog.

Never paste “please approve `docs/design-specs/…`” unless that file is filled and the mock folder exists.

## Agents

See `agents/` — Brand Guardian, Visual Storyteller, UX Researcher.

## Playbooks

- `knowledge-base/design-direction-playbook.md` — gate 2a interview + uniqueness fail lines
- `knowledge-base/design-team-canon-ledger.md` — Teams 10 / 11 / 05 split
- `knowledge-base/growth-mechanics-playbook.md` — commercial surfaces (pair Team 11)
- `knowledge-base/anti-slop-design-ux.md`
- `knowledge-base/product-ux-playbook.md` — Garrett / Cooper goals (UX-001)
- `knowledge-base/interaction-ux-playbook.md` — Nielsen / Wroblewski / Cooper IxD (UX-002)
- `knowledge-base/contextual-ia-playbook.md` — placement + labeling (UX-003)
- `knowledge-base/ux-research-playbook.md` — mental models (UX-004); 2a is a **human** interview
- `knowledge-base/design-science-playbook.md`
- `knowledge-base/atomic-design-playbook.md`
- `knowledge-base/visual-storytelling-playbook.md`
- `knowledge-base/delight-playbook.md` — visceral / behavioral / reflective; **no new skill**
- `knowledge-base/skill-extensions/motion-transitions.md` — §2d Motion; kit open/close scales
- `knowledge-base/brand-guardian-checklist.md`
- `knowledge-base/aesthetic-presets/README.md` — optional footnote

## Studio skill extensions

See [knowledge-base/skill-extensions/README.md](../../knowledge-base/skill-extensions/README.md) — motion, compliance, PLG, delight UX, security (extend existing CL/GM/UX/PE skills).
