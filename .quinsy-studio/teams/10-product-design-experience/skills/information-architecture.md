# Skill: Information Architecture (UX-003)

> Decides where a capability lives: navigation structure and contextual feature placement given user intent and the surface they are on. Runs before width, spacing, or tokens on any ticket that adds, moves, or merges a capability. The bar: ≤7 top-level items, depth ≤3, no dumping-ground surface, and a written placement rationale.

## Metadata

```
skill_id: UX-003
name: Information Architecture
team: 10-product-design-experience
lead_role: Information Architect
support_roles: [Product Designer, UX Designer]
phases: [3, 4]
activation_triggers:
  - ticket_type: ia-navigation, ia-feature-placement, ui-composition (multi-surface)
  - Phrases: "move X to Y", "wrong place", "dumping ground", "share dialog", "menu merge", "nav", "settings IA"
pairs_with: [UX-001, UX-002, UX-006]
```

Default verdict: placement undecided means the ticket is not ready for visual design.

## When to load

- Top-level navigation, settings IA, wayfinding (Nav IA mode).
- A feature that spans dialogs, routes, or builders (Contextual placement mode).
- Any `ui-composition` that touches two or more surfaces, even when the title says "layout" or "redesign".
- Not for: a single component on one signed surface.

## Rules

### 1. Two IA modes, one deliverable each

| Mode | When | Deliverable |
|------|------|-------------|
| **Nav IA** | Top-level navigation, settings IA, wayfinding | Nav map; ≤7 top-level items; depth ≤3; `./studio ia-audit` |
| **Contextual placement** | Feature spans dialogs, routes, builders | Surface map delta; §2 Context & placement in the design spec |

### 2. Placement before pixels

Run placement before width, spacing, or tokens. A redesign of a dialog that hosts multiple intents (collaborate + client + admin) is an `ia-feature-placement` ticket first.

### 3. No dumping grounds

A surface that collects unrelated capabilities fails. Each capability names the intent that brings a user to the surface where it lives.

### 4. Zones own their rails

When a canvas zone owns a kit or inspector rail, the rail follows the **current** zone children on add and delete. Stored palettes must not keep removed items (`PB-20260916-003`).

### 5. The gate reads the spec, not the human

`./studio approve-design` fails when §2 Context & placement is empty; `ia-navigation` also needs `./studio ia-audit` green (top ≤7, depth ≤3). Human approval does not skip an unwritten spec.

### 6. Read the catalog

the PB- bullets in `contextual-ia-playbook.md` and `design_playbook.md`, and the push-back log for the surface; cite in §7b. The `flow` code often has a placement cause.

## Workflow

1. Classify the ticket: Nav IA or Contextual placement (set `ticket_type` with groom if missing).
2. Read the current `docs/ia/surface-map.md`, the catalog, the push-back log.
3. Write the placement or nav rationale; update the surface map or nav map.
4. Write §2 Context & placement (and §2b workflow map when multi-step with UX-001).
5. Run `./studio ia-audit` on nav tickets.

## Deliverables

- All UX-003 tickets: placement or nav rationale; anti-pattern check (no dumping grounds).
- `ia-navigation`: nav map diagram; IA metrics in spec §4 Navigation IA.
- `ia-feature-placement`: `docs/ia/surface-map.md` created or updated; §2 in linked UI specs; workflow map if multi-step.

## Done evidence

```markdown
## Design skill
- UX-003: placement rationale — docs/design-specs/<TICKET>.md §2
- UX-003: surface map — docs/ia/surface-map.md (or nav map + ./studio ia-audit PASS)
```

## Anti-patterns

- Spacing and tokens decided before placement.
- A second settings product because a later ticket "sounded like a new page".
- A one-off workbench, inbox, or editor beside the live one.
- Rails that keep removed items.

## Handoff

- **To UX-002:** the surfaces and the steps across them.
- **To UX-005 / UX-006:** the signed placement; they draw inside it.
- **To Team 01:** routes and surface map; no new top-level entries without an IA ticket.

## Deltas

- **PB-20260929-001** helpful=0 harmful=0 :: Keep operator account settings on the existing authenticated settings surface. A later IA ticket that sounds like a new page is not a second settings product.
- **PB-20260926-001** helpful=0 harmful=0 :: Keep layout and composition work on the live layout-picker cards. Do not invent a second block-list editor, a second intake inbox, or a one-off product-detail workbench.
- **PB-20260916-004** helpful=0 harmful=0 :: When a chrome ticket removes or rewires a control, update the gold-path source test in the same change.

## References

- [contextual-ia-playbook.md](../../../knowledge-base/contextual-ia-playbook.md) · [workflow-definition-playbook.md](../../../knowledge-base/workflow-definition-playbook.md)
- External: `ux-information-architecture`
