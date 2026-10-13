# How Quinsy Studio works

You have an idea, or you already have a product. The studio finds out if the idea is worth building, writes down the whole product, and then builds it. You stop the work at named gates. Between those gates the agent keeps going. You do not have to say "continue."

Read this page once. The other pages are the words you type, and the command list.

| You want | Read |
|----------|------|
| The reference | [docs/README.md](../docs/README.md) |
| This story | This file |
| The words you type | [What you say](../docs/15-what-you-say.md) |
| Every command | [Commands](../docs/05-commands.md) |
| Teams and skills | [Teams](../docs/10-teams.md) |
| What the agent must do | [AGENTS.md](../../AGENTS.md) |

## The path

```
You name a direction
    → the desk researches
    → you pick an idea only when more than one remains
    → the desk explains the case
    → you say yes, and that writes the product definition
    → bootstrap starts the product
    → you sign gate 0, gate 1, gate 2a, gate 2b
    → the phase train designs, writes the architecture, and builds
    → you sign each design phase and each architecture phase
    → every few build phases you review what shipped
    → you ship to production
```

Three ways in:

- No product yet. Start at "You name a direction."
- You already wrote the product definition. Skip to bootstrap.
- The code already exists. Skip to adopt. Same gates after that.

The research desk does not open a sprint and does not run `./studio execute`. The product starts at bootstrap or adopt. Use a new chat for the product. The research chat stays the research chat.

## A walk-through

Here is one product, from the first sentence to the first build. Your product uses the same steps.

1. You say: "Look into sole traders who already wrote the invoice and still chase the payment."
2. The desk reads the web, scores what it found, and explains one case: the problem, the idea, every step of the chase, and the chunks of work.
3. You say: "Yes, write the PRD." A PRD is the product definition. It lands in `intake/` on your machine.
4. You say: "Bootstrap chase from that file and walk me through gate 0."
5. You sign gate 0, then gate 1, then gate 2a, then gate 2b. Each one is a packet you can read. You can send a packet back.
6. You say: "Let the sprint run." The agent designs, specifies, and builds. It stops when a packet or a review needs you.
7. You say: "Ship chase to main." The agent waits until you approve that ship.

## 1. You name a direction

Say what to look into. A market is optional. If you do not name a topic, the desk asks once and does not search.

```text
Look into sole traders who already wrote the invoice and still chase the payment.
```

The desk is `./studio ideate`. The method is [ideation-desk.md](../teams/09-studio-operations-evolution/skills/ideation-desk.md). Notes stay in `ideation/` on this machine. That folder is not the product, and it is not in studio git. The empty seed the desk copies on a fresh machine is `.quinsy-studio/studio-templates/ideation/`.

## 2. The desk researches

After your brief, the same turn runs the research. You are not asked to start the next section. You answer a question only when a fact only you know would change the problem.

| Section | What it settles |
|---------|-----------------|
| Signals | Who has the pain, from pages the desk fetched |
| Cluster | The problem, in one sentence |
| Ideas | One product shape for each problem the sources kept |
| Compete | What already exists, how it connects, and what it costs |
| Shape | The problem, the solution, the architecture, the experience, every step, the first two-month chunk, and the later chunks |
| Score | Ten dimensions. An empty dimension stays empty. It is not a guess |
| Present | `ideation/shortlist/YYYY-MM-DD.md`, the record of what the research kept |

Builder time is not a ceiling. One person, with AI agents for coding and design, ships in chunks of about two months. Each chunk is a full web app. The first chunk is the MVP. Later chunks stay in the idea. Medicine and clinical care are out of reach. Other trades stay in reach when the work is software and the activity is allowed.

When more than one idea remains, the desk stops and asks which problem or idea to focus on. When one remains, it does not ask. It writes the case.

## 3. The case, then the product definition

The desk explains the case in the chat:

- the problem and the evidence
- the idea that came from it
- the solution vision: what the person does, how it connects to tools they already use, and what the product does not become
- every step of the finished product
- the scope: the first two-month chunk, the later chunks, and the scope modules

The last line asks whether this should become the intake PRD. Yes writes `intake/<slug>.md`. No leaves intake empty of that file. Reject or park dismisses the idea. The desk runs approve and promote from that yes. You do not have to say those command names.

