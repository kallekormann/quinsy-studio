# How Quinsy Studio works

You bring a direction, or a product that already exists. The studio researches that direction, writes a product definition, and then builds it. You stop the loop at named gates. Between those gates the agent keeps going.

Read this page for the path. The linked pages are the detail for each step.

| You want | Read |
|----------|------|
| The path on one page | This file |
| What to say in chat | [GETTING_STARTED.md](../GETTING_STARTED.md) |
| Day-to-day operation, skills, and the learning loop | [Operations manual](../README.md) |
| The short entry | [README.md](../../README.md) |
| What the agent must do | [AGENTS.md](../../AGENTS.md) |

## The path

```
You name a direction
    → ideation researches and presents a shortlist
    → you approve one idea
    → promote writes the PRD (intake/<slug>.md)
    → bootstrap starts the product
    → you sign gate 0, gate 1, gate 2a, gate 2b
    → the phase train designs, specifies architecture, and implements
    → you sign each design phase and each architecture phase
    → cadence review every few implementation phases
    → you ship to production
```

A product that already has a codebase skips ideation and starts at adopt. A product that already has a PRD you wrote skips ideation and starts at bootstrap.

Ideation does not open a sprint and does not call `./studio execute`. The product loop starts only after bootstrap or adopt.

## 1. You name a direction

Say what to look into. A market is optional. If you do not name a topic, the desk asks once and does not search.

```text
Look into sole traders who already wrote the invoice and still chase the payment.
```

The desk is `./studio ideate`. The method is [ideation-desk.md](../teams/09-studio-operations-evolution/skills/ideation-desk.md). Notes stay in `ideation/` on this machine. That folder is not the product and it is not studio git.

## 2. The desk researches and presents

After your brief, the same turn runs through the shortlist. You are not asked to continue between sections.

| Section | What it settles |
|---------|-----------------|
| Signals | Who has the pain, from fetched pages |
| Cluster | The problem sentence |
| Ideas | One product shape per problem the sources kept |
| Compete | What already exists, how it connects, and what it costs |
| Shape | Problem, solution, architecture, experience, every step, the first two-month chunk, and the later chunks |
| Score | Ten dimensions. An empty dimension is not a guess |
| Present | `ideation/shortlist/YYYY-MM-DD.md` |

Builder time is not a ceiling. One person, with AI agents for coding and design, ships in chunks of about two months. Each chunk is a full web app. The first chunk is the MVP. Later chunks stay in the idea. Medicine and clinical care are out of reach. Other trades stay in reach when the work is software and the activity is allowed.

You then say one of: **approve** the idea, **reject** it with a reason, or **park** it with a note.

## 3. Promote writes the PRD

Approve is not the PRD. Promote is.

```bash
./studio ideate approve I-001
./studio ideate promote
```

Promote writes `intake/<slug>.md`. That file is the product definition the rest of the studio reads. It states the full solution: user tasks, system tasks, backend, infrastructure, and scope modules. The module that says bootstrap focuses on it is the first build. Later modules stay in the PRD so the final goal is written down. Promote refuses a thin brief.

`intake/` is local. It is not committed in studio git.

## 4. Intake starts the product

You name the project and point at that PRD.

```text
Bootstrap <project> from intake/<slug>.md and walk me through gate 0.
```

`./studio bootstrap` copies the definition into `projects/<project>/` and fills `docs/definitions/`. The product has its own git repo. Studio git never commits `projects/`.

Use one chat for the product from here on. The ideation chat does not become the build chat.

If the code already exists, say adopt instead of bootstrap. The agent reconstructs what is built, then you sign the same gates. See [brownfield-adopt.md](brownfield-adopt.md).

## 5. You sign the prototype

The agent produces the artifact, then stops. You approve, or you send it back. `./studio revise <project> --gate N --feedback "..."` is how a gate is redone.

| Gate | What you are signing | Command |
|------|----------------------|---------|
| 0 | The PRD and the definitions | `./studio approve <project> --gate 0` |
| 1 | Architecture and ADRs | `./studio approve <project> --gate 1` |
| 2a | Design direction, after the interview and `design/DESIGN.md` | `./studio approve <project> --gate 2a` |
| 2b | The project kit: tokens, coded components, sticker sheet of all states | `./studio approve <project> --gate 2b` |

`--gate 2` is refused. Sign 2a, then 2b. Detail: [gates.md](gates.md) and [human-in-the-loop.md](human-in-the-loop.md).

Gate 2a and gate 2b are the prototype. Expect several rounds. The agent does not invent the brand in the discovery interview.

## 6. The build

After gate 2b you approve a milestone roadmap (`docs/phases/`). Then each cycle is a design phase, an architecture phase, and an implementation phase. A phase with no tickets is skipped.

| Phase | You sign |
|-------|----------|
| Design | `./studio approve-design <project> --phase` after the spec and the in-context mocks exist |
| Architecture | `./studio approve-arch <project> --phase` after `docs/architecture/<TICKET>.md` exists |
| Implementation | No ticket-by-ticket approval. The agent runs `./studio execute` until the cadence review |

Implementation only builds tickets whose design and architecture are already approved, or marked not applicable. One unsigned ticket does not freeze a sibling that is ready.

Every few implementation phases (the default is two) the agent stops for a cadence review. You look at what shipped. Small notes become tickets only after `./studio feedback` and `./studio clarify`. A change of direction is an amendment, not a sprint note. See [amendment-intake.md](amendment-intake.md).

Before that review, the agent may ship the branch to `dev`. Production is the next section.

## 7. Production

`main` is not pushed for you.

```bash
./studio ship <project> --to dev
./studio ship <project> --to main --approve
```

The second command is the production kickoff. You pass `--approve`. Without it, the ship does not happen.

## 8. The studio learns while this runs

A mistake in a product is harvested as soon as it is identified. The product chat keeps building. A separate HQ chat infuses the lesson into the studio so the next product does not repeat it.

```
learning identified
    → classify
    → inbox + LO ticket
    → product chat keeps IMPLEMENT
    → HQ chat runs ./studio train
    → the playbook or the tool changes
```

That loop is the detail under this overview:

- [learning-loop.md](learning-loop.md) — harvest, portability, infusion
- [agentic-loop-playbook.md](../knowledge-base/agentic-loop-playbook.md) — how a lesson lands as a delta, not a rewritten file
- [Operations manual §10](../README.md#10-the-dual-loop) — local project loop and global studio loop
- [GETTING_STARTED § learnings](../GETTING_STARTED.md#learnings-harvest-when-identified) — what you see in chat

Studio improvements are `LO-*` tickets in `.quinsy-studio/backlog/`. They are not product tickets.

## Where things live

| Thing | Path | Git |
|-------|------|-----|
| This process | `.quinsy-studio/process/` | Studio repo |
| Ideation notes | `ideation/` | Local |
| PRD before bootstrap | `intake/<slug>.md` | Local |
| Product | `projects/<name>/` | That product's repo |

## What you say, in order

| Step | You say |
|------|---------|
| Direction | *"Look into …"* |
| Shortlist | *"Approve I-001"* or *"Reject I-001 because …"* or *"Park I-001 because …"* |
| PRD | *"Promote I-001"* |
| Product | *"Bootstrap <project> from intake/<slug>.md and walk me through gate 0."* |
| Gates | *"Approve gate 0"* then 1, then 2a, then 2b |
| Build | *"Let the sprint run — execute until HITL."* |
| Production | *"Ship <project> to main."* The agent waits for `--approve` |
