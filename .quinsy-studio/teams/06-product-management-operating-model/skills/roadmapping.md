# Skill: Roadmapping

> The Product Manager owns the roadmap from gate 2b to the last milestone. The roadmap in `docs/phases/` describes the **finished product**, not the MVP: every area the PRD needs has a milestone, M0 is the first two-month chunk, and the human signs each milestone review before the next one is planned. The bar: `./studio approve <p> --milestones` and `./studio milestone <p> --approve` pass without the human filling gaps the PM left open.

## Metadata

```
skill_id: PM-002
name: Roadmapping
team: 06-product-management-operating-model
lead_role: Product Manager
support_roles: [Product Strategist, Systems Architect]
phases: [3, 4, 5, 6, 7]
activation_triggers:
  - After gate 2b, before the first sprint
  - Every milestone's tickets are done (`./studio milestone <p> review`)
  - An approved amendment changes scope (`./studio amend`)
  - Phrases: "roadmap", "milestone", "prioritization", "planning", "milestone plan"
pairs_with: [PM-004, PS-002, PS-004, UX-001, PE-001]
```

Default verdict: a roadmap is incomplete until every required row in `knowledge-base/milestone-coverage-checklist.md` names a milestone.

## When to load

- Drafting or revising `docs/phases/README.md` and `M<n>-*.md`.
- `./studio milestone <p> plan`, `review`, `plan --next`.
- An amendment's `03-milestone-roadmap.md`.
- Not for sprint scope inside a milestone (`./studio sprint`), and not for ticket staffing alone (PM-004).

## Rules

### 1. Plan the whole product

Read the PRD, `docs/definitions/`, the architecture packet and the design baseline. Walk the coverage checklist row by row. Each required row gets a home: a milestone and a depth (foundation, hardening, complete). A row the PRD does not need is marked not required with the PRD sentence that decides it. `approve --milestones` refuses a roadmap with an uncovered required row.

### 2. One milestone is one usable version

Each `M<n>-*.md` follows `studio-templates/phases/milestone.md`: goal for a named persona, in and out of scope, coverage rows, success criteria with the command or route that proves them, decisions for the human. M0 carries scaffolding, data model, auth, app shell, security and ops foundation; it is a thin product, not a demo.

### 3. Tickets for the active milestone only

After the roadmap is signed, write `- <title> :: <scope>` lines under `## Tickets` of the active milestone and run `./studio milestone <p> plan`. The CLI creates and staffs each ticket (PM-004) and stamps `milestone: M<n>`. Later milestones stay as outlines.

### 4. Review before planning the next one

When every milestone ticket is done or cancelled, run `./studio milestone <p> review`. The review reads production state (reality-check verdict), gate and QA metrics, blocked tickets and open feedback, and recommends: an architecture ticket (PS-002) when tickets ended blocked, a design phase when design feedback is open, re-ordered or added sub-milestones when coverage gaps remain. Fill `## Roadmap changes` and edit the `M<n>` files before asking the human.

### 5. Show the HQ knowledge you used

Before planning or reviewing, read the PM CARD files: PM-002, PM-004, PS-002, the coverage checklist, `process/milestone-planning.md`, and the learnings READMEs for process, backend, frontend and design. Cite the PB-ids that changed a recommendation under `## Catalog applied`. A review with no citation is approved with a soft warning; the PM owes an explanation.

### 6. Prioritise within a milestone with RICE and MoSCoW

Reach × Impact × Confidence / Effort orders tickets inside a milestone. Must means the milestone's goal fails without it. Dependencies are written on the ticket (`dependencies:`), and the critical path is named in the milestone file.

## Workflow

1. Gate 2b signed → draft `docs/phases/` from the checklist → `./studio approve <p> --milestones` (human).
2. `./studio milestone <p> plan` → tickets → `./studio groom` → `./studio sprint` cycles.
3. Every ticket done → `./studio milestone <p> review` → fill roadmap changes and catalog citations → `./studio milestone <p> --approve` (human).
4. `./studio milestone <p> plan --next` → step 2.
5. Amendment approved → revise `M<n>` files → `./studio approve <p> --milestones` again.

## Deliverables

- `docs/phases/README.md` — table of milestones, current milestone, links.
- `docs/phases/M<n>-<slug>.md` — one per version, from the template.
- `docs/phases/M<n>-review.md` — written by `review`, completed by the PM.
- Tickets with `milestone: M<n>` in the frontmatter.

## Done evidence

```markdown
## Roadmap
- docs/phases/README.md lists M0–M4; coverage check PASS (./studio approve <p> --milestones)
- docs/phases/M1-review.md: ## Roadmap changes filled, ## Catalog applied cites PB-20261002-004
```

## Anti-patterns

- A roadmap of dates ("MVP, Beta, Launch") with no area rows.
- Security, privacy, operations or growth parked in "later" with no PRD sentence.
- Writing M1 tickets while M0 is open.
- Planning the next milestone without reading the reality-check verdict and the blocked tickets.
- A review whose recommendations ignore the PB- bullets in the playbooks and skills it read.

## Handoff

- **To PM-004:** ticket titles and scope lines; PM-004 staffs them.
- **To PS-002:** an architecture ticket when the review names blocked work.
- **To Team 10:** a design phase when the review names open design feedback.
- **To the human:** `approve --milestones` and `milestone --approve` packets.

## Deltas

Replaced the Now/Next/Later calendar with milestone ownership to project finish, because the calendar hid uncovered areas until they became incidents.

## References

- `knowledge-base/milestone-coverage-checklist.md`
- `process/milestone-planning.md`, `process/lifecycle.md`, `process/iterative-delivery.md`
- `studio-tools/studio_milestones.py`
