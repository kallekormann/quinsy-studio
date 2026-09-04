# Quinsy Studio — Human-in-the-Loop

> Some decisions are too important to leave to the agent alone.
> Human-in-the-loop ensures that irreversible actions receive human approval.

## Core principle

```
Agent: "I cannot decide this alone."
Human: "I decide."
Agent: "Implemented."
```

---

## When is HITL needed?

| Category | Actions | HITL? |
|----------|---------|-------|
| **Budget** | costs above X €/month | **Yes** |
| **Legal** | contracts, licenses, GDPR exceptions | **Yes** |
| **Irreversible** | deleting data, production deploy, DNS changes | **Yes** |
| **Security** | security exceptions, access rights | **Yes** |
| **Architecture** | large architecture changes | **Yes** |
| **Release** | production release | **Yes** |
| **Sprint review** | approve shipped sprint work | **Yes** |
| **Milestone roadmap** | approve version plan after gate 2 | **Yes** |
| **Milestone review** | approve completed product version (M0, M1, …) | **Yes** |
| **Sprint feedback** | new ideas from review → backlog | **Yes** (clarify before ticket) |
| **UI design spec** | new component / marketing / workflow UI | **Yes** (`./studio approve-design`) — requires §2 placement **and** §2c **in-context mocks** (AM-007) |
| **Feature** | new features (incremental, in sprint) | No (if ticket exists) |
| **Bugfix** | fixing bugs | No |
| **Docs** | documentation | No |

---

## Sprint cadence HITL (after gate 2 + milestone roadmap)

Pre-implementation uses gates 0–2 (`./studio approve`). **After gate 2**, the agent drafts a **milestone roadmap** (`docs/phases/`); the human approves it before tickets and sprints. **During sprints**, the agent executes autonomously; the human joins at **sprint review**, then helps plan the **next** sprint. **Between milestones**, the human approves milestone completion before the next milestone backlog is written.

See [milestone-planning.md](milestone-planning.md) for roadmap and milestone-review ceremony.

### Autonomous execution (mid-sprint)

While sprint tickets are not all `done`:

| Do | Don't |
|----|-------|
| Agent implements every groomed sprint ticket in order | Ask the human "should I continue?" between tickets |
| Agent moves tickets `implement` → `done` without pausing | Let the human change direction mid-sprint |
| Human may `./studio feedback` (queued for after review) | Turn feedback into tickets or code before sprint review |
| Agent captures feedback only during review | Agent implements feedback in project code during review |
| `./studio resume` points at the next ticket to implement | Block on a single ticket for human approval |

**Enforced by CLI:** `./studio move … implement` is blocked when sprint review is pending or the sprint is closed.

### Post gate 2 — before first sprint

```
Gate 2 approved
  → Agent drafts docs/phases/ (M0, M1, … outlines)
  → Human approves milestone roadmap
  → Agent writes tickets for active milestone only → product backlog
  → ./studio sprint → --approve-scope → groom → implement
```

### Feedback → backlog → sprint planning

```
Sprint review feedback (once per theme)
  → ./studio feedback (deduped)
  → ./studio clarify --approve
  → ./studio ticket --from-feedback  → product backlog (backlog/*.md, no sprint tag)
  → ./studio review --approve → **reuse review** → retro
  → ./studio sprint  → scope proposal (mature tickets proposed; immature flagged)
  → ./studio sprint --approve-scope  → human approves sprint scope
  → ./studio groom --approve → implement
```

| Step | What happens |
|------|----------------|
| **Feedback** | One FB item per theme; similar text merges to existing FB-NNN |
| **Ticket** | `--from-feedback` creates ticket in **product backlog** (`backlog/`) **without** `sprint:` |
| **Sprint plan** | `./studio sprint` proposes mature tickets in `scope-proposal.md` + `scope-proposal.json`; immature stay in backlog |
| **Scope approval** | Human runs `./studio sprint --approve-scope` after reviewing proposal (**JSON is authoritative** — rewrite both if editing scope by hand) |
| **Immature** | `planning-questions.md` — owner (design/arch/eng) fills gaps before next planning |

