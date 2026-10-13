# What you say

You talk. The agent runs `./studio`. These are the sentences that map cleanly.

## Starting

| You want | You say |
|----------|---------|
| A direction, no product | *"Look into …"* Then, if the case is the one, *"Yes, write the PRD."* |
| A definition already in `intake/` | *"Bootstrap `<project>` and walk me through gate 0."* |
| Code that already runs | *"Adopt `<project>` from this folder and reconstruct as-built."* |
| This Cursor chat owns the product | *"Bind this chat to `<project>`."* Then *"Show what this chat is bound to."* |
| Return later | *"Execute `<project>`. Back on track."* |
| A checklist, not the work | *"Resume `<project>`."* Prefer execute. |
| Where things stand | *"What's the status of `<project>`?"* |

## Gates and versions

| You want | You say |
|----------|---------|
| Sign | *"Approve gate 0"* (then 1, then 2a, then 2b) |
| Send back | *"Revise gate 2a: …"* |
| The version plan | *"Approve milestones"* or *"Revise M0 scope: …"* |
| The version is finished | *"Milestone review."* |
| A new direction | *"I added `intake/amendments/<project>/amendment_01.md`. Run amendment intake."* Then *"Approve amendment AM-001."* |

## During a build

| You want | You say |
|----------|---------|
| Let it run | *"Execute until it stops."* |
| See one ticket | *"Show the card for `<ticket>`."* |
| Sign the design phase | *"Approve the design phase."* You have opened the mock URL. |
| Push one design back | *"Reject `<ticket>`, reason: flow."* (or hierarchy, density, motion, copy, uniqueness, a11y, brand) |
| A small idea | *"Feedback: …"* It is not a ticket yet. |
| Stop the ticket | *"Abort."* |
| A side note | Say it. The agent queues it and continues. It does not switch tasks. |

## Studio

| You want | You say |
|----------|---------|
| A lesson for the next product | *"Log a tooling gap: …"* in a studio chat, or let the product chat record it and tell you the count. Infusion is `./studio train` in the studio chat. |
| The load cap | *"Show studio settings for `<project>`."* On `INFORM cost-cap`, raise the named key. See [Load caps](14-settings.md). |

## What a "looks good" does not do

*"Looks good"* on a non-design ticket does not close anything and does not start the next step. The agent runs execute again. You sign the packets in [The product loop](08-product-loop.md), not each ticket.
