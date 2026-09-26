# Skill: Information Architecture (UX-003)

```
skill_id: UX-003
team: 10-product-design-experience
lead_role: Information Architect
```

**Scope:** Navigation **and** contextual feature placement — where capabilities live given user intent and surface context.

**External:** `ux-information-architecture`

---

## Two IA modes

| Mode | When | Deliverable |
|------|------|-------------|
| **Nav IA** | Top-level navigation, settings IA, wayfinding | Nav map; ≤7 top-level items; depth ≤3; `design_math.ia_nav_audit` |
| **Contextual placement** | Feature spans dialogs, routes, builders | Surface map delta; §2 Context & placement in design spec |

**Playbook:** `.quinsy-studio/knowledge-base/contextual-ia-playbook.md`

---

## Mandatory deliverables

### All UX-003 tickets

- [ ] Placement or nav rationale documented
- [ ] Anti-pattern check: no capability dumping grounds

### `ia-navigation`

- Nav map diagram
- IA metrics in design spec §4 Navigation IA

### `ia-feature-placement`

- Update or create `docs/ia/surface-map.md`
- §2 Context & placement in linked UI specs
- Workflow map if multi-step (`workflow-definition-playbook.md`)

### `ui-composition` (multi-surface)

- §2 Context & placement **required** even when ticket title says "layout" or "redesign"

---

## Ticket triggers

Agent or groom should set `ticket_type: ia-feature-placement` when request includes:

- "move X to Y surface", "wrong place", "dumping ground", "share dialog", "menu merge"
- Layout redesign of a dialog that hosts **multiple intents** (collaborate + client + admin)

Run **placement before** width/spacing/tokens.

When a canvas zone owns a kit/inspector rail, the rail follows **current** zone children (add/delete). Stored palettes must not keep removed items (LO-0290 / `PB-20260916-003`).

---

## Approve-design gate

`./studio approve-design` **fails** if the spec file is missing or **§2 Context & placement** is empty. For `ia-navigation`, also run **`./studio ia-audit`** — missing `ia_nav` metrics or top > 7 / depth > 3 fails the CLI. Human approval is not a skip for an unwritten spec.

---

## Related skills

- UX-002 — workflow steps across surfaces
- UX-006 — brand/token compliance on chosen surface

## Deltas

- **PB-20260926-001** helpful=0 harmful=0 :: Keep layout and composition work on the live layout-picker cards. Do not invent a second block-list editor, a second intake inbox, or a one-off product-detail workbench.
- **PB-20260916-004** helpful=0 harmful=0 :: When a chrome ticket removes or rewires a control, update the gold-path source test in the same change.