| Step | Who | Command |
|------|-----|---------|
| **Scope proposal** | Agent | `./studio sprint <p>` → read `scope-proposal.md` |
| **Approve scope** | **Human** | `./studio sprint <p> --approve-scope` |
| **Sprint groom** | **Human** + agent | `./studio groom <p> --approve` before first `implement` |
| **Sprint work** | **Agent only** | `./studio move <p> <ID> implement` … `done` (all sprint tickets) |
| **Status brief** | Agent prepares | `./studio review <p>` → `sprints/SPRINT-NN/review.md` |

**Rule (sprint capacity):** Each sprint proposes **3–6** mature tickets (planner `max_tickets=6`; warn if fewer than 3). Agents must **not** manually narrow `scope-proposal.json` to 1–2 tickets unless the human explicitly asks for a hotfix / surgical sprint. Prefer filling with related P0/P1 backlog.
| **Sprint review** | **Human** tries shipped work | Read review.md — **live app** (`npm run dev` at project root) and extension `dist/` if shipped; **not** `design/prototype` after implement |

**Rule (LO-0026):** If review hits **board/page 500** with webpack `Cannot read properties of undefined (reading 'call')` (or every route 404 while `next dev` is “Ready”), treat it as **dev cache / port collision**, not a product bug: stop listeners on the review port, `rm -rf .next`, restart `npm run dev`, hard-refresh `127.0.0.1:<port>` (prefer IP over `localhost` when duplicates confuse the browser). Only then re-smoke the ticket surface.

**Rule (LO-0028):** Tickets that ship **PDF export** (board Export PDF, brand-guide Download PDF / Playwright) are not done until smoke **downloads a file** on the free path. Watch for: (1) brand-guide API 503 + “Install Chromium / `npx playwright install chromium`”, (2) Export error `Failed to load export image for watermark` with no download. Unit tests alone do not catch these.

**Rule (LO-0051):** Before marking any ticket "done" whose acceptance criteria is a **visible design/UX outcome** (not just a function/type returning the right value), the agent must walk a real end-to-end user scenario through the **actual default product flow** — not a state or code path only reachable via a test harness, preview toggle, or manual override — and attach a before/after screenshot to the ticket. A feature gated behind an unconfirmed or undiscoverable app state (e.g. an unactivated setting nobody would find, or output only produced by a code path the default flow never calls) counts as **not shipped**, even if its unit tests and QA gate are green. This applies to sprint review too: "human tries shipped work" means trying it through the same flow a real user would reach, on real project data / the primary user surface — not just reading review.md's ticket list.

**Rule (LO-0039):** Tickets that **reuse docked chrome** (`StudioPanel` / `StudioRail` / `StudioDock` / floating right rails) are not done if they only reuse **CSS class names** inside a padded content shell. Before `./studio move … done`, assert **live layout DoD**: (1) flush to the intended edge (no content-inset gutter), (2) full height of the stage (top→bottom of the chrome content area, not a mid-page card). Prefer naming the **component** (`StudioPanel`) in acceptance criteria — not `studioPanelClass` alone. Screenshot or Playwright smoke of the edge is preferred.

**Rule (LO-0040):** Before inventing parallel UI chrome, apply the **component reuse ladder**: (1) reuse an existing component, (2) else extract a **project-scoped** reusable component shared across surfaces, (3) else promote/author in **studio-library** when cross-project generic. Right-rail **icon nav + detail panel** (`StudioDock` / `studio-rail`) must be mounted as that organism — not a one-off lookalike. LO titles and infusions stay **general** (no single-surface copy as the primary rule); cite `--source <project>` only as provenance.

**Rule (LO-0032):** Tickets that ship an **on-screen brand guide / print preview** and a **PDF (or printable HTML) of the same surface** must include DoD that **screen and PDF share the same type stack** (hero/title + body). Serif on screen + sans in PDF (or reverse) is a WYSIWYG bug — not done. Prefer one shared CSS/token source for both renderers.
| **Approve / reject** | **Human** | `./studio review <p> --approve` or `--reject --reason "..."` — **LO-0025:** `--approve` is refused unless every current-sprint ticket is `done` |

