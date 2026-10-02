# Quinsy Studio

You name a direction. The studio researches it, writes the product down, and builds it. You stop at named gates. Between those gates the agent keeps going.

The story, in order, is [How Quinsy Studio works](.quinsy-studio/process/studio-overview.md). The words you type are in [Getting Started](.quinsy-studio/GETTING_STARTED.md). Every command is in the [operations manual](.quinsy-studio/README.md). The agent contract is [AGENTS.md](AGENTS.md).

## What is in this repo

Studio git holds the skilled studio: process, teams, skills, the learnings catalog, the library, and the templates. A clone does not contain your products, your research notes, or the tickets that produced a lesson.

| Layer | Path | In studio git? |
|-------|------|----------------|
| Studio HQ | `.quinsy-studio/`, `studio`, `AGENTS.md` | Yes |
| Learnings catalog | `knowledge-base/learnings/<domain>/` | Yes — the principle |
| Ideation seed | `.quinsy-studio/studio-templates/ideation/` | Yes — empty desk |
| Ideation notes | `ideation/` | No |
| Products | `projects/<name>/` | No — each product has its own git repo |
| Product definition before bootstrap | `intake/*.md` | No |
| Amendment briefs | `intake/amendments/<project>/` | No |
| Amendment template | `.quinsy-studio/studio-templates/amendment_01.example.md` | Yes |
| Tickets, retros, sprint notes, train queue | `.quinsy-studio/backlog/`, `retros/`, `sprints/`, `learnings/train-queue.json`, `learnings/archive/` | No |

The commit hook refuses to add the local rows. See [worlds.md](.quinsy-studio/process/worlds.md).

## After you clone

```bash
./studio install                    # once: Tailwind and Headless UI
./studio verify-worlds              # studio git is not product git
./studio verify-abstraction         # studio docs say <project>, not a client name
```

Node.js 20 or newer. `node_modules/` is not committed. Optional skill packages: `./studio install --with-skills`.

Open this repo in Cursor, Claude Code, or Gemini CLI. You talk. The agent runs `./studio`. Keys stay in that host.

## Three ways to start

| You have | You say |
|----------|---------|
| A direction, no product | *"Look into …"* The desk explains the case. You say *"Yes, write the PRD."* |
| A product definition in `intake/<project>.md` | *"Bootstrap <project> and walk me through gate 0."* |
| Code that already runs | *"Adopt <project> from this folder and reconstruct as-built."* |

Then you sign gate 0, gate 1, gate 2a, and gate 2b, in that order. `approve --gate 2` is refused. After that the agent designs, specifies, and builds until it needs you again. Production is `./studio ship <project> --to main --approve`.

The walk-through is in [the story](.quinsy-studio/process/studio-overview.md). The full script is in [Getting Started](.quinsy-studio/GETTING_STARTED.md#start-here-tell-the-agent).

## What stays true

1. **Library first.** Suggest and pull before coding. Do not pull the stubs `billing` and `feature-gating`. Promote only when the generic piece got better.
2. **No product code before the gates.** Gates are 0, then 1, then 2a, then 2b. An existing app uses `./studio adopt`, never an empty init.
3. **No code without a ticket** after gate 2b.
4. **Execute until it stops.** `./studio execute` is the driver. `./studio resume` is only a checklist. A finished ticket needs a receipt and gate 5. The agent does not wait for "looks good" on that ticket.
5. **You sign packets, not every ticket.** Design phase, architecture phase, then a cadence review every few implementation phases. Hygiene sits outside that train.
6. **Milestones** after gate 2b. Finish a milestone review before the next version's tickets.
7. **Amendments** are a change of direction. Sprint feedback is a small note. They are different commands.
8. **Placement before layout.** A UI spec is a file on disk, with every state, using the project's tokens. Motion is on unless the spec says `motion: off`.
9. **A lesson is infused while the product keeps building.** The catalog, the playbook, or the skill is what gets committed. The ticket stays local.
10. **Two git repos.** Product commits live in `projects/<name>/`. Studio commits never include `projects/`, `intake/`, or `ideation/`.
11. **One chat per product.** `./studio focus` hides the other products from the agent. It is an assignment, not a sandbox. The default is five products at once.
12. **Load caps** are in `studio.settings.yaml`. On `INFORM cost-cap`, raise the named key. Do not paste more files in.
13. **Docker is required** to boot, migrate, and pass a gate. Env names live in `env.schema.json`. Values go in with `./studio env … --approve`. Do not read `.env` values into chat.

## Where to read the rest

| Topic | Document |
|-------|----------|
| The path | [process/studio-overview.md](.quinsy-studio/process/studio-overview.md) |
| Words you type | [GETTING_STARTED.md](.quinsy-studio/GETTING_STARTED.md) |
| Ideation desk | [Getting Started § ideation](.quinsy-studio/GETTING_STARTED.md#ideation-desk) · [ideation-desk.md](.quinsy-studio/teams/09-studio-operations-evolution/skills/ideation-desk.md) |
| Execute loop | [Getting Started § execute](.quinsy-studio/GETTING_STARTED.md#the-execute-loop-how-work-actually-proceeds) |
| Learnings | [Getting Started § learnings](.quinsy-studio/GETTING_STARTED.md#learnings-harvest-when-identified) |
| Cost and tokens | [Getting Started § settings](.quinsy-studio/GETTING_STARTED.md#studio-settings-cost--tokens) |
| Motion | [Getting Started § motion](.quinsy-studio/GETTING_STARTED.md#motion-default-on) · [motion-transitions](.quinsy-studio/knowledge-base/skill-extensions/motion-transitions.md) |
| Cursor, commands, skills | [Operations manual](.quinsy-studio/README.md) |
| Docker, secrets, leases | [hq-isolation-sprints.md](.quinsy-studio/process/hq-isolation-sprints.md) |
| Two git worlds | [worlds.md](.quinsy-studio/process/worlds.md) |
| Gates | [gates.md](.quinsy-studio/process/gates.md) |
| Human stops | [human-in-the-loop.md](.quinsy-studio/process/human-in-the-loop.md) |
| Adopt an existing repo | [brownfield-adopt.md](.quinsy-studio/process/brownfield-adopt.md) |
| Amendments | [amendment-intake.md](.quinsy-studio/process/amendment-intake.md) |
| Milestones | [milestone-planning.md](.quinsy-studio/process/milestone-planning.md) |
| Library | [library_registry.md](.quinsy-studio/studio-library/library_registry.md) |
| Learning loop | [learning-loop.md](.quinsy-studio/process/learning-loop.md) |
| No client names in HQ | [studio-abstraction.md](.quinsy-studio/process/studio-abstraction.md) |
| Changelog | [CHANGELOG.md](CHANGELOG.md) · [studio changelog](.quinsy-studio/CHANGELOG.md) |

Other hosts use the same `./studio` loop: [Claude Code](CLAUDE.md) · [Gemini CLI](GEMINI.md).
