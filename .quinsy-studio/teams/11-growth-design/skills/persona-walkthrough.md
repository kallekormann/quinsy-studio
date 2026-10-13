# Skill: Persona Walkthrough

> A structured read of a commercial design packet through the eyes of a person the project already knows. Run a five-second test on the first screen, then walk the real-UI mock fold by fold, and write what that person would understand, doubt and do. The personas come from the PRD and research files, never from imagination. The result is an appendix to the design spec that names friction and turns it into hypotheses for GD-001. It is a qualitative simulation, not user evidence.

## Metadata

```
skill_id: GD-003
name: Persona Walkthrough
team: 11-growth-design
lead_role: Growth Designer
support_roles: [UX Researcher, Visual Storyteller]
phases: [3, 4]
activation_triggers:
  - Design packet for a commercial surface: landing, pricing, checkout, cart, PLP, PDP
  - Any design packet: the five-second test only
  - Phrases: "persona walkthrough", "five-second test", "cognitive walkthrough", "first-screen test"
pairs_with: [GD-001, GD-002, UX-004, UX-007, CL-003]
```

## When to load

- In a design phase, after the real-UI mock screenshots exist and before `approve-design --phase`.
- Full walkthrough: commercial surfaces only (landing, pricing, checkout, cart, PLP, PDP).
- Five-second test: every design packet, commercial or not.
- Not after approval. A signed packet changes only through a new design ticket.

## Rules

### 1. Personas come from the project, not from imagination

Build each persona only from `intake/` PRD segments, `docs/design/discovery.md`, UX-004 research notes and sourced feedback (`./studio feedback`). Every field cites its source line. A field with no source says `unknown`. Do not add age, gender, nationality, family status, hobbies, a stock photo or a psychology type. If the PRD names no segment, stop and write the gap into `docs/design/discovery.md` as a question for the human.

### 2. One persona per PRD segment, at most three

Start with the segment the surface serves first. Add a second only when the PRD names a segment with a different job or a different fear. Contradictions between personas are findings, not errors.

### 3. Persona profile fields

- **Segment:** name from the PRD.
- **Job:** what they are trying to finish on this surface.
- **Arrival:** where they come from (search, ad, referral, in-app link) and the words they used, only if research or GM-001 keyword work records them.
- **Already uses:** the tool or competitor they compare against.
- **Open questions:** what they must know before they act (price, total cost, cancellation, data use).
- **Fears:** stated in the source (hidden cost, lock-in, a scam).
- **Device:** default 390 mobile; 1440 when the PRD says desktop first.

### 4. Five-second test, always

Look at the first stable screen of the mock at 390, then at 1440. Answer three questions in one line each:

1. **What is this?**
2. **Is it for me?**
3. **What do I do next?**

Any "no" or "unclear" is a critical finding. Run this on every design packet. On a non-commercial packet it is the only part of this skill that runs.

### 5. Fold by fold, two voices, kept apart

For each fold of the mock screenshot (one viewport height):

- **Persona:** one to three sentences in plain words. No jargon. "I still don't know what this costs" instead of "pricing clarity is low".
- **Analyst:** the structured read (rule 6).

Never blend the two.

### 6. Analyst read per fold

- **LIFT:** which factor moves. Value proposition, relevance, clarity, urgency, anxiety or distraction.
- **Fogg:** motivation, ability and prompt. Is the next action visible and easy at this point?
- **Action reachable:** can the persona act without scrolling? Yes or no, every fold.
- **Trust:** what this fold adds or removes, and the reason.
- **Influence principles in use:** reciprocity, social proof, authority, commitment, liking, unity. Scarcity and urgency only when true.

### 7. Persuasion stays lawful and true

Recommend only claims the product can back. No invented reviews, counts or logos. No false scarcity or countdowns. No pre-ticked add-ons. Prices show the total with VAT and any shipping before the buy step. The Impressum and the privacy notice are reachable from every commercial page. See GD-002 and CL-003.

### 8. Findings are hypotheses

Each recommendation names the fold, the persona reaction and the framework factor. It becomes a GD-001 claim in spec §6 with a metric or stand-in. Do not report a walkthrough finding as a measured result. Do not predict a conversion lift.

### 9. No quota

Report what the walkthrough shows. A fold with no friction is written as "no friction". Do not invent findings to look thorough.

## Workflow

1. Confirm the surface class (spec §6). Commercial means the full walkthrough.
2. Build the persona profiles from the sources (rules 1–3).
3. Five-second test on the first screen at 390 and 1440.
4. Walk each fold of the mock screenshots. Persona voice, then analyst read.
5. Write the verdict: would act, would not act or unclear, with the reason and the fold where they almost left.
6. Write the recommendations, prioritised: quick wins on this packet, larger changes as new tickets.
7. Feed the best one into spec §6 as the claim and update the mock before `approve-design`.

## Deliverables

Appendix at the end of `docs/design-specs/<TICKET>.md`:

```markdown
## Appendix — Persona walkthrough (GD-003)

Qualitative simulation from project sources. Not user evidence.

### Persona: <PRD segment>
| Field | Value | Source |
|-------|-------|--------|
| Job | Compare plans before a trial | intake/<p>.md §Audience |
| Arrival | unknown | — |

### Five-second test
| Question | 390 | 1440 |
|----------|-----|------|
| What is this? | yes: "invoice reminders" | yes |
| Is it for me? | unclear: no trade named | yes |
| What do I do next? | yes: "Start free" | yes |

### Folds
**Fold 1** — Persona: "..."  Analyst: LIFT relevance ↓; Fogg prompt visible; action reachable yes.

### Verdict
Would act: unclear. Almost left at fold 2 (no total price).

### Recommendations
1. Quick win — fold 2, LIFT anxiety: show total incl. VAT next to the plan. → §6 claim.
```

## Done evidence (receipt)

Design packets have no implementation receipt; the packet is the evidence:

- Commercial packet: the appendix exists, every persona field has a source or `unknown`, and the five-second table has both widths.
- Any packet: the five-second test table exists in the spec.
- The top recommendation appears in spec §6 as the claim, or §6 states why not.

## Anti-patterns

- A persona with a name, an age and a hobby and no source line.
- Statistics about how far visitors scroll or how many leave.
- Scores out of ten in place of a verdict.
- UX jargon in the persona voice.
- Fake urgency or invented social proof as a recommendation.
- Running the walkthrough on a hand-drawn sketch instead of the real-UI mock screenshots.

## Handoff

- **To Team 10:** recommendations to change the mock before `approve-design`.
- **To GD-001:** the claim and the stand-in metric in spec §6.
- **To UX-004:** fields that stayed `unknown` become research questions.
- **To CL-003:** any doubt about a legally required item on the page.

## References

- [growth-mechanics-playbook.md](../../../knowledge-base/growth-mechanics-playbook.md)
- [ux-research-playbook.md](../../../knowledge-base/ux-research-playbook.md) — no invented personas
- [design-spec-template.md](../../../knowledge-base/design-spec-template.md) — §2c mocks, §6 Growth intent
- [hq-agency-agents-integration.md](../../../process/hq-agency-agents-integration.md) — L9
- Frameworks: LIFT (Chris Goward), Fogg Behavior Model (B = MAP), Cialdini influence principles
- Source: msitarzewski/agency-agents `design/design-persona-walkthrough.md` (MIT), rewritten without invented demographics
