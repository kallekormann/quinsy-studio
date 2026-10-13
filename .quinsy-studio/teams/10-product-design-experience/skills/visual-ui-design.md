# Skill: Visual UI Design (UX-005)

> Decides how a surface looks: hierarchy, type scale, colour roles, spacing rhythm, Gestalt grouping, and the motion that carries state changes — all as calculable values from the project tokens. The bar: a developer can build the mock from the spec without guessing a single value, and the result does not look like the default kit.

## Metadata

```
skill_id: UX-005
name: Visual UI Design
team: 10-product-design-experience
lead_role: UI/Visual Designer
support_roles: [Brand Guardian, UX Designer]
phases: [2, 3, 4]
activation_triggers:
  - ticket_type: ui-new-component, ui-composition, ui-styling, marketing-page
  - Phrases: "layout", "hierarchy", "typography", "spacing", "looks generic", "polish"
pairs_with: [UX-006, UX-008, UX-002, FE-001, FE-002]
```

Default verdict: a value that is not calculable from tokens is not specified.

## When to load

- Every design-track ticket: §3 Atomic inventory, §4 Design rationale, §2d Motion.
- Gate 2b: the project kit (tokens, coded atoms/molecules/organisms, sticker sheet).
- Not for: placement decisions (UX-003) or copy (UX-002).

## Rules

### 1. Hierarchy first, decoration never

Three levels at most on one surface; the eye lands where the task starts. Elevation and colour exist to separate levels, not to decorate. The `hierarchy` push-back code points here.

### 2. Every value is a token or a ratio of one

Type scale, spacing (8pt grid), radii, shadows, motion durations: name the token. Gestalt grouping and proportion are written as rules the gate can check (`design-science-playbook.md`).

### 3. Uniqueness is designed, not hoped for

Name the two or three moves that make this surface this product's (type pairing, rhythm, a signature component, an imagery rule). If the spec would be true for any product, it is not finished (`uniqueness` code).

### 4. Motion is part of the spec

§2d names each transition (enter, leave, hover, state change) with duration and easing tokens and a reduced-motion path. The kit animates through tokens; a second animation layer is a gate FAIL. `motion: off` is the HITL opt-out only.

### 5. Presets are a footnote

An aesthetic preset may be cited in §4b and mapped onto project tokens. It never becomes a second CSS kit.

### 6. Read the catalog before drawing

`design_playbook.md` and `anti-slop-design-ux.md` PB-ids, plus the push-back log for the surface. Cite in §7b.

## Workflow

1. Read the signed §1–§2 (UX-001, UX-003), DESIGN.md, tokens, catalog, push-back log.
2. Write §3 inventory from the library (pull, do not invent primitives).
3. Write §4 rationale with calculable values; §2d motion.
4. Build the real-UI mock route as an **interactive prototype**: pull `mock-scenario-panel`, wire handlers, scenario states (`?state=`) and every §2d transition. A mock you cannot click is not done.
5. Write §2e Interaction walkthrough (the review script), verify with `./studio mock <p> <TICKET>`, then capture every state at 1440 and 390 as the record.
6. Fill §7 compliance and §7b catalog.

## Deliverables

- Spec §2d, §2e, §3, §4, §4b (optional), §7, §7b.
- Interactive real-UI mock route under `app/(design-mocks)/design-mocks/<TICKET>/` (wired handlers, reachable states, §2d motion) and screenshots of all states in `docs/design-specs/mocks/<TICKET>/`. The route is the review surface and the reference implementation; the screenshots are the record.

## Done evidence

```markdown
## Design skill
- UX-005: §4 values all token-based — docs/design-specs/<TICKET>.md
- UX-005: §2d motion with reduced-motion path — docs/design-specs/<TICKET>.md
- UX-005: mock states at 1440/390 — docs/design-specs/mocks/<TICKET>/
- UX-005: §7b cites <ids>
```

## Anti-patterns

- A hex value or `px` not derived from a token.
- "Modern, clean, minimal" as rationale.
- Framer Motion or another library wrapping kit components.
- Hand-drawn HTML mocks.
- Static per-state frames instead of a clickable prototype — the human must be able to feel the interaction, not infer it from screenshots.
- Shipping the same hierarchy that was rejected on the sibling surface.

## Handoff

- **To UX-006:** the value list for the brand check.
- **To FE-001 / FE-002:** the spec and the mock route code — the reference implementation for interactions, transitions and component wiring; they port it, compose kit + tokens, no new primitives.
- **To UX-009:** the mock shots and the §2e walkthrough the finish gate compares.

## Deltas

- Studio addition: the motion budget check and the `uniqueness` / `hierarchy` push-back codes are enforced by tooling, not by review alone.

## Toolbox (trained — TR-0012)

### Upgrade soft-path composition (LO-0142)

- When checkout is deferred, the soft-path must land on a **real** plan/Account surface (not a dead hash) with Free + Upgrade in the first viewport, **or** auto-open the upgrade dialog (`?upgrade=1`).
- A modal that only opens after an unmarked click fails "upgrade now" intent.
- Compose with Headless UI dialog + library Button/Badge; keep plan copy in the project.
- Pattern: [upgrade-soft-path.md](../../../studio-library/ui/docs/patterns/upgrade-soft-path.md). FE cross-link: [frontend_playbook.md](../../../knowledge-base/frontend_playbook.md).

## References

- [design-science-playbook.md](../../../knowledge-base/design-science-playbook.md) · [atomic-design-playbook.md](../../../knowledge-base/atomic-design-playbook.md) · [delight-playbook.md](../../../knowledge-base/delight-playbook.md)
- [motion-transitions.md](../../../knowledge-base/skill-extensions/motion-transitions.md) · [figma-token-handoff.md](../../../knowledge-base/skill-extensions/figma-token-handoff.md)
- [aesthetic-presets.md](aesthetic-presets.md) · External: `ux-visual-design`, `ux-typography`, `ux-color-theory`, `taste-skill`
