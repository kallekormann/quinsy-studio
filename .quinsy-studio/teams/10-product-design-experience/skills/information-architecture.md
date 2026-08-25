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

---

## Approve-design gate

`./studio approve-design` checks design spec for **§2 Context & placement**. Missing section → warning; human may still approve with notes.

---

## Related skills

- UX-002 — workflow steps across surfaces
- UX-006 — brand/token compliance on chosen surface
