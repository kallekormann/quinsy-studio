# Quinsy Studio

> Filesystem-based operating system for AI-driven software development.  
> After a sprint is groomed, the agent **executes until HITL** — it does not ask “should I continue?”

## What it is

Quinsy Studio separates **Studio HQ** (process, tools, library) from **projects** (client code, each with its own git repo). An IDE agent reads [`AGENTS.md`](AGENTS.md) and runs the `./studio` CLI.

| Layer | Path | In studio git? |
|-------|------|----------------|
| **Studio HQ** | `.quinsy-studio/`, `studio`, `AGENTS.md` | Yes |
| **Projects** | `projects/<name>/` | No — separate repo per project |
| **Intake** | `intake/*.md` | No — local PRDs and optional adopt intent |
| **Amendment briefs** | `intake/amendments/<project>/` | No — local only |
| **Amendment templates** | `.quinsy-studio/studio-templates/amendment_*.md` | Yes — project-agnostic examples |

## Quick start (AI-driven)

**After git clone:**

```bash
./studio install                    # tailwindcss + @headlessui/react (once)
./studio verify-worlds              # studio git ≠ project git
./studio verify-abstraction         # studio docs/tools use <project>, not a client name
```

Pick one path. **`execute` is the driver** after that — one next action until HITL. `./studio resume` is only a checklist.

### New product (PRD)

Add `intake/<project>.md` → *"Bootstrap &lt;project&gt; and walk me through gate 0"*.

```bash
./studio bootstrap my-project     # from intake/<prd>.md
./studio focus my-project
./studio execute my-project       # do NEXT; loop until ACTION is HITL
```

### Existing codebase (adopt — implemented)

Do **not** `init` / `bootstrap` over a live tree. Hand over the repo + how to run it (optional intent from [adopt_intent.md](.quinsy-studio/studio-templates/adopt_intent.md)):

```bash
./studio adopt my-project --from /path/to/repo    # or a git URL
./studio focus my-project
./studio execute my-project       # fill docs/as-built/ → synthesize PRD → HITL gate 0
```

The agent reconstructs **implementation state in depth** (cite file paths; a README restatement is not done). You still approve as-built truth, architecture, design of what exists, then a further-work milestone plan. Process: [brownfield-adopt.md](.quinsy-studio/process/brownfield-adopt.md)

If a learning is identified, execute returns `STUDIO_LO` **before the next project ticket** (including mid-sprint).

