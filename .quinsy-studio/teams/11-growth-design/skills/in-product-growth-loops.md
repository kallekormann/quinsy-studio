# Skill: In-Product Growth Loops

> Designs the mechanics inside the product that bring the next user, the next action, or the next upgrade without a campaign: invites, sharing, public artifacts, referrals, activation moments, and upgrade paths. Works with Team 10 at the flow stage so the loop is part of the feature, not a banner bolted on afterwards. The bar: every loop is drawn as input → action → output → new input, with the metric that closes it and no dark pattern anywhere in it.

## Metadata

```
skill_id: GD-004
name: In-Product Growth Loops
team: 11-growth-design
lead_role: Growth Designer
support_roles: [Product Designer, UX Designer, Content Strategist]
phases: [1, 3, 4]
activation_triggers:
  - Flow touches signup, onboarding, first success, sharing, invites, export, public pages, upgrade, referral
  - Milestone plan with the coverage area `growth` (Growth loops)
  - Phrases: "viral loop", "referral", "invite", "share", "public link", "watermark", "activation", "aha moment", "upgrade path", "network effect"
pairs_with: [UX-001, UX-002, GD-001, GD-002, GM-003, GM-007, CL-002]
```

Default verdict: a feature that creates value for one user and never reaches a second is not a loop; name whether that is intended.

## When to load

- Gate 1 and milestone planning: decide which loops the product has (acquisition, engagement, monetisation) and in which milestone each ships.
- Design phase: any flow in `activation_triggers`; write `docs/growth/loop-map.md` and the loop section of the spec with UX-001.
- Not for: public marketing pages (GD-002 / GM-007) or email sequences (GM-006).

## Rules

### 1. Draw the loop before the screen

Every loop is a cycle: input (a user or action) → product step → output that reaches someone or something → new input. Use `studio-templates/growth/growth-loop-map.md`. A loop with a missing arrow is a funnel, not a loop; say so.

### 2. One loop per milestone is enough; zero is a decision

The milestone coverage area `growth` (Growth loops) is satisfied by a loop map that names the active loop for the milestone or states `none — reason`. PM-002 reads it at the milestone review.

### 3. Activation is designed as a moment, not a checklist

Name the first-success moment (the "aha") in the persona's words, the shortest path to it, and the metric (time to first success, % reaching it). Onboarding exists to reach that moment; strip steps that do not.

### 4. Sharing creates an artifact someone else wants

Public links, exports, embeds, and watermarks carry value for the receiver first. The receiver's first screen is a GD-002 commercial surface and gets the five-second test (GD-003).

### 5. Upgrade paths are honest and in context

The upgrade moment sits where the limit is felt, shows the plan difference in one sentence, and leaves a free path. Soft paths land on a real plan surface (`upgrade-soft-path` pattern, UX-005 toolbox).

### 6. No dark patterns, no inferred sensitive data

No fake scarcity, guilt streaks, confirmshaming, pre-ticked boxes, or variable-reward loops. Invite and share flows need consent for any contact data (CL-001 / CL-002). Growth that depends on manipulating the user is refused and ticketed as a violation.

### 7. Every loop has one closing metric

Invite acceptance rate, share-to-signup, activation %, upgrade conversion. The metric is in the spec §1 and in `docs/growth/loop-map.md`; GD-001 runs the experiment when the loop underperforms.

## Workflow

1. Read the PRD, personas, positioning (`12-positioning.md`), and the existing loop map.
2. Classify the ticket's flow: acquisition, engagement, or monetisation loop (or none).
3. Draw the loop with the template; name the metric and the dark-pattern check.
4. With UX-001 / UX-002, weave the loop into the flow and the state matrix; the receiver's surface goes to GD-002.
5. Add `## Growth loop` to the design spec; update `docs/growth/loop-map.md`.

## Deliverables

- `docs/growth/loop-map.md` (from `studio-templates/growth/growth-loop-map.md`): loops, status per milestone, metrics.
- Design spec `## Growth loop` block: loop id, step this ticket builds, metric, dark-pattern check.
- Receiver surface named for GD-002 when the loop exits the product.

## Done evidence

```markdown
## Growth
- GD-004: loop <id> drawn — docs/growth/loop-map.md
- GD-004: metric <name> read path — <event/query>
- GD-004: dark-pattern check PASS — docs/design-specs/<TICKET>.md ## Growth loop
```

## Anti-patterns

- A "Share" button with nothing worth receiving.
- Onboarding tours that delay the first success.
- Referral credits before the product has an activation moment.
- Growth banners added after the design is signed.
- Counting a funnel as a loop.

## Handoff

- **To UX-001 / UX-002:** the loop step and the state it adds to the flow.
- **To GD-002 / GD-003:** the receiver's first screen.
- **To GD-001:** the metric and the hypothesis when it underperforms.
- **To GM-003 / GM-007:** the loop's message for content and positioning.
- **To PM-002:** the loop status line for the milestone review.

## Deltas

- Studio addition: the loop map is a milestone coverage area; the source material treats growth loops as a separate marketing concern.

## References

- [growth-mechanics-playbook.md](../../../knowledge-base/growth-mechanics-playbook.md) § In-product loops · [growth-content-playbook.md](../../../knowledge-base/growth-content-playbook.md)
- [studio-templates/growth/growth-loop-map.md](../../../studio-templates/growth/growth-loop-map.md)
- [milestone-coverage-checklist.md](../../../knowledge-base/milestone-coverage-checklist.md)