**Rule (LO-0025):** `./studio review <p> --approve` must **refuse** while any current-sprint ticket is still `open` / `implement` / not `done`. Mid-sprint approve freezes implementation incorrectly. Finish tickets → `./studio review` → human `--approve`.
| **Reuse review** | **Agent** + **Human** | `./studio reuse <p>` → promote / LO ticket / `--record local` → `./studio reuse <p> --approve` |
| **Raw feedback** | **Human** | `./studio feedback <p> "I want X"` — **not a ticket** |
| **Clarify** | Agent + **human** | `./studio clarify <p> FB-001 --title ... --acceptance ... --approve` |
| **Ticket** | Agent (after clarify) | `./studio ticket <p> "..." --from-feedback FB-001` |
| **Grooming** | **Human** + agent | `./studio groom <p>` — reprioritize backlog for next sprint |
| **Retro** | **Agent** fills content, **human** reviews | `./studio retro <p>` → fill `retro.md` → `./studio retro <p> --complete` + meta-retro + `./studio learn` → `./studio infusion` (LO gate clear) |
| **Next sprint** | **Human** + agent | `./studio sprint <p>` → `./studio groom <p> --approve` |

**Rule:** Ideas from sprint review never become tickets directly. Flow is always **feedback → clarify → ticket**.

**Rule:** During sprint review, the agent **never implements** feedback in project code — only `./studio feedback` → clarify → ticket for the **next** sprint.

**Rule (LO-0033):** Large / strategic review feedback must be **clarified and sliced** into multiple phase-aligned tickets (and optionally a short sprint roadmap under `docs/phases/`) **before** the next `./studio sprint`. Do not leave one mega-ticket that mixes IA, research, Figma, and experience work. Prefer 3–6 ticket sprints mapped to active milestones; keep deep companion / billing tracks deferred until product DNA is ready.

**Rule (LO-0017):** AI / vision / hint-pipeline tickets are **not done** if only an adapter, API, or queue ships. The same sprint must include a **user-visible surface** (inspector, tags list, presentation block, etc.) that sprint review can open. Gate 5 green alone is insufficient when the human cannot see the capability.

**Rule (LO-0018):** When a project uses cloud LLM model IDs (e.g. Gemini Flash-Lite), pin the **current GA** id in the project ADR / `.env.example` defaults. Before calling sprint review ready on AI tickets, the agent must **smoke a live call** (or document that `API_KEY` is unset and the empty-state was verified). Retired model 404s discovered only at human review are a process failure.

**Rule (LO-0021):** PLG entry and paywall tickets must state **UX DoD explicitly** in acceptance criteria:
1. **Which screen** the user lands on (route / dialog / form) — not only a latency target.
2. **Blocking vs soft CTA** — if the ticket promises a paywall / upgrade moment, the modal or gate must open at that moment (e.g. free-tier raster export), not only a buried text link.
3. **Speed heuristics must not skip named HITL surfaces** — e.g. “&lt;5s to canvas” must not remove a required naming / consent step the human expects to see in review.
Clarify drafts and design specs for `marketing-page` / monetization UI must spell out these three fields before `implement`.

**Rule (LO-0022):** Figma / plugin / host-network tickets are **not done** on unit tests + `npm run build` alone. Before `./studio move … done`, the agent must **smoke in the real plugin host** (e.g. Figma desktop → Load plugin → Login / fetch boards) and confirm **CORS / `origin: null` paths** work via the **plugin main thread** (or documented CORS headers). UI-iframe-only `fetch` to localhost that fails preflight is a process failure if marked done.

**Rule (LO-0043):** Figma **stickersheet / kit placement** tickets are **not done** when only section headlines (Atoms / Molecules / Organisms) appear. Before `./studio move … done`, assert **inventory children exist on the canvas** (buttons, inputs, cards, etc. — count or screenshot). Empty scaffold frames with blurbs only = process failure. Prefer an automated node-count / name-prefix check in plugin tests or a human smoke step that fails if sections have title+blurb only. See `knowledge-base/figma-plugin-host-networking.md`.

**Rule (LO-0044):** Design-system / Figma kit tickets that claim **shadcn-class / professional** quality need a **written fidelity north-star** (what “good” looks like: Figma Components vs frames, type ramp from DNA, elevation/border chrome, moodboard refs) **and screenshot DoD** against that bar. **Component count alone is not done** — themed wireframe chrome (thin strokes, empty white cards, Inter-only when DNA has faces) fails review. Lock the north-star before more inventory breadth. See `knowledge-base/figma-plugin-host-networking.md`.

