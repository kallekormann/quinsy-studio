# Quinsy Studio

> Filesystem-based operating system for AI-driven software development.  
> After a sprint is groomed, the agent **executes until HITL** — it does not ask “should I continue?”

## What it is

Quinsy Studio separates **Studio HQ** (process, tools, library) from **projects** (client code, each with its own git repo). An IDE agent reads [`AGENTS.md`](AGENTS.md) and runs the `./studio` CLI. A direction becomes a product on [How Quinsy Studio works](.quinsy-studio/process/studio-overview.md): research, a PRD, the gates, the build, then you ship.

| Layer | Path | In studio git? |
|-------|------|----------------|
| **Studio HQ** | `.quinsy-studio/`, `studio`, `AGENTS.md` | Yes |
| **Ideation** | `ideation/` | No — local research desk |
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

The whole path, from a direction to production, is [How Quinsy Studio works](.quinsy-studio/process/studio-overview.md).

Pick one path. **`execute` is the driver** after a product exists — one next action until HITL. `./studio resume` is only a checklist.

Start-of-project HITL (you, not the agent): **gate 0 PRD/as-built → gate 1 architecture → gate 2a direction → gate 2b project kit**. `approve --gate 2` is refused. After the milestone roadmap, each cycle is a design phase, then an architecture phase, then an implementation phase. An empty phase is skipped.

### Ideation, then a PRD

Say what to look into. The desk researches and explains the case: the problem, the idea, the solution vision, and the full scope. You pick an idea only when several remain. You say yes, and that writes `intake/<slug>.md`. The first scope module is what bootstrap builds.

```text
Look into <direction>.
Approve I-001.
Promote I-001.
```

