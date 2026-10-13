# Skill: Positioning & Messaging

> Distils what the product is, for whom, against what alternative, and why it wins into one core message and a message hierarchy per persona — then keeps every public surface, page, and email on that message. Loads at gate 0 (positioning definition) and on every public surface ticket. The bar: a stranger reads the first screen and can repeat the problem, the audience, and the promise in one sentence.

## Metadata

```
skill_id: GM-007
name: Positioning & Messaging
team: 05-growth-marketing-content
lead_role: Content Strategist
support_roles: [UX Researcher, Growth Designer, Visual Storyteller]
phases: [0, 3, 4]
activation_triggers:
  - docs/definitions/12-positioning.md (gate 0)
  - ticket_type: marketing-page, workflow-explainer; any public page, email, or store listing
  - Phrases: "positioning", "core message", "tagline", "value proposition", "who is it for", "messaging", "hero copy", "persona page"
pairs_with: [UX-004, GM-003, GM-001, GM-002, GD-002, GD-003, UX-007, UX-008]
```

Default verdict: without a filled positioning definition, public copy is not writable.

## When to load

- Gate 0: write `docs/definitions/12-positioning.md` from the PRD and personas; gate 0 refuses a stub.
- Design phase for commercial surfaces: the message hierarchy for the page; problem-first structure.
- Content engine (GM-003) and SEO/AEO (GM-001 / GM-002): the message every piece must carry.
- Not for: UI microcopy inside the product (UX-002).

## Rules

### 1. Positioning is one filled table

Audience (task segment from UX-004), problem in their words, alternative they use today, the product's category, the one difference that matters, and the proof. `12-positioning.md` holds it; everything else derives from it.

### 2. One core message, then a hierarchy

Core message: one sentence a persona would repeat. Then per persona: the problem line, the mechanism line, the proof line, the next step. Pages, emails, and listings pull from this hierarchy; they do not invent new claims.

### 3. Problem first, features last

Every public page opens with the problem in the persona's words, then the mechanism, then proof, then the ask. A feature grid above the fold fails (`anti-slop-design-ux.md` rule 7). Multi-persona products get one page set per persona (`studio-templates/growth/persona-page-set.md`), not one page that speaks to everyone.

### 4. Claims are provable and lawful

Each claim maps to a proof (number, quote with permission, demo). Comparative and superlative claims follow `skill-extensions/marketing-law.md` (UWG). No invented testimonials.

### 5. Say the same thing everywhere

Hero, meta description, OG text, store listing, first email, AEO answer block: same core message, same vocabulary. GM-001 / GM-002 read the hierarchy for titles and answer blocks.

### 6. Messages are tested, not debated

A message change on a live surface is a GD-001 hypothesis with a five-second test (GD-003) before and after.

## Workflow

1. Read the PRD, `02-personas.md`, the problem statements from UX-004, and competitor alternatives.
2. Fill `12-positioning.md`: positioning table, core message, message hierarchy per persona, proof list.
3. For a public surface ticket: write the page's message block (problem → mechanism → proof → ask) into the design spec §5 Story and §6 Growth intent.
4. Hand the hierarchy to GM-001 / GM-002 / GM-003 / GM-006 for titles, answers, content, and email.

## Deliverables

- `docs/definitions/12-positioning.md` (gate 0 requirement).
- Message block in the design spec of every commercial surface.
- Proof list with sources.

## Done evidence

```markdown
## Growth
- GM-007: positioning filled — docs/definitions/12-positioning.md
- GM-007: page opens problem-first — docs/design-specs/<TICKET>.md §5
- GM-007: claims mapped to proof — docs/definitions/12-positioning.md § Proof
```

## Anti-patterns

- "The all-in-one platform for modern teams."
- A hero that lists features.
- One generic page for three personas.
- A claim without a proof line.
- Different taglines on the site, the listing, and the first email.

## Handoff

- **To GD-002 / UX-007:** the message block for the surface and the story.
- **To GM-001 / GM-002:** titles, descriptions, and answer blocks from the hierarchy.
- **To GM-003:** the content engine's message spine.
- **To GM-006:** first-email and lifecycle copy.
- **To PM-002:** the positioning line for the milestone review when the audience changes.

## Deltas

- Studio addition: positioning is a gate-0 definition the tooling refuses to skip; the source method treats it as a marketing exercise after launch.

## References

- [growth-content-playbook.md](../../../knowledge-base/growth-content-playbook.md) · [growth-mechanics-playbook.md](../../../knowledge-base/growth-mechanics-playbook.md)
- [studio-templates/growth/persona-page-set.md](../../../studio-templates/growth/persona-page-set.md) · [studio-templates/growth/seo-foundation-pack.md](../../../studio-templates/growth/seo-foundation-pack.md)
- [skill-extensions/marketing-law.md](../../../knowledge-base/skill-extensions/marketing-law.md) · [anti-slop-design-ux.md](../../../knowledge-base/anti-slop-design-ux.md)
