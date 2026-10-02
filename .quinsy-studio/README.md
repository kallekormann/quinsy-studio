# Quinsy Studio — Operations Manual

> The Studio HQ: a highly autonomous, self-learning software development and
> growth agency at Director level. This document describes how to **operate** the
> studio, how to **extend skills**, how to **optimize the process**, and how the
> **Dual-Loop** ensures the studio learns from projects.

---

## Table of Contents

1. [What is Quinsy Studio?](#1-what-is-quinsy-studio)
2. [Folder Structure](#2-folder-structure)
3. [Quick Start: Launch a Project (5 Minutes)](#3-quick-start-launch-a-project)
4. [Using Quinsy Studio in Cursor](#4-using-quinsy-studio-in-cursor)
5. [Where Is What? (Templates, PRDs, Tickets)](#5-where-is-what)
6. [The Studio Process (Dual-Speed)](#6-the-studio-process-dual-speed)
7. [All CLI Commands](#7-all-cli-commands)
8. [Managing Skills (Internal + External)](#8-managing-skills)
9. [Optimizing the Process (Learning Loop)](#9-optimizing-the-process)
10. [The Dual-Loop: Studio Learns from Projects](#10-the-dual-loop)
11. [Studio Library: Reusable Assets](#11-studio-library)
12. [Quality Assurance & Gates](#12-quality-assurance)
13. [Troubleshooting](#13-troubleshooting)

---

## 1. What is Quinsy Studio?

Quinsy Studio is a **file-system-based operating system for software projects**.
It consists of:

- **Process Documents** (`process/`) — Lifecycle, Gates, Anti-Slop, Ticket Workflow
- **Teams & Skills** (`teams/`) — 11 teams (01–09 + Team 10 product design + Team 11 growth design), internal skills + skill registry
- **Knowledge Base** (`knowledge-base/`) — Playbooks (Design, Frontend, Backend, Compliance, AI)
- **Studio Tools** (`studio-tools/`) — Python CLI with all commands
- **Studio Templates** (`studio-templates/`) — PRD, Ticket, ADR, Docker base
- **Studio Library** (`studio-library/`) — Reusable assets (UI, Packages, Tokens)
- **External Skills** (`external-skills/`) — Imported best-in-class skill packages

A direction becomes a product on the path in [studio-overview.md](process/studio-overview.md): ideation, a PRD, the gates, the phase train, then you ship `main`.

The studio operates in **Dual-Speed mode**:
- **IDEATE** — no product yet. `./studio ideate` researches, explains the case, and writes `intake/<slug>.md` when you say yes
- **CORE** — new platforms from that PRD, or from a PRD you wrote. HITL: **gate 0 PRD → gate 1 architecture → gate 2a direction → gate 2b project kit**, then milestones and the phase train
- **ADOPT** — existing codebase (`./studio adopt`); as-built reconstruction, then the same gates
- **LEAN** — iterations & features on a studio-managed project (4 phases)

---

## 2. Folder Structure

```
quinsy-studio/
├── .quinsy-studio/                 ← THE STUDIO (everything here)
│   ├── process/                    # Process documents (Lifecycle, Gates, Anti-Slop)
│   ├── teams/                      # 10 teams × skills + skill-registry.md
│   │   ├── 01-frontend-experience/
│   │   ├── 02-backend-systems/
│   │   ├── 03-compliance-legal/
│   │   ├── 04-product-strategy-architecture/
│   │   ├── 05-growth-marketing-content/
│   │   ├── 06-product-management-operating-model/
│   │   ├── 07-ai-autonomous-systems/
│   │   ├── 08-platform-enterprise-engineering/
│   │   ├── 09-studio-operations-evolution/
│   │   ├── 10-product-design-experience/
│   │   └── 11-growth-design/
│   ├── knowledge-base/             # Playbooks + learnings/inbox.md (immediate harvest)
│   ├── studio-tools/               # Python CLI (studio.py + all tools)
│   ├── studio-templates/           # PRD, Ticket, ADR, Docker base, Learning logs
│   ├── studio-library/             # Reusable assets (ui/, packages/, tokens)
│   ├── external-skills/            # Imported skill packages (hallmark, marketing, ...)
│   ├── backlog/                    # LO tickets (gitignored; local only)
│   ├── retros/                     # Meta-retros (gitignored; local only)
│   └── skill-dependencies.json     # Subscribed external skill sources
├── projects/                       # ALL client projects (each with own backlog, Docker)
│   └── <project>/                  # status.json, docs/, backlog/, sprints/, docker/, design/
├── ideation/                       # Research desk (gitignored): problems, ideas, shortlist
├── intake/                         # PRDs from promote, or a PRD you wrote (gitignored)
├── studio                          # CLI wrapper (delegates to .quinsy-studio/studio-tools/)
├── README.md                       # Project README (this file is .quinsy-studio/README.md)
└── CHANGELOG.md
```

**Important separation:**
- **Studio World** (`.quinsy-studio/`) — Process, skills, templates, library, and the learnings catalog. **This git repo.** Backlog tickets, retros, and sprint notes stay local.
- **Project World** (`projects/<name>/`) — Tickets, code, design, docker. **Each project has its own `.git`.**
- **`ideation/`**, **`intake/`**, **`projects/`**, and the local working notes **`backlog/`**, **`retros/`**, **`sprints/`** are gitignored. The shared result is the process, the skills, the learnings catalog, and the library. See [process/worlds.md](process/worlds.md).

**IDE agents:** read [`AGENTS.md`](../AGENTS.md) + [process/agent-context.md](process/agent-context.md). Session driver: `./studio execute <project>` until HITL.

---

## 3. Quick Start: Launch a Project

See also: [GETTING_STARTED.md](GETTING_STARTED.md) (canonical) · [`AGENTS.md`](../AGENTS.md) (agent contract).

### AI-driven (recommended)

Pick one path. [GETTING_STARTED.md](GETTING_STARTED.md) is canonical.

**New product** (PRD in `intake/`):

```bash
./studio install                   # once after git clone
./studio verify-worlds
./studio verify-abstraction
./studio bootstrap my-project
./studio focus my-project
./studio execute my-project            # do NEXT; loop until ACTION is HITL
```

**Existing codebase** (implemented — do not empty-init):

```bash
./studio adopt my-project --from /path/to/repo   # or a git URL
./studio focus my-project
./studio execute my-project            # fill docs/as-built/ → PRD → HITL gate 0
```

Optional intent: copy [adopt_intent.md](studio-templates/adopt_intent.md) → `intake/<slug>.md` and pass `--intent`. Process: [brownfield-adopt.md](process/brownfield-adopt.md).

`./studio resume my-project` prints a checklist. **`execute` is the driver** — see [The execute loop](#the-execute-loop). Start-of-project HITL: **gate 0 PRD → gate 1 architecture → gate 2a direction → gate 2b project kit** (`approve --gate N` needs N-1; bare `--gate 2` is refused). After the roadmap, each cycle is design, then architecture, then implementation. An empty phase is skipped. Product execute **INFORM**s open HQ LO counts; infuse with `./studio train` in a **HQ session**. `STUDIO_LO` only when idle. **Docker is required.** Desktop values live in gitignored `projects/<p>/.env`; `./studio env <p> up --approve` injects that file. Production values live in Coolify.

Greenfield scaffold includes UI kit peers (`radix-ui`, `class-variance-authority`, `clsx`, `tailwind-merge`, `lucide-react`). See `docs/setup/ui-kit.md`. Pending schema is agent-applied when the DB is reachable.

### Step 1: Place a PRD **or** point at an existing repo

New product:

```bash
cp studio-templates/prd_template.md ../intake/my-project.md
# edit PRD, then bootstrap (step 2)
```

Existing codebase: skip the PRD. Use `./studio adopt` (step 2). Optional intent: `intake/<slug>.md` from [adopt_intent.md](studio-templates/adopt_intent.md).

### Step 2: Bootstrap (new) or adopt (existing)

```bash
./studio bootstrap my-project
# OR existing codebase (never empty-init):
./studio adopt my-project --from /path/to/repo
# OR manual greenfield:
./studio init my-project --archetype saas-application
./studio intake my-project intake/my-project.md
./studio start my-project --mode core
```

Intake does **not** create implementation tickets. After gate 2b, the agent drafts a **milestone roadmap** (`docs/phases/`); you approve it before M0 tickets and the phase train.

### Step 3: Human gate 0 — PRD + definitions (or as-built)

New product: agent fills `projects/my-project/docs/definitions/`.  
Adopted repo: agent fills `docs/as-built/`, synthesizes `docs/intake/prd.md`, then you confirm “this is what we have.”

```bash
./studio approve my-project --gate 0
```

### Step 4: Human gate 1 — Architecture

```bash
./studio blueprint my-project
# fill docs/architecture/, docs/adr/
./studio approve my-project --gate 1
```

### Step 5: Human gate 2a — Direction, then gate 2b — Project kit

```bash
./studio design my-project --discovery
# Answer docs/design/discovery.md. The agent must not invent the brand.
./studio approve my-project --gate 2a            # only after the critique passes
./studio design my-project --scope core-views   # or: journey | as-built
# Greenfield: Next.js prototype in design/prototype/, sticker sheet, ui/tokens
# Adopt: surface map of existing UI — do not scaffold a parallel prototype
./studio approve my-project --gate 2b            # copies the prototype into the product app
```

`./studio approve --gate 2` is refused. Gate 2b does not merge the product look into studio-library.

### Step 6: Milestone roadmap

```bash
# Agent drafts docs/phases/README.md + M0/M1 outlines
./studio approve my-project --milestones         # human approves roadmap
# Agent writes M0 tickets → product backlog (milestone: M0)
```

### Step 7: Library-first implementation

```bash
./studio library suggest my-project "auth button"
./studio library pull my-project auth tokens button   # not stubs (billing, feature-gating)
# kit peers must already be in the app package.json (docs/setup/ui-kit.md)
./studio sprint my-project                            # next phase; an empty phase is skipped
./studio sprint my-project --approve-scope            # agent-owned; you may override
./studio groom my-project --approve
./studio execute my-project                 # until HITL; INFORM open HQ LOs
# on done: promote only if the generic asset improved
```

### Step 8: QA & learning

```bash
./studio gate my-project --level 5
./studio retro my-project --complete    # auto-harvests LOs from badly / improve
./studio train SO-001 --from mistake --topic "…" --lo LO-NNNN   # HQ session, not this product chat
./studio infusion                       # lists open LOs; does not block IMPLEMENT
```

### Amendment intake (strategic direction, post gate 2b)

When product direction shifts before the next milestone — not for sprint-review nits.

```bash
cp .quinsy-studio/studio-templates/amendment_01.example.md intake/amendments/<project>/amendment_01.md
# Fill vision; check teams/skills — do not write milestones
./studio amend <project> intake/amendments/<project>/amendment_01.md
./studio amendments <project>
# Agent fills docs/amendments/AM-001-*/ (UX surface map, FE/BE arch, milestone roadmap, ticket drafts)
./studio approve <project> --amendment AM-001
./studio approve <project> --milestones   # if roadmap changed
```

See [process/amendment-intake.md](process/amendment-intake.md) · Example: [studio-templates/amendment_01.example.md](studio-templates/amendment_01.example.md)

---

## 4. Using Quinsy Studio in Cursor

Quinsy Studio is designed to run **inside Cursor** with the agent driving `./studio` CLI commands.

### Setup (once)

1. Clone/open this repo in Cursor (`kallekormann/quinsy-studio`).
2. **Always-on rules** load from [`.cursor/rules/quinsy-studio.mdc`](../.cursor/rules/quinsy-studio.mdc).
3. The agent reads [`AGENTS.md`](../AGENTS.md) + [process/agent-context.md](process/agent-context.md) at session start.

No separate plugin — the repo *is* the integration.

### Session ritual

```bash
./studio install                 # once after git clone
./studio verify-worlds
./studio verify-abstraction
./studio settings                # HQ train ledger
./studio settings <project>     # product execute ledger
./studio focus <project>
./studio execute <project>          # loop: do NEXT until ACTION is HITL
./studio ship <project> --to dev   # before cadence review (never auto main)
```

`resume` prints a **checklist**. **`execute` is the driver** — one action at a time. Do not ask “should I continue?” mid-sprint. Stop only on `HITL`. Harvest LOs immediately; INFORM the count; `./studio train` in a **HQ chat**. `STUDIO_LO` only when the product loop is idle.

If Cursor prompts **Allow** on `./studio move … done`, that is IDE Auto-review, not studio HITL. See [GETTING_STARTED — Cursor Auto-run](GETTING_STARTED.md#cursor-auto-run-vs-studio-hitl).

### The execute loop

Execute drives **gate 0 → gate 1 → gate 2a → gate 2b**, then the phase train. After phase scope + groom (agent-owned):

```
focus → execute → do NEXT → execute again → … until HITL
```

| ACTION | Meaning |
|--------|---------|
| `IMPLEMENT` | Adopt as-built, blueprint, design track, a phase packet, or the next **ready** implementation ticket. Load the **CARD** (`./studio ticket-card`); open that one `.md` only |
| `VERIFY` | Fill `./studio receipt` (plan, AC coverage, default user flow, skill QA headings) |
| `GATE` | `./studio gate --level 5` (fresh after this ticket’s implement) |
| `DEBUG` | Gate red → `sprints/SPRINT-NN/debug/<id>.md`, retry up to 3 times |
| `MOVE_DONE` | Receipt + gate 5 → `move … done` **and a product git commit**. Then execute again (**agent**, not HITL) |
| `INFORM` | Reuse / inbox drain / **N open HQ LOs** — loop; **not** architecture or design. **`cost-cap`:** stop; raise the named key (`ledger=` HQ vs product) |
| `STUDIO_LO` | Idle infusion in `.quinsy-studio/` only when there is no in-flight product ticket — classified path on the CARD |
| `HITL` | **You:** gates 0 → 1 → 2a → 2b, batch `approve-design --phase` / `approve-arch --phase`, `./studio env … --approve`, cadence review. Not a morning brief |

**Priority:** HITL gates 0 → 1 → 2a → 2b → design phase, then architecture phase, then implementation (an empty phase is skipped) → finish in-progress ticket → next ready `IMPLEMENT` (INFORM open LOs). One unsigned ticket does not freeze a ready sibling. `STUDIO_LO` only when idle. Learnings are harvested when identified (see [§9](#9-optimizing-the-process) and [GETTING_STARTED — learnings](GETTING_STARTED.md#learnings-harvest-when-identified)).

```bash
./studio execute <project> [--json]
./studio ticket-card <project> <ID>
./studio receipt <project> <ID>
./studio health <project>
```

Tickets stay **Markdown**. Compact cards save tokens; there is no SQL ticket database. `move … done` requires a receipt **and** QA level 5, then **commits** `projects/<p>/`. Before cadence HITL, `./studio ship <p> --to dev`. Never auto-push `main` (`--approve` HITL).

### What you say in chat

See [GETTING_STARTED.md — prompt cheat sheet](GETTING_STARTED.md#talk-to-the-agent--prompt-cheat-sheet) for the full list. Essentials:

| You want | Example prompt |
|----------|----------------|
| **Start from PRD** | *"I added intake/my-project.md — bootstrap my-project and stop at gate 0 for my review"* |
| **Start from existing repo** | *"Adopt my-project from this folder and reconstruct as-built"* |
| **Continue** | *"Focus &lt;project&gt; and execute — loop until HITL"* |
| **Approve gate** | *"Gate 0 looks good — approve"* → `./studio approve <project> --gate 0` |
| **Send back for revision** | *"Revise gate 1: no Supabase yet, IndexedDB only"* |
| **Design** | *"Design &lt;project&gt; with scope core-views"* |
| **Milestones** | *"Draft milestone roadmap"* → *"Approve milestones"* |
| **Amendment** | *"Run amendment intake for amendment_01"* → review `docs/amendments/AM-001/` → *"Approve amendment AM-001"* |
| **Sprint + build** | *"Let the sprint run — execute until HITL"* (agent owns scope; you may override) |
| **Cadence review** | Every N implementation sprints: *"Sprint review"* → try UI → *"Approve review"*. Off-cadence: retro |
| **Sprint close** | reuse inform (auto-harvest) → retro `--complete` (auto-harvest) → `./studio train` in a HQ session → next `./studio sprint` |
| **Mid-sprint thought** | *"Note: also consider denser type"* → `./studio note` (ACK; continue current ticket) |
| **New idea (sprint)** | *"Feedback: I want offline mode"* — **not** "create a ticket for offline" |
| **Drift recovery** | *"Back on track"* / *"Execute &lt;project&gt;"* |
| **Status** | *"What's the status of &lt;project&gt;?"* / *"Studio health"* |
| **Off-sprint scope** | *"Is adding payments in scope?"* → agent runs `./studio guard` |
| **Studio improvement** | *"Log a tooling gap: …"* → `./studio learn` then `./studio train` (also auto on retro / reuse / 3rd gate fail) |

### First session walkthrough

```
You:  I added intake/my-app.md. Bootstrap my-app and walk me through gate 0.
  — or —  Adopt my-app from this folder and reconstruct as-built.
Agent: verify-worlds → bootstrap or adopt → focus → execute
       (new: docs/definitions/; adopt: docs/as-built/ then PRD) → HITL gate 0
You:  Gate 0 looks good — approve.
Agent: ./studio approve my-app --gate 0 → blueprint phase
You:  Continue with architecture.
Agent: blueprint + ADRs (as-is on adopt) → waits for gate 1
You:  Approve gate 1. Design core views only.   — or —  Map the existing UI.
Agent: design --scope core-views  (adopt: surface map, no fake prototype)
You:  Approve gate 2a, then approve gate 2b.
Agent: milestone roadmap in docs/phases/ → you approve milestones → M0 tickets → agent-owned phase scope → execute until HITL (design phase, then architecture phase, then implementation; cadence review every N implementation phases)
```

### Two git worlds in Cursor

| World | Path | Commit from |
|-------|------|-------------|
| Studio HQ | `.quinsy-studio/`, `AGENTS.md` | Studio repo root |
| Project | `projects/<name>/` | **Inside** `projects/<name>/` (separate `.git`) |

`projects/` and `intake/` are gitignored in the studio repo. Run `./studio verify-worlds` if unsure.

**Several products in one IDE:** `./studio focus` / `execute <project>` assign the loop and rewrite a local `.cursorignore` (including **QUINSY-SECRETS**) plus generated isolation rule so Read/Grep should not see sibling `projects/` trees. They do **not** sandbox Shell. **One chat per product.** `parallel.max_projects` (default 5) leases executes; a sixth is queued. `./studio focus` will not clobber another live lease unless `--force`. Guard returns `CROSS_PROJECT` if the request names a sibling. Product commits: `git -C projects/<name>`. Studio HQ commits: this repo only — HQ pre-commit refuses `projects/`. Env **names** in `env.schema.json`; inject with `./studio env <p> up|migrate|dev --approve`. Plan: [process/hq-isolation-sprints.md](process/hq-isolation-sprints.md).

### Agent vs. you

| You (human) | Agent |
|-------------|-------|
| Approve gates **0–2** (sequential), `approve-design` / `approve-arch`, **`env … --approve`**, cadence review, tech-veto, **`ship --to main --approve`** | Fill artifacts; **execute loop** on ready tickets. INFORM open HQ LOs. `MOVE_DONE` commits product git; `ship --to dev` before git-host review |
| Mid-sprint notes (`./studio note`) | ACK and continue; drain after `MOVE_DONE` |
| Review PRs / mocks / shipped UI | Library pull before coding (not stubs); compact cards; receipts + gate 5 before `done` |
| Final product decisions | `./studio train` in a **HQ session** when LOs are open (product chat stays IMPLEMENT) |

See [GETTING_STARTED.md](GETTING_STARTED.md) for the full gate + library workflow.

---

## 5. Where Is What?

| What | Where? |
|------|--------|
| **PRD Template** | `.quinsy-studio/studio-templates/prd_template.md` |
| **PRD (edited)** | `projects/<name>/docs/intake/prd.md` |
| **Raw Idea/Input** | `intake/<name>.md` |
| **Amendment brief (local)** | `intake/amendments/<p>/amendment_NN.md` |
| **Amendment example (studio)** | `.quinsy-studio/studio-templates/amendment_01.example.md` |
| **Amendment analysis** | `projects/<name>/docs/amendments/AM-NNN-*/` |
| **IA surface map (project)** | `projects/<name>/docs/ia/surface-map.md` |
| **Milestone roadmap** | `projects/<name>/docs/phases/` |
| **Tickets** | `projects/<name>/backlog/*.md` (+ `implement/`, `done/`, `blocked/`) |
| **Execution log / receipts / debug** | `projects/<name>/sprints/SPRINT-NN/execution-log.json`, `receipts/`, `debug/` |
| **ADRs** | `projects/<name>/docs/adr/` |
| **Decision Records** | `projects/<name>/docs/decisions/` |
| **Sprints** | `projects/<name>/sprints/SPRINT-NN/` |
| **Design blueprint** | `projects/<name>/design/DESIGN.md` |
| **Architecture** | `projects/<name>/docs/architecture/` |
| **Design prototype** | `projects/<name>/design/prototype/` |
| **Library usage log** | `projects/<name>/docs/library-usage.json` |
| **Library promotion log** | `projects/<name>/docs/library-promotions.json` |
| **Library registry** | `studio-library/library_registry.md` |
| **Docker (project-specific)** | `projects/<name>/docker/` |
| **Docker Base Template** | `.quinsy-studio/studio-templates/docker/` |
| **Status (Phase/Gate)** | `projects/<name>/status.json` |
| **Studio Learning Items** | `.quinsy-studio/backlog/open/LO-*.md` (portable HQ only; project incidents stay in the project) |
| **Retros** | `.quinsy-studio/retros/` |
| **Studio Library** | `.quinsy-studio/studio-library/` |

---

## 6. The Studio Process (Dual-Speed)

### Before a PRD exists

[studio-overview.md](process/studio-overview.md) is the map. You name a direction. `./studio ideate` researches and explains the case. You pick an idea only when several remain, then say yes or no to the PRD. Yes writes `intake/<slug>.md`. Bootstrap reads that file. The desk does not run `./studio execute`.

### CORE / ADOPT (human gates 0, 1, 2a, 2b, then milestones)

Same gate sequence. **CORE** starts from a PRD. **ADOPT** (`./studio adopt`) reconstructs as-built first, then synthesizes a PRD. Do not empty-init a live tree. **No product IMPLEMENT until gates 0, 1, 2a, and 2b are approved.**

| Phase | Action | Artifact | Gate |
|-------|--------|----------|------|
| **1. Intake** | PRD + definitions, **or** as-built reconstruction (adopt) | `docs/intake/`, `docs/definitions/`, `docs/as-built/` | **HUMAN 0** |
| **2. Architecture** | Blueprint, ADRs (as-is on adopt) | `docs/architecture/`, `docs/adr/` | **HUMAN 1** |
| **3a. Direction** | Discovery interview, `design/DESIGN.md`, critique | `docs/design/discovery.md`, `design/DESIGN.md` | **HUMAN 2a** |
| **3b. Project kit** | CSS tokens, coded A/M/O, sticker all-states (adopt: token-map of what exists) | `design/`, `ui/tokens/` | **HUMAN 2b** |
| **3c. Milestones** | Version roadmap, M0/M1 outlines | `docs/phases/` | **HUMAN** (`--milestones`) |
| **3d. Amendments** | Strategic direction → revised roadmap + tickets | `docs/amendments/AM-NNN/` | **HUMAN** (`--amendment`) |
| **4. Phase planning** | Next phase: design, then architecture, then implementation. An empty phase is skipped. | `sprints/SPRINT-NN/` | Agent-owned (you may override) |
| **5. The phase** | Execute until HITL | Packets, or code + receipts + gate 5 | Batch `approve-design --phase` / `approve-arch --phase`; cadence review every N implementation phases |
| **6. QA** | Anti-slop, tests | QA report | Gate 5 (QA level) |
| **7. Learning** | Harvest when identified (not a later batch) | Inbox + LO-* → HQ `./studio train` | INFORM count / idle `STUDIO_LO` |

### LEAN Mode (Features, Iterations)

| Phase | Action |
|-------|--------|
| **1. Ticket Drop** | Ticket directly in backlog |
| **2. Quick Align** | Short solution path → **HUMAN-GATE 1** (Go/No-Go) |
| **3. Execute & QA** | Immediate implementation + tests |
| **4. Fast Sync** | Commit + global asset alignment |

### UI design discipline (Team 10, post gate 2b)

As products grow, **where** a capability lives matters more than dialog width. Studio order:

1. **Context & placement** — `knowledge-base/contextual-ia-playbook.md` (UX-003)
2. **Workflow map** — `workflow-definition-playbook.md` (multi-surface features)
3. **Design spec** — write `docs/design-specs/<TICKET>.md` from `design-spec-template.md` (**§2 + §2c**). Mocks in `docs/design-specs/mocks/<TICKET>/` must use **project CSS tokens**, sit in the **real product view**, and show **all states**. Do not ask for `approve-design` until those files exist.
4. **Implement** — library-first + `design-system-compliance-checklist.md`, only in an implementation phase after `./studio approve-design <p> --phase`

Ticket types: `ia-feature-placement` (move/split surfaces), `ui-composition` (layout on the **right** surface). Design-track tickets get a **ticket-specific** `docs/design-specs/<TICKET>.md` with §2 + §2c before `--approve-scope`. Amendment analysis must include a surface map in `04-ui-ux-concept.md`.

---

## 7. All CLI Commands

```bash
# Project management
./studio adopt <project> --from <git-url-or-path> [--intent intake/<p>.md]
./studio bootstrap [project] [intake-file]
./studio init <project> --archetype <type>
./studio start <project> --mode [core|lean]
./studio status <project>
./studio board <project>
./studio focus <project> [--force]   # hide siblings; will not clobber a live lease unless --force
./studio isolate <project>           # hide sibling projects/ from the agent
./studio resume <project>            # checklist
./studio execute <project> [--json] [--release]  # one next action; loop until HITL
./studio ticket-card <project> <id>
./studio receipt <project> <id>
./studio health <project>
./studio guard <project> "request"
./studio install [--with-skills]     # after git clone: npm UI deps (+ optional skills)
./studio verify-worlds
./studio verify-abstraction

# Intake & pre-implementation (gates 0–2)
./studio adopt <project> --from <git-url-or-path> [--intent intake/<p>.md]
./studio intake <project> <input-file>
./studio blueprint <project>
./studio design <project> --scope journey|core-views|as-built
./studio approve <project> --gate 0|1|2
./studio approve-design <project> <TICKET-ID>   # after spec + all-state mocks exist
./studio approve-arch <project> <TICKET-ID>     # after docs/architecture/<TICKET>.md exists
./studio approve <project> --milestones
./studio revise <project> --gate <n> --feedback "..."

# Amendment intake (post gate 2)
./studio amend <project> intake/amendments/<p>/amendment_NN.md
./studio amendments <project>
./studio approve <project> --amendment AM-001
./studio approve <project> --prd-amendment AM-001   # class C PRD tier change

# Studio library (library-first)
./studio library list
./studio library suggest <project> <query>
./studio library pull <project> auth tokens button   # not stubs (billing, feature-gating)
./studio library promote <project> <path> [--force] [--ticket ID]
./studio library promote-design <project> [--force]
./studio promote-library <project> [--force]    # alias: design promotion

# Sprints & tickets
./studio sprint <project>
./studio sprint <project> --kind hygiene         # lint/debt; does not count toward cadence
./studio sprint <project> --approve-scope       # next phase; an empty phase is skipped
./studio note <project> "…"                     # mid-execute inbox (ACK; drain after MOVE_DONE)
./studio review <project> [--approve|--reject --reason "..."]
./studio feedback <project> "raw idea"
./studio clarify <project> FB-001 [--title ...] [--acceptance ...] [--approve]
./studio feedback-list <project>
./studio ticket <project> "title" [--from-feedback FB-001]
./studio move <project> <id> <status> [--reason "..."]
./studio ship <project> --to dev               # before cadence review
./studio ship <project> --to main --approve    # production — HITL
./studio groom <project>
./studio execute <project>           # loop until HITL; INFORM open HQ LOs
./studio execute <project> --release # free the execute lease
./studio settings [--reset-usage]              # HQ train ledger
./studio settings <project> [--init] [--reset-usage]

# Quality & decisions
./studio gate <project> [--level N]
./studio adr <project> "title"
./studio decide <project> "title"
./studio decisions <project>

# Environment (Docker required; --approve injects projects/<p>/.env)
./studio env <project> init
./studio env <project> up|migrate|dev --approve
./studio env <project> down|status
./studio repo <project> create|status

# Learning & legacy sync
./studio learn "title" --signal <s>            # harvest now (inbox + classified LO)
./studio learn-list
./studio train SO-001 --from mistake --topic "…" --lo LO-NNNN
./studio train --purge-empty                    # close jobs with blank observation
./studio infusion                              # lists open LOs; does not block IMPLEMENT
./studio retro <project> [--complete]          # --complete auto-harvests LOs from badly/improve
./studio sync <project>              # heuristic scan project → library
./studio promote <project> <asset>   # single-path promote (legacy)
./studio update-skills
```

---

## 8. Managing Skills

### Internal Skills (`.quinsy-studio/teams/`)

Each team has a `README.md` (roles) and `skills/` (one markdown per skill).
Each skill contains: **Metadata** (ID, trigger words, phases, roles), **Behavioral rules**,
**Anti-patterns**, and **References**.

**Skill Registry:** `.quinsy-studio/teams/skill-registry.md` — the central index.
The agent assigns matching skills to each ticket via trigger words
(max. 5 per ticket).

**Create a new internal skill:**
1. Create file `teams/<team>/skills/<name>.md` (copy schema from existing skills)
2. Register skill in `skill-registry.md` (trigger words, phases, archetype)
3. Run test: `python3 .quinsy-studio/studio-tools/test_skill_matching.py`

Motion is an internal skill, not an external subscription. [knowledge-base/skill-extensions/motion-transitions.md](knowledge-base/skill-extensions/motion-transitions.md) is loaded by UX-002, UX-005, FE-001, and FE-002. Every UI spec has **§2d Motion**. The kit uses `--motion-*` in `studio-library/ui/tokens/design-tokens.css`. HITL `motion: off` sets those durations to `0ms` in the project token file.

### External Skills (Skill Package Manager)

The studio subscribes to best-in-class skills from external repositories:

```json
// .quinsy-studio/skill-dependencies.json
{
  "design":         "github:Nutlope/hallmark@main",
  "marketing_aeo":  "github:coreyhaines31/marketingskills@main",
  "gamedev":        "github:gamedev-skills/awesome-gamedev-agent-skills@main",
  "compliance":     "github:samir-abis/cookiecomply-skills@main",
  "geo":            "github:bloomprotocol/agent-visibility-skill@main",
  "all_domains":    "github:seb1n/awesome-ai-agent-skills@main"
}
```

**Workflow:**
```bash
./studio update-skills               # import/update all sources
./studio update-skills --list        # show declared sources
./studio update-skills design        # single domain only
```

Imports go to `.quinsy-studio/external-skills/<domain>/`.
Then check `INDEX.md` and update the conflict matrix
(`knowledge-base/external_skills_conflict_matrix.md`).

**Important:** External skills are ALWAYS subordinate to the internal anti-slop protocol and
Zero-Data Architecture. They are tools, not authority.

### Adding a new external skill

1. **Declare the source** in [`.quinsy-studio/skill-dependencies.json`](skill-dependencies.json):

```json
"my_domain": {
  "repo": "github:owner/repo@main",
  "install": "npx skills add owner/repo",
  "why": "One-line reason for the studio",
  "team": "05-growth-marketing-content",
  "usage": "when to activate (trigger words or workflow)"
}
```

2. **Import into the studio** (git clone → `.quinsy-studio/external-skills/<my_domain>/`):

```bash
./studio update-skills my_domain    # single domain
./studio update-skills              # all domains
./studio update-skills --list         # show declared sources
```

3. **Register for ticket matching** — add a row in [`teams/skill-registry.md`](teams/skill-registry.md) (external source → internal team/skill, activation triggers).

4. **Check conflicts** — review/update [`knowledge-base/external_skills_conflict_matrix.md`](knowledge-base/external_skills_conflict_matrix.md) if the external skill contradicts anti-slop or Zero-Data rules.

5. **Verify** — `python3 .quinsy-studio/studio-tools/test_skill_matching.py`

**Optional — install into your local Cursor agent** (not the studio repo):

```bash
./studio update-skills --npx my_domain
```

Uses `npx skills add` per the `install` field (e.g. into `~/.cursor/skills`). Default studio import uses **git clone** so skills are versioned with the project and referenced from `external-skills/INDEX.md`.

---

## 9. Optimizing the Process

The studio optimizes itself via **Learning Items** (LO-*):

```bash
./studio learn "Gate check takes too long" --signal tooling-gap
./studio learn-list
```

Signals: `tooling-gap`, `process-gap`, `design-gap`, `quality-risk`, `conflict`, ...

**Workflow (Meta-Loop):**
1. **Detect signal** — Gate failure, rework, tooling/design gap, reuse path
2. **Harvest immediately** — `./studio learn`, retro `--complete`, reuse, or 3rd gate fail (inbox + classified LO)
3. **Train in a HQ session** — `./studio train` while product `IMPLEMENT` continues in its own chat. `STUDIO_LO` only when the product loop is idle
4. **Infuse** — playbook / package / process / tooling (generalize — no client names, no project UI copy)
5. **CHANGELOG** + move LO to `backlog/done/`
6. **Check** — `./studio infusion` lists remaining LOs (does **not** block the next project IMPLEMENT)
7. **Test** — `python3 -m unittest test_studio_execute.py test_studio_harvest.py` (from `studio-tools/`)

**Edit process documents directly:**
- `process/lifecycle.md` — Phases
- `process/gates.md` — Gate definitions
- `process/ticket-workflow.md` — 9 steps
- `process/milestone-planning.md` — Milestone roadmap
- `process/amendment-intake.md` — Strategic direction → phases + tickets
- `process/learning-loop.md` — Dual loop + Studio Infusion Gate
- `process/studio-abstraction.md` — Studio HQ must not name client projects
- `process/human-in-the-loop.md` — HITL decisions
- `knowledge-base/contextual-ia-playbook.md` — Feature placement (UX-003)
- `knowledge-base/workflow-definition-playbook.md` — End-to-end flows before UI specs
- `knowledge-base/design-system-compliance-checklist.md` — Library-only UI
- `knowledge-base/design-spec-template.md` — Team 10 spec; file + all-state in-context token mocks required before `approve-design`
- `knowledge-base/` — Playbooks

---

## 10. The Dual-Loop: Studio Learns from Projects

### Loop 1: Local Project Loop (Project World)

Project-specific insights remain **captured in the project**:
- ADRs → `projects/<name>/docs/adr/`
- Learnings → `projects/<name>/docs/studio-learnings-local.md`
- Schema decisions → `docs/definitions/`

These do **not** influence how the studio operates in other projects.

### Loop 2: Global Studio Evolution (Studio World)

Universally applicable insights are **harvested the moment they are identified** and **trained in a HQ session** (`./studio train`). They do **not** replace the next product `IMPLEMENT`:

1. **Harvest** — learn / retro `--complete` / reuse / 3rd gate fail → inbox + classified LO
2. **Train in a HQ session** — `./studio train` (product execute INFORM the count). `STUDIO_LO` only when idle
3. **Check** — `./studio infusion` lists open LOs (does **not** block IMPLEMENT or `./studio sprint`)
4. **Project kit (gate 2b)** → `./studio approve --gate 2b` copies the prototype into the product app. The product look stays in the project.
5. **Code** → `./studio library promote <project> <path> --ticket <id>` only if the **generic** asset improved (never raw project UI copy)
6. **CHANGELOG** — every studio change documented

Registry: [studio-library/library_registry.md](studio-library/library_registry.md)

**Selection criteria:**
- ✅ Generic, no secrets, quality-verified
- ✅ Logged in `manifest.json` with version
- ❌ Project-specific hacks

**Example:**
```bash
./studio library pull new-app auth tokens button   # not stubs
./studio library promote my-project packages/auth --ticket MY-0003 --force
```

The next project starts with `./studio library pull` from an improved library.

---

## 11. Studio Library

The reusable assets are located in `.quinsy-studio/studio-library/`:

```
studio-library/
├── library_registry.md / .json   # Canonical kinds & paths
├── ui/
│   ├── tokens/
│   ├── components/               # button/, … (functional + neutral Tailwind)
│   ├── page-types/
│   └── sticker-sheet/            # catalog + latest sheet page
├── packages/                     # auth, billing, feature-gating (+ providers/)
└── manifest.json                 # versioned asset registry
```

**Rules:**
- **Pull** (library → project): `./studio library pull <project> auth tokens button` — **not** stubs (`billing`, `feature-gating`)
- **UI kit peers** (product app, on setup): `radix-ui`, `class-variance-authority`, `clsx`, `tailwind-merge`, `lucide-react` (+ `@headlessui/react`) — `docs/setup/ui-kit.md`
- **Host `packages/ui`:** product-local at reuse; do not treat it as an unpromoted studio-library path
- **Project kit** (gate 2b): `./studio approve --gate 2b`. Do not promote the product look into studio-library.
- **Motion:** dialogs, menus, tooltips, sheets, buttons, and the other interactive controls already animate from `--motion-*`. Pull them. Do not add a second fade. Pattern: [studio-library/ui/docs/patterns/transitions.md](studio-library/ui/docs/patterns/transitions.md).
- **Promote code**: only if the generic asset improved — `./studio library promote <project> <path> --ticket <id>`
- No secrets or client branding in library assets

See [library_registry.md](studio-library/library_registry.md).

## 12. Quality Assurance

| Check | When | How |
|-------|------|-----|
| **Anti-Slop Audit** | Every commit | `python3 .quinsy-studio/studio-tools/validate_anti_slop.py .` |
| **QA Gate** | Before `move … done` | `./studio gate <project> --level 5` |
| **Execution receipt** | Before `move … done` | `./studio receipt <project> <ID>` — Plan, AC coverage, default flow |
| **Execute / health** | Each session / when stuck | `./studio execute <project>` · `./studio health <project>` |
| **Skill Matching Test** | Every QA gate + registry change | `python3 .quinsy-studio/studio-tools/test_skill_matching.py` |
| **Studio abstraction** | After studio doc/tool edits | `./studio verify-abstraction` |
| **Conflict Matrix** | After `update-skills` | `knowledge-base/external_skills_conflict_matrix.md` |
| **Gate Exit Criteria** | Per gate | `process/gates.md` |

**QA Gate Levels:**
- Level 0–1: Structure + Status
- Level 2: Linting
- Level 3: Type Check
- Level 4: Tests
- Level 5: Build + Audit + Anti-Slop + **Skill Matching**

---

## 13. Troubleshooting

| Problem | Solution |
|---------|----------|
| `./studio` not found | `chmod +x studio` (one-time) |
| External skills missing | `./studio update-skills` (requires git) |
| Duplicate ticket IDs | `rm projects/<name>/.ticket_counter` (will be rebuilt) |
| QA gate red on npm_audit | Lockfile missing → `npm i --package-lock-only` in project |
| Skill matching test red | Check registry triggers → `teams/skill-registry.md` |
| Docker template missing | Located at `studio-templates/docker/` — do not delete |
| Studio files lost | **Git backup!** Check `.gitignore` (external skills are regenerable) |
| Agent asks “should I continue?” mid-sprint | Tell it to `./studio execute` until `HITL` — do not approve ticket-by-ticket |
| `move … done` refused | Need gate **level 5** passed **and** a filled `sprints/SPRINT-NN/receipts/<ID>.md` |
| `INFORM cost-cap` | Raise the **named** key in product `docs/studio.settings.local.yaml` or HQ local yaml (`ledger=` on COST). Size S–XL: [GETTING_STARTED](GETTING_STARTED.md#studio-settings-cost--tokens) |
| Execute says `HITL` | Gate 0–2 (N needs N-1), packet `approve-design` / `approve-arch`, `env --approve`, cadence review, or tech-veto — not a morning brief |
| Cursor asks to Allow `./studio move … done` | IDE Auto-review, not studio HITL — see [GETTING_STARTED — Cursor Auto-run](GETTING_STARTED.md#cursor-auto-run-vs-studio-hitl) |
| Execute says `STUDIO_LO` | Product loop is idle — infuse the LO in `.quinsy-studio/` (not project code), CHANGELOG, move to `backlog/done/`, then `./studio execute` again |
| Open LOs mid-sprint | Harvest immediately; INFORM the count; `./studio train` in a **HQ** chat — product IMPLEMENT continues |
| Docker missing / env without `--approve` | Install Docker Desktop. `./studio env <p> up --approve` is required to inject secrets. Do not Read `.env` values |
| Sixth concurrent execute | `parallel.max_projects` (default 5). Wait or `./studio execute <p> --release` on an idle product |
| Focus would rewrite another chat’s isolation | Another product holds a lease. Use a **new chat**, or `--force` only if you intend to steal isolation |
| Mid-execute chat | `./studio note` — ACK and continue; drain after `MOVE_DONE`. Only abort preempts |
| Sibling tree still visible | Focus is not a sandbox. Use one chat per product; do not Shell `ls`/`git` another `projects/` folder |
| Guard says `CROSS_PROJECT` | Stay on the active project unless the human explicitly switches `./studio focus` |

---

## Further Documentation

- `process/studio-overview.md` — direction → shortlist → PRD → gates → phase train → production
- `GETTING_STARTED.md` — Execute loop, **ideation desk**, **learnings / harvest**, **studio load caps (S–XL)**, **secrets / Docker / leases**, **motion**, prompts, session ritual
- `process/hq-isolation-sprints.md` — HQ isolation epic (`LO-0314`–`LO-0326`)
- `process/lifecycle.md` — 7-phase lifecycle
- `process/agent-context.md` — Session start + execute until HITL
- `process/gates.md` — Gate definitions
- `process/adr-policy.md` — ADR rules
- `process/human-in-the-loop.md` — HITL
- `process/studio-abstraction.md` — Project-agnostic studio HQ
- `process/ticket-team-allocation.md` — Team 10 / `ia-feature-placement`
- `teams/skill-registry.md` — Skill index
- `knowledge-base/aesthetic-presets/` — Team 10 visual direction presets
- `knowledge-base/skill-extensions/` — Deep playbooks extending CL/GM/UX/PE skills
- `knowledge-base/anti_ai_slop_protocol.md` — Anti-slop
- `knowledge-base/external_skills_conflict_matrix.md` — Skill conflicts
- `CHANGELOG.md` — Version history
