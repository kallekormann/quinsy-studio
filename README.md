# Quinsy Studio

> Filesystem-based operating system for AI-driven software development.

## What it is

Quinsy Studio separates **Studio HQ** (process, tools, library) from **projects** (client code, each with its own git repo). An IDE agent reads [`AGENTS.md`](AGENTS.md) and runs the `./studio` CLI.

| Layer | Path | In studio git? |
|-------|------|----------------|
| **Studio HQ** | `.quinsy-studio/`, `studio`, `AGENTS.md` | Yes |
| **Projects** | `projects/<name>/` | No — separate repo per project |
| **Intake** | `intake/*.md` | No — local only |

## Quick start (AI-driven)

```bash
./studio verify-worlds              # studio git ≠ project git
./studio bootstrap my-project     # from intake/<prd>.md
./studio focus my-project         # active context for agent
./studio resume my-project        # next step only
```

**Three human gates before implementation:**

| Gate | You approve | Then |
|------|-------------|------|
| 0 | PRD + definitions | `./studio blueprint` |
| 1 | Architecture + ADRs | `./studio design --scope journey\|core-views` |
| 2 | Design mocks + sticker sheet | Tickets generated + library promotion |

```bash
./studio approve my-project --gate 0
./studio blueprint my-project && ./studio approve my-project --gate 1
./studio design my-project --scope core-views && ./studio approve my-project --gate 2
./studio sprint my-project
```

Full guide: [`.quinsy-studio/GETTING_STARTED.md`](.quinsy-studio/GETTING_STARTED.md) · Agent contract: [`AGENTS.md`](AGENTS.md)

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
├── .cursor/rules/            # Cursor always-on rules
├── .quinsy-studio/
│   ├── process/              # Lifecycle, gates, ticket workflow, worlds
│   ├── teams/                # 9 teams + skills
│   ├── studio-library/       # Reusable UI + packages (auth, billing, …)
│   ├── studio-tools/         # Python CLI (studio.py)
│   ├── studio-templates/
│   ├── knowledge-base/
│   └── backlog/              # LO-* studio improvements only
├── intake/                   # Raw PRDs (gitignored)
├── projects/                 # Client projects (gitignored, own .git each)
└── studio                    # CLI entrypoint
```

## Documentation

| Topic | Document |
|-------|----------|
| Operations manual | [.quinsy-studio/README.md](.quinsy-studio/README.md) |
| Getting started | [.quinsy-studio/GETTING_STARTED.md](.quinsy-studio/GETTING_STARTED.md) |
| Using in Cursor | [.quinsy-studio/README.md §4](.quinsy-studio/README.md#4-using-quinsy-studio-in-cursor) |
| External skills | [.quinsy-studio/README.md §8](.quinsy-studio/README.md#8-managing-skills) |
| Lifecycle | [process/lifecycle.md](.quinsy-studio/process/lifecycle.md) |
| Human gates 0–2 | [process/gates.md](.quinsy-studio/process/gates.md) |
| Ticket workflow (9 steps) | [process/ticket-workflow.md](.quinsy-studio/process/ticket-workflow.md) |
| Studio library | [studio-library/library_registry.md](.quinsy-studio/studio-library/library_registry.md) |
| Agent context | [process/agent-context.md](.quinsy-studio/process/agent-context.md) |
| Git separation | [process/worlds.md](.quinsy-studio/process/worlds.md) |

## Quality rules

1. **Library-first** — suggest + pull before coding; promote when generic
2. **No code without a ticket** (after gate 2)
3. **Three human gates** — no implementation before gate 2
4. **Two git worlds** — never commit `projects/` to this repo
5. **Anti-slop + ADRs + HITL** — see process docs

## CLI overview

```bash
./studio --help
./studio library list
./studio bootstrap <project>
./studio board <project>
./studio learn "..." --signal tooling-gap
```

## Changelog

See [CHANGELOG.md](CHANGELOG.md).

---

**Version:** 1.5.0  
**Date:** 2026-08-20
