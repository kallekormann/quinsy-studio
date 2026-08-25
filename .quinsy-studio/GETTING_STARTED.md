# Quinsy Studio — Getting Started

> Canonical workflow: intake → architecture → design → implementation.  
> Root overview: [`README.md`](../README.md) · Agent: [`AGENTS.md`](../AGENTS.md)

## Start here: PRD in `intake/` → tell the agent

**You do not run a long CLI chain by hand.** Drop a PRD, open Cursor, and talk to the agent. It runs `./studio` for you; you **approve gates** and **product decisions**.

### 1. Add your PRD (local only — `intake/` is gitignored)

```bash
cp .quinsy-studio/studio-templates/prd_template.md intake/my-project.md
# Edit intake/my-project.md — use a slug that matches the project name (e.g. nudge.md → project "nudge")
```

Or copy an existing PRD: `intake/nudge.md` → project `nudge`.

### 2. Open the repo in Cursor

Clone/open **quinsy-studio** (repo root, not `projects/<name>/` alone). Rules load from [`.cursor/rules/quinsy-studio.mdc`](../.cursor/rules/quinsy-studio.mdc).

### 3. First message to the agent

Pick one:

| Situation | What you say |
|-----------|----------------|
| **New project** | *"I added `intake/my-project.md`. Bootstrap my-project and walk me through the next human gate."* |
| **Same session, continue** | *"Focus my-project and resume — what's next?"* |
| **Returning later** | *"Resume my-project. Back on track."* |

The agent should run:

```bash
./studio install                    # once after clone (Tailwind + Headless UI)
./studio verify-worlds
./studio verify-abstraction         # studio HQ must not hard-code client project names
./studio bootstrap my-project    # or intake if already bootstrapped
./studio focus my-project
./studio resume my-project
```

Then it does **only** what `resume` lists — usually filling artifacts until **you** approve a gate.

### 4. End-to-end: example conversation (project `nudge`)

| Phase | You say | Agent does | You approve |
|-------|---------|------------|-------------|
| **Intake** | *"Bootstrap nudge from intake/nudge.md"* | `./studio bootstrap nudge` → fills `docs/definitions/` | *"Gate 0 looks good — approve"* → `./studio approve nudge --gate 0` |
| **Architecture** | *"Continue with blueprint"* | `./studio blueprint nudge` → architecture + ADRs | *"Approve gate 1"* |
| **Design** | *"Design core views only"* | `./studio design nudge --scope core-views` → prototype + sticker sheet | *"Approve gate 2"* → library promotion |
| **Milestones** | *"Draft the milestone roadmap"* | Fills `docs/phases/` (M0, M1, …) | *"Approve milestones"* → agent writes M0 tickets |
| **Sprint** | *"Start the sprint and implement the first ticket"* | `./studio sprint nudge` → `--approve-scope`, library pull, `./studio move … implement` | Review scope proposal; groom |
| **Sprint review** | *"Give me a sprint review"* | `./studio review nudge` | *"Shipped looks good"* → `--approve` → reuse → retro → infusion → next sprint |
| **New idea** | *"I want offline mode"* | `./studio feedback nudge "…"` → clarify with you → ticket | Confirm clarified ticket before implement |