**Rule (LO-0041):** Figma local allowlists use **`http://localhost:<port>` only** — never `127.0.0.1` (manifest rejects it; CSP treats them as different hosts). Plugin API base defaults and `clientStorage` prefs must normalize to `localhost`. A CSP error naming `127.0.0.1` while allowlisting `localhost` is a **stale prefs / wrong host** bug, not a broken allowlist. Rebuild does not clear `figma.clientStorage`. See `knowledge-base/figma-plugin-host-networking.md`.

**Rule (LO-0042):** Extension cloud-inbox sync that probes multiple local ports must **continue** past plain-text wrong-app 404s (e.g. `Server action not found.` from another Next app) until the product API returns JSON shaped like `{ error }` / `{ ok, item }`, or a real auth/validation rejection. Do not treat sibling-app HTML/text as a fatal product error. Keep baked `VITE_*` / `NEXT_PUBLIC_APP_URL` aligned with the live app port. See `knowledge-base/chrome-mv3-vite-content-scripts.md`.

**Rule (LO-0023):** QA / fidelity / motion / delight tickets must ship **numbered human smoke steps** in `sprints/SPRINT-NN/review.md` (auto-generated under “Per-ticket smoke”). Agent may also add a `## Review smoke` section on the ticket. Vague “see motion” / “check responsive” without click-paths fails review readiness.

**Rule (LO-0034):** Auto-generated review smoke steps must **match the ticket surface**. Do not emit Figma plugin / OAuth steps for webapp Brand kit / board tickets that only mention Figma as future/out-of-scope. Prefer live board / Brand kit routes unless the ticket is clearly a `figma-plugin` / plugin-OAuth ticket (or has an explicit `## Review smoke` section).

**Rule (LO-0035):** If a product uses a **canvas shell** (`h-dvh` + `overflow-hidden`) for infinite-canvas routes, **nested document routes** under the same layout (brand guide, presentation builder, settings-in-board) must provide their **own** `h-dvh overflow-y-auto` scroll container (route `layout.tsx`). Do not assume `body` scroll works under a locked board shell. Tall DialogShell content needs `max-h` + scrollable body.

**Rule (LO-0024):** Guest→auth / local→cloud migration must use **idempotent writes** (`put` / upsert), never blind `add` that throws `ConstraintError: Key already exists`. Auth, share, and **plugin OAuth handoff** screens must not show raw IndexedDB / Dexie errors as “Sync issue” banners. Before marking migration or plugin-login tickets done, smoke the handoff path and confirm no ConstraintError UI.

**Rule:** One feedback item per theme per sprint — `./studio feedback` dedupes similar notes (use `--force` to split).

**Rule:** Feedback tickets land in **backlog without a sprint tag** until `./studio sprint` assigns mature tickets. Mature tickets need: `phase` in frontmatter, ≥2 specific BDD acceptance criteria, and `**Scope:**` in the body when created from feedback (`--from-feedback`).

**Rule:** `./studio sprint` is blocked until the current sprint is done, review is **approved**, **reuse review is approved**, retro is **complete** (`--complete`), **studio infusion gate** is clear (no open LO-* tickets), and (for the first sprint) the **milestone roadmap** is approved.

**Rule:** `./studio retro` and `./studio sprint --approve-scope` are blocked until `./studio reuse --approve` completes for the closed sprint.

**Rule:** When all tickets for the **current milestone** are `done`, `./studio resume` surfaces **milestone review pending** — do not write next-milestone tickets until the human approves milestone completion.

### Example

```bash
./studio review nudge
# human tries the app, then:
./studio feedback nudge "Habits should work offline"
./studio clarify nudge FB-001 \
  --title "Offline habit tracking" \
  --scope "Cache today's habits in IndexedDB" \
  --acceptance "Completing a habit works offline" \
  --approve
./studio ticket nudge "Offline habit tracking" --from-feedback FB-001
./studio review nudge --approve --notes "Sprint 1 shipped, offline next"
./studio reuse nudge
./studio reuse nudge --approve
./studio groom nudge
./studio retro nudge
./studio sprint nudge
./studio groom nudge --approve
```

---

## Decision record template

```markdown
# Decision Record — DR-NNNN

**Status:** pending | approved | rejected
**Date:** YYYY-MM-DD
**Requested by:** <role/agent>
**Decision by:** <human>

## Decision
What needs to be decided?

## Context
Why is this decision necessary?

## Options

### Option A: <name>
- Pros: ...
- Cons: ...
- Costs: ...

### Option B: <name>
- Pros: ...
- Cons: ...
- Costs: ...

## Recommendation
Which option does the agent recommend and why?

## Risks
What can go wrong?

## Consequences
What does the decision mean for the project?
```

