# Brownfield adopt — hand an existing project to Quinsy Studio

> **When:** You already have a codebase. You want the studio to **understand what is implemented** (thorough, not a README restatement), then plan further work through the normal gates and execute loop.  
> **Not:** Greenfield PRD → empty scaffold (`./studio bootstrap`). Not LEAN “drop a ticket.” Not an amendment (amendments assume gate 2 already passed).

---

## What you hand over

You do **not** write a full PRD first.

| Item | Required | Notes |
|------|----------|--------|
| **The repo** | Yes | Git URL or local folder. Lands in `projects/<slug>/` (World B). **Keep the project’s own `.git`.** Never `git add projects/` from studio root. |
| **How to run it** | Yes | README / scripts / env. Secrets stay in `.env` (not committed). If it does not run, as-built must say **broken** vs **unimplemented**. |
| **Intent brief** | Optional | `intake/<slug>.md` from `studio-templates/adopt_intent.md`: problem, audience, what “further” means. If omitted, first HITL is continue-as-is vs change course. |
| **Access constraints** | If any | APIs, paid keys, production data the agent must not use. |

```bash
./studio adopt <slug> --from <git-url-or-path> [--intent intake/<slug>.md]
./studio focus <slug>
./studio execute <slug>    # fill as-built → synthesize PRD → HITL gate 0
```

---

## Overlay rules (never wipe the app)

`./studio adopt` **overlays** studio folders onto the live tree:

- Adds `docs/`, `backlog/`, `sprints/`, `status.json`, `agent-briefing.md`, `RUNBOOK.md` if missing
- Sets `status.json` `mode: "adopt"`
- Copies as-built templates into `docs/as-built/`
- Does **not** run full `init_project()` (that scaffolds an empty app)
- Does **not** `git init` if `.git` already exists
- Does **not** copy the studio Docker template if the project already has Docker/Compose/a documented run command
- Does **not** merge project UI/tokens into `studio-library/`

Application source (`src/`, `app/`, `packages/`, etc.) is left untouched.

---

## Phases

### A — As-built (thorough)

Agent fills `docs/as-built/` by **reading the code**, not restating the README.

| File | Must include |
|------|----------------|
| `00-product.md` | What it is, who it is for, **default user path** (from routes/UI) |
| `01-surfaces.md` | Every user-facing route / surface / CLI; implemented vs stub vs dead |
| `02-domain-and-data.md` | Stores, schemas, migrations, sync; what is actually written/read |
| `03-architecture.md` | Runtime topology, packages, key modules, integrations (**file paths**) |
| `04-auth-and-boundaries.md` | Auth, tenancy, secrets, client vs server |
| `05-ui-inventory.md` | Real components/pages (not a hoped-for design system) |
| `06-quality.md` | Tests, CI, how to run, known red |
| `07-implemented-vs-gap.md` | Matrix: shipped / partial / stub / debt |

**Done means:** each claim cites paths; stubs and TODO/FIXME are listed; a default-flow walk was attempted (`RUNBOOK.md` updated). “It’s a Next.js app with auth” is **not** done.

Then synthesize `docs/intake/prd.md` from as-built + intent (constitution for further work). Fill `docs/definitions/` from the same evidence.

**HITL gate 0:** human confirms “this is what we have” + PRD. `./studio approve <p> --gate 0`

### B — Architecture reconciliation (gate 1)

`./studio blueprint` in adopt mode documents **as-is**, plus ADRs for:

- decisions already in the code (document, don’t reinvent)
- proposed changes **only** where the intent brief requires them

No greenfield stack swap unless the human asked for it.

**HITL:** `./studio approve <p> --gate 1`

### C — Design truth (gate 2)

Do **not** build a parallel `design/prototype` as if the product did not exist.

- Surface map + placement of **current** UI (`docs/ia/surface-map.md`, `design/DESIGN.md`)
- Token/component reality vs studio-library (gaps → LO-*, no auto-copy of project UI)
- Optional mocks **only** for net-new surfaces in the gap matrix

**HITL:** `./studio approve <p> --gate 2` — “design of what exists + debt,” not “approve a new sticker sheet only.”

### D — Plan to go further

Same as post–gate 2:

1. Gap matrix → `docs/phases/` (M0 = stabilize / make as-built honest, then net-new)
2. Human `./studio approve <p> --milestones`
3. Tickets for **active milestone only** → sprint → `./studio execute`

Later strategic pivots: [amendment-intake.md](amendment-intake.md).

---

## Execute loop

`mode: adopt` still uses gates 0–2. Differences:

| Situation | Execute ACTION |
|-----------|----------------|
| As-built templates still empty | `IMPLEMENT` — fill `docs/as-built/` (cite paths) |
| As-built ready, PRD missing | `VERIFY` — synthesize `docs/intake/prd.md` |
| PRD + as-built, gate 0 open | `HITL` gate 0 |
| After gate 1 | Fill as-is blueprint + ADRs; do **not** invent a new stack |
| After gate 1, before gate 2 | Surface map of **existing** UI — do not scaffold an empty Next.js prototype over the live app |
| After milestones | Normal sprint execute (`IMPLEMENT` / `STUDIO_LO` / `HITL`) |

Library-first applies to **new** UI/packages only.

QA: `./studio gate --level 5` where the project is Node. `docs/as-built/06-quality.md` records the real command. Do not fake a Next.js prototype for a non-Node app.

---

## Two worlds

Adopted code is a **project repo**. Studio HQ stays in `.quinsy-studio/`. See [worlds.md](worlds.md).