**Sprint feedback** = small, concrete ideas. **Amendments** = strategic direction (vision brief → milestone + ticket breakdown). See [Amendment intake](#amendment-intake-strategic-direction) below.

**No product implementation before gate 2.** After gate 2, approve the **milestone roadmap** before sprints; tickets populate per active milestone (M0, M1, …).

---

## Talk to the agent — prompt cheat sheet

Use natural language. The agent maps your intent to `./studio` commands.

### Starting & continuing

| You want | Example message |
|----------|-----------------|
| New project from PRD | *"Bootstrap &lt;project&gt; from intake/&lt;project&gt;.md"* |
| Set context | *"Focus &lt;project&gt;"* |
| What's next? | *"Resume &lt;project&gt;"* / *"What should we do next?"* |
| Recover from drift | *"Back on track"* / *"Resume project — only the next step"* |
| Project status | *"What's the status of &lt;project&gt;?"* → `./studio status` + `./studio board` |

### Human gates (you must approve)

| Gate | You say when ready | You say when not ready |
|------|--------------------|-------------------------|
| **0** PRD + definitions | *"Approve gate 0"* | *"Revise gate 0: personas need more detail on …"* |
| **1** Architecture | *"Approve gate 1"* | *"Revise gate 1: use IndexedDB only, no Supabase yet"* |
| **2** Design + mocks | *"Approve gate 2"* / *"Approve design"* | *"Revise gate 2: sticker sheet missing dark mode"* |
| **Milestones** | *"Approve milestones"* / *"Roadmap looks good"* | *"Revise M0 scope: defer legal pages to M1"* |

Agent runs `./studio approve` or `./studio revise --gate N --feedback "..."`. Milestone roadmap lives in `docs/phases/` — see [milestone-planning.md](process/milestone-planning.md).

### Milestone planning (after gate 2)

| You want | Example message |
|----------|-----------------|
| Draft roadmap | *"Draft milestone roadmap for &lt;project&gt; from the PRD"* |
| Approve roadmap | *"Approve milestones"* → `./studio approve &lt;p&gt; --milestones` |
| Start M0 work | *"Write M0 tickets and plan the first sprint"* |
| Milestone complete | *"M0 is done — milestone review"* (before M1 tickets) |

### Design scope (gate 2)

| You want | Example message |
|----------|-----------------|
| Key screens only | *"Design &lt;project&gt; with scope core-views"* |
| Full user journey | *"Design &lt;project&gt; with scope journey"* |

### Implementation (after milestones approved)

| You want | Example message |
|----------|-----------------|
| Propose sprint scope | *"Plan the next sprint"* → `./studio sprint &lt;p&gt;` → review `scope-proposal.md` |
| Approve sprint scope | *"Approve sprint scope"* → `./studio sprint &lt;p&gt; --approve-scope` |
| Start sprint | *"Groom and implement the first ticket"* |
| Work a ticket | *"Implement NUDG-0003"* (agent: design spec if UI → `approve-design` → library pull → move implement) |
| Finish ticket | *"Mark NUDG-0003 done if DoD is met"* |
| Off-sprint idea | *"Can we add X?"* → agent should **not** code silently; uses guard → feedback or ticket |

### Sprint review & feedback (human in the loop)

| You want | Example message |
|----------|-----------------|
| Review shipped work | *"Sprint review for &lt;project&gt;"* |
| Approve sprint | *"Sprint looks good — approve review"* |
| Raw product feedback | *"Feedback: users need offline habits"* (→ `./studio feedback`, **not** a direct ticket) |
| Prioritize backlog | *"Run grooming"* |
| Retro | *"Run retro for this sprint"* → fill retro → `./studio retro <p> --complete` → `./studio infusion` |

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
| Log studio gap | *"Log a tooling gap: …"* → `./studio learn` |
| Infusion gate (LO backlog) | `./studio infusion` — blocks next project sprint while LO-* open |
| Check studio docs are generic | `./studio verify-abstraction` |
| Check if request is in scope | *"Is this in scope for nudge: …?"* → `./studio guard` |

### What the agent should **not** do without you

- Skip gates 0–2 and write product code
- Create tickets directly from sprint-review chat (must: feedback → clarify → ticket)
- Commit `projects/` to the studio repo
- Implement features with no backlog ticket (after gate 2)

---

## Crucial commands (reference)

You can run these yourself; in Cursor the agent usually runs them for you.

| When | Command |
|------|---------|
| **After git clone** | `./studio install` · optional `./studio install --with-skills` |
| Session start | `./studio verify-worlds` · `./studio verify-abstraction` · `./studio focus <p>` · `./studio resume <p>` |
| New project from PRD | `./studio bootstrap <p>` |
| Approve / revise gate | `./studio approve <p> --gate 0\|1\|2` · `./studio revise <p> --gate N --feedback "..."` |
| UI design HITL | `./studio approve-design <p> <TICKET-ID>` (after Team 10 spec with §2 placement) |
| Milestones | `./studio approve <p> --milestones` (after `docs/phases/` drafted) |
| Architecture | `./studio blueprint <p>` |
| Design | `./studio design <p> --scope journey\|core-views` |
| Status / board | `./studio status <p>` · `./studio board <p>` |
| Sprint | `./studio sprint <p>` · `./studio sprint <p> --approve-scope` · `./studio move <p> <ID> implement` · `./studio move <p> <ID> done` |
| Library-first | `./studio library suggest <p> "auth billing"` · `./studio library pull <p> …` |
| Sprint review | `./studio review <p>` · `./studio review <p> --approve` |
| Your feedback → backlog | `./studio feedback <p> "..."` · `./studio clarify <p> FB-001 --approve` · `./studio ticket <p> "..." --from-feedback FB-001` |
| Amendment intake | `./studio amend <p> intake/amendments/<p>/amendment_NN.md` · `./studio amendments <p>` · `./studio approve <p> --amendment AM-001` |
| Groom / retro / infusion | `./studio groom <p>` · `./studio retro <p>` · `./studio retro <p> --complete` · `./studio infusion` |
| Studio learnings | `./studio learn "..." --signal <s>` · `./studio learn-list` |
| Scope check | `./studio guard <p> "your request text"` |

---

## Using Quinsy Studio in Cursor

1. Open the **quinsy-studio** repo in Cursor (not a project subfolder alone).
2. Cursor loads [`.cursor/rules/quinsy-studio.mdc`](../.cursor/rules/quinsy-studio.mdc) automatically.
3. Start each session:

```bash
./studio verify-worlds
./studio verify-abstraction
./studio focus <project>
./studio resume <project>
```

4. Talk to the agent in plain language — e.g. *"Bootstrap nudge"*, *"Resume nudge"*, *"Approve gate 0"*. The agent runs `./studio` commands; you approve gates and product decisions.

5. **Two repos in one workspace:** studio commits from root; project code commits from `projects/<name>/` (separate `.git`). Never `git add projects/` from the studio root. Studio docs use `<project>` placeholders — see [studio-abstraction.md](process/studio-abstraction.md).

Details: [Operations manual — Using Cursor](README.md#4-using-quinsy-studio-in-cursor) · [agent-context](process/agent-context.md)

## Session ritual (IDE + agent)

```bash
./studio install                 # once after git clone
./studio verify-worlds
./studio verify-abstraction
./studio focus <project>
./studio resume <project>
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

| Gate | You approve | CLI |
|------|-------------|-----|
| **0** | PRD + definitions | `./studio approve <p> --gate 0` |
| **1** | Architecture blueprint + ADRs | `./studio approve <p> --gate 1` |
| **2** | Design + Next.js mocks + sticker sheet | `./studio approve <p> --gate 2` |

Gate 2 promotes design artifacts to [studio-library](studio-library/library_registry.md). **Tickets** are written for the **active milestone** after you approve the roadmap (`./studio approve <p> --milestones`).

## Milestone roadmap (before first sprint)

1. Agent drafts `docs/phases/README.md` + M0/M1 outlines from PRD + blueprint
2. You approve: `./studio approve <p> --milestones`
3. Agent writes **M0 tickets only** → product backlog (`backlog/*.md`, `milestone: M0`)
4. Sprint planning: `./studio sprint <p>` → you `--approve-scope` → groom → implement

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

## AI-driven bootstrap

1. Drop PRD in [`intake/`](../intake/) (gitignored — local only)
2. Tell the agent: **"Bootstrap &lt;project&gt;"**
3. Approve each gate when artifacts are ready
4. At design: choose `--scope journey` (full flow) or `--scope core-views` (key screens)

```bash
./studio bootstrap my-project
./studio approve my-project --gate 0
./studio blueprint my-project && ./studio approve my-project --gate 1
./studio design my-project --scope core-views
./studio approve my-project --gate 2
./studio approve my-project --milestones
./studio sprint my-project
./studio sprint my-project --approve-scope
./studio groom my-project --approve
./studio move my-project MY-0001 implement
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
| Before coding | `./studio library suggest <p> "billing auth button"` |
| Pull boilerplate | `./studio library pull <p> auth billing button tokens` |
| Promote code | `./studio library promote <p> packages/billing [--force] [--ticket ID]` |
| Promote design | `./studio promote-library <p> [--force]` |

On `./studio move <p> <ID> implement` → library hint.  
On `./studio move … done` → warns if registry paths changed without promotion.

## Project artifacts (all under `projects/<p>/`)

| Artifact | Path |
|----------|------|
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
| Library pull log | `docs/library-usage.json` |
| Library promote log | `docs/library-promotions.json` |

Run prototype: `cd projects/<p>/design/prototype && npm install && npm run dev`

## Agent hardening

| Concern | Doc / command |
|---------|----------------|
| Scope & drift | [process/agent-context.md](process/agent-context.md) |
| Two git worlds | [process/worlds.md](process/worlds.md) · `./studio verify-worlds` |
| Studio HQ generic docs | [process/studio-abstraction.md](process/studio-abstraction.md) · `./studio verify-abstraction` |
| Learning loop + infusion gate | [process/learning-loop.md](process/learning-loop.md) · `./studio infusion` |
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

On `./studio move … done` → warns if registry paths changed without promotion.

## Sprint cadence (human in the loop)

After the **milestone roadmap** is approved, the **agent runs each sprint autonomously**; you join at **sprint scope approval** and **sprint review**. Ideas do **not** become tickets blindly.

| Phase | Who | What |
|-------|-----|------|
| Sprint scope | **You** | Review `scope-proposal.md` → `./studio sprint <p> --approve-scope` |
| Mid-sprint | Agent | Implements all groomed sprint tickets — no "should I continue?" between tickets |
| Sprint review | **You** | Try shipped work; approve or reject |
| Milestone done | **You** | Approve milestone complete before next milestone backlog |
| After review | **You** + agent | Feedback → clarify → ticket; retro → **infuse LO-***; plan next sprint |

| Step | Command |
|------|---------|
| Propose scope | `./studio sprint <p>` (blocked while open LO-* — run `./studio infusion` first) |
| Approve scope | `./studio sprint <p> --approve-scope` |
| Status brief | `./studio review <p>` |
| Your feedback | `./studio feedback <p> "..."` |
| Clarify → ticket | `./studio clarify <p> FB-001 ... --approve` → `./studio ticket <p> "..." --from-feedback FB-001` |
| Approve sprint | `./studio review <p> --approve` |
| Reuse review | `./studio reuse <p> --approve` |
| Retro | `./studio retro <p>` → fill `retro.md` → `./studio retro <p> --complete` |
| Capture studio gaps | `./studio learn "..." --signal process-gap --source <p>` |
| Infusion gate | `./studio infusion` (must pass before next `./studio sprint`) |
| Groom + next sprint | `./studio groom <p>` · `./studio sprint <p>` · `./studio groom <p> --approve` |

When all sprint tickets are `done`, `./studio resume` shows **sprint review pending** and blocks further implementation until you approve.

## Studio infusion gate (dual loop)

Sprint review learnings must **infuse into studio HQ** before the next project sprint — not linger as open LO-* tickets.

```
review --approve → reuse --approve
→ retro (fill) → retro --complete
→ ./studio learn (if new signals)
→ implement LO-* in .quinsy-studio/
→ ./studio infusion   ← must be green
→ ./studio sprint <p>
```

| Signal | Infuse into |
|--------|-------------|
| `design-gap` | `knowledge-base/`, UX skills, design-spec template |
| `process-gap` | `process/`, HITL docs |
| `tooling-gap` | `studio-tools/`, CLI |
| `library-gap` | `studio-library/` (+ promote from project) |

Full loop: [learning-loop.md](process/learning-loop.md) · [studio-abstraction.md](process/studio-abstraction.md)

## Studio-only improvements

Use **LO-*** tickets in `.quinsy-studio/backlog/` — not project code. Studio docs must stay **project-agnostic** (`<project>`, not a client codename).

```bash
./studio learn "..." --signal design-gap --source <project>
./studio learn-list
./studio verify-abstraction
./studio infusion   # must be green before next project sprint
```

Recent studio sprint: [sprints/STUDIO-SPRINT-01/README.md](sprints/STUDIO-SPRINT-01/README.md) · Changelog: [CHANGELOG.md](CHANGELOG.md)
