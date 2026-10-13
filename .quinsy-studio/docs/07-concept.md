# The concept

Quinsy Studio is a way to go from a direction to a shipped product, and to keep the method when the product is done.

You name a direction. The studio researches it, writes the product down, and builds it. You stop at named gates. Between those gates the agent keeps going. You do not have to say "continue."

Three ideas hold the whole thing together.

**One chat, one job.** Ideation, a product, and studio learning do not share a backlog. A sentence moves from one to the next only at a named door: you say yes, or a finished ticket produces a lesson generic enough to keep. See [The three loops](02-three-loops.md).

**You sign packets, not every ticket.** A packet is a definition, an architecture, a design direction, a project kit, a design phase, a milestone, or a production ship. A ticket in the middle of a build does not wait for "looks good." See [The product loop](08-product-loop.md).

**The studio gets better without stopping the product.** A lesson that would help the next product is infused in a separate chat. The product chat keeps building. See [Studio learning](09-hq-learning.md).

## Two worlds

| World | Path | Git |
|-------|------|-----|
| Studio | `.quinsy-studio/`, `studio`, this manual | This repo |
| Product | `projects/<name>/` | That product's own repo |
| Research and intake | `ideation/`, `intake/` | Not committed |

Studio git holds the method: process, teams, skills, the learnings catalog, the library, and the templates. A clone does not contain your products, your research notes, or the tickets that produced a lesson.

The commit hook refuses to add the local rows. `./studio verify-worlds` checks the split. `./studio verify-abstraction` checks that studio docs say `<project>`, not a client name. A client name in the studio would teach the next product the wrong lesson.

## What stays true

1. **Library first.** Suggest and pull before coding. Do not pull the `feature-gating` stub. `billing` is pullable. Promote only when the generic piece got better. See [Library](12-library.md).
2. **No product code before the gates.** Gates are 0, then 1, then 2a, then 2b. An existing app uses `./studio adopt`, never an empty init.
3. **No code without a ticket** after gate 2b.
4. **Execute until it stops.** `./studio execute` is the driver. `./studio resume` is only a checklist.
5. **Done means proven.** A receipt with PASS / FAIL / NOT TESTED and real paths, a green automated gate 5, a QA PASS from a reviewer that has not seen the chat, and on UI tickets a screen that matches the signed mock. Three failed attempts move a ticket to `blocked`. The others continue.
6. **Every ticket is staffed.** An owner skill plus companions, with reasons. `./studio groom` refuses gaps. See [Teams](10-teams.md).
7. **Mocks are a prototype you can click.** A design mock is a route in the product app. Screenshots are the record. You review the running route.
8. **You sign packets, not every ticket.** Design phase, then architecture (the agent signs, you can veto), then a cadence brief every few implementation phases. Hygiene sits outside that train.
9. **Milestones** after gate 2b. Finish a milestone review before the next version's tickets.
10. **Amendments** are a change of direction. Sprint feedback is a small note. They are different commands.
11. **Placement before layout.** A UI spec is a file on disk, with every state, using the project's tokens. Motion is on unless the spec says `motion: off`.
12. **A lesson is infused while the product keeps building.** The catalog, the playbook, or the skill is what gets committed.
13. **Two git repos.** Product commits live in `projects/<name>/`. Studio commits never include `projects/`, `intake/`, or `ideation/`.
14. **One chat per product.** In Cursor, bind the chat. Elsewhere, `./studio focus` hides the other products. Five products can execute at once.
15. **Load caps** are in `studio.settings.yaml`. They are not your model bill. On `INFORM cost-cap`, raise the named key. See [Load caps](14-settings.md).
16. **Docker is required** to boot, migrate, and pass a gate. Env names live in `env.schema.json`. Do not read `.env` values into chat.

## Where the long specs live

This folder is the book you browse. The files under `.quinsy-studio/process/` are the spec the agent follows. When a chapter here and a process file disagree on a human stop, the process file [human-in-the-loop.md](../process/human-in-the-loop.md) is the checklist. This book is the explanation.
