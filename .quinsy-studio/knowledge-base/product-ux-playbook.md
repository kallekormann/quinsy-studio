# Product UX playbook (UX-001)

End-to-end product design **before** pixels. Distilled from Garrett *The Elements of User Experience*, Cooper *About Face* (goal-directed design), Lou Downe / Stickdorn when the product is a service. Not a reprint.

Load with [workflow-definition-playbook.md](workflow-definition-playbook.md) when the job crosses surfaces. Commercial funnels also load [growth-mechanics-playbook.md](growth-mechanics-playbook.md). How the journey *feels* after the job: [delight-playbook.md](delight-playbook.md) (reflective / service truth — not surface confetti).

## Always

**Do**

- Name the **user goal** (what “done” looks like), not the database entity.
- Work **strategy → scope → structure → skeleton → surface**. Spec §1 must state the job; §2 the structure (placement/flow); visual is last. JTBD / posture check (sovereign vs transient) in §1.
- Pick a **posture**: sovereign (long session, dense, keyboard) vs transient (quick dialog, one job, easy to dismiss).
- Design the **happy path and the recovery path** in the same spec.
- After pay/publish/export: the confirmation **matches the work done** (delight / *Good Services*).

**Don’t**

- Start at the surface (colors, cards) when placement or the job is unset (Garrett).
- Expose the implementation model (tables, IDs, “submit record”) as the UI (Cooper).
- Add a screen because a ticket listed a feature; if it does not serve the goal, cut it.

**Spec / mock fail**

- No goal / success metric in §1.
- Multi-surface feature with no §2b workflow map.
- Mock of a pretty panel whose job is only named in chat.

## Garrett planes (use as a gate, not a poster)

| Plane | Spec must answer | Fail if |
|-------|------------------|---------|
| Strategy | Who is this for, why now | Audience is “everyone” |
| Scope | What is in / out this ticket | Infinite “and also” |
| Structure | IA + interaction (where, in what order) | Only a moodboard |
| Skeleton | Layout of this view, grouping | Unlabeled wire with “TBD” |
| Surface | Tokens, type, states | Surface with no structure above |

Skip a plane only when the ticket is explicitly `ui-styling` on an already placed control.

## Cooper — goals and posture

**Do:** One primary persona *goal* per flow (not a demographic poster). Transient UI: one column, obvious dismiss, no settings dump. Sovereign: preserve context, don’t bounce to a new site chrome for a side task.

**Don’t:** Modal that contains three unrelated jobs. Wizard that restates the same form across four steps with no new decision.

**Fail:** Settings page that is a list of schema fields. Destructive action with no confirm *and* no undo path when the product can undo.

## Service (only if people cross channels)

**Do:** Name the offering in one sentence; the next step is the same in UI, email, and ops (Downe *Good Services*).

**Don’t:** A “success” screen that contradicts the confirmation email.

**Fail:** In-app “you’re done” while a required human step is unnamed (point Team 11/ops, don’t hide it).
