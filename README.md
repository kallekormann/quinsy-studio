# Quinsy Studio

> Filesystem-based operating system for AI-driven software development.

## What it is

Quinsy Studio separates **Studio HQ** (process, tools, library) from **projects** (client code, each with its own git repo). An IDE agent reads [`AGENTS.md`](AGENTS.md) and runs the `./studio` CLI.

| Layer | Path | In studio git? |
|-------|------|----------------|
| **Studio HQ** | `.quinsy-studio/`, `studio`, `AGENTS.md` | Yes |
| **Projects** | `projects/<name>/` | No — separate repo per project |
| **Intake** | `intake/*.md` | No — local only |
| **Amendment examples** | `intake/amendments/**/amendment_*.example.md` | Yes — templates only |

## Quick start (AI-driven)

**After git clone:**

```bash
./studio install                    # tailwindcss + @headlessui/react (once)
./studio verify-worlds              # studio git ≠ project git
```

**Fastest path:** add `intake/<project>.md` → in Cursor say *"Bootstrap &lt;project&gt; and walk me through gate 0"*.

```bash
./studio bootstrap my-project     # from intake/<prd>.md
./studio focus my-project         # active context for agent
./studio resume my-project        # next step only
```

Full agent prompts: [GETTING_STARTED — prompt cheat sheet](.quinsy-studio/GETTING_STARTED.md#talk-to-the-agent--prompt-cheat-sheet)

**Three human gates before implementation, then milestone planning:**

| Gate | You approve | Then |
|------|-------------|------|
| 0 | PRD + definitions | `./studio blueprint` |
| 1 | Architecture + ADRs | `./studio design --scope journey\|core-views` |
| 2 | Design mocks + sticker sheet | Library promotion |
| Milestones | Version roadmap (`docs/phases/`) | Tickets for **active milestone** → sprints |

```bash
./studio approve my-project --gate 0
./studio blueprint my-project && ./studio approve my-project --gate 1
./studio design my-project --scope core-views && ./studio approve my-project --gate 2
./studio approve my-project --milestones    # after agent drafts docs/phases/
./studio sprint my-project --approve-scope  # after scope proposal
```

Full guide: [`.quinsy-studio/GETTING_STARTED.md`](.quinsy-studio/GETTING_STARTED.md) · Agent contract: [`AGENTS.md`](AGENTS.md)

## Talk to the agent (Cursor)

Open this repo in Cursor. You approve; the agent runs `./studio`.

| Step | You say |
|------|---------|
| 1. PRD in `intake/my-project.md` | *"Bootstrap my-project and walk me through the next gate."* |
| 2. Gate 0 ready | *"Approve gate 0"* |
| 3. Architecture ready | *"Approve gate 1"* |
| 4. Design ready | *"Approve gate 2"* (or *"Design core-views first"*) |
| 5. Milestones | *"Draft milestone roadmap"* → *"Approve milestones"* |
| 6. Build | *"Start sprint and implement the first ticket"* |
| 7. Sprint done | *"Sprint review"* → *"Approve review"* · feedback via *"I want …"* (not blind tickets) |
| 8. Strategic pivot | *"Run amendment intake for amendment_01"* → review `docs/amendments/AM-001/` → *"Approve amendment AM-001"* |
| Drift | *"Resume my-project — back on track"* |

More examples: [GETTING_STARTED — from PRD to sprint](.quinsy-studio/GETTING_STARTED.md#start-here-prd-in-intake--tell-the-agent) · [prompt cheat sheet](.quinsy-studio/GETTING_STARTED.md#talk-to-the-agent--prompt-cheat-sheet)

## Using in Cursor

Open this repo in Cursor. Always-on rules: [`.cursor/rules/quinsy-studio.mdc`](.cursor/rules/quinsy-studio.mdc). Each session: `./studio verify-worlds` → `focus` → `resume`. You approve gates; the agent runs `./studio` and fills artifacts. See [Using Cursor](.quinsy-studio/README.md#4-using-quinsy-studio-in-cursor).

## Library-first (UI + code)

Before writing new code, pull from the studio library:

```bash
./studio library list
./studio library suggest my-project "auth billing"
./studio library pull my-project auth billing button
```

After a ticket is done, promote generic changes:

```bash
./studio library promote my-project packages/billing --ticket MY-0001
```

Registry: [`.quinsy-studio/studio-library/library_registry.md`](.quinsy-studio/studio-library/library_registry.md)

**Team 10 aesthetic presets:** [`.quinsy-studio/knowledge-base/aesthetic-presets/README.md`](.quinsy-studio/knowledge-base/aesthetic-presets/README.md) — required in UI design specs (stripe-like, apple-like, soft-ui, …).

## Context & scope (agent)

```bash
./studio focus <project>                    # scope banner
./studio guard <project> "user request"     # in-scope / needs ticket / pre-impl
./studio revise <project> --gate 1 --feedback "..."
```

Docs: [agent-context](.quinsy-studio/process/agent-context.md) · [two worlds](.quinsy-studio/process/worlds.md)

## Repository layout

```
quinsy-studio/
├── AGENTS.md                 # IDE agent contract (read first)
├── package.json              # Studio UI deps (Tailwind + Headless UI)
├── .cursor/rules/            # Cursor always-on rules
├── .quinsy-studio/
│   ├── process/              # Lifecycle, gates, ticket workflow, worlds
│   ├── teams/                # 9 teams + skills
│   ├── studio-library/       # Reusable UI + packages (auth, billing, …)
│   ├── studio-tools/         # Python CLI (studio.py)
│   ├── studio-templates/
│   ├── knowledge-base/
│   └── backlog/              # LO-* studio improvements only
├── intake/                   # Raw PRDs (gitignored); amendment *.example.md committed
│   └── amendments/<p>/       # Human briefs local; amendment_*.example.md in git
├── projects/                 # Client projects (gitignored, own .git each)
└── studio                    # CLI entrypoint
```

## Documentation

| Topic | Document |
|-------|----------|
| Operations manual | [.quinsy-studio/README.md](.quinsy-studio/README.md) |
| Getting started | [.quinsy-studio/GETTING_STARTED.md](.quinsy-studio/GETTING_STARTED.md) |
| Agent prompts (PRD → sprint) | [GETTING_STARTED § start here](.quinsy-studio/GETTING_STARTED.md#start-here-prd-in-intake--tell-the-agent) |
| Prompt cheat sheet | [GETTING_STARTED § talk to the agent](.quinsy-studio/GETTING_STARTED.md#talk-to-the-agent--prompt-cheat-sheet) |
| Using in Cursor | [.quinsy-studio/README.md §4](.quinsy-studio/README.md#4-using-quinsy-studio-in-cursor) |
| External skills | [.quinsy-studio/README.md §8](.quinsy-studio/README.md#8-managing-skills) |
| Lifecycle | [process/lifecycle.md](.quinsy-studio/process/lifecycle.md) |
| Milestone planning | [process/milestone-planning.md](.quinsy-studio/process/milestone-planning.md) |
| Amendment intake | [process/amendment-intake.md](.quinsy-studio/process/amendment-intake.md) |
| Product backlog | [process/backlog-model.md](.quinsy-studio/process/backlog-model.md) |
| Human gates 0–2 | [process/gates.md](.quinsy-studio/process/gates.md) |
| Ticket workflow (9 steps) | [process/ticket-workflow.md](.quinsy-studio/process/ticket-workflow.md) |
| Studio library | [studio-library/library_registry.md](.quinsy-studio/studio-library/library_registry.md) |
| Aesthetic presets (Team 10) | [knowledge-base/aesthetic-presets/README.md](.quinsy-studio/knowledge-base/aesthetic-presets/README.md) |
| Agent context | [process/agent-context.md](.quinsy-studio/process/agent-context.md) |
| Git separation | [process/worlds.md](.quinsy-studio/process/worlds.md) |

## Quality rules

1. **Library-first** — suggest + pull before coding; promote when generic
2. **No code without a ticket** (after gate 2)
3. **Three human gates** — no implementation before gate 2
4. **Sprint HITL** — scope approval → review → feedback → clarify → ticket (see [HITL](.quinsy-studio/process/human-in-the-loop.md))
5. **Milestones** — roadmap after gate 2; milestone review before next version backlog
6. **Amendments** — strategic direction after gate 2 → analysis → revised roadmap → tickets (see [amendment-intake](.quinsy-studio/process/amendment-intake.md))
7. **Two git worlds** — never commit `projects/` to this repo
8. **Anti-slop + ADRs + HITL** — see process docs

## CLI overview

```bash
./studio --help
./studio install                  # after git clone
./studio library list
./studio bootstrap <project>
./studio review <project>
./studio feedback <project> "..."
./studio amend <project> intake/amendments/<p>/amendment_01.md
./studio amendments <project>
./studio board <project>
./studio learn "..." --signal tooling-gap
```

## Changelog

See [CHANGELOG.md](CHANGELOG.md).

---

**Version:** 1.10.0  
**Date:** 2026-08-25
