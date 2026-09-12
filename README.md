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

Start-of-project HITL (you, not the agent): **gate 0 PRD/as-built → gate 1 architecture → gate 2 design track** (direction, design system, stills/mocks or clickable prototype). Then sprints.

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

The agent reconstructs **implementation state in depth** (cite file paths; a README restatement is not done). You still approve as-built truth, architecture, and design of what exists, then a further-work milestone plan. Process: [brownfield-adopt.md](.quinsy-studio/process/brownfield-adopt.md)

If a learning is identified mid-sprint, harvest is immediate and `./studio train` runs **beside** product work. Execute returns `STUDIO_LO` only when the product loop is idle.

Full loop: [GETTING_STARTED — execute loop](.quinsy-studio/GETTING_STARTED.md#the-execute-loop-how-work-actually-proceeds) · [learnings](.quinsy-studio/GETTING_STARTED.md#learnings-harvest-when-identified)

**Three human gates before implementation, then milestone planning:**

| Gate | You approve | Then |
|------|-------------|------|
| 0 | PRD + definitions **or** as-built truth (adopt) | `./studio blueprint` |
| 1 | Architecture + ADRs after PRD (as-is on adopt) | Design track starts — `./studio design` |
| 2 | Design direction + system + stills/mocks or clickable prototype (adopt: design of what exists) | Library promotion (greenfield only) → milestones |
| Milestones | Version roadmap (`docs/phases/`) | Tickets for **active milestone** → sprints |

You also approve **UI design specs** (`approve-design`) and **UI sprint review**. Sprint scope/groom are agent-owned (you may override). Mid-sprint, the agent loops tickets on its own. Open LOs train in parallel — they do not replace `IMPLEMENT`.

```bash
./studio approve my-project --gate 0
./studio blueprint my-project && ./studio approve my-project --gate 1
./studio design my-project --scope core-views && ./studio approve my-project --gate 2
./studio approve my-project --milestones    # after agent drafts docs/phases/
./studio sprint my-project --approve-scope  # agent-owned; you may override
./studio execute my-project                 # until HITL (UI sprint-review, design-approve, …)
```

### Execute actions

| ACTION | Meaning |
|--------|---------|
| `IMPLEMENT` | Adopt: fill `docs/as-built/`. Pre-impl: blueprint or design track. Sprint: next unblocked ticket (CARD lists skills + playbooks) |
| `VERIFY` → `GATE` → `DEBUG` → `MOVE_DONE` | Adopt: synthesize PRD. Sprint: receipt + fresh QA level 5, then mark done |
| `INFORM` | Reuse brief / inbox drain — loop. **`cost-cap`:** stop; raise the named key in `studio.settings.local.yaml` |
| `STUDIO_LO` | Idle infusion in `.quinsy-studio/` when there is no ready IMPLEMENT |
| `HITL` | **You:** gate 0, gate 1 architecture, gate 2 design track, `approve-design`, UI sprint review, tech-veto, abort |

Priority: adopt as-built (if needed) → HITL gates 0–2 → finish an in-progress ticket → next `IMPLEMENT` (train sidecar if LOs are open). Learnings are harvested automatically (`learn`, retro `--complete`, reuse, 3rd gate fail). Do not let them pile until the next sprint.

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
| 6. Build | *"Let the sprint run — execute until HITL"* (agent owns scope; you may override) |
| 7. Sprint done | *"Sprint review"* → UI: *"Approve review"* → reuse inform + retro **auto-harvest** → `./studio train` beside execute |
| 8. Mid-sprint thought | Agent queues `./studio note` and **keeps implementing** — it does not switch to your new message |
| 9. Strategic pivot | *"Run amendment intake for amendment_01"* → review `docs/amendments/AM-001/` → *"Approve amendment AM-001"* |
| Drift | *"Execute my-project — back on track"* |

More examples: [GETTING_STARTED — start here](.quinsy-studio/GETTING_STARTED.md#start-here-tell-the-agent) · [prompt cheat sheet](.quinsy-studio/GETTING_STARTED.md#talk-to-the-agent--prompt-cheat-sheet) · [execute loop](.quinsy-studio/GETTING_STARTED.md#the-execute-loop-how-work-actually-proceeds) · [learnings](.quinsy-studio/GETTING_STARTED.md#learnings-harvest-when-identified)

## Using in Cursor

Open this repo in Cursor. Always-on rules: [`.cursor/rules/quinsy-studio.mdc`](.cursor/rules/quinsy-studio.mdc). Each session: `./studio verify-worlds` → `./studio verify-abstraction` → `./studio settings` → `focus` (isolates siblings) → **`execute`** (loop until HITL). You approve gates; the agent runs `./studio`. See [Using Cursor](.quinsy-studio/README.md#4-using-quinsy-studio-in-cursor).

**Other hosts (same `./studio` loop, keys stay in that tool):** [Claude Code](CLAUDE.md) · [Gemini CLI](GEMINI.md). Codex already reads [`AGENTS.md`](AGENTS.md). Product Gemini keys in a project `.env` are not the coding-agent key.

## Cost & token policy

Committed defaults in [`.quinsy-studio/studio.settings.yaml`](.quinsy-studio/studio.settings.yaml) are sized for a **medium project** (PRD → architecture → design → one sprint) so you should not need to tune them to start. Intake, architecture, and design have higher per-step budgets than implement / reuse / retro.

```bash
./studio settings                 # merged policy + estimated usage
```

Override locally (gitignored, **no API keys**): copy [studio.settings.local.example.yaml](.quinsy-studio/studio-templates/studio.settings.local.example.yaml) → `.quinsy-studio/studio.settings.local.yaml`. Set `cost.profile` (`economy` / `standard` / `premium`) or raise a single step (`cost.steps.design.context`). Estimates are `chars/4` of CARD + listed files — not Cursor/Anthropic/Google billing. `model_hint` is the biggest dollar lever (the host must honor it).

When execute says `INFORM cost-cap`, it names the yaml key. Raise **that** key, then execute again. Do not keep stuffing files.

## Library-first (UI + code)

Before writing new code, pull from the studio library:

```bash
./studio library list
./studio library suggest my-project "auth button"
./studio library pull my-project auth tokens button
```

**Stubs** (`billing`, `feature-gating`) are **not pullable** — build in-project, then promote a working generic.

After a ticket is done, promote **only if the generic asset improved**:

```bash
./studio library promote my-project packages/billing --ticket MY-0001
```

Registry: [`.quinsy-studio/studio-library/library_registry.md`](.quinsy-studio/studio-library/library_registry.md)

**Team 10 aesthetic presets:** [`.quinsy-studio/knowledge-base/aesthetic-presets/README.md`](.quinsy-studio/knowledge-base/aesthetic-presets/README.md) — required in UI design specs (stripe-like, apple-like, soft-ui, …).

**Design discipline (placement before layout):** UI specs require **§2 Context & placement** before polish. See [contextual-ia-playbook](.quinsy-studio/knowledge-base/contextual-ia-playbook.md) · [design-spec-template](.quinsy-studio/knowledge-base/design-spec-template.md) · `./studio approve-design` (warns if missing).

**Studio skill extensions:** [`.quinsy-studio/knowledge-base/skill-extensions/README.md`](.quinsy-studio/knowledge-base/skill-extensions/README.md) — deep playbooks for compliance, PLG, delight UX, security audits (extend CL/GM/UX/PE skills, no new ticket IDs).

## Context & scope (agent)

```bash
./studio focus <project>                    # assign loop + isolate siblings
./studio isolate <project>                   # rewrite local .cursorignore only
./studio guard <project> "user request"     # in-scope / needs ticket / pre-impl / CROSS_PROJECT
./studio revise <project> --gate 1 --feedback "..."
```

`focus` / `execute` / `verify-worlds` hide other `projects/*` from Read/Grep via a **local** `.cursorignore` and generated Cursor rule (gitignored). That is an **assignment**, not a sandbox: Shell can still see sibling trees, and parallel chats in the same window can mix products. One chat (or CLI process) per product. Product git: `git -C projects/<name> …`. Studio HQ git (this repo): never `git add projects/`.

Docs: [agent-context](.quinsy-studio/process/agent-context.md) · [two worlds](.quinsy-studio/process/worlds.md)

## Repository layout

```
quinsy-studio/
├── AGENTS.md                 # IDE agent contract (read first)
├── package.json              # Studio UI deps (Tailwind + Headless UI)
├── .cursor/rules/            # Cursor always-on rules
├── .quinsy-studio/
│   ├── process/              # Lifecycle, gates, ticket workflow, worlds
│   ├── teams/                # 10 teams + skills (01–09 + Team 10 design)
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
| Immediate harvest + parallel train | [GETTING_STARTED § learnings](.quinsy-studio/GETTING_STARTED.md#learnings-harvest-when-identified) |
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
| Cost / token policy | [.quinsy-studio/studio.settings.yaml](.quinsy-studio/studio.settings.yaml) · `./studio settings` |
| Git separation | [process/worlds.md](.quinsy-studio/process/worlds.md) |
| Host ports / local URLs | [host-port-allocation.md](.quinsy-studio/knowledge-base/host-port-allocation.md) |

## Quality rules

1. **Library-first** — suggest + pull before coding; do not pull stubs; promote only when the generic asset improved
2. **No code without a ticket** (after gate 2)
3. **Three human gates** — PRD, architecture, design track. No product IMPLEMENT before gate 2. Existing apps: `./studio adopt` (never empty-init)
4. **Execute loop** — `./studio execute` until HITL; compact cards (skills + playbooks); receipt + gate 5 before `done`; train LOs in parallel (idle `STUDIO_LO` only)
5. **Sprint HITL** — UI review + per-ticket `approve-design`; scope/groom/reuse are inform (see [HITL](.quinsy-studio/process/human-in-the-loop.md))
6. **Milestones** — roadmap after gate 2; milestone review before next version backlog
7. **Amendments** — strategic direction after gate 2 → analysis → revised roadmap → tickets (see [amendment-intake](.quinsy-studio/process/amendment-intake.md))
8. **Placement before layout** — Team 10 §2 Context & placement in design specs; `ia-feature-placement` for cross-surface moves
9. **Immediate harvest** — classify + inbox + LO when a learning is identified; `./studio train` beside product execute
10. **Two git worlds** — never commit `projects/` to this repo; product commits from `projects/<name>/`; studio HQ stays project-agnostic (`./studio verify-abstraction`). LO-* in HQ are portable process/tooling only — product incidents stay in the project.
11. **Isolation** — `./studio focus` / `isolate`; guard `CROSS_PROJECT` for sibling names; do not treat focus as a jail
12. **Cost caps** — medium-project defaults in `studio.settings.yaml`; on `INFORM cost-cap` raise the named key (do not dump more files)
13. **Anti-slop + ADRs + HITL** — see process docs

## CLI overview

```bash
./studio --help
./studio install                  # after git clone
./studio focus <project> && ./studio execute <project>   # isolate + loop until HITL
./studio isolate <project>            # hide sibling projects/ from the agent
./studio settings                 # policy + estimated token usage
./studio note <project> "…"       # mid-execute inbox (ACK; drain after MOVE_DONE)
./studio train SO-001 --from mistake --topic "…"
./studio health <project>
./studio ticket-card <project> <ID>
./studio receipt <project> <ID>
./studio learn "..." --signal tooling-gap
./studio infusion                 # lists open LOs; does not block IMPLEMENT
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
**Date:** 2026-09-12
