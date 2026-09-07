# Quinsy Studio — Getting Started

> Canonical workflow: **new product** (PRD → **architecture HITL** → **design-track HITL**) **or existing codebase** (`./studio adopt` → as-built) → **execute loop** (implement until HITL; train LOs in parallel) → UI sprint review.  
> Root overview: [`README.md`](../README.md) · Agent: [`AGENTS.md`](../AGENTS.md) · Operations: [`README.md`](README.md)

**How the studio runs:** the agent does **not** wait for “continue.” It runs `./studio execute <project>`, does the `NEXT` command, then execute again, until `ACTION` is `HITL` (you). Start of a project is HITL at **gate 0 (PRD)** → **gate 1 (architecture)** → **gate 2 (design track)**. After that, `INFORM` still loops. Open learnings spawn `./studio train` beside product work — they do **not** replace the next `IMPLEMENT`. Markdown tickets stay the source of truth; the agent loads a **compact card** (skills + playbooks), not the whole backlog.

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

### Track B — Existing codebase (adopt)

Do **not** run `./studio bootstrap` / `init` on a live tree — that scaffolds an empty app. Hand over:

1. The repo (git URL or folder)
2. How to run it (README / env). Secrets stay in `.env`
3. Optional intent: copy [adopt_intent.md](studio-templates/adopt_intent.md) → `intake/<slug>.md`

```bash
./studio adopt my-project --from /path/to/repo   # or https://github.com/org/repo.git
./studio focus my-project
./studio execute my-project   # fill as-built → synthesize PRD → HITL gate 0
```

The agent reconstructs **implementation state in depth** (`docs/as-built/`, cite file paths). Then: as-is architecture (gate 1) → design of what exists (gate 2, **no fake prototype**) → milestone plan from the gap matrix → execute loop.

Full process: [brownfield-adopt.md](process/brownfield-adopt.md)

### End-to-end: example conversation

**Existing repo** (adopt) and **new product** (bootstrap) are alternatives for the first HITL — not sequential steps.

| Phase | You say | Agent does | You approve |
|-------|---------|------------|-------------|
| **Adopt** | *"Adopt my-project from this folder and reconstruct as-built"* | `./studio adopt` → fills `docs/as-built/` + PRD | *"This is what we have — approve gate 0"* |
| **or new product** | *"Bootstrap my-project from intake/my-project.md"* | `./studio bootstrap` → fills `docs/definitions/` | *"Gate 0 looks good — approve"* |
| **Architecture** | *"Continue with blueprint"* | `./studio blueprint` | *"Approve gate 1"* (core stack decision) |
| **Design** | *"Design core views"* / stills or clickable prototype | `./studio design` + Team 10 iteration | *"Approve gate 2"* |
| **Sprint** | *"Let the sprint run"* | agent `--approve-scope` → groom → **`./studio execute` loop** | Override scope if you want; stay out until UI review |
| **Milestones** | *"Draft the milestone roadmap"* | Fills `docs/phases/` from gap matrix or PRD | *"Approve milestones"* → agent writes M0 tickets |
| **Sprint review** | *"Give me a sprint review"* | `./studio review` | UI: *"Shipped looks good"* → `--approve`. Backend: inform → retro |
| **New idea** | *"I want offline mode"* | `./studio feedback "…"` → clarify → ticket | Confirm clarified ticket before the **next** sprint |

