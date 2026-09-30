# Quinsy Studio — Getting Started

> Canonical workflow: **new product** (PRD → architecture → direction 2a → project kit 2b) **or existing codebase** (`./studio adopt` → as-built) → **phase train** (design, then architecture, then implementation; an empty phase is skipped) → cadence review every N implementation phases.  
> Root overview: [`README.md`](../README.md) · Agent: [`AGENTS.md`](../AGENTS.md) · Operations: [`README.md`](README.md) · Isolation epic: [hq-isolation-sprints.md](process/hq-isolation-sprints.md)

**How the studio runs:** the agent does **not** wait for “continue.” It runs `./studio execute <project>`, does the `NEXT` command, then execute again, until `ACTION` is `HITL` (you). Start of a project is HITL at **gate 0 (PRD)** → **gate 1 (architecture)** → **gate 2a (direction)** → **gate 2b (project kit)** — `approve --gate 2` is refused. After that, `INFORM` still loops. Product execute **INFORM**s open HQ learning counts; infuse in a **separate HQ chat** (`./studio train`). `STUDIO_LO` does **not** replace `IMPLEMENT`. Markdown tickets stay the source of truth; the agent loads a **compact card** (skills + playbooks + **CONSTITUTION**), not the whole backlog.

## Start here: tell the agent

**You do not run a long CLI chain by hand.** Open Cursor (default), Claude Code, or Gemini CLI and talk. The agent runs `./studio`; you **approve gates** and **product decisions**. Keys stay in that host — never in studio git.

Two ways in — both are implemented:

| Situation | What you say |
|-----------|----------------|
| **New product** | *"I added `intake/my-project.md`. Bootstrap my-project and walk me through the next human gate."* |
| **Existing codebase** | *"Adopt this repo into my-project and reconstruct as-built state."* |
| **Same session, continue** | *"Focus my-project and execute — loop until HITL."* |
| **Returning later** | *"Execute my-project. Back on track."* |

Open **quinsy-studio** at the repo root (not `projects/<name>/` alone). Cursor rules: [`.cursor/rules/quinsy-studio.mdc`](../.cursor/rules/quinsy-studio.mdc). Claude Code: [`CLAUDE.md`](../CLAUDE.md). Gemini CLI: [`GEMINI.md`](../GEMINI.md).

**Several products in one workspace:** `./studio focus <project>` / `execute <project>` assign which product the loop should run and rewrite a **local** `.cursorignore` + generated isolation rule (Read/Grep). They are not a sandbox. **One chat (or IDE window) per product** — five concurrent products need five chats, not one ignore list. `parallel.max_projects` (default 5) file-leases executes; a sixth is queued. `./studio focus` will not clobber another live lease unless `--force`. Shell can still see other `projects/` trees. Guard returns `CROSS_PROJECT` if the request names a sibling. Product git runs **inside** `projects/<name>/`. Studio HQ git never stages `projects/`. HQ train stays in a **separate** session.

**Docker is required** for gate, migrate, and product boot (`./studio env <p> up|migrate|dev --approve`). Missing Docker stops those commands with install instructions — there is no host fallback that cats `.env` into the chat.

### Secrets, Docker, and concurrent products

| Rule | What to do |
|------|------------|
| **Names, not values** | Agents Read `env.schema.json` / `*.env.example`. Do not Read `.env` / `.env.local` values (Cursor ignore: QUINSY-SECRETS). |
| **Local dotenv** | Desktop: gitignored `projects/<p>/.env` (copy `.env.example`). `./studio env <p> up --approve` passes it to Compose. |
| **Production** | Coolify environment variables. No project `.env` on the VPS. |
| **Inject** | `./studio env <p> up\|migrate\|dev --approve`. Without `--approve` the command exits non-zero. |
| **Docker** | Required. Install Docker Desktop if the CLI is missing. Gate/QA output is redacted. |
| **Leases** | `parallel.max_projects: 5` in `.quinsy-studio/studio.settings.yaml`. A sixth `./studio execute` is queued. HITL idle or `./studio execute <p> --release` frees a slot. |
| **Focus** | `./studio focus` will not rewrite `.cursorignore` while another product holds a lease, unless `--force`. |
| **HITL packets** | Sign-off is spec/mocks, `docs/architecture/<TICKET>.md`, or env `--approve` intent — not a morning-brief dashboard. |

Plan: [hq-isolation-sprints.md](process/hq-isolation-sprints.md) (`LO-0314`–`LO-0326`).

```bash
./studio install                    # once after clone (Tailwind + Headless UI)
./studio verify-worlds
./studio verify-abstraction
```

`./studio resume` still prints a **checklist**. Prefer **execute**: one machine-readable step, loop until `HITL`. After a groomed sprint, the agent implements tickets without asking “should I continue?”

### Track A — New product (PRD)

`intake/` is gitignored (local only).

```bash
cp .quinsy-studio/studio-templates/prd_template.md intake/my-project.md
# Edit intake/my-project.md — slug should match the project name
./studio bootstrap my-project
./studio focus my-project
./studio execute my-project         # HITL at gate 0 when definitions are ready
```

Bootstrap / `init` / `design` install **UI kit peers** in the prototype `package.json` (`radix-ui`, `class-variance-authority`, `clsx`, `tailwind-merge`, `lucide-react`, `@headlessui/react`) and write `docs/setup/ui-kit.md`. Do not wait until a component import fails.

### Track B — Existing codebase (adopt)

Do **not** run `./studio bootstrap` / `init` on a live tree — that scaffolds an empty app. Hand over:

1. The repo (git URL or folder)
2. How to run it (README / env **names**). Desktop values stay in gitignored `projects/<p>/.env`. Production values stay in Coolify. Do not paste either into chat.
3. Optional intent: copy [adopt_intent.md](studio-templates/adopt_intent.md) → `intake/<slug>.md`

```bash
./studio adopt my-project --from /path/to/repo   # or https://github.com/org/repo.git
./studio focus my-project
./studio execute my-project   # fill as-built → synthesize PRD → HITL gate 0
```

The agent reconstructs **implementation state in depth** (`docs/as-built/`, cite file paths). Overlay also writes `docs/setup/ui-kit.md` and merges kit peers into existing app `package.json`s. Then: as-is architecture (gate 1) → keep vs evolve (2a) → token-map of what exists (2b, **no fake prototype**) → milestone plan from the gap matrix → execute loop.

Full process: [brownfield-adopt.md](process/brownfield-adopt.md)

### End-to-end: example conversation

**Existing repo** (adopt) and **new product** (bootstrap) are alternatives for the first HITL — not sequential steps.