Full loop: [GETTING_STARTED — execute loop](.quinsy-studio/GETTING_STARTED.md#the-execute-loop-how-work-actually-proceeds) · [learnings](.quinsy-studio/GETTING_STARTED.md#learnings-harvest-when-identified)

**Three human gates before implementation, then milestone planning:**

| Gate | You approve | Then |
|------|-------------|------|
| 0 | PRD + definitions **or** as-built truth (adopt) | `./studio blueprint` |
| 1 | Architecture + ADRs (as-is on adopt) | `./studio design --scope journey\|core-views` or as-built |
| 2 | Design mocks **or** design of what exists (adopt) | Library promotion (greenfield only) |
| Milestones | Version roadmap (`docs/phases/`) | Tickets for **active milestone** → sprints |

You also approve **sprint scope**, **UI design specs** (`approve-design`), and **sprint review**. Mid-sprint, the agent loops tickets on its own — and infuses studio learnings as soon as they appear (`STUDIO_LO`), without waiting for you to run `./studio learn`.

```bash
./studio approve my-project --gate 0
./studio blueprint my-project && ./studio approve my-project --gate 1
./studio design my-project --scope core-views && ./studio approve my-project --gate 2
./studio approve my-project --milestones    # after agent drafts docs/phases/
./studio sprint my-project --approve-scope  # after scope proposal
./studio execute my-project                 # until HITL (sprint-review) or STUDIO_LO
```

### Execute actions

| ACTION | Meaning |
|--------|---------|
| `IMPLEMENT` | Adopt: fill `docs/as-built/` from code. Sprint: next unblocked ticket (compact CARD) |
| `VERIFY` → `GATE` → `DEBUG` → `MOVE_DONE` | Adopt: synthesize PRD. Sprint: receipt + fresh QA level 5, then mark done |
| `STUDIO_LO` | Infuse an open LO-* in `.quinsy-studio/` **now** — before the next project ticket |
| `HITL` | **You:** gates 0–2 (as-built on adopt), design-approve, sprint scope, sprint review |

Priority: adopt as-built (if needed) → HITL gates → finish an in-progress ticket → **infuse open LOs** → next `IMPLEMENT`. Learnings are harvested automatically (`learn`, retro `--complete`, reuse, 3rd gate fail) into `knowledge-base/learnings/inbox.md` + a classified LO. Do not let them pile until the next sprint.

Full guide: [`.quinsy-studio/GETTING_STARTED.md`](.quinsy-studio/GETTING_STARTED.md) · Agent contract: [`AGENTS.md`](AGENTS.md)

## Talk to the agent (Cursor)

Open this repo in Cursor. You approve HITL stops; the agent runs `./studio execute` in between.

| Step | You say |
|------|---------|
| 1a. New product — PRD in `intake/my-project.md` | *"Bootstrap my-project and walk me through the next gate."* |
| 1b. Existing repo | *"Adopt my-project from this folder and reconstruct as-built."* |
| 2. Gate 0 ready | *"Approve gate 0"* (as-built truth on adopt, or PRD + definitions) |
| 3. Architecture ready | *"Approve gate 1"* |
| 4. Design ready | *"Approve gate 2"* (or *"Design core-views first"*) |
| 5. Milestones | *"Draft milestone roadmap"* → *"Approve milestones"* |
| 6. Build | *"Approve sprint scope, then execute until HITL"* |
| 7. Sprint done | *"Sprint review"* → *"Approve review"* → reuse + retro **auto-harvest** → execute `STUDIO_LO` → next sprint |
| 8. Strategic pivot | *"Run amendment intake for amendment_01"* → review `docs/amendments/AM-001/` → *"Approve amendment AM-001"* |
| Drift | *"Execute my-project — back on track"* |

More examples: [GETTING_STARTED — start here](.quinsy-studio/GETTING_STARTED.md#start-here-tell-the-agent) · [prompt cheat sheet](.quinsy-studio/GETTING_STARTED.md#talk-to-the-agent--prompt-cheat-sheet) · [execute loop](.quinsy-studio/GETTING_STARTED.md#the-execute-loop-how-work-actually-proceeds) · [learnings](.quinsy-studio/GETTING_STARTED.md#learnings-harvest-when-identified)

## Using in Cursor

Open this repo in Cursor. Always-on rules: [`.cursor/rules/quinsy-studio.mdc`](.cursor/rules/quinsy-studio.mdc). Each session: `./studio verify-worlds` → `./studio verify-abstraction` → `focus` → **`execute`** (loop until HITL). You approve gates; the agent runs `./studio`. See [Using Cursor](.quinsy-studio/README.md#4-using-quinsy-studio-in-cursor).

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

**Design discipline (placement before layout):** UI specs require **§2 Context & placement** before polish. See [contextual-ia-playbook](.quinsy-studio/knowledge-base/contextual-ia-playbook.md) · [design-spec-template](.quinsy-studio/knowledge-base/design-spec-template.md) · `./studio approve-design` (warns if missing).

**Studio skill extensions:** [`.quinsy-studio/knowledge-base/skill-extensions/README.md`](.quinsy-studio/knowledge-base/skill-extensions/README.md) — deep playbooks for compliance, PLG, delight UX, security audits (extend CL/GM/UX/PE skills, no new ticket IDs).

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
│   │   └── learnings/inbox.md  # harvest landing pad (immediate, not batched)
│   └── backlog/              # LO-* studio improvements only
├── intake/                   # Raw PRDs + amendment briefs (gitignored)
├── projects/                 # Client projects (gitignored, own .git each)
└── studio                    # CLI entrypoint
```

## Documentation

| Topic | Document |
|-------|----------|
| Execute loop (agentic sprint) | [GETTING_STARTED § execute loop](.quinsy-studio/GETTING_STARTED.md#the-execute-loop-how-work-actually-proceeds) |
| Immediate harvest + STUDIO_LO | [GETTING_STARTED § learnings](.quinsy-studio/GETTING_STARTED.md#learnings-harvest-when-identified) |
| Operations manual | [.quinsy-studio/README.md](.quinsy-studio/README.md) |
| Getting started | [.quinsy-studio/GETTING_STARTED.md](.quinsy-studio/GETTING_STARTED.md) |
| Agent prompts (new product or existing repo) | [GETTING_STARTED § start here](.quinsy-studio/GETTING_STARTED.md#start-here-tell-the-agent) |
| Prompt cheat sheet | [GETTING_STARTED § talk to the agent](.quinsy-studio/GETTING_STARTED.md#talk-to-the-agent--prompt-cheat-sheet) |
| Using in Cursor | [.quinsy-studio/README.md §4](.quinsy-studio/README.md#4-using-quinsy-studio-in-cursor) |
| External skills | [.quinsy-studio/README.md §8](.quinsy-studio/README.md#8-managing-skills) |
| Lifecycle | [process/lifecycle.md](.quinsy-studio/process/lifecycle.md) |
| Milestone planning | [process/milestone-planning.md](.quinsy-studio/process/milestone-planning.md) |
| Amendment intake | [process/amendment-intake.md](.quinsy-studio/process/amendment-intake.md) |
| Existing codebase (adopt) | [process/brownfield-adopt.md](.quinsy-studio/process/brownfield-adopt.md) |
| Studio abstraction (no client names in HQ) | [process/studio-abstraction.md](.quinsy-studio/process/studio-abstraction.md) |
| Learning loop + infusion gate | [process/learning-loop.md](.quinsy-studio/process/learning-loop.md) |
| Contextual IA (feature placement) | [knowledge-base/contextual-ia-playbook.md](.quinsy-studio/knowledge-base/contextual-ia-playbook.md) |
| Product backlog | [process/backlog-model.md](.quinsy-studio/process/backlog-model.md) |
| Human gates 0–2 | [process/gates.md](.quinsy-studio/process/gates.md) |
| Ticket workflow (9 steps) | [process/ticket-workflow.md](.quinsy-studio/process/ticket-workflow.md) |
| Studio library | [studio-library/library_registry.md](.quinsy-studio/studio-library/library_registry.md) |
| Aesthetic presets (Team 10) | [knowledge-base/aesthetic-presets/README.md](.quinsy-studio/knowledge-base/aesthetic-presets/README.md) |
| Skill extensions (deep playbooks) | [knowledge-base/skill-extensions/README.md](.quinsy-studio/knowledge-base/skill-extensions/README.md) |
| Agent context | [process/agent-context.md](.quinsy-studio/process/agent-context.md) |
| Git separation | [process/worlds.md](.quinsy-studio/process/worlds.md) |

## Quality rules

1. **Library-first** — suggest + pull before coding; promote when generic
2. **No code without a ticket** (after gate 2)
3. **Three human gates** — no implementation before gate 2. Existing apps: `./studio adopt` (never empty-init)
4. **Execute loop** — `./studio execute` until HITL; compact cards; receipt + gate 5 before `done`; `STUDIO_LO` before the next project ticket
5. **Sprint HITL** — scope approval → review → feedback → clarify → ticket (see [HITL](.quinsy-studio/process/human-in-the-loop.md))
6. **Milestones** — roadmap after gate 2; milestone review before next version backlog
7. **Amendments** — strategic direction after gate 2 → analysis → revised roadmap → tickets (see [amendment-intake](.quinsy-studio/process/amendment-intake.md))
8. **Placement before layout** — Team 10 §2 Context & placement in design specs; `ia-feature-placement` for cross-surface moves
9. **Immediate harvest** — classify + inbox + LO when a learning is identified; execute `STUDIO_LO` in the same session (`./studio infusion`)
10. **Two git worlds** — never commit `projects/` to this repo; studio HQ stays project-agnostic (`./studio verify-abstraction`)
11. **Anti-slop + ADRs + HITL** — see process docs

## CLI overview

```bash
./studio --help
./studio install                  # after git clone
./studio focus <project> && ./studio execute <project>   # loop until HITL; STUDIO_LO before next project ticket
./studio health <project>
./studio ticket-card <project> <ID>
./studio receipt <project> <ID>
./studio learn "..." --signal tooling-gap   # harvest now → execute STUDIO_LO
./studio infusion                           # must be clear before next project ticket
./studio verify-abstraction
./studio library list
./studio adopt <project> --from <git-url-or-path>
./studio bootstrap <project>
./studio review <project>
./studio feedback <project> "..."
./studio board <project>
```

## Changelog

See [CHANGELOG.md](CHANGELOG.md) · studio process: [`.quinsy-studio/CHANGELOG.md`](.quinsy-studio/CHANGELOG.md)

---

**Version:** 1.15.0  
**Date:** 2026-09-07
