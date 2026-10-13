# Studio learning

This loop exists so the second product is easier than the first. A mistake that stays in one chat is paid for again on the next product.

The product chat does not stop to rewrite the studio. It records the lesson, tells you how many are open, and keeps building. You open a **separate** chat for training. That chat infuses the lesson into a playbook, a skill, or a tool, and you commit that studio change.

| | |
|--|--|
| **Input** | A portable principle. Another product would still need it if the client name were removed. |
| **Output** | A committed change under `.quinsy-studio/` (a playbook, a skill, the learnings catalog, or a tool). |
| **Not an output** | The learning ticket, the inbox row, and anything that names one product. Those stay on your machine. |

## Why a training session

Harvest without infusion is a note nobody reads. Infusion is the step that changes what the next agent does: a line in a skill, a check in a playbook, a default in a tool.

Do it while the context is still warm. If lessons pile up until a later week, the reason is gone and the next product repeats the mistake. The product chat informs you of the open count. It does not steal the conversation to do the infusion itself while a ticket is in progress.

## What is allowed in

A lesson enters the studio only if it is a rule the next product would still need.

| Belongs in the studio | Stays in the product |
|-----------------------|----------------------|
| A must / should / never that any product could hit | A ticket id, a vendor name, a one-off incident |
| A better default in a skill or playbook | This brand's colors, copy, or navigation labels |
| A reusable package that got better | A raw copy of one product's UI |

`./studio verify-abstraction` fails if a client name or a product folder name lands in studio docs. That check is the point of the loop: the studio teaches a method, not a client.

A dropped lesson is written to `projects/<project>/docs/studio-learnings-local.md` so it is not lost. It is not infused.

## How a lesson moves

```
someone sees the gap
→ rewrite it without the client
→ portable?  no  → local log in the product
                 yes → catalog + a local learning ticket
→ product chat keeps building and reports the open count
→ studio chat runs ./studio train
→ you commit the studio change
```

The same gate runs when you ask to log a gap, when a retro is completed, when a reusable package was never promoted, and when a ticket fails its automated gate a third time. Incidents stay local. Principles go on.

Find a rule already written with `./studio learn-find`. Do not paste the inbox into a product chat. The agent reads the catalog, not the queue.

The spec the agent follows is [learning-loop.md](../process/learning-loop.md). The skill is Team 09, dual-loop learning. See [Teams](10-teams.md).
