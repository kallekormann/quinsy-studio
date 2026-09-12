# Team 10 — Product Design & Experience

Owns **what** and **why** for UI/UX. Team 01 implements after design-track HITL (`approve-design`).

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

All design specs, mocks, and microcopy follow [anti-slop-design-ux.md](../../knowledge-base/anti-slop-design-ux.md). Skill: [skills/anti-slop-design-ux.md](skills/anti-slop-design-ux.md).

## Aesthetic presets (visual repertoire)

Team 10 selects from **17 studio aesthetic presets** when writing design specs:

- Catalog: [knowledge-base/aesthetic-presets/README.md](../../knowledge-base/aesthetic-presets/README.md)
- Skill: [skills/aesthetic-presets.md](skills/aesthetic-presets.md)
- Foundation: `soft-ui`, `minimalist-ui`, `brutalist-ui`
- Industry: `stripe-like-ui`, `apple-like-ui`, `linear-like-ui`, `notion-like-ui`, `adobe-like-ui`, `paypal-like-ui`, `amazon-like-ui`, `nike-like-ui`, `space-x-like-ui`
- Specialty: `nordic-design-ui`, `cosmic-void-ui`, `technical-blueprint-ui`, `technical-ui`, `academic-editorial-ui`

Every UI design spec must declare **one primary preset** (or `project-brand-only`).

## Studio skill extensions

See [knowledge-base/skill-extensions/README.md](../../knowledge-base/skill-extensions/README.md) — compliance, PLG, delight UX, security (extend existing CL/GM/UX/PE skills).

## Workflow

1. `./studio ticket` → design-track tickets get `design_status: pending` and a **stub** at `docs/design-specs/<TICKET>.md`
2. Team 10 **fills** that spec (remove the stub banner) and writes HTML mocks under `docs/design-specs/mocks/<TICKET>/` using **project tokens**, in the **real product view**, **all states** (see `knowledge-base/design-spec-template.md`)
3. Human → `./studio approve-design <project> <ticket-id>` — **fails** if the spec is missing, still a stub, or mocks omit tokens/states/context
4. Team 01 → `./studio move … implement` (library-first, Atomic Design)

Never paste “please approve `docs/design-specs/…`” unless that file is filled and the mock folder exists.

## Agents

See `agents/` — Brand Guardian, Visual Storyteller, UX Researcher.

## Playbooks

- `knowledge-base/design-team-canon-ledger.md` — Teams 10 / 11 / 05 split
- `knowledge-base/growth-mechanics-playbook.md` — commercial surfaces (pair Team 11)
- `knowledge-base/anti-slop-design-ux.md`
- `knowledge-base/product-ux-playbook.md` — Garrett / Cooper goals (UX-001)
- `knowledge-base/interaction-ux-playbook.md` — Nielsen / Wroblewski / Cooper IxD (UX-002)
- `knowledge-base/contextual-ia-playbook.md` — placement + labeling (UX-003)
- `knowledge-base/ux-research-playbook.md` — mental models (UX-004)
- `knowledge-base/design-science-playbook.md`
- `knowledge-base/atomic-design-playbook.md`
- `knowledge-base/visual-storytelling-playbook.md`
- `knowledge-base/delight-playbook.md` — visceral / behavioral / reflective; **no new skill**
- `knowledge-base/brand-guardian-checklist.md`
- `knowledge-base/aesthetic-presets/README.md`
