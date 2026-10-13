# Commands

You rarely type these. The agent does. This page says what each one does so you can check, or run one yourself.

`<project>` is the folder name under `projects/`. `<ticket>` is that product's ticket id.

## Start and daily driver

| Command | What it does |
|---------|----------------|
| `./studio install` | Once after clone. Installs UI packages the library expects. |
| `./studio verify-worlds` | Checks studio git and product git are not mixed. |
| `./studio verify-abstraction` | Checks studio docs do not name a client. |
| `./studio ideate` | Research desk. Does not build. |
| `./studio bootstrap <project>` | Creates the product from intake and walks toward gate 0. |
| `./studio adopt <project> --from <path-or-url>` | Lays studio docs over code you already have. Does not wipe it. |
| `./studio execute <project>` | The driver. Prints the one next step. The agent does it, then runs execute again, until a human stop. |
| `./studio resume <project>` | A checklist. It does not do the work. Prefer execute. |
| `./studio guard <project> "…"` | Says whether your sentence belongs to this product, the desk, or the studio. |
| `./studio note <project> "…"` | Queues a side note while a ticket is in progress. The agent does not switch tasks. |
| `./studio status <project>` | Where the product is: phase, gate, sprint. |
| `./studio board <project>` | The ticket board. |

## Cursor chats and focus

| Command | What it does |
|---------|----------------|
| `./studio bind <project>` | From the **agent** in that Cursor chat: this chat owns this product. You do not pass an id. See [Several products](03-several-products.md). |
| `./studio bind --show` | From that same chat: prints the bound product, or `(unbound)`. |
| `./studio bind --clear` | From that same chat: drops the binding. |
| `./studio focus <project>` | Picks one product for the whole window and hides the others. Use this when `runtime` is not `cursor`. A bound Cursor chat should not focus a sibling. |
| `./studio isolate <project>` | Rewrites the hide-list. Same idea as focus, without the status banner. |
| `./studio execute <project> --release` | Frees this product's execute slot so another product can start. |

## Gates and phases

| Command | What it does |
|---------|----------------|
| `./studio approve <project> --gate 0` | You sign the product definition. |
| `./studio approve <project> --gate 1` | You sign the architecture. |
| `./studio approve <project> --gate 2a` | You sign the design direction. |
| `./studio approve <project> --gate 2b` | You sign the project kit. Tickets can start after this. |
| `./studio approve <project> --milestones` | You sign the version roadmap. |
| `./studio milestone <project> plan` | Writes the tickets for the active version. |
| `./studio milestone <project> review` | Writes the review when that version's tickets are done. You approve it before the next version. |
| `./studio sprint <project>` | Opens the next phase: design, then architecture, then implementation. An empty phase is skipped. |
| `./studio approve-design <project> --phase` | You sign every design packet in the current phase. |
| `./studio approve-design <project> <ticket> --reject --reason <code>` | Sends one design back. Codes: hierarchy, density, motion, copy, flow, uniqueness, a11y, brand. |
| `./studio mock <project> <ticket>` | Checks the interactive mock and prints the URL plus the click-through script. |
| `./studio approve-arch <project> --phase` | The agent signs the architecture phase. You can still veto. |

## Build, proof, ship

| Command | What it does |
|---------|----------------|
| `./studio ticket <project> "Title"` | Adds a backlog ticket. Staffed with skills. |
| `./studio move <project> <ticket> implement` | Starts the ticket. |
| `./studio move <project> <ticket> done` | Closes it only if the gate, the receipt, and QA pass. |
| `./studio gate <project> --level 5` | Build, tests, and the checks required before done. Level 2 (lint only) is not enough. |
| `./studio qa <project> <ticket>` | A review from a context that did not write the code. |
| `./studio qa <project> <ticket> --finish` | Compares the shipped screen with the signed mock, including the click-through, at desktop and phone width. |
| `./studio env <project> up` | Starts local Docker. The agent may run this. |
| `./studio env <project> migrate` | Applies local database migrations. |
| `./studio env <project> prod --explain` | Lists production variable names. Does not print values. |
| `./studio ops <project> readiness` | Checks the production-shaped compose file. |
| `./studio ops <project> deploy` | Deploys from the agent, using the names in `.env.local`. |
| `./studio ops <project> logs` | Production logs. |
| `./studio ops <project> migrate --prod --approve` | Production migration. Waits for you. |
| `./studio ship <project> --to dev` | Pushes the product repo to `dev`. |
| `./studio ship <project> --to main --approve` | Pushes production. You. Refuses if readiness fails. |
| `./studio reality-check <project>` | A fresh pass over the dev build before the cadence brief. |

