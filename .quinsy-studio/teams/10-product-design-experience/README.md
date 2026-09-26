# Team 10 — Product Design & Experience

Owns **what** and **why** for UI/UX. Team 01 implements after the **project kit** is signed (gates **2a → 2b**) and, later, after per-ticket `approve-design`.

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

## Anti-slop (mandatory)

All design specs, mocks, and microcopy follow [anti-slop-design-ux.md](../../knowledge-base/anti-slop-design-ux.md). Skill: [skills/anti-slop-design-ux.md](skills/anti-slop-design-ux.md). Default SaaS indigo is a process fail (U-C2).

## Aesthetic presets (optional footnote)

The catalog is a **repertoire**, not the source of truth. Uniqueness in `design/DESIGN.md` beats a Linear/Stripe clone.

- Catalog: [knowledge-base/aesthetic-presets/README.md](../../knowledge-base/aesthetic-presets/README.md)
- Skill: [skills/aesthetic-presets.md](skills/aesthetic-presets.md)

A spec **may** name one preset (or `project-brand-only`) as a footnote mapped onto **project tokens**. It is not required.

## Workflow

**Start of a product (before any sprint):**

1. **2a** — CARD: UX-001, UX-004, UX-006, UX-008. Unanswered questions in `docs/design/discovery.md`. HITL until the human answers. Fill `design/DESIGN.md` (uniqueness, token names). `./studio approve --gate 2a`. Do **not** scaffold `design/prototype`. Playbook: [design-direction-playbook.md](../../knowledge-base/design-direction-playbook.md)
2. **2b** — CARD: UX-005, UX-002, UX-003, UX-006, UX-008, FE-002. Project CSS tokens + Tailwind mapped to those variables, coded atoms / molecules / organisms, sticker sheet with **inventory children** (all states), mocks on those tokens. `./studio revise --gate 2b` until `./studio approve --gate 2b`. Do **not** promote this product’s look into studio-library.

**Per-ticket (after 2b):**

1. `./studio ticket` → design-track tickets get `design_status: pending` and a **stub** at `docs/design-specs/<TICKET>.md`
2. Team 10 **fills** that spec (remove the stub banner) and writes HTML mocks under `docs/design-specs/mocks/<TICKET>/` using **the same project tokens**, in the **real product view**, **all states**
3. Human → `./studio approve-design <project> <ticket-id>`
4. Team 01 → `./studio move … implement` (library-first Headless primitives + this kit)

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
- `knowledge-base/brand-guardian-checklist.md`
- `knowledge-base/aesthetic-presets/README.md` — optional footnote

## Studio skill extensions

See [knowledge-base/skill-extensions/README.md](../../knowledge-base/skill-extensions/README.md) — compliance, PLG, delight UX, security (extend existing CL/GM/UX/PE skills).