**Sprint feedback** = small, concrete ideas. **Amendments** = strategic direction (vision brief → milestone + ticket breakdown). See [Amendment intake](#amendment-intake-strategic-direction) below.

**No product IMPLEMENT until gates 0–2 are approved.** After PRD, you approve architecture, then iterate on the design track (direction, design system, stills/mocks or clickable prototype) until gate 2. During later sprints, design-track tickets still need `./studio approve-design`.

---

## The execute loop (how work actually proceeds)

`./studio execute` drives the whole loop: gates 0–2 (produce artifacts, then **HITL**), then sprints. After sprint **scope** and **groom** (agent-owned; you may override), the agent’s job is:

```
./studio focus <project>
./studio execute <project>     → do the NEXT command
./studio execute <project>     → again
… until ACTION is HITL         → stop and wait for you
         INFORM still loops    → do NEXT, execute again
         TRAIN sidecar         → product IMPLEMENT continues
```

Do **not** ask “should I continue?” between tickets. `resume` is optional background; **execute** is the driver.

### What `./studio execute` can return

| ACTION | Meaning | Who |
|--------|---------|-----|
| `IMPLEMENT` / `IMPLEMENT <id>` | Adopt: fill `docs/as-built/`. Pre-impl: `./studio blueprint` or `./studio design`. Sprint: next unblocked ticket — read the **CARD** (and that one `.md` only) | Agent |
| `VERIFY` | Adopt: synthesize `docs/intake/prd.md`. Sprint: fill the **execution receipt** (`./studio receipt`) | Agent |
| `GATE` | Run `./studio gate <p> --level 5` (build + smoke + tests). Must be **fresh** after this ticket’s implement | Agent |
| `DEBUG` | Gate went red. Write hypotheses in `sprints/SPRINT-NN/debug/<id>.md`, fix, re-gate (max 3 tries) | Agent |
| `MOVE_DONE` | Receipt + gate 5 green → `move … done`, then execute again | Agent |
| `STUDIO_LO <id>` | Idle infusion in `.quinsy-studio/` when there is no ready IMPLEMENT. Mid-sprint: TRAIN sidecar instead | Agent |
| `INFORM` | Reuse brief / inbox drain — do NEXT, loop; **not** architecture or design. **`cost-cap`:** stop; raise the named key | Agent or **you** |
| `HITL` | **Stop.** Gate 0, gate 1 architecture, gate 2 design track, design-approve, UI sprint review, tech-veto, abort, or retries exhausted | **You** |

**What execute picks (in order):**

1. **Adopt as-built** — if `mode: adopt` and `docs/as-built/` still has `_TODO_`, `IMPLEMENT` those files (cite paths). Then `VERIFY` the synthesized PRD
2. **HITL gate 0** — PRD / as-built confirm
3. **Architecture (gate 1)** — `IMPLEMENT` `./studio blueprint` until artifacts are ready, then **HITL** `./studio approve --gate 1`
4. **Design track (gate 2)** — after architecture, `IMPLEMENT` `./studio design` (direction, design system, stills/mocks or clickable prototype), then **HITL** `./studio approve --gate 2`. Iterate with `./studio revise --gate 2`
5. **Finish in-progress** — a ticket already in `implement` still runs VERIFY → GATE → DEBUG → MOVE_DONE (inbox notes wait)
6. **`IMPLEMENT`** — next unblocked sprint ticket. Design-track tickets still need `approve-design`. Open LOs → `TRAIN` sidecar, not `STUDIO_LO`
7. **`STUDIO_LO`** — only when idle (no ready product ticket)

```bash
./studio execute <project>           # human-readable
./studio execute <project> --json    # machine-readable (scripts / automations)
./studio ticket-card <project> <ID>  # compact card only (~AC, files, deps)
./studio receipt <project> <ID>      # scaffold receipt before done
./studio health <project>            # state-graph: open LOs, missing receipts, deps
./studio settings                    # token policy + estimated usage
```

## Studio settings (cost / tokens)

Defaults in [studio.settings.yaml](studio.settings.yaml) are for a **medium project**. You should finish PRD → architecture → design → a normal sprint without hitting a cap. Intake, architecture, and design allow more estimated tokens than implement, reuse, or retro.

```bash
./studio settings
```

Copy [studio-templates/studio.settings.local.example.yaml](studio-templates/studio.settings.local.example.yaml) → `.quinsy-studio/studio.settings.local.yaml` (gitignored). Set `cost.profile` (`economy` ~0.5×, `standard`, `premium` ~2×) or raise one step, e.g. `cost.steps.design.context`. **No API keys** in that file.

Estimates are `chars/4` of the CARD and listed files — not the host invoice. `model_hint` is the main dollar control (Cursor / Claude / Gemini must honor it). Product Gemini keys in a project `.env` are not the coding agent.

If execute returns `INFORM cost-cap`, it names the yaml key (`cost.steps.design.context`, `cost.steps.implement.budget`, or `cost.session_token_budget`). Raise **that** key and execute again. At 80% the CARD warns and work continues.

**Tickets stay Markdown** in git (no SQL). Tokens are saved by **layered load**: execute shows a short card; the agent opens the full ticket file only on `IMPLEMENT`.

**New tickets** are compact: frontmatter is the machine record; body is Target, Scope, and specific AC. Boilerplate “gate 5 / anti-slop / tests” lives in process docs — not pasted on every ticket.

**Definition of done (enforced):** `move … done` requires QA **level 5** **and** a filled receipt (`Plan`, `AC coverage`, `Default flow`). Visible UX tickets must walk the **default product path** (not a test-only toggle).

---

## Learnings: harvest when identified

Studio HQ must learn **in the same session** the gap appears. If LOs pile until a human runs `./studio learn` or until the next sprint, the originating context is gone and the next project repeats the mistake.

| When identified | What happens (no extra human trigger) |
|-----------------|----------------------------------------|
| You or the agent log a gap | `./studio learn "…"` → classified LO + inbox line |
| Retro `--complete` | “Went badly” / “improve” bullets become LOs |
| Reuse review | Unpromoted `packages/` / `ui/components/` become LOs (not a raw copy of project UI) |
| 3rd red gate on a ticket | Auto-LO (`signal: gate-fail`) |

Each harvest **classifies** the learning, appends [knowledge-base/learnings/inbox.md](knowledge-base/learnings/inbox.md), and opens a compact LO. Product `./studio execute` **continues IMPLEMENT**. Infusion is `./studio train` in parallel (or `STUDIO_LO` when idle).

The agent **generalizes** into that path (playbook, process, tooling, or library asset). It does **not** merge project tokens or UI into `studio-library/`.

```
learning identified → inbox + classified LO
→ product: ./studio execute  → ACTION IMPLEMENT
→ train:   ./studio train SO-001 --from mistake --topic "…"
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

### Human gates (you must approve)

| Gate | You say when ready | You say when not ready |
|------|--------------------|-------------------------|
| **0** PRD + definitions **or** as-built (adopt) | *"Approve gate 0"* | *"Revise gate 0: …"* |
| **1** Architecture (as-is on adopt) | *"Approve gate 1"* | *"Revise gate 1: use IndexedDB only, no Supabase yet"* |
| **2** Design direction + system + mocks/prototype | *"Approve gate 2"* / *"Approve design"* | *"Revise gate 2: …"* |
| **Milestones** | *"Approve milestones"* / *"Roadmap looks good"* | *"Revise M0 scope: defer legal pages to M1"* |

Agent runs `./studio approve` or `./studio revise --gate N --feedback "..."`. Milestone roadmap lives in `docs/phases/` — see [milestone-planning.md](process/milestone-planning.md).

### Milestone planning (after gate 2)

| You want | Example message |
|----------|-----------------|
| Draft roadmap | *"Draft milestone roadmap for &lt;project&gt;"* (from PRD **or** as-built gap matrix) |
| Approve roadmap | *"Approve milestones"* → `./studio approve &lt;p&gt; --milestones` |
| Start M0 work | *"Write M0 tickets and plan the first sprint"* |
| Milestone complete | *"M0 is done — milestone review"* (before M1 tickets) |

### Design scope (gate 2)

| You want | Example message |
|----------|-----------------|
| Key screens only | *"Design &lt;project&gt; with scope core-views"* |
| Full user journey | *"Design &lt;project&gt; with scope journey"* |
| Existing product (adopt) | *"Map the existing UI — do not scaffold a prototype"* |

### Implementation (after milestones approved)

| You want | Example message |
|----------|-----------------|
| Propose sprint scope | *"Plan the next sprint"* → `./studio sprint &lt;p&gt;` → agent `--approve-scope` (you may override) |
| Let the sprint run | *"Execute until HITL"* — agent loops tickets; open LOs train in parallel; you join at UI review |
| Compact ticket view | *"Show the card for &lt;ID&gt;"* → `./studio ticket-card` |
| Work a ticket | Agent follows execute: design spec if UI → `approve-design` → library pull → implement → receipt → gate 5 → done |
| Finish ticket | Receipt + `./studio gate --level 5` must be green; then `move … done` |
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

### UI design (Team 10, after gate 2)

| You want | Example message |
|----------|-----------------|
| Design spec for UI ticket | *"Write design spec for &lt;TICKET&gt; — include context and placement"* |
| Approve design (HITL) | *"Approve design for &lt;TICKET&gt;"* → `./studio approve-design <p> <TICKET>` |
| Cross-surface move | *"Create ia-feature-placement ticket: move X to Y surface"* |
| Layout-only concern | Agent should ask: *"Is placement correct before we widen the dialog?"* |

**Order:** placement → workflow map → atomic inventory → visual polish. Spec template: [design-spec-template.md](knowledge-base/design-spec-template.md). Playbooks: [contextual-ia](knowledge-base/contextual-ia-playbook.md) · [workflow-definition](knowledge-base/workflow-definition-playbook.md) · [design-system compliance](knowledge-base/design-system-compliance-checklist.md).

### Studio / process (not project code)

| You want | Example message |
|----------|-----------------|
| Log studio gap | *"Log a tooling gap: …"* → `./studio learn` then `./studio train` (also auto on retro/reuse/gate-fail) |
| Infusion | `./studio infusion` lists open LOs (does not block IMPLEMENT). `./studio train` infuses in parallel |
| Check studio docs are generic | `./studio verify-abstraction` |
| Check if request is in scope | *"Is this in scope for &lt;project&gt;: …?"* → `./studio guard` |

### What the agent should **not** do without you

- Skip gates 0–2 and write product code (architecture and design track are HITL after PRD)
- Run `./studio init` / `bootstrap` on a live codebase (use `./studio adopt`)
- Skip architecture or design HITL (`inform --gate 1` does **not** approve architecture)
- Implement sprint-review **design** feedback in the same cycle (must: feedback → clarify → next sprint)
- Create tickets directly from sprint-review chat
- Commit `projects/` to the studio repo
- Implement features with no backlog ticket (after gate 2)
- Dump the whole backlog into context (use `ticket-card` / execute CARD)
- Pull library **stubs** (`billing`, `feature-gating`) — build in-project, then promote a working generic
- Leave open LO-* piled for a later human `learn` prompt — harvest immediately; `./studio train` in parallel
- Treat a mid-execute chat message as a new assignment. Run `./studio guard <p> "<verbatim>"` first. On `INBOX_ACK`, resume the current ACTION. `FEEDBACK_ONLY` / `NEEDS_TICKET` must not preempt an in-flight ticket.
- Keep stuffing files after `INFORM cost-cap` — wait for the named key to be raised in `studio.settings.local.yaml`

---

## Crucial commands (reference)

You can run these yourself; in Cursor the agent usually runs them for you.

| When | Command |
|------|---------|
| **After git clone** | `./studio install` · optional `./studio install --with-skills` |
| Session start | `./studio verify-worlds` · `./studio verify-abstraction` · `./studio settings` · `./studio focus <p>` · **`./studio execute <p>`** |
| Checklist | `./studio resume <p>` (optional; execute is the driver) |
| New project from PRD | `./studio bootstrap <p>` |
| Existing codebase | `./studio adopt <p> --from <git-url-or-path> [--intent intake/<p>.md]` |
| Approve / revise gate | `./studio approve <p> --gate 0\|1\|2` · `./studio revise <p> --gate N --feedback "..."` |
| UI design HITL | `./studio approve-design <p> <TICKET-ID>` (after Team 10 spec with §2 placement) |
| Milestones | `./studio approve <p> --milestones` (after `docs/phases/` drafted) |
| Architecture | `./studio blueprint <p>` |
| Design | `./studio design <p> --scope journey\|core-views` |
| Status / board / health | `./studio status <p>` · `./studio board <p>` · `./studio health <p>` |
| Sprint | `./studio sprint <p>` · `--approve-scope` (agent-owned) · `./studio execute <p>` (loop) · `./studio move <p> <ID> implement\|done` |
| Ticket card / receipt | `./studio ticket-card <p> <ID>` · `./studio receipt <p> <ID>` |
| Mid-execute chat | `./studio guard <p> "…"` → `INBOX_ACK` (queued). Drain: `./studio note <p> --drain` |
| Library-first | `./studio library suggest <p> "auth button"` · `./studio library pull <p> auth tokens button` (not stubs) |
| Sprint review | `./studio review <p>` · `./studio review <p> --approve` |
| Your feedback → backlog | `./studio feedback <p> "..."` · `./studio clarify <p> FB-001 --approve` · `./studio ticket <p> "..." --from-feedback FB-001` |
| Amendment intake | `./studio amend <p> intake/amendments/<p>/amendment_NN.md` · `./studio amendments <p>` · `./studio approve <p> --amendment AM-001` |
| Groom / retro / train | `./studio groom <p>` · `./studio retro <p> --complete` (auto-harvest) · `./studio train SO-001 --from mistake --topic "…"` · `./studio infusion` |
| Studio learnings | `./studio learn "..." --signal <s>` (harvests immediately) · `./studio learn-list` · then train beside execute |
| Cost / tokens | `./studio settings` · `./studio settings --reset-usage` · local override `studio.settings.local.yaml` |
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

4. Talk to the agent in plain language — e.g. *"Bootstrap my-project"*, *"Adopt my-project from this repo"*, *"Execute my-project"*, *"Approve gate 0 / 1 / 2"*. The agent runs `./studio` commands; you approve HITL stops.

5. **Two repos in one workspace:** studio commits from root; project code commits from `projects/<name>/` (separate `.git`). Never `git add projects/` from the studio root. Studio docs use `<project>` placeholders — see [studio-abstraction.md](process/studio-abstraction.md).

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

17 visual direction presets for UI design specs (e.g. `stripe-like-ui`, `apple-like-ui`, `soft-ui`):

- Catalog: [knowledge-base/aesthetic-presets/README.md](knowledge-base/aesthetic-presets/README.md)
- Team skill: [teams/10-product-design-experience/skills/aesthetic-presets.md](teams/10-product-design-experience/skills/aesthetic-presets.md)

Every UI design spec must declare one primary preset (or `project-brand-only`). UX-005 loads the preset `SKILL.md` alongside project tokens.

## UI design discipline (placement before layout)

When complexity grows, avoid "layout-first" tickets that polish the wrong surface.

| Step | Doc / command |
|------|----------------|
| 1. Where does this live? | [contextual-ia-playbook.md](knowledge-base/contextual-ia-playbook.md) — surface map, `ia-feature-placement` |
| 2. End-to-end flow | [workflow-definition-playbook.md](knowledge-base/workflow-definition-playbook.md) |
| 3. Design spec | [design-spec-template.md](knowledge-base/design-spec-template.md) — **§2 Context & placement** required |
| 4. Library + tokens | [design-system-compliance-checklist.md](knowledge-base/design-system-compliance-checklist.md) |
| 5. Human gate | `./studio approve-design <p> <TICKET>` |
| 6. Implement | `./studio library pull` → `./studio move … implement` |

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

## Three human gates (before coding)

These are the **core start-of-project decisions**. Execute produces the artifacts, then **stops for you**.

| Gate | You approve | CLI |
|------|-------------|-----|
| **0** | PRD + definitions **or** as-built truth + synthesized PRD (adopt) | `./studio approve <p> --gate 0` |
| **1** | Architecture + ADRs after PRD (as-is on adopt; no stack swap unless you asked) | `./studio blueprint` then `./studio approve <p> --gate 1` |
| **2** | Design track after architecture: direction, design system, stills/mocks **or** clickable prototype (adopt: design of what exists — no fake prototype) | `./studio design` then `./studio approve <p> --gate 2`. Iterate: `./studio revise --gate 2` |

Gate 2 promotes design artifacts to [studio-library](studio-library/library_registry.md) on **greenfield** only. Adopted UI stays in the project; gaps become LOs. **No product IMPLEMENT until gates 0–2 are approved.** During later sprints, new UI tickets still need `./studio approve-design`.

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
./studio design my-project --scope core-views    # adopt: --scope as-built (no prototype)
./studio approve my-project --gate 2
./studio approve my-project --milestones
./studio sprint my-project
./studio sprint my-project --approve-scope
./studio groom my-project --approve
./studio execute my-project          # loop until HITL; train LOs in parallel
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

On `./studio move <p> <ID> implement` → library hint.  
On `./studio move … done` → requires gate level 5 **and** a filled execution receipt; warns if registry paths changed without promotion.

## Project artifacts (all under `projects/<p>/`)

| Artifact | Path |
|----------|------|
| As-built (adopt) | `docs/as-built/*.md` |
| PRD | `docs/intake/prd.md` |
| Definitions | `docs/definitions/` |
| Architecture | `docs/architecture/` |
| ADRs | `docs/adr/` |
| Design spec (per ticket) | `docs/design-specs/<TICKET>.md` |
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
| Library pull log | `docs/library-usage.json` |
| Library promote log | `docs/library-promotions.json` |

Run prototype: `cd projects/<p>/design/prototype && npm install && npm run dev`

## Agent hardening

| Concern | Doc / command |
|---------|----------------|
| Brownfield adopt | [process/brownfield-adopt.md](process/brownfield-adopt.md) · `./studio adopt` |
| Scope & drift | [process/agent-context.md](process/agent-context.md) |
| Two git worlds | [process/worlds.md](process/worlds.md) · `./studio verify-worlds` |
| Studio HQ generic docs | [process/studio-abstraction.md](process/studio-abstraction.md) · `./studio verify-abstraction` |
| Cost / token policy | [studio.settings.yaml](studio.settings.yaml) · `./studio settings` |
| Learning loop + infusion gate | [process/learning-loop.md](process/learning-loop.md) · [§ learnings](#learnings-harvest-when-identified) · `./studio infusion` |
| Feature placement (IA) | [knowledge-base/contextual-ia-playbook.md](knowledge-base/contextual-ia-playbook.md) |
| Off-sprint work | `./studio guard <p> "request"` |
| Ticket workflow | [process/ticket-workflow.md](process/ticket-workflow.md) |
| Team 10 allocation | [process/ticket-team-allocation.md](process/ticket-team-allocation.md) |

## External skills (optional)

Subscribe to best-in-class skill packages (design, marketing, gamedev, compliance):

```bash
./studio update-skills --list
./studio update-skills              # import all into .quinsy-studio/external-skills/
./studio update-skills design       # one domain only
```

To **add** a new source: edit `skill-dependencies.json` → `./studio update-skills <name>` → register in `teams/skill-registry.md`. Full guide: [Managing Skills](README.md#8-managing-skills).

On `./studio move … done` → requires gate 5 + receipt; warns if registry paths changed without promotion.

## Sprint cadence (human in the loop)

After gates **0–2** (PRD, architecture, design track) and the milestone roadmap, the **agent runs each sprint autonomously**; you join at **UI sprint review**, per-ticket `approve-design`, and rare tech-vetoes. Ideas do **not** become tickets blindly.

| Phase | Who | What |
|-------|-----|------|
| Sprint scope | **Agent** (you may override) | `./studio sprint <p> --approve-scope` |
| Mid-sprint | Agent | `./studio execute` until HITL — implements tickets; open LOs train in parallel |
| UI sprint review | **You** | Try shipped UI → `./studio review <p> --approve` |
| After review | **You** + agent | Feedback → clarify → ticket; reuse inform; retro → train / idle `STUDIO_LO` |
| Milestone done | **You** | Approve milestone complete before next milestone backlog |

| Step | Command |
|------|---------|
| Propose scope | `./studio sprint <p>` |
| Approve scope | `./studio sprint <p> --approve-scope` (agent-owned) |
| Run the sprint | `./studio execute <p>` (loop until HITL) |
| Status brief | `./studio review <p>` |
| Your feedback | `./studio feedback <p> "..."`  or  `./studio note <p> "..."` mid-sprint |
| Clarify → ticket | `./studio clarify <p> FB-001 ... --approve` → `./studio ticket <p> "..." --from-feedback FB-001` |
| Approve UI sprint | `./studio review <p> --approve` |
| Reuse brief | `./studio reuse <p>` (inform only — no `--approve`) |
| Retro | `./studio retro <p>` → fill `retro.md` → `./studio retro <p> --complete` (**auto-harvests** LOs) |
| Capture studio gaps | Immediate: `./studio learn`, 3rd gate fail, reuse scan, retro `--complete`. Then `./studio train` beside execute |
| Infusion | `./studio infusion` lists LOs; product IMPLEMENT is not blocked |
| Groom + next sprint | `./studio groom <p>` · `./studio sprint <p>` |

When all **UI** sprint tickets are `done`, `./studio execute` shows **HITL sprint-review**. Backend-only sprints inform and continue to retro.

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

Use **LO-*** tickets in `.quinsy-studio/backlog/` — not project code. Studio docs must stay **project-agnostic** (`<project>`, not a client codename).

```bash
./studio learn "..." --signal design-gap --source <project>
./studio learn-list
./studio verify-abstraction
./studio infusion   # lists open LOs; does not block product IMPLEMENT
```

Recent studio sprint: [sprints/STUDIO-SPRINT-01/README.md](sprints/STUDIO-SPRINT-01/README.md) · Changelog: [CHANGELOG.md](CHANGELOG.md)