## Feedback and direction changes

| Command | What it does |
|---------|----------------|
| `./studio feedback <project> "…"` | Saves a raw note. Not a ticket yet. |
| `./studio clarify <project> FB-001 --approve` | Turns the note into something that can become a ticket. |
| `./studio review <project> --inform` | Writes the cadence brief and continues. You answer later. |
| `./studio amend <project> <brief>` | A change of direction. Analysis only, until you approve the amendment. |
| `./studio groom <project>` | Checks the sprint is staffed and sized. Refuses gaps. |
| `./studio retro <project>` | Writes the sprint retro, including design push-back counts. |

## Library and learning

| Command | What it does |
|---------|----------------|
| `./studio library list` | What the studio can pull. |
| `./studio library suggest <project> "button"` | Finds a match before anyone writes a new component. |
| `./studio library pull <project> button` | Copies that asset into the product. The product adapts it. |
| `./studio learn "Title"` | Opens a studio lesson candidate, only if the wording is reusable. |
| `./studio learn LO-NNNN --verdict studio\|project --reason … --assumed … --signed … --next … [--target …]` | The product agent's answer: was this about the product or about the studio? A retro cannot close without it. |
| `./studio train LO-NNNN` | The training chat. Writes the Impact block; low impact infuses, high impact stops for you. |
| `./studio train LO-NNNN --approve` / `--defer --reason "…"` / `--reopen` | Your decision on a high-impact lesson. Deferred ones wait in `backlog/deferred/`. |
| `./studio infusion-delta --lo LO-NNNN --path <target> --op add --body "assumed: … signed: … next: …"` | Writes the PB- bullet into the file the next product follows. |
| `./studio train --done LO-NNNN` | Closes the lesson. Refuses until the bullet is in the target, the CHANGELOG names it, and verify-abstraction is clean. |
| `./studio train --promote <project> --topic "…"` | You overrule a `project` verdict; the line becomes a studio candidate. |
| `./studio settings` | Shows the studio load caps. Not your model bill. |
| `./studio settings <project>` | The same caps for that product's execute loop. |

On `INFORM cost-cap`, raise the named key in the local settings file. Do not keep stuffing files into the chat. What the numbers mean is [Load caps](14-settings.md).

## Also on the command line

| Command | What it does |
|---------|----------------|
| `./studio init <project> --archetype <type>` | Scaffolds an empty product. Do not use this on code that already runs. Use `adopt`. |
| `./studio intake <project> <file>` | Reads a definition you dropped in `intake/`. |
| `./studio blueprint <project>` | Writes the architecture packet for gate 1. |
| `./studio design <project> --scope journey\|core-views` | Writes the project kit for gate 2b. `as-built` maps an adopted UI and does not invent a prototype. |
| `./studio revise <project> --gate N --feedback "…"` | Sends a gate packet back with your note. |
| `./studio ticket-card <project> <ticket>` | The compact card the agent reads. Not the whole backlog. |
| `./studio receipt <project> <ticket>` | The proof sheet a ticket needs before it can close. |
| `./studio health <project>` | Whether the loop is well formed: gates, skills, worlds. |
| `./studio adr <project> "title"` | Records an architecture decision. |
| `./studio veto <project> --decision … --reason …` | Your tech veto. Stops that approach. |
| `./studio inform <project> …` | An agent-run notice. It does not sign a gate. |
| `./studio env <project> down` | Stops the local Docker stack. |
| `./studio env <project> status` | Whether that stack is up. |
| `./studio repo <project> create\|status` | The product's own git remote. |
| `./studio learn-list` | Open studio lessons and the TRAIN_DUE block. |
| `./studio learn-find "topic"` | Finds a PB- rule already in a playbook, process file, or skill. |
| `./studio infusion` | Lists lessons waiting for a training chat. Does not stop the product. |
| `./studio train --purge-empty` | Closes training jobs that have no observation. |
| `./studio lint-skills` | Checks skill lists and templates still match. |
| `./studio update-skills` | Refreshes an imported skill package. Internal skills stay in charge. |
| `./studio install --with-skills` | Also installs the optional external skill packages. |

`<project>` in every row is the folder name, not a client brand. Studio docs stay generic on purpose. See [The concept](07-concept.md).