Detail: [studio-overview.md](.quinsy-studio/process/studio-overview.md) · [GETTING_STARTED § ideation](.quinsy-studio/GETTING_STARTED.md#ideation-desk)

### New product (PRD)

Add `intake/<project>.md` yourself, or use the file promote just wrote → *"Bootstrap &lt;project&gt; and walk me through gate 0"*.

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

If a learning is identified mid-sprint, harvest is immediate. Product execute **INFORM**s the open HQ LO count and keeps `IMPLEMENT`. Infuse with `./studio train` in a **separate HQ chat**. Execute returns `STUDIO_LO` only when the product loop is idle.

Full loop: [GETTING_STARTED — execute loop](.quinsy-studio/GETTING_STARTED.md#the-execute-loop-how-work-actually-proceeds) · [learnings](.quinsy-studio/GETTING_STARTED.md#learnings-harvest-when-identified)

**Human gates before implementation, then milestone planning:**

| Gate | You approve | Then |
|------|-------------|------|
| 0 | PRD + definitions **or** as-built truth (adopt) | `./studio blueprint` |
| 1 | Architecture + ADRs after PRD (as-is on adopt) | Direction interview — `./studio design --discovery` |
| 2a | Design direction (`design/DESIGN.md` after a passing critique) | `./studio design` |
| 2b | Project kit: CSS tokens, coded A/M/O, sticker all-states (adopt: token-map, no fake prototype) | Milestones |
| Milestones | Version roadmap (`docs/phases/`) | Tickets for **active milestone** → the phase train |

You also sign a **design phase** (`approve-design --phase`) and an **architecture phase** (`approve-arch --phase`), then a **cadence review** every N implementation phases (default 2). Implementation only scopes tickets whose design and architecture are `approved` or `n/a`. Ready tickets close via receipt skill QA + gate 5 — no ticket ACK. An empty phase is skipped. Hygiene stays outside the train.

Greenfield `bootstrap` / `init` / `design` put UI kit peers in the prototype `package.json`. Adopt merges them into the live app. Schema migrate is agent work when Compose is up — you get an INFORM, not a “please run migrate.” **Docker is required.** Env **names** live in `env.schema.json`. Desktop values live in gitignored `projects/<p>/.env` and are injected with `./studio env <p> up --approve`. Production values live in Coolify. Never Read `.env` values into chat.

`./studio approve --gate N` refuses unless gate N-1 is already approved (re-approve of the same gate is allowed). Every execute CARD reprints a short **CONSTITUTION** (worlds, secrets-as-names, packet HITL).

```bash
./studio approve my-project --gate 0
./studio blueprint my-project && ./studio approve my-project --gate 1
./studio design my-project --discovery && ./studio approve my-project --gate 2a
./studio design my-project --scope core-views && ./studio approve my-project --gate 2b
./studio approve my-project --milestones    # after agent drafts docs/phases/
./studio sprint my-project --approve-scope  # agent-owned; you may override
./studio execute my-project                 # until HITL (packet sign-off or cadence review)
```

### Execute actions

| ACTION | Meaning |
|--------|---------|
| `IMPLEMENT` | Adopt: fill `docs/as-built/`. Pre-impl: blueprint or design track. Design or architecture phase: write the open packet. Implementation phase: next **ready** ticket (CARD lists skills + playbooks) |
| `VERIFY` → `GATE` → `DEBUG` → `MOVE_DONE` | Receipt + QA 5, then `move … done` (product git commit). Cadence: `ship --to dev`. `main` is HITL |
| `INFORM` | Reuse brief / inbox drain / **open HQ LO count** — loop. **`cost-cap`:** stop; raise the named key |
| `STUDIO_LO` | Idle infusion in `.quinsy-studio/` only when there is no in-flight product ticket |
| `HITL` | **You:** gates 0 → 1 → 2a → 2b, batch `approve-design --phase` / `approve-arch --phase`, `./studio env … --approve`, cadence review. Not a morning brief. Not a feature-ticket ACK |

Priority: adopt as-built (if needed) → HITL gates 0 → 1 → 2a → 2b → the phase train (design, then architecture, then implementation; empty phases skip) → finish an in-progress ticket → next ready `IMPLEMENT`. One unsigned ticket does not freeze a ready sibling. Learnings are harvested automatically (`learn`, retro `--complete`, reuse, 3rd gate fail). Do not let them pile until the next sprint.

If Cursor asks you to **Allow** `./studio move … done`, that is the IDE Auto-review prompt — not studio HITL. See [GETTING_STARTED — Cursor Auto-run](.quinsy-studio/GETTING_STARTED.md#cursor-auto-run-vs-studio-hitl).

### Product git (every product has its own repo)

Work lives in `projects/<name>/` (separate `.git`). Studio HQ never `git add projects/`.

| When | What |
|------|------|
| Each `MOVE_DONE` | One **commit** on the product repo (ticket-sized; `git revert` that ticket) |
| Before cadence review | If `origin` exists: `./studio ship <p> --to dev` (never auto-push `main`) |
| Local Docker / Compose review | RUNBOOK URL; `dev` push is optional backup if a remote exists |
| Production / `main` | **HITL:** `./studio ship <p> --to main --approve` |

Full guide: [`.quinsy-studio/GETTING_STARTED.md`](.quinsy-studio/GETTING_STARTED.md) · Agent contract: [`AGENTS.md`](AGENTS.md)

## Talk to the agent (Cursor)

Open this repo in Cursor. You approve HITL stops; the agent runs `./studio execute` in between. Closing a ticket (`MOVE_DONE`) is agent work once the receipt and gate 5 are green.

| Step | You say |
|------|---------|
| 0. A direction, no product yet | *"Look into …"* → *"Approve I-001"* → *"Promote I-001"* |
| 1a. New product — PRD in `intake/my-project.md` | *"Bootstrap my-project and walk me through the next gate."* |
| 1b. Existing repo | *"Adopt my-project from this folder and reconstruct as-built."* |
| 2. Gate 0 ready | *"Approve gate 0"* (as-built truth on adopt, or PRD + definitions) |
| 3. Architecture ready | *"Approve gate 1"* |
| 4. Direction ready | *"Approve gate 2a"* |
| 5. Project kit ready | *"Approve gate 2b"* (or *"Design core-views first"*) |
| 6. Milestones | *"Draft milestone roadmap"* → *"Approve milestones"* |
| 7. Build | *"Let the sprint run — execute until HITL"* — design phase, then architecture phase, then implementation. An empty phase is skipped. |
| 8. Cadence | Every N implementation phases: *"Sprint review"* → *"Approve review"*. Off-cadence: retro without a UI review |
| 9. Mid-sprint thought | Agent queues `./studio note` and **keeps implementing** — it does not switch to your new message |
| 10. Strategic pivot | *"Run amendment intake for amendment_01"* → review `docs/amendments/AM-001/` → *"Approve amendment AM-001"* |
| Drift | *"Execute my-project — back on track"* |

More examples: [GETTING_STARTED — start here](.quinsy-studio/GETTING_STARTED.md#start-here-tell-the-agent) · [prompt cheat sheet](.quinsy-studio/GETTING_STARTED.md#talk-to-the-agent--prompt-cheat-sheet) · [execute loop](.quinsy-studio/GETTING_STARTED.md#the-execute-loop-how-work-actually-proceeds) · [learnings](.quinsy-studio/GETTING_STARTED.md#learnings-harvest-when-identified)

## Using in Cursor

Open this repo in Cursor. Always-on rules: [`.cursor/rules/quinsy-studio.mdc`](.cursor/rules/quinsy-studio.mdc). Each session: `./studio verify-worlds` → `./studio verify-abstraction` → `./studio settings` → `focus` (isolates siblings) → **`execute`** (loop until HITL). You approve gates; the agent runs `./studio`. See [Using Cursor](.quinsy-studio/README.md#4-using-quinsy-studio-in-cursor).

**Other hosts (same `./studio` loop, keys stay in that tool):** [Claude Code](CLAUDE.md) · [Gemini CLI](GEMINI.md). Codex already reads [`AGENTS.md`](AGENTS.md). Product LLM **names** live in `env.schema.json`. Desktop values live in gitignored `projects/<p>/.env`; production values live in Coolify. They are not the coding-agent key and must not be pasted into chat.

## Cost & token policy (studio load, not Cursor billing)

Studio does **not** meter Cursor spend. It estimates how much CARD + files `./studio execute` loaded (`characters ÷ 4`) and stops stuffing files at a cap.

| Ledger | Who it is for | You look at |
|--------|----------------|-------------|
| **HQ** | Train / infusion / `STUDIO_LO` | `./studio settings` |
| **Each product** | That product’s execute loop | `./studio settings <project>` |

Committed baseline is **M**: session **400k**, implement context **28k**. Size **S / L / XL** and how to estimate a turn: [GETTING_STARTED — Studio settings](.quinsy-studio/GETTING_STARTED.md#studio-settings-cost--tokens). Existing trees: `./studio settings <project> --init`.

```bash
./studio settings                 # HQ
./studio settings my-project   # product
```

Override in gitignored **local** yaml (HQ or `docs/studio.settings.local.yaml`). `cost.profile`: `economy` / `standard` / `premium` multiplies that file. `INFORM cost-cap` prints `ledger=project` or `ledger=hq` — raise the **named** key there. No API keys. `model_hint` is the host-model lever.

Session must be **≥** the step budgets you will burn in one focus, or session fires first.

## Library-first (UI + code)

Before writing new code, pull from the studio library:

```bash
./studio library list
./studio library suggest my-project "auth button"
./studio library pull my-project auth tokens button
```

Product apps that use the kit **must** have `radix-ui`, `class-variance-authority`, `clsx`, `tailwind-merge`, and `lucide-react` (plus `@headlessui/react`). These are baked into `./studio init` / `design` / `adopt` (`docs/setup/ui-kit.md`). Do not wait for a missing-module crash.

**Stubs** (`billing`, `feature-gating`) are **not pullable** — build in-project, then promote a working generic.

After a ticket is done, promote **only if the generic asset improved**:

```bash
./studio library promote my-project packages/billing --ticket MY-0001
```

Registry: [`.quinsy-studio/studio-library/library_registry.md`](.quinsy-studio/studio-library/library_registry.md)

**Team 10 aesthetic presets:** [`.quinsy-studio/knowledge-base/aesthetic-presets/README.md`](.quinsy-studio/knowledge-base/aesthetic-presets/README.md) — required in UI design specs (stripe-like, apple-like, soft-ui, …).

**Design discipline (placement before layout):** The agent **writes** `docs/design-specs/<TICKET>.md` and in-context HTML mocks that use **project CSS tokens** and show **all states**. Every UI spec includes **§2d Motion**. The kit already animates with `--motion-*` tokens. The only off switch is HITL `motion: off`. Do not ask a human to approve a spec that is not on disk. See [design-spec-template](.quinsy-studio/knowledge-base/design-spec-template.md) and [motion-transitions](.quinsy-studio/knowledge-base/skill-extensions/motion-transitions.md).

**Studio skill extensions:** [`.quinsy-studio/knowledge-base/skill-extensions/README.md`](.quinsy-studio/knowledge-base/skill-extensions/README.md) — deep playbooks for compliance, PLG, delight UX, security audits (extend CL/GM/UX/PE skills, no new ticket IDs).

## Context & scope (agent)

```bash
./studio focus <project>                    # assign loop + isolate siblings
./studio isolate <project>                   # rewrite local .cursorignore only
./studio guard <project> "user request"     # in-scope / needs ticket / pre-impl / CROSS_PROJECT
./studio revise <project> --gate 1 --feedback "..."
```

`focus` / `execute` / `verify-worlds` hide other `projects/*` from Read/Grep via a **local** `.cursorignore` (including a **QUINSY-SECRETS** block) and generated Cursor rule. That is an **assignment**, not a sandbox. **One chat per product.** `parallel.max_projects` (default 5) leases executes; a sixth is queued and does not rewrite isolation. `./studio focus` will not clobber another live lease unless `--force`. Product git: `git -C projects/<name> …`. Studio HQ git: never `git add projects/` (HQ pre-commit refuses `projects/`).

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
│   │   └── learnings/            # domain/topic catalog + inbox.md (open queue) + archive/
│   └── backlog/              # LO-* studio improvements only
├── ideation/                 # Research desk (gitignored): problems, ideas, shortlist
├── intake/                   # Raw PRDs + amendment briefs (gitignored)
├── projects/                 # Client projects (gitignored, own .git each)
└── studio                    # CLI entrypoint
```

## Documentation

| Topic | Document |
|-------|----------|
| The path: direction → PRD → gates → production | [process/studio-overview.md](.quinsy-studio/process/studio-overview.md) |
| Ideation desk | [GETTING_STARTED § ideation](.quinsy-studio/GETTING_STARTED.md#ideation-desk) · [ideation-desk.md](.quinsy-studio/teams/09-studio-operations-evolution/skills/ideation-desk.md) |
| Execute loop (agentic sprint) | [GETTING_STARTED § execute loop](.quinsy-studio/GETTING_STARTED.md#the-execute-loop-how-work-actually-proceeds) |
| HQ isolation (Docker, secrets, leases) | [process/hq-isolation-sprints.md](.quinsy-studio/process/hq-isolation-sprints.md) |
| Immediate harvest + HQ train session | [GETTING_STARTED § learnings](.quinsy-studio/GETTING_STARTED.md#learnings-harvest-when-identified) |
| Operations manual | [.quinsy-studio/README.md](.quinsy-studio/README.md) |
| Getting started | [.quinsy-studio/GETTING_STARTED.md](.quinsy-studio/GETTING_STARTED.md) |
| Agent prompts (new product or existing repo) | [GETTING_STARTED § start here](.quinsy-studio/GETTING_STARTED.md#start-here-tell-the-agent) |
| Prompt cheat sheet | [GETTING_STARTED § talk to the agent](.quinsy-studio/GETTING_STARTED.md#talk-to-the-agent--prompt-cheat-sheet) |
| Using in Cursor | [.quinsy-studio/README.md §4](.quinsy-studio/README.md#4-using-quinsy-studio-in-cursor) |
| External skills | [.quinsy-studio/README.md §8](.quinsy-studio/README.md#8-managing-skills) |
| Motion (default on) | [GETTING_STARTED § motion](.quinsy-studio/GETTING_STARTED.md#motion-default-on) · [motion-transitions](.quinsy-studio/knowledge-base/skill-extensions/motion-transitions.md) |
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
4. **Execute loop** — `./studio execute` until HITL; compact cards (skills + playbooks); receipt + gate 5 before `done`; INFORM open HQ LO counts; train in a separate HQ session (idle `STUDIO_LO` only)
5. **Sprint HITL** — no feature-ticket ACK; `PRODUCTION` then `approve-design` / `approve-arch`; cadence review every N implementation sprints. Hygiene: `./studio sprint --kind hygiene` (see [HITL](.quinsy-studio/process/human-in-the-loop.md))
6. **Milestones** — roadmap after gate 2; milestone review before next version backlog
7. **Amendments** — strategic direction after gate 2 → analysis → revised roadmap → tickets (see [amendment-intake](.quinsy-studio/process/amendment-intake.md))
8. **Placement before layout** — Team 10 writes the spec file (§2 + §2c + §2d Motion); mocks use project tokens, sit in the real view, and cover all states; `ia-feature-placement` for cross-surface moves. Motion is on unless the spec says `motion: off`.
9. **Immediate harvest** — classify + inbox + LO when a learning is identified; product chat **INFORM**s; `./studio train` in a HQ session
10. **Two git worlds** — never commit `projects/` to this repo; product commits from `projects/<name>/` on each `MOVE_DONE`. Cadence review may push **`origin/dev`**. `main` / production is HITL `./studio ship --to main --approve`. Studio HQ stays project-agnostic (`./studio verify-abstraction`).
11. **Isolation** — one chat per product; `./studio focus` / `isolate`; guard `CROSS_PROJECT`; focus does not clobber a live execute lease unless `--force`. Not a kernel jail.
12. **Cost caps** — medium-project defaults in `studio.settings.yaml`; `parallel.max_projects` (default 5); on `INFORM cost-cap` raise the named key (do not dump more files)
13. **Docker + secrets** — Docker required for gate/migrate/boot; env **names** only; values via `./studio env … --approve`
14. **Anti-slop + ADRs + HITL packets** — see process docs; no morning-brief dashboard

## CLI overview

```bash
./studio --help
./studio install                  # after git clone
./studio focus <project> [--force] && ./studio execute <project>   # isolate + loop until HITL
./studio execute <project> --release  # free an execute lease
./studio env <project> up --approve   # inject named vars into Compose
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
./studio approve-design <p> <TICKET>
./studio approve-arch <p> <TICKET>
./studio train --purge-empty
./studio ship <p> --to dev
./studio ship <p> --to main --approve
./studio review <project>
./studio feedback <project> "..."
./studio board <project>
```

## Changelog

See [CHANGELOG.md](CHANGELOG.md) · studio process: [`.quinsy-studio/CHANGELOG.md`](.quinsy-studio/CHANGELOG.md)

---

**Version:** 1.16.0  
**Date:** 2026-09-22
