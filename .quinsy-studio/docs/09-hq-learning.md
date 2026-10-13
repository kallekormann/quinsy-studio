# Studio learning

This loop exists so the second product is easier than the first. A mistake that stays in one chat is paid for again on the next product.

The product chat does not stop to rewrite the studio. It records the lesson, decides whether it was about this product or about the studio, tells you a training session is due, and keeps building. You open a **separate** chat for training. That chat weighs the impact, asks you when the change is large, writes the rule into the file the next product follows, and you commit that studio change.

| | |
|--|--|
| **Input** | A deviation: a gate signed only after two or more rounds, a retro line, a design rejection, a third gate failure. |
| **Output** | One `PB-` bullet in a playbook, a `process/` file, a skill, a template, or a tool — committed in the studio repo, named in the CHANGELOG. |
| **Not an output** | The learning ticket, a catalog entry, anything that names one product. Those stay on your machine. There is no learnings folder in the repo. |

## Why a training session

A note nobody reads changes nothing. The step that changes what the next agent does is the bullet in the skill it reads, the check in the playbook it follows, the default in the tool it runs. That is the only thing this loop counts as done: `./studio train --done` refuses until the target file contains the bullet.

Do it while the context is still warm. If lessons pile up until a later week, the reason is gone and the next product repeats the mistake. The product chat tells you with a **TRAIN_DUE** block on the retro, the execute card, `./studio status`, and `./studio settings`. Say "run training" in a studio chat.

## Project or studio

When a definition only gets signed after several rounds, the check is one question: did this change because of this product, or because the studio's process was wrong?

Every lesson ticket carries the answer in a `## Lesson` block:

| Field | Meaning |
|-------|---------|
| `assumed` | What the studio process, template, or default said. |
| `signed` | What you finally accepted. |
| `verdict` | `project` or `studio`, with one sentence why. |
| `next` | The rule, written as the bullet that goes into the studio file. |
| `target` | The real file: a playbook, a `process/` file, a skill, a template, a tool. |

A retro cannot close while a lesson has no verdict. `project` lands in `projects/<project>/docs/studio-learnings-local.md` with its reason and opens no studio work. `studio` must name a `next` the next product would still need and a real target. You can overrule a `project` verdict from the TRAIN_DUE list (`./studio train --promote <project> --topic "…"`).

## What the training chat does

```
./studio train LO-NNNN
→ ## Impact: files and who reads them, in-flight sprints, signed packets, pro, contra, severity
→ severity floor from the target: process/, studio-tools/, studio-templates/, teams/**/skills/ = high
                                  a knowledge-base playbook = low   (the agent may raise, never lower)
→ low  → infuse now, you are informed
→ high → the card shows pro and contra and stops:
         ./studio train LO-NNNN --approve   |   ./studio train LO-NNNN --defer --reason "…"
→ ./studio infusion-delta --lo LO-NNNN --path <target> --op add --body "assumed: … signed: … next: …"
→ CHANGELOG line → ./studio verify-abstraction → ./studio train --done LO-NNNN
```

A deferred lesson moves to `backlog/deferred/`, stays first in every TRAIN_DUE list, and comes back with `--reopen`. Nothing is written to the studio while it waits.

## What is allowed in

A lesson enters the studio only if it is a rule the next product would still need.

| Belongs in the studio | Stays in the product |
|-----------------------|----------------------|
| A must / should / never that any product could hit | A ticket id, a vendor name, a one-off incident |
| A better default in a skill or playbook | This brand's colors, copy, or navigation labels |
| A reusable package that got better | A raw copy of one product's UI |

`./studio verify-abstraction` fails if a client name or a product folder name lands in studio docs, and `train --done` refuses while it fails. That check is the point of the loop: the studio teaches a method, not a client.

Find a rule already written with `./studio learn-find "<topic>"`. It searches the `PB-` bullets in playbooks, process files, and skills — the places the agent reads. Design specs and milestone reviews cite those ids in `## Catalog applied`; an `LO-` id is a local ticket and does not count.

The spec the agent follows is [learning-loop.md](../process/learning-loop.md). The skill is Team 09, dual-loop learning. See [Teams](10-teams.md).
