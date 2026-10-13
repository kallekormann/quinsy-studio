# Growth loop map — <product>

Skill GD-004. Copy to `projects/<p>/docs/growth/loop-map.md`. One row per loop; one loop active per milestone is enough. `none — reason` is a valid milestone line. PM-002 reads this at every milestone review.

## Loops

| Id | Type | Input → step → output → new input | Closing metric | Read path | Status |
|----|------|-----------------------------------|----------------|-----------|--------|
| L1 | activation | signup → <shortest path> → first success (<aha in persona words>) → retained user | time to first success; % reaching it | <event / query> | planned M1 |
| L2 | sharing | <user action> → <artifact worth receiving> → receiver lands on <GD-002 surface> → signup | share-to-signup | <event / query> | planned M2 |
| L3 | upgrade | <limit felt here> → one-sentence plan difference, free path kept → upgrade | upgrade conversion at the moment | <event / query> | planned M3 |

## Per milestone

| Milestone | Active loop | Ticket(s) | Dark-pattern check | Result |
|-----------|-------------|-----------|--------------------|--------|
| M1 | L1 | <ticket ids> | PASS / FAIL | <metric value or `not yet read`> |

## Dark-pattern check (every loop)

- [ ] No fake scarcity, countdowns, or guilt streaks
- [ ] No confirmshaming or pre-ticked options
- [ ] Consent for any contact data in invites or shares (CL-001 / CL-002)
- [ ] No variable-reward mechanics
- [ ] No inferred health, mood, or other Art. 9 data used to tune the loop
- [ ] A free path stays next to every upgrade prompt

## Handoffs

- Receiver's first screen → GD-002 commercial surface + GD-003 five-second test.
- Underperforming metric → GD-001 hypothesis.
- Loop message → GM-007 message hierarchy.
