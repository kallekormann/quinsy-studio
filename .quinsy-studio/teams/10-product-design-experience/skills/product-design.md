# Skill: Product Design (UX-001)

> Owns the end-to-end flow of a feature: the user's goal, the job it serves, the surfaces it crosses, and the one success metric that proves it. Loads on every design-track ticket before anyone draws. The bar: a reader of spec §1 can say who does what, where, and how we know it worked.

## Metadata

```
skill_id: UX-001
name: Product Design
team: 10-product-design-experience
lead_role: Product Designer
support_roles: [UX Designer, Information Architect]
phases: [3, 4, 5]
activation_triggers:
  - ticket_type: ui-composition, workflow-explainer, ia-feature-placement, marketing-page
  - Phrases: "flow", "journey", "onboarding", "first run", "job to be done", "multi-step"
pairs_with: [UX-002, UX-003, UX-004, PM-001, GD-004]
```

Default verdict: a feature without a named goal and success metric is not designed yet.

## When to load

- Any design-track ticket (the design phase writes the spec; this skill writes §1 and the workflow map).
- A milestone review that re-plans a flow or opens a design sprint.
- Not for: single-component styling on a signed surface (UX-005 / UX-006 only).

## Rules

### 1. Start from the goal, not the screen

Spec §1 names the persona, the goal in their words, the trigger, and the end state. Cooper's goal-directed design: design for the goal, then the tasks, then the controls. A screen list is not a flow.

### 2. One success metric per flow

Write the metric and how it is read (event, query, or observed behaviour). A flow that cannot be measured gets an explicit assumption and a date to revisit.

### 3. Map every surface the job touches

If the job crosses two or more surfaces (route, dialog, email, extension), write the workflow map (§2b) following `workflow-definition-playbook.md`. Placement is decided with UX-003 before width or spacing.

### 4. Read the catalog and the push-back log first

Before drafting, read the PB- bullets in `knowledge-base/design_playbook.md` and `design-science-playbook.md` for the surface and the product's `docs/design-specs/pushback-log.md`. Cite what you applied in spec §7b. A rejection code repeating on the same surface is a skill failure, not a taste difference.

### 5. Platform posture is explicit

Desktop app, web app, extension, or mobile web: name it, and name the posture rules that follow (density, keyboard, thumb zones). External skills: `ux-design-process`, `ux-knowledge-work`, `ux-desktop-app`, `ux-web-app`.

### 6. Growth is part of the flow

On a flow that touches signup, sharing, invites, upgrade, or first success, bring GD-004 (in-product growth loops) in at the flow stage, not after the mock.

## Workflow

1. Read the ticket, the PRD section, the personas, the catalog topics, and the push-back log.
2. Write §1 (goal, persona, trigger, end state, metric) and the platform posture.
3. Decide surfaces with UX-003; write §2 / §2b.
4. Hand the state matrix to UX-002 and the visual pass to UX-005; keep the metric in §1 unchanged.
5. Fill §7b Catalog applied with the ids you used.

## Deliverables

- `docs/design-specs/<TICKET>.md` §1 Summary (goal, persona, metric), §2 Context & placement, §2b Workflow map when multi-surface.
- Platform posture line in §4 Platform.
- One success metric with its read path.

## Done evidence

```markdown
## Design skill
- UX-001: spec §1 names goal + metric — docs/design-specs/<TICKET>.md
- UX-001: workflow map §2b (or `single surface`) — docs/design-specs/<TICKET>.md
- UX-001: §7b cites <PB/LO ids> and push-back codes read
```

## Anti-patterns

- A spec that opens with a component list and no user goal.
- "Improve the experience" as a success metric.
- Deciding spacing before placement.
- Redrawing a surface the human already signed without a push-back code that asks for it.

## Handoff

- **To UX-002:** goal, persona, surfaces; they write the state matrix and microcopy.
- **To UX-003:** the job and the candidate surfaces; they decide placement.
- **To UX-005 / UX-006:** the signed §1–§2; they draw inside the project kit.
- **To Team 01:** the finished spec and the interactive real-UI mock route after `approve-design` — the mock code is the reference implementation for behavior.

## Deltas

- Studio addition: the push-back log and §7b are required reading and writing; the source method (Cooper) assumes a designer who remembers earlier critique.

## References

- [product-ux-playbook.md](../../../knowledge-base/product-ux-playbook.md) · [workflow-definition-playbook.md](../../../knowledge-base/workflow-definition-playbook.md) · [design-direction-playbook.md](../../../knowledge-base/design-direction-playbook.md)
- External: `ux-design-process`, `ux-knowledge-work`, `ux-desktop-app`, `ux-web-app`
