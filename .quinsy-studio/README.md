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
4. [Where Is What? (Templates, PRDs, Tickets)](#4-where-is-what)
5. [The Studio Process (Dual-Speed)](#5-the-studio-process-dual-speed)
6. [All CLI Commands](#6-all-cli-commands)
7. [Managing Skills (Internal + External)](#7-managing-skills)
8. [Optimizing the Process (Learning Loop)](#8-optimizing-the-process)
9. [The Dual-Loop: Studio Learns from Projects](#9-the-dual-loop)
10. [Studio Library: Reusable Assets](#10-studio-library)
11. [Quality Assurance & Gates](#11-quality-assurance)
12. [Troubleshooting](#12-troubleshooting)

---

## 1. What is Quinsy Studio?

Quinsy Studio is a **file-system-based operating system for software projects**.
It consists of:

- **Process Documents** (`process/`) — Lifecycle, Gates, Anti-Slop, Ticket Workflow
- **Teams & Skills** (`teams/`) — 9 teams, 37 internal skills + skill registry
- **Knowledge Base** (`knowledge-base/`) — Playbooks (Design, Frontend, Backend, Compliance, AI)
- **Studio Tools** (`studio-tools/`) — Python CLI with all commands
- **Studio Templates** (`studio-templates/`) — PRD, Ticket, ADR, Docker base
- **Studio Library** (`studio-library/`) — Reusable assets (UI, Packages, Tokens)
- **External Skills** (`external-skills/`) — Imported best-in-class skill packages

The studio operates in **Dual-Speed mode**:
- **CORE** — for new platforms & complex systems (6 phases with human gates)
- **LEAN** — for iterations & features in existing projects (4 phases)

---

## 2. Folder Structure

```
quinsy-studio/
├── .quinsy-studio/                 ← THE STUDIO (everything here)
│   ├── process/                    # Process documents (Lifecycle, Gates, Anti-Slop)
│   ├── teams/                      # 9 teams × skills + skill-registry.md
│   │   ├── 01-frontend-experience/
│   │   ├── 02-backend-systems/
│   │   ├── 03-compliance-legal/
│   │   ├── 04-product-strategy-architecture/
│   │   ├── 05-growth-marketing-content/
│   │   ├── 06-product-management-operating-model/
│   │   ├── 07-ai-autonomous-systems/
│   │   ├── 08-platform-enterprise-engineering/
│   │   └── 09-studio-operations-evolution/
│   ├── knowledge-base/             # Playbooks (Design, Frontend, Backend, Compliance, AI, Anti-Slop)
│   ├── studio-tools/               # Python CLI (studio.py + all tools)
│   ├── studio-templates/           # PRD, Ticket, ADR, Docker base, Learning logs
│   ├── studio-library/             # Reusable assets (ui/, packages/, tokens)
│   ├── external-skills/            # Imported skill packages (hallmark, marketing, ...)
│   ├── backlog/                    # Studio improvements only (LO-*)
│   ├── retros/                     # Retrospectives & audits
│   └── skill-dependencies.json     # Subscribed external skill sources
├── projects/                       # ALL client projects (each with own backlog, Docker)
│   └── <project>/                  # status.json, docs/, backlog/, sprints/, docker/, design/
├── intake/                         # Raw project ideas (Markdown)
├── studio                          # CLI wrapper (delegates to .quinsy-studio/studio-tools/)
├── README.md                       # Project README (this file is .quinsy-studio/README.md)
└── CHANGELOG.md
```

**Important separation:**
- **Studio World** (`.quinsy-studio/`) — Process, skills, templates, library, LO-* backlog. **This git repo.**
- **Project World** (`projects/<name>/`) — Tickets, code, design, docker. **Each project has its own `.git`.**
- **`intake/`** and **`projects/`** are gitignored in the studio repo. See [process/worlds.md](process/worlds.md).

**IDE agents:** read [`AGENTS.md`](../AGENTS.md) at repo root + [process/agent-context.md](process/agent-context.md).

---

## 3. Quick Start: Launch a Project

See also: [GETTING_STARTED.md](GETTING_STARTED.md) (canonical) · [`AGENTS.md`](../AGENTS.md) (agent contract).

### AI-driven (recommended)

```bash
./studio verify-worlds
./studio bootstrap my-project          # intake → stop at next human gate
./studio focus my-project
./studio resume my-project
```

### Step 1: Place PRD

```bash
cp studio-templates/prd_template.md ../intake/my-project.md
# edit PRD, then:
```

### Step 2: Bootstrap or manual init

```bash
./studio bootstrap my-project
# OR:
./studio init my-project --archetype saas-application
./studio intake my-project intake/my-project.md
./studio start my-project --mode core
```

Intake does **not** create tickets until gate 2.

### Step 3: Human gate 0 — PRD + definitions

Agent fills `projects/my-project/docs/definitions/`, then:

```bash
./studio approve my-project --gate 0
```

### Step 4: Human gate 1 — Architecture

```bash
./studio blueprint my-project
# fill docs/architecture/, docs/adr/
./studio approve my-project --gate 1
```

### Step 5: Human gate 2 — Design

```bash
./studio design my-project --scope core-views   # or: journey
# Next.js prototype in design/prototype/, sticker sheet, ui/tokens
./studio approve my-project --gate 2             # tickets + promote-library
```

### Step 6: Library-first implementation

```bash
./studio library suggest my-project "auth billing"
./studio library pull my-project auth billing button
./studio sprint my-project
./studio move my-project MY-0001 implement
# on done: ./studio library promote my-project packages/... --ticket MY-0001
```

### Step 7: QA & learning

```bash
./studio gate my-project --level 5
./studio retro my-project
```

---

## 4. Where Is What?

| What | Where? |
|------|--------|
| **PRD Template** | `.quinsy-studio/studio-templates/prd_template.md` |
| **PRD (edited)** | `projects/<name>/docs/intake/prd.md` |
| **Raw Idea/Input** | `intake/<name>.md` |
| **Tickets** | `projects/<name>/backlog/open|done|blocked/` |
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
| **Studio Learning Items** | `.quinsy-studio/backlog/open/LO-*.md` |
| **Retros** | `.quinsy-studio/retros/` |
| **Studio Library** | `.quinsy-studio/studio-library/` |

---

## 5. The Studio Process (Dual-Speed)

### CORE Mode (New Platforms, Complex Systems)

| Phase | Action | Artifact | Gate |
|-------|--------|----------|------|
| **1. Intake** | PRD, definitions | `docs/intake/`, `docs/definitions/` | **HUMAN 0** |
| **2. Architecture** | Blueprint, ADRs | `docs/architecture/`, `docs/adr/` | **HUMAN 1** |
| **3. Design** | Mocks, tokens, sticker sheet | `design/prototype/`, `ui/` | **HUMAN 2** (+ tickets) |
| **4. Sprint planning** | Groom, sprint | `sprints/SPRINT-01/` | — |
| **5. Implementation** | Library-first, tickets | Code in project | Reuse on `done` |
| **6. QA** | Anti-slop, tests | QA report | Gate 5 (QA level) |
| **7. Learning** | Retro, promote | Library, LO-* | — |

### LEAN Mode (Features, Iterations)

| Phase | Action |
|-------|--------|
| **1. Ticket Drop** | Ticket directly in backlog |
| **2. Quick Align** | Short solution path → **HUMAN-GATE 1** (Go/No-Go) |
| **3. Execute & QA** | Immediate implementation + tests |
| **4. Fast Sync** | Commit + global asset alignment |

---

## 6. All CLI Commands

```bash
# Project management
./studio bootstrap [project] [intake-file]
./studio init <project> --archetype <type>
./studio start <project> --mode [core|lean]
./studio status <project>
./studio board <project>
./studio focus <project>
./studio resume <project>
./studio guard <project> "request"
./studio verify-worlds

# Intake & pre-implementation (gates 0–2)
./studio intake <project> <input-file>
./studio blueprint <project>
./studio design <project> --scope journey|core-views
./studio approve <project> --gate 0|1|2
./studio revise <project> --gate <n> --feedback "..."

# Studio library (library-first)
./studio library list
./studio library suggest <project> <query>
./studio library pull <project> auth billing [tokens] [button...]
./studio library promote <project> <path> [--force] [--ticket ID]
./studio library promote-design <project> [--force]
./studio promote-library <project> [--force]    # alias: design promotion

# Sprints & tickets
./studio sprint <project>
./studio ticket <project> "title"
./studio move <project> <id> <status> [--reason "..."]
./studio groom <project>

# Quality & decisions
./studio gate <project> [--level N]
./studio adr <project> "title"
./studio decide <project> "title"
./studio decisions <project>

# Environment
./studio env <project> init|up|down|status
./studio repo <project> create|status

# Learning & legacy sync
./studio learn "title" --signal <s>
./studio learn-list
./studio retro <project>
./studio sync <project>              # heuristic scan project → library
./studio promote <project> <asset>   # single-path promote (legacy)
./studio update-skills
```

---

## 7. Managing Skills

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

---

## 8. Optimizing the Process

The studio optimizes itself via **Learning Items** (LO-*):

```bash
./studio learn "Gate check takes too long" --signal tooling-gap
./studio learn-list
```

Signals: `tooling-gap`, `process-gap`, `design-gap`, `quality-risk`, `conflict`, ...

**Workflow (Meta-Loop):**
1. **Detect signal** — Gate failure, rework, tooling gap, design gap
2. **Create learning item** (`./studio learn ...`)
3. **Retrospective** (`./studio retro <project>`) — discuss LO items
4. **Decision** — improve process doc, skill file, or Python tool
5. **CHANGELOG entry** — document change
6. **Test** — `test_skill_matching.py` + `./studio gate <project>`

**Edit process documents directly:**
- `process/lifecycle.md` — Phases
- `process/gates.md` — Gate definitions
- `process/ticket-workflow.md` — 9 steps
- `process/human-in-the-loop.md` — HITL decisions
- `knowledge-base/` — Playbooks

---

## 9. The Dual-Loop: Studio Learns from Projects

### Loop 1: Local Project Loop (Project World)

Project-specific insights remain **captured in the project**:
- ADRs → `projects/<name>/docs/adr/`
- Learnings → `projects/<name>/docs/local_learnings.md`
- Schema decisions → `docs/definitions/`

These do **not** influence how the studio operates in other projects.

### Loop 2: Global Studio Evolution (Studio World)

Universally applicable insights are **promoted to the studio**:

1. **Design (gate 2)** → `./studio approve --gate 2` auto-runs `promote-library`
2. **Code** → `./studio library promote <project> <path> --ticket <id>`
3. **Heuristic** → `./studio sync <project>` (legacy scan)
4. **Process** → playbooks, LO-* backlog

Registry: [studio-library/library_registry.md](studio-library/library_registry.md)

**Selection criteria:**
- ✅ Generic, no secrets, quality-verified
- ✅ Logged in `manifest.json` with version
- ❌ Project-specific hacks

**Example:**
```bash
./studio library pull new-app auth billing
./studio library promote my-project packages/billing --ticket MY-0003 --force
```

The next project starts with `./studio library pull` from an improved library.

---

## 10. Studio Library

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
- **Pull** (library → project): `./studio library pull <project> auth billing`
- **Promote design** (gate 2): `./studio approve --gate 2` or `promote-library`
- **Promote code**: `./studio library promote <project> <path> --ticket <id>`
- No secrets or client branding in library assets

See [library_registry.md](studio-library/library_registry.md).

## 11. Quality Assurance

| Check | When | How |
|-------|------|-----|
| **Anti-Slop Audit** | Every commit | `python3 .quinsy-studio/studio-tools/validate_anti_slop.py .` |
| **QA Gate** | Before every release | `./studio gate <project> --level 5` |
| **Skill Matching Test** | Every QA gate + registry change | `python3 .quinsy-studio/studio-tools/test_skill_matching.py` |
| **Conflict Matrix** | After `update-skills` | `knowledge-base/external_skills_conflict_matrix.md` |
| **Gate Exit Criteria** | Per gate | `process/gates.md` |

**QA Gate Levels:**
- Level 0–1: Structure + Status
- Level 2: Linting
- Level 3: Type Check
- Level 4: Tests
- Level 5: Build + Audit + Anti-Slop + **Skill Matching**

---

## 12. Troubleshooting

| Problem | Solution |
|---------|----------|
| `./studio` not found | `chmod +x studio` (one-time) |
| External skills missing | `./studio update-skills` (requires git) |
| Duplicate ticket IDs | `rm projects/<name>/.ticket_counter` (will be rebuilt) |
| QA gate red on npm_audit | Lockfile missing → `npm i --package-lock-only` in project |
| Skill matching test red | Check registry triggers → `teams/skill-registry.md` |
| Docker template missing | Located at `studio-templates/docker/` — do not delete |
| Studio files lost | **Git backup!** Check `.gitignore` (external skills are regenerable) |

---

## Further Documentation

- `process/lifecycle.md` — 7-phase lifecycle
- `process/gates.md` — Gate definitions
- `process/adr-policy.md` — ADR rules
- `process/human-in-the-loop.md` — HITL
- `teams/skill-registry.md` — Skill index
- `knowledge-base/anti_ai_slop_protocol.md` — Anti-slop
- `knowledge-base/external_skills_conflict_matrix.md` — Skill conflicts
- `CHANGELOG.md` — Version history
