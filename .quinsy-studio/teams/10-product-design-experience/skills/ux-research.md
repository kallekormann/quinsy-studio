# Skill: UX Research (UX-004)

> Supplies the evidence a design decision rests on: personas as task-based segments, mental-model notes, usability criteria, and explicit assumptions where evidence is missing. Loads at gate 0 definitions, gate 2a direction, and on any ticket that changes who the product is for. The bar: every persona claim is traceable to a source or marked as an assumption.

## Metadata

```
skill_id: UX-004
name: UX Research
team: 10-product-design-experience
lead_role: UX Researcher
support_roles: [Product Designer, Product Manager]
phases: [0, 2, 3]
activation_triggers:
  - definitions/02-personas.md, definitions/12-positioning.md
  - gate 2a design interview
  - Phrases: "persona", "mental model", "who is this for", "usability test", "interview"
pairs_with: [PM-001, UX-001, GM-007, GD-004]
```

Default verdict: a persona without tasks and a source is an assumption and is labelled as one.

## When to load

- Gate 0: the personas and positioning definitions; gate 2a: the design interview.
- A milestone review that changes the audience or adds a persona page set (Team 11).
- Not for: cosmetic work on a signed surface.

## Rules

### 1. Personas are task segments, not demographic posters

Indi Young: segment by what people are trying to do and how they think about it, not by age or title. Each persona lists its top tasks, the words it uses, and what it already uses today.

### 2. Evidence or assumption, never a blend

Every claim carries a source (interview, review corpus, support log, analytics) or the label **assumption** with a date and the cheapest test that would settle it.

### 3. Usability criteria are written before the mock

Name the task, the success condition, and the acceptable time or error rate. UX-009 reads them at the finish gate.

### 4. Research feeds growth and positioning

The persona's problem statement, in their words, is the input to GM-007 (positioning) and to Team 11 persona pages. Do not let marketing invent a second persona set.

### 5. Push-back is data

Read `docs/design-specs/pushback-log.md`. A recurring code is a research finding about the human's expectations for this product; write it into the persona notes.

## Workflow

1. Collect what exists: PRD, definitions, reviews, support threads, prior push-back.
2. Write or revise `02-personas.md` as task segments with sources and assumptions.
3. Write usability criteria for the flows in scope.
4. Hand the problem statements to PM-001 / GM-007 and the criteria to UX-001 / UX-009.

## Deliverables

- `docs/definitions/02-personas.md` (task segments, sources, assumptions).
- Usability criteria block in the design spec §1 or a linked `docs/research/<topic>.md`.
- Mental-model notes when a flow is new to the audience.

## Done evidence

```markdown
## Design skill
- UX-004: personas as task segments with sources — docs/definitions/02-personas.md
- UX-004: usability criteria for <flow> — docs/design-specs/<TICKET>.md §1
```

## Anti-patterns

- Invented demographics ("Sarah, 34, marketing manager, loves coffee").
- A persona list that marketing and design each keep separately.
- Criteria written after the screenshots exist.

## Handoff

- **To PM-001 / PM-002:** problem statements for the PRD and milestone scope.
- **To GM-007 / GD-001:** persona language for positioning and persona pages.
- **To UX-001:** goals and tasks for spec §1.

## Deltas

- Studio addition: push-back codes count as research input; the source method assumes live users only.

## References

- [ux-research-playbook.md](../../../knowledge-base/ux-research-playbook.md) · [design-direction-playbook.md](../../../knowledge-base/design-direction-playbook.md)
- Agent: `agents/design-ux-researcher.md` · External: `ux-mental-models`