| Phase | You say | Agent does | You approve |
|-------|---------|------------|-------------|
| **Adopt** | *"Adopt my-project from this folder and reconstruct as-built"* | `./studio adopt` → fills `docs/as-built/` + PRD | *"This is what we have — approve gate 0"* |
| **or new product** | *"Bootstrap my-project from intake/my-project.md"* | `./studio bootstrap` → fills `docs/definitions/` | *"Gate 0 looks good — approve"* |
| **Architecture** | *"Continue with blueprint"* | `./studio blueprint` | *"Approve gate 1"* (core stack decision) |
| **Design direction** | *"Interview me for look and feel"* | `./studio design --discovery` | *"Approve gate 2a"* |
| **Design kit** | *"Design core views"* / live prototype | `./studio design` + Team 10 iteration | *"Approve gate 2b"* |
| **Phase** | *"Let the sprint run"* | `./studio sprint` opens design, then architecture, then implementation, and skips an empty phase → **`./studio execute`** | Sign the phase once when every packet is written |
| **Milestones** | *"Draft the milestone roadmap"* | Fills `docs/phases/` from gap matrix or PRD | *"Approve milestones"* → agent writes M0 tickets |
| **Cadence review** | *"Give me a sprint review"* | `./studio review` | Every N implementation phases: *"Shipped looks good"* → `--approve`. Design and architecture phases do not count. Off-cadence / backend: inform → retro |
| **New idea** | *"I want offline mode"* | `./studio feedback "…"` → clarify → ticket | Confirm clarified ticket before the **next** sprint |