The PRD states the full solution: user tasks, system tasks, backend, infrastructure, and scope modules. The module that says bootstrap focuses on it is the first build. Later modules stay in the PRD so the final goal is written down. A thin case is refused.

`intake/` is local. Studio git does not commit it.

## 4. Intake starts the product

You name the project and point at that PRD.

```text
Bootstrap chase from intake/<slug>.md and walk me through gate 0.
```

You can also bring your own material instead of a desk PRD. Put every source file in `intake/<project>/`: several PRDs, notes, a PDF, an old spec. Bootstrap keeps every file, unedited, and writes an index PRD that points at each of them. A single `intake/<project>.md` still works.

`./studio bootstrap` copies the definition into `projects/<project>/` and fills `docs/definitions/`. The product has its own git repo. Studio git never commits `projects/`.

If the code already exists, say adopt instead of bootstrap. The agent writes down what is built, citing file paths, then you sign the same gates. Do not bootstrap over a live tree. See [brownfield-adopt.md](brownfield-adopt.md).

## 5. You sign the prototype

The agent writes the packet, then stops. You approve it, or you send it back. `./studio revise <project> --gate N --feedback "..."` is how a gate is redone.

| Gate | What you are signing | Command |
|------|----------------------|---------|
| 0 | The PRD and the definitions. On adopt, this is "this is what we have." | `./studio approve <project> --gate 0` |
| 1 | Architecture and the decision records. A web project says `Payload: in`, or opts out in an ADR. The next execute writes `apps/web`. | `./studio approve <project> --gate 1` |
| 2a | Design direction, after the interview and `design/DESIGN.md` | `./studio approve <project> --gate 2a` |
| 2b | The project kit: tokens, coded components, a sticker sheet of every state | `./studio approve <project> --gate 2b` |

Sign them in that order. `./studio approve --gate 2` is refused. Gate N waits until gate N-1 is signed. Signing the same gate again is allowed.

Gate 2a and gate 2b are the prototype. Expect several rounds. In the direction interview the agent asks you. It does not invent the brand.

On adopt, gate 2b maps the UI that already exists. It does not build a second, fake prototype.

Detail: [gates.md](gates.md) and [human-in-the-loop.md](human-in-the-loop.md).

## 6. The build

After gate 2b you approve a milestone roadmap in `docs/phases/`. A milestone is a version. M0 is the first. Add as many later versions as the PRD and its source files need. The agent writes tickets for the active milestone only.

Then each cycle is three phases. A phase with no tickets is skipped and does not open a sprint.

| Phase | You sign |
|-------|----------|
| Design | `./studio approve-design <project> --phase` after the spec and the in-context mocks exist |
| Architecture | `./studio approve-arch <project> --phase` after `docs/architecture/<TICKET>.md` exists |
| Implementation | No ticket-by-ticket approval. The agent runs `./studio execute` until the review |

Each ticket is staffed the way a product manager would staff it: an owner skill, plus companion skills from other teams, each with a reason. Login or payments bring in security, personal data brings in privacy, and a screen brings in accessibility and tests. `./studio groom` refuses a sprint with a gap.

A design mock is not a drawing. It is a route inside your product app that renders your own screens with the change woven in, with a screenshot of every state: rest, hover, focus, disabled, empty, loading, error. You sign only mocks that look exactly like the app will.

A design ticket says `architecture delta: none` or names the architecture ticket. An architecture that cannot be built goes back with `./studio approve-arch <project> <TICKET> --reject`.

Implementation only builds tickets whose design and architecture are already approved, or marked not applicable. One unsigned ticket does not freeze a sibling that is ready.

A ticket is done only when four things hold:

1. **A receipt.** Every acceptance criterion has a line that says PASS, FAIL or NOT TESTED, with the file or command that proves it. Paths must exist.
2. **Gate 5 is green.** Build, tests, smoke, plus the security and quality checks (secrets, env leaks, Payload access rules, webhook signatures, accessibility, performance budgets).
3. **A second reviewer passes it.** `./studio qa` hands the ticket to an agent that has not seen the chat. Without proof it fails.
4. **The screen matches the mock.** A ticket with signed mocks is captured at desktop and phone width next to them (`./studio qa --finish`).