---

## HITL workflow

```
┌─────────────────────────────────────────────────────────┐
│               HUMAN-IN-THE-LOOP WORKFLOW                │
└─────────────────────────────────────────────────────────┘

 1. Agent recognizes a HITL situation
       │
 2. Create a decision record
       │
 3. Present the decision record
       │
 4. ┌─────────────────┐
    │  WAIT FOR      │
    │  DECISION      │
    └─────────────────┘
       │
 5. Human decides
       │
 6. Update the decision record
       │
 7. Implement the decision
```

---

## Commands

```bash
# Create a decision record
./studio decide <project> "<title>"

# Overview of all decision records
./studio decisions <project>

# Mark a decision record as approved
./studio decide <project> DR-NNNN --approve

# Mark a decision record as rejected
./studio decide <project> DR-NNNN --reject
```

---

## Decision record directory

```
<project>/docs/decisions/
├── README.md              # overview of all DRs
├── DR-0001-...
├── DR-0002-...
```

### README.md

```markdown
# Decision Records

| DR | Title | Status | Date | Decision-maker |
|----|-------|--------|------|----------------|
| DR-0001 | ... | approved | YYYY-MM-DD | ... |
| DR-0002 | ... | pending | YYYY-MM-DD | — |

## Legend
- **pending:** waiting for a decision
- **approved:** approved
- **rejected:** rejected
```

---

## HITL examples

### Example 1: Deployment costs

```markdown
# Decision Record — DR-0001

**Status:** pending
**Date:** 2026-08-20
**Requested by:** Platform Engineering

## Decision
Should the project use a managed Kubernetes cluster (€150/month) or a simpler docker host (€30/month)?

## Context
The project expects 10k users in the first year. Performance requirements are moderate.

## Options

### Option A: Managed Kubernetes
- Pros: auto-scaling, high availability
- Cons: complexity, costs
- Costs: €150/month

### Option B: Docker host
- Pros: simple, cheap
- Cons: manual scale-up
- Costs: €30/month

## Recommendation
Option B (docker host) — sufficient for the expected load, saves €1440/year.

## Risks
- On sudden traffic spikes: possible downtime
- Manual scaling required
```

---

### Example 2: License decision

```markdown
# Decision Record — DR-0002

**Status:** pending
**Date:** 2026-08-20
**Requested by:** Product Management

## Decision
Should a commercial UI license (€500/year) be purchased or should an open-source alternative be used?

## Context
The project needs an advanced data-grid component.

## Options

### Option A: Commercial license
- Pros: support, features
- Cons: costs, vendor lock-in
- Costs: €500/year

### Option B: Open source
- Pros: free, flexibility
- Cons: fewer features, no support
- Costs: €0

## Recommendation
Option B — the needed features are available in the open-source version.

## Risks
- If advanced features are needed: manual implementation required
```

---

## Automated HITL detection

The agent automatically recognizes HITL situations:

```yaml
# In the agent configuration
hitl_triggers:
  - pattern: "costs.*€[0-9]+"
    category: budget
  - pattern: "delete.*data"
    category: irreversible
  - pattern: "production.*deploy"
    category: release
  - pattern: "contract.*signature"
    category: legal
  - pattern: "gdpr.*exception"
    category: compliance
```

---

## HITL report

```markdown
# HITL Report — Monthly

## Decisions this month

| DR | Title | Status | Decision-maker | Date |
|----|-------|--------|----------------|------|
| DR-0001 | ... | approved | Max | 2026-08-15 |
| DR-0002 | ... | rejected | Max | 2026-08-18 |

## Pending decisions

| DR | Title | Requested by | Waiting since |
|----|-------|--------------|---------------|
| DR-0003 | ... | Agent | 2026-08-20 |

## Statistics
- Approved: 5
- Rejected: 1
- Pending: 1
- Average decision time: 2 days
```

---

## References

- `.quinsy-studio/process/lifecycle.md` — phases
- `.quinsy-studio/process/gates.md` — gates
- `./studio decide <project> "<title>"` — create a decision record
- `./studio decisions <project>` — show the overview
