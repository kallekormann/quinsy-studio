# Skill: Brand Guardian (UX-006)

> Keeps every shipped surface inside the signed `design/DESIGN.md` and the project tokens: colour roles, type, spacing, voice, imagery. Required companion on every UI implement ticket and on every design packet. The bar: nothing on screen that the token file or DESIGN.md cannot explain.

## Metadata

```
skill_id: UX-006
name: Brand Guardian
team: 10-product-design-experience
lead_role: Brand Guardian
support_roles: [UI/Visual Designer]
phases: [2, 4, 5]
activation_triggers:
  - every ticket with ticket_type ui-*, marketing-page, workflow-explainer
  - every design packet before approve-design
  - Phrases: "brand", "tokens", "voice", "off-brand", "palette", "preset"
pairs_with: [UX-005, UX-008, UX-009, FE-001]
```

Default verdict: a value not in the token file is off-brand until a token is added through a design ticket.

## When to load

- Any UI implement ticket (companion) and any design-track packet (reviewer).
- Gate 2b (project kit) and whenever a preset is proposed.
- Not for: backend-only tickets.

## Rules

### 1. Tokens are the only source of colour, type, and spacing

Hex values, ad-hoc font sizes, and arbitrary spacing in product UI fail the gate (`run_qa_gate` hard-checks tokens on UI tickets). A missing token is a design ticket, not an inline value.

### 2. Presets map onto project tokens, never replace them

An aesthetic preset may inform the look; its palette is translated into project token names. Never auto-apply a catalog palette; the theme-factory pick is a HITL ritual at gate 2a/2b.

### 3. Voice follows DESIGN.md

Microcopy tone, capitalisation, and vocabulary follow the signed voice section. Run the `anti-slop-design-ux.md` banned-vocabulary list on every string.

### 4. Imagery and iconography are one family

SVG icons from the kit only (no emoji as chrome). Imagery follows the DESIGN.md imagery rules and the pixel budgets in `design_playbook.md`.

### 5. The `brand` push-back code is yours

When the human rejects with `--reason brand`, read the note, find the drift (token, voice, imagery), and fix the rule that allowed it in the spec or the kit, not only the instance.

## Workflow

1. Read `design/DESIGN.md`, `ui/tokens/`, and the `brand` lines in `docs/design-specs/pushback-log.md`.
2. Walk the spec or the diff: every colour, type, spacing, string, and image against the sources.
3. Fill `knowledge-base/brand-guardian-checklist.md` in the receipt or spec §7.
4. On drift: name the token or voice rule to add, file a design ticket if the kit lacks it.

## Deliverables

- Completed brand-guardian checklist in spec §7 (design-track) or in the receipt (implement).
- Token delta list when the kit lacks a value (goes to a design ticket).

## Done evidence

```markdown
## Design skill
- UX-006: brand checklist PASS — docs/design-specs/<TICKET>.md §7 (or receipt)
- UX-006: no raw values in <paths> — ./studio gate <p> --level 5 (tokens hard-check)
```

## Anti-patterns

- A "temporary" hex value.
- Applying a preset palette directly to components.
- A second icon set for one screen.
- Fixing the instance the human pointed at and leaving the rule that produced it.

## Handoff

- **To UX-005:** token names for every value in the spec.
- **To FE-001:** the checklist; they implement with kit + tokens only.
- **To UX-009:** the signed look the finish gate compares against.

## Deltas

- Studio addition: the `brand` push-back code and the hard token gate replace the advisory review in the source material.

## References

- [brand-guardian-checklist.md](../../../knowledge-base/brand-guardian-checklist.md) · [design-system-compliance-checklist.md](../../../knowledge-base/design-system-compliance-checklist.md)
- [aesthetic-presets/README.md](../../../knowledge-base/aesthetic-presets/README.md) · Agent: `agents/design-brand-guardian.md`