**Sprint feedback** = small, concrete ideas. **Amendments** = strategic direction (vision brief → milestone + ticket breakdown). See [Amendment intake](#amendment-intake-strategic-direction) below.

**No product IMPLEMENT until gates 0, 1, 2a, and 2b are approved.** After PRD, you approve architecture, then direction (2a), then the project kit (2b). Passing 2b does not mean later screens are designed. After the milestone roadmap, each cycle is a **design phase**, then an **architecture phase**, then an **implementation phase**. A phase with no tickets is skipped and does not open a sprint. Design tickets are written, then signed once with `./studio approve-design <p> --phase`. Each one states `architecture delta: none` or names the architecture ticket. Implementation only builds tickets whose design and architecture are already `approved` or `n/a`. Polish on the signed kit stays `design_status: n/a` and never enters the design phase.

---

## The execute loop (how work actually proceeds)

`./studio execute` drives the whole loop: gates 0 → 1 → 2a → 2b (produce artifacts, then **HITL**), then sprints. After sprint **scope** and **groom** (agent-owned; you may override), the agent’s job is:

```
./studio focus <project>
./studio execute <project>     → do the NEXT command
./studio execute <project>     → again
… until ACTION is HITL         → stop and wait for you
         INFORM still loops    → do NEXT, execute again (includes open HQ LO count)
         TRAIN                 → separate HQ session; product IMPLEMENT continues
```

Do **not** ask “should I continue?” between tickets. `resume` is optional background; **execute** is the driver.

### Product git

Each product is its own git repo under `projects/<name>/`. Studio HQ git never stages `projects/`.

| When | Agent does |
|------|-----------|
| `MOVE_DONE` | **Commit** that ticket on the product repo (`git revert` works per ticket). Does **not** push `main`. |
| Cadence review | If `origin` exists, execute may `NEXT` `./studio ship <p> --to dev` so a git-tracked **dev** host can see the work. |
| No remote | Commits stay local. Local Docker / Compose HITL uses the RUNBOOK URL. |
| Production / `main` | **You:** `./studio ship <p> --to main --approve` (or refuse). The agent may propose and must wait. |

### What `./studio execute` can return

| ACTION | Meaning | Who |
|--------|---------|-----|
| `IMPLEMENT` / `IMPLEMENT <id>` | Adopt: fill `docs/as-built/`. Pre-impl: `./studio blueprint` or `./studio design --discovery` then `./studio design`. Sprint: next unblocked ticket — **or write missing design spec+mocks**. Read the **CARD** (and that one `.md` only) | Agent |
| `VERIFY` | Adopt: synthesize `docs/intake/prd.md`. Sprint: fill the **execution receipt** (`./studio receipt`) | Agent |
| `GATE` | Run `./studio gate <p> --level 5` (build + smoke + tests). Must be **fresh** after this ticket’s implement | Agent |
| `DEBUG` | Gate went red. Write hypotheses in `sprints/SPRINT-NN/debug/<id>.md`, fix, re-gate (max 3 tries) | Agent |
| `MOVE_DONE` | Receipt + gate 5 → `move … done` (product git commit). Then execute again | Agent |
| `VERIFY` (ship) | Before cadence HITL: `./studio ship <p> --to dev` when origin is behind `dev` | Agent |
| `STUDIO_LO <id>` | Idle infusion in `.quinsy-studio/` when there is no in-flight product ticket | Agent (HQ chat) |
| `INFORM` | Reuse / inbox drain / **N open HQ LOs** — do NEXT, loop; **not** architecture or design. **`cost-cap`:** stop; raise the named key | Agent or **you** |
| `HITL` | **Stop.** Gates 0 → 1 → 2a → 2b (sequential), batch **`approve-design --phase` / `approve-arch --phase`** after every packet in that phase is written, **`env --approve`**, cadence review. Not a morning brief. Not a feature-ticket ACK. | **You** |

**What execute picks (in order):**

1. **Adopt as-built** — if `mode: adopt` and `docs/as-built/` still has `_TODO_`, `IMPLEMENT` those files (cite paths). Then `VERIFY` the synthesized PRD
2. **HITL gate 0** — PRD / as-built confirm
3. **Architecture (gate 1)** — `IMPLEMENT` `./studio blueprint` until artifacts are ready, then **HITL** `./studio approve --gate 1`
4. **Design direction (gate 2a)** — unanswered questions in `docs/design/discovery.md`, then **HITL** `./studio approve --gate 2a`. Do not scaffold prototype.
5. **Design kit (gate 2b)** — `IMPLEMENT` `./studio design` (CSS tokens, coded A/M/O, sticker all-states), then **HITL** `./studio approve --gate 2b`. Iterate with `./studio revise --gate 2b`
6. **Finish in-progress** — a ticket already in `implement` still runs VERIFY → GATE → DEBUG → MOVE_DONE (inbox notes wait)
7. **Design phase** — write every spec and all-state mock, then one HITL `./studio approve-design <p> --phase`. An empty design backlog skips to architecture in the same turn.
8. **Architecture phase** — write the notes the design phase filed, plus boundary tickets with no screen, then one HITL `./studio approve-arch <p> --phase`. `./studio approve-arch <p> <TICKET> --reject` sends an infeasible design to the next design cycle. An empty architecture backlog skips to implementation.
9. **`IMPLEMENT`** — next unblocked ticket whose design and architecture are `approved` or `n/a`. One unsigned ticket does not freeze a ready sibling. INFORM open HQ LO count; do **not** `STUDIO_LO` in this chat
10. **`STUDIO_LO`** — only when idle (`implementation_in_flight` is false)

```bash
./studio execute <project>           # human-readable (CONSTITUTION + CARD)
./studio execute <project> --json    # machine-readable (scripts / automations)
./studio execute <project> --release # free the execute lease
./studio env <project> up --approve  # inject named vars into Compose
./studio ticket-card <project> <ID>  # compact card only (~AC, files, deps)
./studio receipt <project> <ID>      # scaffold receipt before done
./studio health <project>            # state-graph: open LOs, missing receipts, deps
./studio settings                    # HQ train ledger
./studio settings <project>        # product execute ledger
```

## Studio settings (cost / tokens)

These numbers are **not Cursor / Claude / Gemini invoices**. They are a **studio load estimate**: roughly `characters ÷ 4` of the CARD plus the files execute listed for that turn. They stop the agent from stuffing more files (`INFORM cost-cap`). They do **not** make the model smarter.

Think of an agency: HQ has a budget for internal training; each client has its own engagement cap. There is still **no money total** — only a **session** counter (resets on `focus` for the product, or `./studio settings --reset-usage` for HQ).

### Two ledgers

| Ledger | Command | Committed file | You override here (gitignored) | Pays for |
|--------|---------|----------------|----------------------------------|----------|
| **HQ** | `./studio settings` | `.quinsy-studio/studio.settings.yaml` | `.quinsy-studio/studio.settings.local.yaml` | Train, infusion, `STUDIO_LO` |
| **Product** | `./studio settings <p>` | `projects/<p>/docs/studio.settings.yaml` | `docs/studio.settings.local.yaml` | That product’s execute loop |

Existing products that predate this split: `./studio settings <p> --init` (does not overwrite a yaml you already edited). New `init` / `adopt` write the product file. **No API keys** in any of these files.

`./studio focus <p>` resets **that product’s** `.studio-session-usage.json`. HQ usage stays until `./studio settings --reset-usage`.

When execute prints `COST … ledger=project` or `ledger=hq`, raise the named key in **that** local yaml.

### What each number means

| Knob | Limits | If you hit it |
|------|--------|----------------|
| `steps.<step>.context` | **This one** execute turn (CARD + listed files) | This ticket’s files are too fat for one load. Raise `context`, or list fewer/smaller files on the ticket. |
| `steps.<step>.budget` | **All** turns of that kind in this session (every implement ticket shares `implement.budget`) | Many execute loops since last focus. Raise that step’s `budget`, or `focus` again to reset usage. |
| `session_token_budget` | **All** steps added together until reset | Session is the real ceiling. Set it **at least as high** as the step budgets you expect to use in one focus (gates + a sprint without re-focusing). |

`cost.profile` (`economy` ≈ 0.5×, `standard` = 1×, `premium` ≈ 2×) multiplies **that file’s** table. Editing the numbers **and** choosing a profile both matter. Put day-to-day tweaks in the **local** yaml so clones keep the medium baseline.

### How to estimate (so you can size the baseline)

Execute counts text it told the agent to load, not every tool call in Cursor.

- **1 estimated token ≈ 4 characters** of CARD + files (`chars_div_4`).
- One implement turn may include up to **12 files** (first 80k characters each) plus an optional `READ` file (up to 120k characters). A theoretical fat turn is on the order of **~250k** estimated tokens — so `implement.context: 28000` will fire on large tickets even if the session is huge.
- A **typical** turn with a small CARD and a few modest files is a few thousand estimated tokens.
- **Session used** ≈ (turns since last reset) × (those estimates). A sprint of ~8 tickets × ~8 execute loops × ~5–15k ≈ **300k–1M**. Watch `./studio settings <p>` after a real sprint.

**Do not** set session below the step budgets you intend to consume in one focus. Example: `design.budget` 400k + `implement.budget` 400k in one focus needs `session_token_budget` **≥ ~800k**, or you will hit session first and the step numbers never matter.

### Size the baseline (committed yaml = **M**)

Committed product + HQ defaults are **M (medium)**: session **400k**, implement context **28k** / budget **400k**, design context **40k** / budget **400k**. That is meant to cover PRD → architecture → design → **one** medium sprint **if you re-focus between phases**, or a short sprint in one focus. HQ’s 400k session is for several train/infusion jobs, not product implement.

| Size | Typical product | `session_token_budget` | `implement.context` | `implement.budget` | How to apply |
|------|-----------------|------------------------|---------------------|--------------------|--------------|
| **S** | Small greenfield, few files per ticket | 200000 | 16000 | 200000 | `cost.profile: economy` on **M**, or lower the three keys in local yaml |
| **M** | Default (committed files) | 400000 | 28000 | 400000 | Leave `profile: standard` |
| **L** | Brownfield / many packages, fat tickets | 800000–1200000 | 60000–100000 | 800000–1500000 | Local yaml, or `profile: premium` on **M** (≈ 800k session, 56k implement context) |
| **XL** | Large monorepo; you never want a mid-sprint cap | 1500000–2500000 | 100000 | 1500000 | Set the keys in **product** local yaml. Keep HQ at M unless train also caps. |

**HQ vs product:** raise **product** when `ledger=project` (normal sprint). Raise **HQ** `steps.learning` / HQ `session_token_budget` only when train / `STUDIO_LO` cap. Four products → four product files; they do not share a burn cap.

**After `INFORM cost-cap`:** raise **only the named key** (e.g. `cost.steps.implement.context`) about 1.5×, then execute again. If session fires while step budgets still have headroom, raise `session_token_budget` first.

### What this does not do

Higher budgets do not improve design or code quality. They only delay the stop. `model_hint` is the lever that can change host model cost (the IDE must honor it). Product LLM **names** live in `env.schema.json`. Desktop **values** live in gitignored `projects/<p>/.env`; production values live in Coolify. Never print `projects/<p>/.env` into chat.

```bash
./studio settings                         # HQ used vs cap
./studio settings <project>            # product used vs cap
./studio settings <project> --init       # write product yaml on an older tree
./studio settings <project> --reset-usage
```

**Tickets stay Markdown** in git (no SQL). Tokens are saved by **layered load**: execute shows a short card; the agent opens the full ticket file only on `IMPLEMENT`.

**New tickets** are compact: frontmatter is the machine record; body is Target, Scope, and specific AC. Boilerplate “gate 5 / anti-slop / tests” lives in process docs — not pasted on every ticket.

**Definition of done (enforced):** `move … done` requires QA **level 5** **and** a filled receipt (`Plan`, `AC coverage`, `Default flow`). Visible UX tickets must walk the **default product path** (not a test-only toggle).

---

## Learnings: harvest when identified

Studio HQ must learn **in the same session** the gap appears. If LOs pile until a human runs `./studio learn` or until the next sprint, the originating context is gone and the next project repeats the mistake.

| When identified | What happens (no extra human trigger) |
|-----------------|----------------------------------------|
| You or the agent log a gap | `./studio learn "…"` → portable? topic file + open inbox + LO : project local log |
| Retro `--complete` | Portable “went badly” / “improve” bullets become LOs; incidents stay local |
| Reuse review | Unpromoted generic `packages/` become LOs (not a raw copy of project UI) |
| 3rd red gate on a ticket | Auto-LO (`signal: gate-fail`) if portable |

Portable harvest writes [knowledge-base/learnings/<domain>/<topic>.md](knowledge-base/learnings/index.md), keeps [inbox.md](knowledge-base/learnings/inbox.md) as the **open queue only**, and opens a compact LO. Find rules with `./studio learn-find`. Product `./studio execute` **continues IMPLEMENT** and **INFORM**s the open LO count. Infusion is `./studio train` in a **HQ session** (or `STUDIO_LO` when the product loop is idle). Infusion-delta aborts if a project folder name appears outside provenance. HQ JSON/inbox writes take a file lock.

The agent **generalizes** into that path (playbook, process, tooling, or library asset). It does **not** merge project tokens or UI into `studio-library/`.

```
learning identified → inbox + classified LO
→ product chat: ./studio execute  → ACTION IMPLEMENT + INFORM N LOs
→ HQ chat:      ./studio train SO-001 --from lo --topic "…" --lo LO-NNNN
→ CHANGELOG + move LO to backlog/done/ (train agent)
```

Details: [learning-loop.md](process/learning-loop.md)

---

## Talk to the agent — prompt cheat sheet

Use natural language. The agent maps your intent to `./studio` commands.

### Starting & continuing

| You want | Example message |
|----------|-----------------|
| New project from PRD | *"Bootstrap &lt;project&gt; from intake/&lt;project&gt;.md"* |
| Existing codebase | *"Adopt &lt;project&gt; from this repo and fill as-built"* |
| Set context | *"Focus &lt;project&gt;"* |
| What's next / keep going | *"Execute &lt;project&gt;"* / *"Loop until HITL"* |
| Checklist only | *"Resume &lt;project&gt;"* (human-readable next-actions list) |
| Recover from drift | *"Back on track"* / *"Focus and execute — only until HITL"* |
| Health of the loop | *"Studio health for &lt;project&gt;"* → `./studio health` |
| Project status | *"What's the status of &lt;project&gt;?"* → `./studio status` + `./studio board` |
| See / raise load caps | *"Show studio settings for &lt;project&gt;"* / *"Init product settings"* — [size S–XL](#studio-settings-cost--tokens) |

### Human gates (you must approve)

| Gate | You say when ready | You say when not ready |
|------|--------------------|-------------------------|
| **0** PRD + definitions **or** as-built (adopt) | *"Approve gate 0"* | *"Revise gate 0: …"* |
| **1** Architecture (as-is on adopt) | *"Approve gate 1"* | *"Revise gate 1: use IndexedDB only, no Supabase yet"* |
| **2a** Design direction (discovery + DESIGN.md) | *"Approve gate 2a"* | *"Revise gate 2a: …"* |
| **2b** Project kit (tokens, A/M/O, sticker) | *"Approve gate 2b"* | *"Revise gate 2b: …"* |
| **Milestones** | *"Approve milestones"* / *"Roadmap looks good"* | *"Revise M0 scope: defer legal pages to M1"* |

Agent runs `./studio approve` or `./studio revise --gate N --feedback "..."`. Milestone roadmap lives in `docs/phases/` — see [milestone-planning.md](process/milestone-planning.md).

### Milestone planning (after gate 2b)

| You want | Example message |
|----------|-----------------|
| Draft roadmap | *"Draft milestone roadmap for &lt;project&gt;"* (from PRD **or** as-built gap matrix) |
| Approve roadmap | *"Approve milestones"* → `./studio approve &lt;p&gt; --milestones` |
| Start M0 work | *"Write M0 tickets and plan the first sprint"* |
| Milestone complete | *"M0 is done — milestone review"* (before M1 tickets) |

### Design scope (gate 2b)

| You want | Example message |
|----------|-----------------|
| Key screens only | *"Design &lt;project&gt; with scope core-views"* |
| Full user journey | *"Design &lt;project&gt; with scope journey"* |
| Existing product (adopt) | *"Map the existing UI — do not scaffold a prototype"* |

### Implementation (after milestones approved)

| You want | Example message |
|----------|-----------------|
| Propose the next phase | *"Plan the next sprint"* → `./studio sprint &lt;p&gt;` opens design, then architecture, then implementation, and skips an empty phase. Agent `--approve-scope` (you may override). |
| Let the phase run | *"Execute until HITL"* — a design or architecture phase writes every packet, then stops once for `--phase`. An implementation phase loops ready tickets with no ticket ACK. |
| Compact ticket view | *"Show the card for &lt;ID&gt;"* → `./studio ticket-card` |
| Work a ticket | Design phase: write spec+mocks and `architecture delta: none` or a ticket id. Architecture phase: write the note. Implementation: library + tokens (agent migrates if DB reachable) → receipt → gate 5 → done → execute again |
| Finish ticket | Receipt + gate 5 → `move … done` (commits product git). Cadence HITL: `./studio ship --to dev` first. `main` is HITL `--approve` |
| Off-sprint idea | *"Can we add X?"* → agent should **not** code silently; uses guard → feedback or ticket |

### Sprint review & feedback (human in the loop)

| You want | Example message |
|----------|-----------------|
| Review shipped work | *"Sprint review for &lt;project&gt;"* |
| Approve sprint | *"Sprint looks good — approve review"* |
| Raw product feedback | *"Feedback: users need offline habits"* (→ `./studio feedback`, **not** a direct ticket) |
| Prioritize backlog | *"Run grooming"* |
| Retro | *"Run retro for this sprint"* → fill retro → `./studio retro <p> --complete` (auto-harvests LOs) → `./studio train` beside execute |

### Amendment intake (strategic direction)

Use when product direction shifts mid-flight — **not** for sprint-review nits (use feedback for those).

| You want | Example message |
|----------|-----------------|
| Start amendment | *"I added `intake/amendments/<project>/amendment_01.md` — run amendment intake"* |
| List status | *"Show amendments for &lt;project&gt;"* → `./studio amendments <project>` |
| After agent analysis | Review `projects/<p>/docs/amendments/AM-001-*/` (vision, UX concept, FE/BE arch, milestone roadmap, ticket drafts) |
| Approve | *"Approve amendment AM-001"* → `./studio approve <p> --amendment AM-001` |
| Roadmap changed | *"Approve milestones"* → `./studio approve <p> --milestones` |

```bash
cp .quinsy-studio/studio-templates/amendment_01.example.md intake/amendments/<project>/amendment_01.md
# Fill vision (§1–7); check teams + skills (§8–9) — do not write milestones
./studio amend <project> intake/amendments/<project>/amendment_01.md
./studio amendments <project>
# Agent fills docs/amendments/AM-001-*/ artifacts
./studio approve <project> --amendment AM-001
./studio approve <project> --milestones   # if 03-milestone-roadmap.md changed M*
```

Full process: [amendment-intake.md](process/amendment-intake.md) · Example: [studio-templates/amendment_01.example.md](studio-templates/amendment_01.example.md)

### UI design (Team 10, after gate 2b)

| You want | Example message |
|----------|-----------------|
| Design spec for UI ticket | *"Write design spec for &lt;TICKET&gt; — include context and placement"* |
| Approve the design phase (HITL) | *"Approve the design phase"* → `./studio approve-design <p> --phase` |
| Approve the architecture phase (HITL) | *"Approve the architecture phase"* → `./studio approve-arch <p> --phase` |
| Send a design back | *"This design cannot be built"* → `./studio approve-arch <p> <TICKET> --reject` |
| Missing component | *"File a ui-new-component ticket — do not invent it in the feature ticket"* |
| Cross-surface move | *"Create ia-feature-placement ticket: move X to Y surface"* |
| Layout-only concern | Agent should ask: *"Is placement correct before we widen the dialog?"* |

**Order:** placement → workflow map → atomic inventory → visual polish. Commercial surfaces (landing, pricing, checkout, PLP, PDP) also load **Team 11** growth intent. Spec path is **ticket-specific** (`docs/design-specs/<TICKET>.md`). The agent **writes** that file and `docs/design-specs/mocks/<TICKET>/` HTML (project tokens, real product chrome, **all states**) for every ticket in the design phase before anyone runs `./studio approve-design <p> --phase`. A stub or a path with no file is not reviewable. Each design ticket closes with `architecture delta: none` or a filed architecture ticket. Spec template: [design-spec-template.md](knowledge-base/design-spec-template.md). Playbooks: [contextual-ia](knowledge-base/contextual-ia-playbook.md) · [workflow-definition](knowledge-base/workflow-definition-playbook.md) · [growth-mechanics](knowledge-base/growth-mechanics-playbook.md) · [canon ledger](knowledge-base/design-team-canon-ledger.md) · [design-system compliance](knowledge-base/design-system-compliance-checklist.md).

### Studio / process (not project code)

| You want | Example message |
|----------|-----------------|
| Log studio gap | *"Log a tooling gap: …"* → `./studio learn` then `./studio train` (also auto on retro/reuse/gate-fail) |
| Infusion | `./studio infusion` lists open LOs (does not block IMPLEMENT). `./studio train` infuses in parallel |
| Check studio docs are generic | `./studio verify-abstraction` |
| Check if request is in scope | *"Is this in scope for &lt;project&gt;: …?"* → `./studio guard` |

### What the agent should **not** do without you

- Skip gates 0 → 1 → 2a → 2b and write product code (architecture and design track are HITL after PRD)
- Run `./studio init` / `bootstrap` on a live codebase (use `./studio adopt`)
- Skip architecture or design HITL (`inform --gate 1` does **not** approve architecture)
- Implement sprint-review **design** feedback in the same cycle (must: feedback → clarify → next sprint)
- Create tickets directly from sprint-review chat
- Commit `projects/` to the studio repo (product git is `git -C projects/<name>`)
- Implement features with no backlog ticket (after gate 2)
- Dump the whole backlog into context (use `ticket-card` / execute CARD)
- Pull library **stubs** (`billing`, `feature-gating`) — build in-project, then promote a working generic
- Leave open LO-* piled for a later human `learn` prompt — harvest immediately; INFORM the count; infuse with `./studio train` in a **HQ** session
- Treat a mid-execute chat message as a new assignment. Run `./studio guard <p> "<verbatim>"` first. On `INBOX_ACK`, resume the current ACTION. `FEEDBACK_ONLY` / `NEEDS_TICKET` must not preempt an in-flight ticket.
- Wait for a feature-ticket ACK / “looks good” after `MOVE_DONE` — loop `./studio execute` until HITL (cadence review, or the batch phase signature **after every packet in that phase exists**)
- Ask the human to `approve-design` when `docs/design-specs/<TICKET>.md` or all-state token mocks are missing — write them first (execute will say IMPLEMENT, not HITL)
- Hold a ready implementation ticket behind one unsigned sibling. The unsigned ticket waits for its phase. The ready ticket proceeds.
- Ask the human to run schema migrate when you can reach the database (Compose via `./studio env <p> migrate --approve`, documented VPS). Apply it yourself, then INFORM. Do not Read `.env` values. Destructive `migrate:fresh` / drop is HITL.
- Skip UI kit peers (`radix-ui`, `class-variance-authority`, `clsx`, `tailwind-merge`, `lucide-react`) on scaffold — they belong in the product app `package.json` from day one (`docs/setup/ui-kit.md`)
- Keep stuffing files after `INFORM cost-cap` — wait for the named key in the **product** or HQ local yaml (`ledger=` on COST)

---

## Crucial commands (reference)

You can run these yourself; in Cursor the agent usually runs them for you.

| When | Command |
|------|---------|
| **After git clone** | `./studio install` · optional `./studio install --with-skills` |
| Session start | `./studio verify-worlds` · `./studio verify-abstraction` · `./studio settings` · `./studio focus <p>` · **`./studio execute <p>`** |
| Isolate siblings | `./studio isolate <p>` (also applied by `focus` / `execute` / `verify-worlds`). Focus will not clobber a live execute lease unless `--force`. |
| Docker / secrets | `./studio env <p> init` · `./studio env <p> up\|migrate\|dev --approve` (names from schema; values from gitignored `projects/<p>/.env`; production in Coolify) |
| Approve / revise gate | `./studio approve <p> --gate 0\|1\|2` (gate N needs N-1) · `./studio revise <p> --gate N --feedback "..."` |
| Checklist | `./studio resume <p>` (optional; execute is the driver) |
| New project from PRD | `./studio bootstrap <p>` (writes `docs/setup/ui-kit.md`; prototype `package.json` has kit peers) |
| Existing codebase | `./studio adopt <p> --from <git-url-or-path> [--intent intake/<p>.md]` (same ui-kit note; merge peers into live `package.json` if present) |
| Phase signature | `./studio approve-design <p> --phase` after every design packet; `./studio approve-arch <p> --phase` after every architecture note. `--reject` sends one design back to the next cycle. |
| Milestones | `./studio approve <p> --milestones` (after `docs/phases/` drafted) |
| Architecture | `./studio blueprint <p>` |
| Design | `./studio design <p> --scope journey\|core-views` |
| Status / board / health | `./studio status <p>` · `./studio board <p>` · `./studio health <p>` |
| Sprint | `./studio sprint <p>` (next phase; empty phases skip) · `--kind design\|architecture\|implementation\|hygiene` · `--approve-scope` · `./studio execute <p>` · `./studio move <p> <ID> implement\|done` · `./studio ship <p> --to dev` |
| Ticket card / receipt | `./studio ticket-card <p> <ID>` · `./studio receipt <p> <ID>` |
| Mid-execute chat | `./studio guard <p> "…"` → `INBOX_ACK` (queued). Drain: `./studio note <p> --drain` |
| Library-first | `./studio library suggest <p> "auth button"` · `./studio library pull <p> auth tokens button` (not stubs). Kit peers must already be in the app. |
| Schema migrate | `./studio env <p> migrate --approve` (or project migrate inside Compose). INFORM. Do not Read `.env` values. |
| Product git / production | `./studio ship <p> --to dev` · `./studio ship <p> --to main --approve` (HITL) |
| Your feedback → backlog | `./studio feedback <p> "..."` · `./studio clarify <p> FB-001 --approve` · `./studio ticket <p> "..." --from-feedback FB-001` |
| Amendment intake | `./studio amend <p> intake/amendments/<p>/amendment_NN.md` · `./studio amendments <p>` · `./studio approve <p> --amendment AM-001` |
| Groom / retro / train | `./studio groom <p>` · `./studio retro <p> --complete` (auto-harvest) · `./studio train SO-001 --from mistake --topic "…"` · `./studio infusion` |
| Studio learnings | `./studio learn "..." --signal <s>` · `./studio learn-find` · `./studio learn-compact` · train in a **HQ** session |
| Cost / tokens | `./studio settings` (HQ) · `./studio settings <p> [--init] [--reset-usage]` · product `docs/studio.settings.local.yaml` |
| Scope check | `./studio guard <p> "your request text"` |

---

## Using Quinsy Studio in Cursor

1. Open the **quinsy-studio** repo in Cursor (not a project subfolder alone).
2. Cursor loads [`.cursor/rules/quinsy-studio.mdc`](../.cursor/rules/quinsy-studio.mdc) automatically.
3. Start each session:

```bash
./studio verify-worlds
./studio verify-abstraction
./studio settings
./studio focus <project>
./studio execute <project>          # loop until HITL
```

4. Talk to the agent in plain language — e.g. *"Bootstrap my-project"*, *"Adopt my-project from this repo"*, *"Execute my-project"*, *"Approve gate 0 / 1 / 2"*. The agent runs `./studio` commands; you approve **studio HITL** stops (gates, packet sign-off, cadence review). `MOVE_DONE` is not one of those stops.

## Cursor Auto-run vs studio HITL

Studio HITL is `ACTION: HITL` from `./studio execute` (gates 0 → 1 → 2a → 2b sequential, batch `approve-design --phase` / `approve-arch --phase`, `./studio env … --approve`, cadence review, tech-veto, abort).

If Cursor shows **Allow** when the agent runs `./studio move <project> <ID> done`, that is **Cursor Auto-review** (Approvals & Execution), not a studio gate. The CLI already requires a filled receipt and gate 5; you should not also ACK the ticket in chat.

**To let the agent close tickets without that prompt:**

1. **Cursor Settings → Agents → Approvals & Execution.** Keep **Auto-review** (recommended). Add `./studio` to the **terminal allowlist** in the IDE UI (prefix match covers `./studio move … done`).
2. This repo also ships [`.cursor/permissions.json`](../.cursor/permissions.json) with `autoRun.allow_instructions` so Auto-review’s classifier leans toward allowing the studio CLI, including `move … done`.
3. Do **not** put a `terminalAllowlist` only in `permissions.json` if you want to stay on Auto-review — a file-based terminal allowlist currently forces Allowlist mode. Prefer the in-app allowlist + the committed `autoRun` hints.
4. **Run Everything** would auto-approve every shell call. That is broader than needed.

Reload the window after changing allowlists. [permissions.json](https://cursor.com/docs/reference/permissions) · [Run modes](https://cursor.com/docs/agent/security/run-modes)

5. **Two repos in one workspace:** studio commits from root; product code commits from `projects/<name>/` **on each `MOVE_DONE`**. Cadence may `./studio ship --to dev`. Production/`main` is HITL. Never `git add projects/` from the studio root. Studio docs use `<project>` placeholders — see [studio-abstraction.md](process/studio-abstraction.md). Focus is an assignment, not a sandbox (see [Start here](#start-here-tell-the-agent)). Smoke UI on the **project RUNBOOK** URL; do not hard-code another product’s host port into HQ.

Details: [Operations manual — Using Cursor](README.md#4-using-quinsy-studio-in-cursor) · [agent-context](process/agent-context.md)

## Session ritual (IDE + agent)

```bash
./studio install                 # once after git clone
./studio verify-worlds
./studio verify-abstraction
./studio settings
./studio focus <project>
./studio execute <project>       # do NEXT until ACTION is HITL
```

## Install (fresh clone)

```bash
./studio install                 # npm: tailwindcss, @headlessui/react
./studio install --with-skills   # optional: external skill packages
```

Requires Node.js 20+. `node_modules/` is not committed.

## Team 10 aesthetic presets

Optional repertoire (e.g. `stripe-like-ui`, `apple-like-ui`, `soft-ui`) — **not** required. Signed `design/DESIGN.md` uniqueness is the source of truth.

- Catalog: [knowledge-base/aesthetic-presets/README.md](knowledge-base/aesthetic-presets/README.md)
- Team skill: [teams/10-product-design-experience/skills/aesthetic-presets.md](teams/10-product-design-experience/skills/aesthetic-presets.md)
- Direction interview: [knowledge-base/design-direction-playbook.md](knowledge-base/design-direction-playbook.md)

## UI design discipline (placement before layout)

When complexity grows, avoid "layout-first" tickets that polish the wrong surface.

| Step | Doc / command |
|------|----------------|
| 1. Where does this live? | [contextual-ia-playbook.md](knowledge-base/contextual-ia-playbook.md) — surface map, `ia-feature-placement` |
| 2. End-to-end flow | [workflow-definition-playbook.md](knowledge-base/workflow-definition-playbook.md) |
| 3. Design spec | [design-spec-template.md](knowledge-base/design-spec-template.md) — **write the file**; §2 + §2c + **all-state, in-context, project-token mocks** |
| 4. Library + tokens | [design-system-compliance-checklist.md](knowledge-base/design-system-compliance-checklist.md) |
| 5. Implement (on-system) | `./studio library pull` → `./studio move … implement` |
| 6. Human taste | `approve-design --phase` / `approve-arch --phase` when every packet in the phase exists; cadence `./studio review` every N implementation phases |

Project IA artifact (3+ surfaces): `projects/<p>/docs/ia/surface-map.md`

## Studio skill extensions

Deep, codebase-aware playbooks extend internal skills (no new ticket IDs). Catalog: [knowledge-base/skill-extensions/README.md](knowledge-base/skill-extensions/README.md)

| Area | Extends | Examples |
|------|---------|----------|
| UX delight | UX-002 | Empty states, micro-interactions, milestone celebration |
| Growth / PLG | GM-003, PS-001 | Share watermarks, activation funnels, usage paywalls |
| Email | GM-003, UX-007 | Transactional HTML, Outlook-safe tables, CTA copy |
| Compliance | CL-001–003 | Privacy audit, cookie CMP, ToS from codebase |
| Security | PE-003 | Frontend XSS/CSP + backend BOLA/SSRF checklists |

Draft new extensions in `intake/skills/` (local) → promote to `knowledge-base/skill-extensions/` after review.

## Four human gates (before coding)

These are the **core start-of-project decisions**. Execute produces the artifacts, then **stops for you**.

| Gate | You approve | CLI |
|------|-------------|-----|
| **0** | PRD + definitions **or** as-built truth + synthesized PRD (adopt) | `./studio approve <p> --gate 0` |
| **1** | Architecture + ADRs after PRD (as-is on adopt; no stack swap unless you asked) | `./studio blueprint` then `./studio approve <p> --gate 1` (refuses if gate 0 is pending) |
| **2a** | Design direction: human interview + unique DESIGN.md (adopt: keep vs evolve). Blocks prototype. | `./studio design --discovery` then `./studio approve <p> --gate 2a` |
| **2b** | Project kit: CSS tokens, coded A/M/O, sticker all-states (adopt: token-map of what exists — no fake prototype) | `./studio design` then `./studio approve <p> --gate 2b`. Iterate: `./studio revise --gate 2b`. Bare `--gate 2` is refused. |

Gate 2b does **not** merge product look into [studio-library](studio-library/library_registry.md). Studio-library stays Headless primitives. **No product IMPLEMENT until 0 → 1 → 2a → 2b are approved.** After a sprint starts, new UI tickets get an agent spec then implement; human taste is sprint review.

Tickets for the **active milestone** are written after you approve the roadmap (`./studio approve <p> --milestones`).

## Milestone roadmap (before first sprint)

1. Agent drafts `docs/phases/README.md` + M0/M1 outlines from PRD + blueprint **or** the as-built gap matrix
2. You approve: `./studio approve <p> --milestones`
3. Agent writes **M0 tickets only** → product backlog (`backlog/*.md`, `milestone: M0`)
4. Sprint planning: `./studio sprint <p>` → agent `--approve-scope` (you may override) → groom → execute

When all M0 tickets are done → **milestone review** → plan M1 tickets → sprints resume.

If strategic direction changes before the next milestone, use **amendment intake** (not sprint feedback alone). Amendments produce a revised `docs/phases/` patch and groomed ticket drafts before backlog materialization.

See [milestone-planning.md](process/milestone-planning.md) · [amendment-intake.md](process/amendment-intake.md).

## Amendment intake (strategic direction)

**When:** After gate 2, when conceptual product direction changes (e.g. agency positioning, new platform surface) — especially before kicking off the next planned milestone.

**Not for:** Sprint-review nits → use `./studio feedback` instead.

1. Copy [.quinsy-studio/studio-templates/amendment_01.example.md](studio-templates/amendment_01.example.md) → `intake/amendments/<p>/amendment_01.md` (local, gitignored)
2. Fill vision sections; **check teams and skills** — do not write milestones or tickets
3. `./studio amend <p> intake/amendments/<p>/amendment_01.md` → scaffolds `docs/amendments/AM-NNN-*/`
4. Agent fills analysis artifacts (UX concept **with surface map**, FE/BE architecture, requirements addendum, **milestone roadmap**, ticket drafts)
5. You approve: `./studio approve <p> --amendment AM-001` (+ `--milestones` if roadmap changed)
6. Agent materializes tickets → normal sprint flow

```bash
./studio amend <project> intake/amendments/<project>/amendment_01.md
./studio amendments <project>
./studio approve <project> --amendment AM-001
./studio approve <project> --milestones
```

## AI-driven launch (new product or existing repo)

**New product:** drop a PRD in [`intake/`](../intake/) (gitignored), then *"Bootstrap &lt;project&gt;"*.

**Existing codebase:** *"Adopt &lt;project&gt; from this repo"* — never empty-init. See [Track B](#track-b--existing-codebase-adopt).

```bash
# New product
./studio bootstrap my-project
# Existing codebase
./studio adopt my-project --from /path/to/repo   # or a git URL

./studio approve my-project --gate 0
./studio blueprint my-project && ./studio approve my-project --gate 1
./studio design my-project --discovery
./studio approve my-project --gate 2a
./studio design my-project --scope core-views    # adopt: --scope as-built (no prototype)
./studio approve my-project --gate 2b
./studio approve my-project --milestones
./studio sprint my-project
./studio sprint my-project --approve-scope
./studio groom my-project --approve
./studio execute my-project          # loop until HITL; INFORM open HQ LOs
```

## Iteration at any gate

```bash
./studio revise my-project --gate 1 --feedback "Use IndexedDB only, defer Supabase"
```

Logged in `projects/<p>/docs/phases/revisions.md`.

## Library-first (UI + code)

| Step | Command |
|------|---------|
| Discover | `./studio library list` |
| Before coding | `./studio library suggest <p> "auth button"` |
| Pull boilerplate | `./studio library pull <p> auth tokens button` — **not** stubs (`billing`, `feature-gating`) |
| Promote code | `./studio library promote <p> packages/auth [--force] [--ticket ID]` only if the **generic** asset improved |
| Promote design | `./studio promote-library <p> [--force]` |

On `./studio move <p> <ID> implement` → library hint. Kit peers (`radix-ui`, `class-variance-authority`, `clsx`, `tailwind-merge`, `lucide-react`) are **setup**, not an afterthought — see `docs/setup/ui-kit.md`.
On `./studio move … done` → requires gate level 5 **and** a filled execution receipt; warns if registry paths changed without promotion.

**Migrations:** if Compose is up (`./studio env <p> migrate --approve`) or a documented VPS is reachable, the agent applies pending migrations as sprint work and tells you it ran. You are not the migrate operator. Secret **values** stay out of chat.

## Project artifacts (all under `projects/<p>/`)

| Artifact | Path |
|----------|------|
| As-built (adopt) | `docs/as-built/*.md` |
| PRD | `docs/intake/prd.md` |
| Definitions | `docs/definitions/` |
| Architecture | `docs/architecture/` |
| ADRs | `docs/adr/` |
| Design spec (per ticket) | `docs/design-specs/<TICKET>.md` |
| Design mocks (per ticket) | `docs/design-specs/mocks/<TICKET>/*.html` (project tokens, in-context, all states) |
| IA surface map | `docs/ia/surface-map.md` |
| Design blueprint | `design/DESIGN.md` |
| Mock scope | `design/DESIGN-SCOPE.md` |
| Design prototype (Next.js) | `design/prototype/` |
| Tokens | `ui/tokens/design-tokens.json` |
| Atomic UI | `ui/components/atoms\|molecules\|organisms/` |
| Sticker sheet | `design/prototype/app/sticker-sheet/` |
| Packages | `packages/auth/`, `packages/billing/`, … |
| Milestone roadmap | `docs/phases/README.md`, `docs/phases/M0-*.md`, … |
| Amendments | `docs/amendments/AM-NNN-*/`, `docs/amendments/registry.json` |
| Revisions log | `docs/phases/revisions.md` |
| Tickets | `backlog/*.md` (product backlog; `implement/`, `done/`, `blocked/`) |
| Execution log | `sprints/SPRINT-NN/execution-log.json` |
| Ticket receipts | `sprints/SPRINT-NN/receipts/<TICKET>.md` |
| Gate-fail debug | `sprints/SPRINT-NN/debug/<TICKET>.md` |
| UI kit peers | `docs/setup/ui-kit.md` |
| Library pull log | `docs/library-usage.json` |
| Library promote log | `docs/library-promotions.json` |

Run prototype: `cd projects/<p>/design/prototype && npm install && npm run dev`

## Agent hardening

| Concern | Doc / command |
|---------|----------------|
| Brownfield adopt | [process/brownfield-adopt.md](process/brownfield-adopt.md) · `./studio adopt` |
| Scope & drift | [process/agent-context.md](process/agent-context.md) |
| Two git worlds | [process/worlds.md](process/worlds.md) · `./studio verify-worlds` |
| Sibling isolation | `./studio focus` / `isolate` · leases (`parallel.max_projects`) · guard `CROSS_PROJECT` · not a sandbox |
| Secrets / Docker | [§ Secrets, Docker, and concurrent products](#secrets-docker-and-concurrent-products) · [hq-isolation-sprints.md](process/hq-isolation-sprints.md) |
| Local URLs / ports | [host-port-allocation.md](knowledge-base/host-port-allocation.md) — smoke the project RUNBOOK URL |
| Studio HQ generic docs | [process/studio-abstraction.md](process/studio-abstraction.md) · `./studio verify-abstraction` |
| Cost / token policy | [Studio settings](#studio-settings-cost--tokens) — HQ vs product, how to estimate, size S–XL |
| Learning loop + infusion gate | [process/learning-loop.md](process/learning-loop.md) · [§ learnings](#learnings-harvest-when-identified) · `./studio infusion` |
| Feature placement (IA) | [knowledge-base/contextual-ia-playbook.md](knowledge-base/contextual-ia-playbook.md) · `./studio ia-audit <p> <TICKET>` |
| HQ skill IDs | FE-007 client security · BE-006 jobs · AI-004 eval — [skill-registry.md](teams/skill-registry.md) · [hq-skill-advancement-sprints.md](process/hq-skill-advancement-sprints.md) |
| Off-sprint work | `./studio guard <p> "request"` |
| Ticket workflow | [process/ticket-workflow.md](process/ticket-workflow.md) |
| UI kit on setup | [installation.md](studio-library/ui/docs/getting-started/installation.md) · `docs/setup/ui-kit.md` |
| Agent-run migrations | [backend_playbook.md](knowledge-base/backend_playbook.md) · HITL table “Schema migrate” |
| Team 10 allocation | [process/ticket-team-allocation.md](process/ticket-team-allocation.md) |
| Team 10 canon playbooks | [design-team-canon-ledger.md](knowledge-base/design-team-canon-ledger.md) · interaction / product-ux / IA / research |

## External skills (optional)

Subscribe to best-in-class skill packages (design, marketing, gamedev, compliance, **superpowers**, **anthropic_docs**). Do **not** `npx claude-code-templates` the whole tree. Do **not** import `executing-plans`.

```bash
./studio update-skills --list
./studio update-skills              # import all into .quinsy-studio/external-skills/
./studio update-skills superpowers  # one domain only
./studio ia-audit <project> <TICKET>
```

To **add** a new source: edit `skill-dependencies.json` → `./studio update-skills <name>` → register in `teams/skill-registry.md`. Full guide: [Managing Skills](README.md#8-managing-skills).

On `./studio move … done` → requires gate 5 + receipt; **commits the product repo**; warns if registry paths changed without promotion. Push `origin/dev` at cadence review (`./studio ship --to dev`). `main` is HITL.

## Sprint cadence (human in the loop)

After gates **0, 1, 2a, and 2b** and the milestone roadmap, each cycle is a design phase, then an architecture phase, then an implementation phase. An empty phase is skipped. You sign a design phase and an architecture phase once each. Implementation runs ready tickets with no ticket ACK. **Cadence review** counts implementation phases only (default every 2). Hygiene (`./studio sprint --kind hygiene`) stays outside the train. A missing UI primitive is a design-phase ticket. Ideas do **not** become tickets blindly.

| Phase | Who | What |
|-------|-----|------|
| Phase scope | **Agent** (you may override) | `./studio sprint <p> --approve-scope`. The next phase is design, then architecture, then implementation. An empty phase does not open a sprint. |
| During a phase | Agent | `./studio execute` until HITL. Design and architecture write every packet, then stop once. Implementation `MOVE_DONE` commits product git (no ticket ACK). Migrate via `env --approve` when Compose is up. INFORM open HQ LOs. |
| Cadence review | **You** | After an implementation phase, when the counter is due, and after `ship --to dev` if needed: try shipped UI → `./studio review <p> --approve` |
| After review | **You** + agent | Feedback → clarify → ticket for the next cycle; reuse inform; retro → train |
| Milestone done | **You** | Approve milestone complete before next milestone backlog |

| Step | Command |
|------|---------|
| Propose scope | `./studio sprint <p>` |
| Approve scope | `./studio sprint <p> --approve-scope` (agent-owned) |
| Run the sprint | `./studio execute <p>` (loop until HITL) |
| Push `dev` before review | `./studio ship <p> --to dev` |
| Production / `main` | `./studio ship <p> --to main --approve` (**HITL**) |
| Status brief | `./studio review <p>` |
| Your feedback | `./studio feedback <p> "..."`  or  `./studio note <p> "..."` mid-sprint |
| Clarify → ticket | `./studio clarify <p> FB-001 ... --approve` → `./studio ticket <p> "..." --from-feedback FB-001` |
| Approve cadence review | `./studio review <p> --approve` |
| Reuse brief | `./studio reuse <p>` (inform only — no `--approve`) |
| Retro | `./studio retro <p>` → fill `retro.md` → `./studio retro <p> --complete` (**auto-harvests** LOs) |
| Capture studio gaps | Immediate: `./studio learn`, 3rd gate fail, reuse scan, retro `--complete`. Then `./studio train` beside execute |
| Infusion | `./studio infusion` lists LOs; product IMPLEMENT is not blocked |
| Groom + next sprint | `./studio groom <p>` · `./studio sprint <p>` |

When an implementation sprint is `done` and cadence is **not** due, `./studio execute` continues to retro. Cadence HITL is every `cost.human_review_every_sprints` implementation sprints. Backend-only sprints inform and continue to retro.

## Studio infusion (dual loop)

See **[Learnings: harvest when identified](#learnings-harvest-when-identified)** above. Summary:

```
learning identified → harvest (inbox + classified LO)
→ product: ./studio execute  → ACTION IMPLEMENT
→ train:   ./studio train SO-001 --from mistake --topic "…"
```

`./studio retro --complete` and `./studio reuse` harvest automatically. After **3** red gates on the same ticket, `./studio gate` auto-harvests an LO (`signal: gate-fail`). Debug notes live in `sprints/SPRINT-NN/debug/<ticket>.md`.

| Kind | Infuse into |
|------|-------------|
| `ui-component` / `package` | `studio-library/` (LO + generalize — no project UI copy) |
| `design` / `layout` / `ux` / `ia` / `usability` | matching `knowledge-base/` playbooks |
| `frontend` / `backend` / `database` / `security` | playbooks / PE–BE skills |
| `process` | `process/` |
| `tooling` | `studio-tools/` |

Full loop: [learning-loop.md](process/learning-loop.md) · [studio-abstraction.md](process/studio-abstraction.md)

## Studio-only improvements

Use **LO-*** tickets in `.quinsy-studio/backlog/` — not project code. Studio docs must stay **project-agnostic** (`<project>`, not a client codename). Product-only incidents belong in the project (`docs/studio-learnings-local.md`), not the HQ backlog.

```bash
./studio learn "..." --signal design-gap --source <project>
./studio learn-list
./studio verify-abstraction
./studio infusion   # lists open LOs; does not block product IMPLEMENT
```

Recent studio sprint: [sprints/STUDIO-SPRINT-01/README.md](sprints/STUDIO-SPRINT-01/README.md) · Changelog: [CHANGELOG.md](CHANGELOG.md)