A failure goes back to the agent with exactly what to fix. After three failed attempts the ticket moves to `blocked` with an escalation note, and the agent carries on with the other tickets. You are asked only when nothing else can run.

Every few implementation phases the agent stops for a cadence review. The default is every two. First it ships to `dev`, and a fresh agent walks the dev build like a user (`./studio reality-check`). If that walk fails, the agent files bug tickets and fixes them before asking you to look. Then you look at what shipped. A small note becomes a ticket only after `./studio feedback` and `./studio clarify`. A change of direction is an amendment, not a sprint note. See [amendment-intake.md](amendment-intake.md).

When the product is ready to meet people, a launch is its own set of tickets: plan, landing page, waitlist, analytics, lifecycle email, legal review, pre-ship check, results. See [launch-playbook.md](../knowledge-base/launch-playbook.md).

Hygiene (`./studio sprint --kind hygiene`) is lint and debt. It sits outside this train and does not count toward the review.

## 7. Production

`main` is not pushed for you.

```bash
./studio ship <project> --to dev
./studio ship <project> --to main --approve
```

The second command is the production step. You pass `--approve`. Without it, the ship does not happen. Coolify builds that branch, installs the packages in `package.json`, and runs `payload migrate` before the new container serves traffic. The studio does not call a Coolify API.

Each finished ticket is one commit in the product repo, so that ticket can be reverted on its own. Studio git is a different repo.

## 8. The studio learns while this runs

A mistake in a product is harvested as soon as it is seen. The product chat keeps building. A separate studio chat infuses the lesson so the next product does not repeat it.

```
a lesson is seen
    → it is classified
    → the rule is written as a PB- bullet into the file the next project follows
    → the product chat keeps building
    → a studio chat runs ./studio train
    → a playbook, a skill, or a tool changes
```

The bullet lands in a playbook under `knowledge-base/`, a `process/` file, a skill under `teams/`, a template, or a tool. That file is what other people receive. The ticket, the retro, and the train queue stay on the machine that did the work. They are not in studio git.

- [learning-loop.md](learning-loop.md) — harvest, what may be shared, infusion
- [agentic-loop-playbook.md](../knowledge-base/agentic-loop-playbook.md) — a lesson lands as a small change, not a rewritten file
- [The three loops](../docs/02-three-loops.md) — ideation, the product, and studio learning
- [Studio learning](../docs/09-hq-learning.md) — what you see in chat, and why a training session exists

## Where things live

| Thing | Path | Git |
|-------|------|-----|
| Process, skills, catalog, library, templates | `.quinsy-studio/` | Studio repo |
| Ideation notes | `ideation/` | Local |
| PRD before bootstrap | `intake/<slug>.md` | Local |
| Product | `projects/<name>/` | That product's repo |
| Tickets, retros, sprint notes, train queue | `.quinsy-studio/backlog/`, `retros/`, `sprints/`, `learnings/train-queue.json` | Local |

Docker is required to boot, migrate, and pass a gate. Env names live in `env.schema.json`. Values on your machine live in `projects/<name>/.env` and go in with `./studio env <name> up --approve`. Production values live in Coolify. Do not paste either into chat.

## What you say, in order

| Step | You say |
|------|---------|
| Direction | *"Look into …"* |
| A choice, only when several ideas remain | *"Focus on the chase."* |
| The PRD | *"Yes, write the PRD."* or *"No."* |
| Product | *"Bootstrap <project> from intake/<slug>.md and walk me through gate 0."* |
| Existing code | *"Adopt <project> from this folder and reconstruct as-built."* |
| Gates | *"Approve gate 0"* then 1, then 2a, then 2b |
| Build | *"Let the sprint run — execute until HITL."* |
| Production | *"Ship <project> to main."* The agent waits for `--approve` |

HITL means the studio has stopped and is waiting for you. It is a gate (0, 1, 2a, 2b), the milestone roadmap or a milestone review, the design-phase signature, `ship --to main`, a production migration or destructive data step, or a tech-veto. Architecture sign-off, local Docker, cadence reviews, and production ops run from the agent seat and INFORM you. It is not a morning brief, and it is not a thumbs-up on a single ticket. Matrix: [human-in-the-loop.md](human-in-the-loop.md#when-is-hitl-needed).
