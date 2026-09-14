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
| **Budget / paid vendor** | new paid vendor, costs above X €/month | **Yes** (tech-veto) |
| **Legal** | contracts, licenses, GDPR exceptions | **Yes** |
| **Irreversible** | deleting data, production deploy, DNS changes | **Yes** |
| **Security** | security exceptions, access rights | **Yes** (tech-veto) |
| **As-built / PRD (gate 0)** | confirm “this is what we have / are building” | **Yes** (`./studio approve --gate 0`) |
| **Architecture (gate 1)** | stack, ADRs, persistence, vendors — after PRD | **Yes** (`./studio approve --gate 1`). Iterate: `./studio revise --gate 1` |
| **Design track (gate 2)** | direction, design system, stills/mocks or clickable prototype | **Yes** (`./studio approve --gate 2`). Starts after architecture. Iterate: `./studio revise --gate 2` |
| **Release** | production release | **Yes** |
| **Cadence review** | shipped UI / product after **N implementation sprints** (default 2) | **Yes** (`./studio review`) — feedback goes into **production** tickets, not a silent next implement |
| **Architecture packet** | ticket-level approach note | **Yes** (`./studio approve-arch`) after `docs/architecture/<TICKET>.md` exists |
| **Backend-only sprint** | API / data work with no UI | **Inform** — continue to retro |
| **Reuse** | what was pulled / promoted / now in registry | **Inform brief** — no `--approve` |
| **Sprint scope / groom** | which tickets this sprint | **Agent-owned** (human may override) |
| **Design-track ticket** | major UX / UI / IA (`ui-new-component`, `ui-composition`, `marketing-page`, `workflow-explainer`, `ia-navigation`, `ia-feature-placement`) | **Yes** (`./studio approve-design`) **only after** Team 10 has written the spec file + in-context, token-based, all-state mocks — then implement. Asking to approve a missing file is forbidden. |
| **Design-system gap** | missing component, token, or pattern vs gate-2 system | **Do not invent in a feature ticket.** Open a design-track ticket; work it in a **design sprint**; HITL `approve-design` before anyone composes it |
| **Other UI / feature / styling** | assemble approved library + project tokens | **No** ticket ACK — stay inside the defined design system |
| **Ticket done** | receipt + gate 5 + `MOVE_DONE` | **No** — never ask the human to ACK a non-design ticket |
| **Feature** | new features (incremental, in sprint) | No (if ticket exists) |
| **Bugfix** | fixing bugs | No |
| **Docs** | documentation | No |
| **Schema migrate (apply)** | Pending migrations on a DB the agent can reach (local Compose, `.env` DSN, documented VPS) | **No** — agent runs the project migrate command, then **informs** the human it happened |
| **Destructive DB reset** | `migrate:fresh`, drop database, wipe production | **Yes** |
| **Mid-execute chat** | thoughts while IMPLEMENT is in flight | **Queue** (`./studio guard` → `INBOX_ACK`) — auto-queued, do not preempt. Drain after MOVE_DONE. Only “stop this ticket” aborts |

---

## Sprint cadence HITL (after gates 0–2)

Start of a project: **gate 0** (PRD) → **gate 1** (architecture) → **gate 2** (design track: direction, **design system**, stills/mocks or clickable prototype). All three are HITL. **After the sprint has started**, the human does **not** ACK every ticket. Packet sign-off is **`approve-design` / `approve-arch`** (execute `ACTION: PRODUCTION` writes the files first). Cadence **`./studio review`** runs every `cost.human_review_every_sprints` **implementation** sprints (default 2), not after every batch. Tickets `done` via **skill QA on the receipt** (QA / Design skill / Architecture skill), not a human ACK. Hygiene is `./studio sprint --kind hygiene`. Safety valves stay: tech-veto, 3× gate fail, abort, `INFORM cost-cap`.

See [milestone-planning.md](milestone-planning.md) for roadmap ceremony.

### Autonomous execution (mid-sprint)

While sprint tickets are not all `done`:

| Do | Don't |
|----|-------|
| Agent implements non-design sprint tickets in order | Ask “looks good?” after a feature/styling ticket |
| Agent applies pending migrations when it can reach the DB, then INFORM | Ask the human to run migrate as sprint work |
| Agent waits for `./studio approve-design` **after spec+mocks exist** | Invent a new component or token in a feature ticket; ask the human to approve a spec that was never written |
| Stay inside gate-2 design system + library pulls | One-off CSS / hallucinated atoms because “the sprint needs it” |
| Agent **ACK-queues** a **product** mid-execute chat (`./studio note`) and resumes ACTION. `HQ-T*`, `LO-NNNN`, `.quinsy-studio`, and “quinsy-studio process” are `studio_meta` (not the product inbox) | Queue studio HQ on the product sprint inbox, or keep product `IMPLEMENT` for an HQ ask |
| Agent captures design feedback only during UI review | Agent implements design feedback in project code during review |
| Open LOs spawn `./studio train` in parallel | Return `STUDIO_LO` instead of the next `IMPLEMENT` |

**Enforced by CLI:** `./studio move … implement` is blocked when cadence review is pending or the sprint is closed pending retro. Implementation `--approve-scope` is blocked when production tickets exist and ready backlog is below `cost.production_ready_min`. When the last sprint ticket is `done` and cadence is not due, execute continues to retro — not HITL.

**Rule (LO-0144):** Close **this** sprint as soon as its tickets are `done` (UI review or backend inform → reuse → retro). Do not keep review open because a later amendment, operator console, or unwritten skill is still only feedback. Capture that work with `./studio feedback` → clarify → ticket for a later sprint.

**Execute loop:** `./studio execute <project>` returns one action. The agent runs `NEXT`, then execute again, until `HITL`. `INFORM` still loops. Gate failures write `sprints/SPRINT-NN/debug/<ticket>.md` and retry up to 3 times, then `blocked` + optional `gate-fail` LO **and** a train job. `move … done` requires a receipt (`./studio receipt`) plus a fresh level-5 gate.

**Rule (LO-0181 / LO-0189 / LO-0192 / LO-0194 — print / multi-page export receipts):** Before `MOVE_DONE` on print or multi-page PDF tickets, the receipt must record a **page-count or print-preview proof** (e.g. “N sections → N pages” or a print-preview screenshot path). Shipping landscape CSS or a page-plan unit test alone is not done. Prefer **forced breaks on real section wrappers** in the print tree (one HTML section → one `@page`); if the human still sees a single truncated sheet, the ticket is not done — re-open or follow-up with DOM/CSS proof, not another plan-only green. When the product shell uses `overflow: hidden` / `h-dvh` on `body` or the app root, print CSS must **unlock overflow/height** for those ancestors under `@media print` or pagination cannot leave the first sheet.

**Operator loop (LO-0155):** A queued job is not the default flow until the operator control that enqueues it ships. When the same sprint has both the start/submit surface and downstream polish (notify, on-demand revalidate), implement the click first if the human is waiting to run the gold path. Unblocked-ticket order is not a reason to skip the button.

### Stay on the defined design system

Gate 2 approved the **design system** (tokens, sticker sheet, library components). Non-design tickets **must** use that system: project `ui/tokens`, studio-library / Headless UI primitives, existing project organisms. No one-off hex, new atom, or new interaction pattern inside a feature/bug/`ui-styling` ticket.

If something is **missing** (no matching component, token, or IA surface):

1. Stop composing a fake control in the feature ticket
2. File a design-track ticket (`ui-new-component`, `ia-feature-placement`, …) with `docs/design-specs/<TICKET>.md` **written** (not only a frontmatter path)
3. Put it in a **design sprint** (or the design slice of scope) — Team 10 spec §2 + §2c, **project-token HTML mocks in the real view, all states**
4. Human: `./studio approve-design` — **then** implement / pull into the product sprint

Do not ship a new primitive “so this ticket can finish.” That is a process fail, not a library-first shortcut.

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

**Rule (LO-0185 — plugin / shell chrome FBs):** When multiple review notes touch the same host shell (auth gate, header, tabs, button styles, sign-out), **bundle into one ticket** instead of shipping a partial icon polish ahead of the cold-open auth path. Partial chrome tickets regress the first paint users see.
| **Immature** | `planning-questions.md` — owner (design/arch/eng) fills gaps before next planning |

| Step | Who | Command |
|------|-----|---------|
| **Scope proposal** | Agent | `./studio sprint <p>` → read `scope-proposal.md` |
| **Approve scope** | **Agent** (human may override) | `./studio sprint <p> --approve-scope` |
| **Sprint groom** | **Agent** (human may override) | `./studio groom <p> --approve` before first `implement` |
| **Sprint work** | **Agent only** | `./studio move <p> <ID> implement` … `done` (all sprint tickets) |
| **Status brief** | Agent prepares | `./studio review <p>` → `sprints/SPRINT-NN/review.md` |

**Rule (sprint capacity / LO-0124):** Each sprint proposes **3–6** mature tickets (planner `max_tickets=6`; warn if fewer than 3). Agents must **not** manually narrow `scope-proposal.json` to 1–2 tickets unless the human explicitly asks for a hotfix / surgical sprint, **or** the sprint is an intentional **review-feedback polish** slice (2 related motion/UI tickets from the prior review). Prefer filling with related P0/P1 backlog when available; under-capacity warnings are expected and OK for those polish sprints.

**Rule (LO-0208):** `scope-proposal.md` row count must match `scope-proposal.json` and what execute will pull. Tickets deferred from this sprint are listed as **deferred**, not omitted so the markdown looks smaller than the JSON.

**Rule (LO-0183 — over-capacity polish):** Human-approved review dumps may exceed 6 tickets. Prefer **splitting into two sprints** (P0 chrome/bugs first, then deeper product stories) over a single 14-ticket sprint that ships incomplete polish and immediate follow-up FBs. If the human insists on one large set, call out which ACs need soak/proof and keep receipts honest.
| **Sprint review** | **Human** tries shipped work | Read review.md — **live app** (`npm run dev` at project root) and extension `dist/` if shipped; **not** `design/prototype` after implement |

**Rule (LO-0066):** Before writing Docker Compose **published host ports** or local app URLs, probe `docker ps` (and listeners). Multiple project stacks share one machine. Do not take 5432 / 6379 / 3000 / Supabase 54321–54323 if they are already bound. Pin via project env and RUNBOOK. See `knowledge-base/host-port-allocation.md`. Do not stop another project’s containers to free a default port.

**Rule (LO-0198 / LO-0199 — one listener per published port):** For each RUNBOOK host port, run **either** the Compose service **or** host `npm run dev` / `next dev`, not both. Adding a service to Compose that publishes a port already used by a host process requires stopping the host listener first (SIGTERM/143 is expected). Do not keep a second Next/dev server on the same port “as a fallback” after Compose is healthy.

**Rule (LO-0026):** If review hits **board/page 500** with webpack `Cannot read properties of undefined (reading 'call')` (or every route 404 while `next dev` is “Ready”), treat it as **dev cache / port collision**, not a product bug: stop listeners on the review port, `rm -rf .next`, restart `npm run dev`, hard-refresh `127.0.0.1:<port>` (prefer IP over `localhost` when duplicates confuse the browser). Only then re-smoke the ticket surface.

**Rule (LO-0028):** Tickets that ship **PDF export** (board Export PDF, brand-guide Download PDF / Playwright) are not done until smoke **downloads a file** on the free path. Watch for: (1) brand-guide API 503 + “Install Chromium / `npx playwright install chromium`”, (2) Export error `Failed to load export image for watermark` with no download. Unit tests alone do not catch these.

**Rule (LO-0167 / LO-0170):** When sprint review is the **deployed git host** (git-backed PaaS / CDN), `MOVE_DONE` is not review-ready until the **product repo** is pushed to the branch that host tracks. Local-only commits are invisible there. Push the product remote (not studio HQ) before asking the human to try shipped UI. Local `npm run dev` / Compose review does not need that push.

**Rule (LO-0051 / LO-0203):** Before marking any ticket "done" whose acceptance criteria is a **visible design/UX outcome** (not just a function/type returning the right value), the agent must walk a real end-to-end user scenario through the **actual default product flow** — not a state or code path only reachable via a test harness, preview toggle, or manual override — and attach a before/after screenshot to the ticket. A feature gated behind an unconfirmed or undiscoverable app state (e.g. an unactivated setting nobody would find, or output only produced by a code path the default flow never calls) counts as **not shipped**, even if its unit tests and QA gate are green. This applies to sprint review too: "human tries shipped work" means trying it through the same flow a real user would reach, on real project data / the primary user surface — not just reading review.md's ticket list.

**Public index is the default flow (LO-0203 / LO-0205):** Chrome, tokens, heroes, and home-rail tickets are not done if `/` (the published public index on the **RUNBOOK host port**) is an empty well while inner routes (`/{slug}`, section fronts) are full. Smoke `/` with published inventory in the same ticket. Inner slugs alone are not the default reader path.

**Rule (LO-0039):** Tickets that **reuse docked chrome** (`StudioPanel` / `StudioRail` / `StudioDock` / floating right rails) are not done if they only reuse **CSS class names** inside a padded content shell. Before `./studio move … done`, assert **live layout DoD**: (1) flush to the intended edge (no content-inset gutter), (2) full height of the stage (top→bottom of the chrome content area, not a mid-page card). Prefer naming the **component** (`StudioPanel`) in acceptance criteria — not `studioPanelClass` alone. Screenshot or Playwright smoke of the edge is preferred.

**Rule (LO-0040):** Before inventing parallel UI chrome, apply the **component reuse ladder**: (1) reuse an existing component, (2) else extract a **project-scoped** reusable component shared across surfaces, (3) else promote/author in **studio-library** when cross-project generic. Right-rail **icon nav + detail panel** (`StudioDock` / `studio-rail`) must be mounted as that organism — not a one-off lookalike. LO titles and infusions stay **general** (no single-surface copy as the primary rule); cite `--source <project>` only as provenance.

**Rule (LO-0148):** When the public site renders a **closed block library**, the operator editor must edit those **blocks** and preview the **visitor template** (iframe or equivalent). A Word/HTML field as the page source of truth is not done.

**Rule (LO-0154):** Operator Save on **published** documents must be what the **public document route** serves. When a live record id exists, do not silently substitute a fixture corpus. Preview iframe and public host must share the same published inventory; revalidate or bypass stale fetch so a reload matches Save.

**Rule (LO-0149):** Ordered collections of named rows (section maps, nav maps, similar admin lists) ship as a **table or list** (one row per item: label, keys, enable, reorder). A stacked card Repeater that hides the full set is not done.

**Rule (LO-0151):** Public masthead/nav items must resolve to a **published, non-empty destination**. Do not list a map row (or equivalent) that 404s or has zero published items. Empty or unpublished sections stay off chrome.

**Rule (LO-0152):** Operator record edit: the **tab bar sits under header actions** (not below the form); the **ordered list/map is the first tab**; remaining metadata is **one field per row** in a single column. A stacked checkbox that is not vertically centered in its table cell is not done.

**Rule (LO-0032):** Tickets that ship an **on-screen brand guide / print preview** and a **PDF (or printable HTML) of the same surface** must include DoD that **screen and PDF share the same type stack** (hero/title + body). Serif on screen + sans in PDF (or reverse) is a WYSIWYG bug — not done. Prefer one shared CSS/token source for both renderers.
| **Approve / reject** | **Human** | `./studio review <p> --approve` or `--reject --reason "..."` — **LO-0025:** `--approve` is refused unless every current-sprint ticket is `done` |

**Rule (LO-0025):** `./studio review <p> --approve` must **refuse** while any current-sprint ticket is still `open` / `implement` / not `done`. Mid-sprint approve freezes implementation incorrectly. Finish tickets → `./studio review` → human `--approve`.

**Rule (LO-0144):** Review is for **this sprint’s shipped tickets**, not for work that is still only feedback (amendments, console, unwritten skills). Do not linger in review waiting for that work to become a ticket in the same close. Ticket it, then plan the next sprint.
| **Reuse review** | **Agent** | `./studio reuse <p>` → promote / LO ticket / `--record local`. Completes when unresolved paths are 0 (LO-0169) — no `--approve` |
| **Raw feedback** | **Human** | `./studio feedback <p> "I want X"` — **not a ticket**. Drop accidental CLI noise (`--help`) before retro (LO-0173) |
| **Clarify** | Agent + **human** | `./studio clarify <p> FB-001 --title ... --acceptance ... --approve` |
| **Ticket** | Agent (after clarify) | `./studio ticket <p> "..." --from-feedback FB-001` |
| **Grooming** | **Human** + agent | `./studio groom <p>` — reprioritize backlog for next sprint |
| **Retro** | **Agent** fills content, **human** reviews | `./studio retro <p>` → fill `retro.md` → `./studio retro <p> --complete` (auto-harvest) → `./studio execute` `STUDIO_LO` |
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

**Rule (LO-0022 / LO-0195):** Figma / plugin / host-network tickets are **not done** on unit tests + `npm run build` alone. Before `./studio move … done`, the agent must **smoke in the real plugin host** (e.g. Figma desktop → Load plugin → Login / fetch boards) and confirm **CORS / `origin: null` paths** work via the **plugin main thread** (or documented CORS headers). UI-iframe-only `fetch` to localhost that fails preflight is a process failure if marked done. When plugin `dist/` is gitignored, review smoke requires a **local rebuild + host reload** after each chrome/palette change — committed `src/` alone does not update the running plugin.

**Rule (LO-0043):** Figma **stickersheet / kit placement** tickets are **not done** when only section headlines (Atoms / Molecules / Organisms) appear. Before `./studio move … done`, assert **inventory children exist on the canvas** (buttons, inputs, cards, etc. — count or screenshot). Empty scaffold frames with blurbs only = process failure. Prefer an automated node-count / name-prefix check in plugin tests or a human smoke step that fails if sections have title+blurb only. See `knowledge-base/figma-plugin-host-networking.md`.

**Rule (LO-0044):** Design-system / Figma kit tickets that claim **shadcn-class / professional** quality need a **written fidelity north-star** (what “good” looks like: Figma Components vs frames, type ramp from DNA, elevation/border chrome, moodboard refs) **and screenshot DoD** against that bar. **Component count alone is not done** — themed wireframe chrome (thin strokes, empty white cards, Inter-only when DNA has faces) fails review. Lock the north-star before more inventory breadth. See `knowledge-base/figma-plugin-host-networking.md`.

**Rule (LO-0041):** Figma local allowlists use **`http://localhost:<port>` only** — never `127.0.0.1` (manifest rejects it; CSP treats them as different hosts). Plugin API base defaults and `clientStorage` prefs must normalize to `localhost`. A CSP error naming `127.0.0.1` while allowlisting `localhost` is a **stale prefs / wrong host** bug, not a broken allowlist. Rebuild does not clear `figma.clientStorage`. See `knowledge-base/figma-plugin-host-networking.md`.

**Rule (LO-0042):** Extension cloud-inbox sync that probes multiple local ports must **continue** past plain-text wrong-app 404s (e.g. `Server action not found.` from another Next app) until the product API returns JSON shaped like `{ error }` / `{ ok, item }`, or a real auth/validation rejection. Do not treat sibling-app HTML/text as a fatal product error. Keep baked `VITE_*` / `NEXT_PUBLIC_APP_URL` aligned with the live app port. See `knowledge-base/chrome-mv3-vite-content-scripts.md`.

**Rule (LO-0023):** QA / fidelity / motion / delight tickets must ship **numbered human smoke steps** in `sprints/SPRINT-NN/review.md` (auto-generated under “Per-ticket smoke”). Agent may also add a `## Review smoke` section on the ticket. Vague “see motion” / “check responsive” without click-paths fails review readiness.

**Rule (LO-0223):** When that smoke is a **create/compose** flow, AC must name the **compose/create path** (where the operator files or builds the thing), not only the later read/list path.

**Rule (LO-0224):** Operator filing for structured programs (content calendars, briefs, similar) stays **structured-first** (fields the product already has). Agent-written briefs keep distinct What / Why / How — do not collapse them into one paste blob.

**Rule (LO-0034):** Auto-generated review smoke steps must **match the ticket surface**. Do not emit Figma plugin / OAuth steps for webapp Brand kit / board tickets that only mention Figma as future/out-of-scope. Prefer live board / Brand kit routes unless the ticket is clearly a `figma-plugin` / plugin-OAuth ticket (or has an explicit `## Review smoke` section).

**Rule (LO-0035):** If a product uses a **canvas shell** (`h-dvh` + `overflow-hidden`) for infinite-canvas routes, **nested document routes** under the same layout (brand guide, presentation builder, settings-in-board) must provide their **own** `h-dvh overflow-y-auto` scroll container (route `layout.tsx`). Do not assume `body` scroll works under a locked board shell. Tall DialogShell content needs `max-h` + scrollable body.

**Rule (LO-0024):** Guest→auth / local→cloud migration must use **idempotent writes** (`put` / upsert), never blind `add` that throws `ConstraintError: Key already exists`. Auth, share, and **plugin OAuth handoff** screens must not show raw IndexedDB / Dexie errors as “Sync issue” banners. Before marking migration or plugin-login tickets done, smoke the handoff path and confirm no ConstraintError UI.

**Rule:** One feedback item per theme per sprint — `./studio feedback` dedupes similar notes (use `--force` to split).

**Rule:** Feedback tickets land in **backlog without a sprint tag** until `./studio sprint` assigns mature tickets. Mature tickets need: `phase` in frontmatter, ≥2 specific BDD acceptance criteria, and `**Scope:**` in the body when created from feedback (`--from-feedback`).

**Rule (LO-0057 / LO-0059):** Before scoping UI tickets from an **amendment surface map** (or kit / brand-guide IA), confirm the **live product home surface** with a short HITL check when product direction may have moved. Amendment IA is a draft — shipping against the wrong home (e.g. kit slots vs narrative/presentation rail) wastes foundation work. Prefer `./studio feedback` → clarify → ticket that names the real home, then defer superseded tickets.

**Rule (LO-0060):** When feedback **rewrites the sprint goal mid-flight**, in the **same turn**: update `sprints/SPRINT-NN/plan.md` (goal + ticket table), set `sprint_deferred: true` (or remove `sprint:`) on superseded tickets, and tag the replacement ticket into the current sprint. Do not leave plan.md and deferred tickets for a later cleanup.

**Rule (LO-0175):** Any supersede or cancel — even without a goal rewrite — must clear `sprint:` or move the ticket to `cancelled/` in that same turn (`ticket-workflow.md`). Ghosts in the current sprint break execute/review.

**Rule (LO-0058):** Tickets **pulled into the current sprint** from feedback skip normal scope-proposal maturity checks and often flag `IMMATURE_TICKET` at groom. Before `implement`, fill mature AC (≥2 BDD) + Scope, and a design spec (§2 + §2c) when the ticket is design-track. Mid-sprint pull is allowed; immature body is not.

**Rule (LO-0054):** Marketing / stylescape / product-still tickets that depict an **infinite canvas or board chrome** must **mount the real product canvas component** (or shared fixtures with public-safe URLs such as `shareInlineUrl`) — never invent parallel DOM frame chrome that only looks similar. Product token/CSS changes must auto-apply on marketing. Screenshot DoD: marketing still vs live product surface.

**Rule (LO-0116):** Marketing **scroll-story** tickets must **lock one motion model in the design spec before IMPLEMENT** (sticky stack vs scroll-scrub vs discrete chapters). Do not iterate models mid-sprint. Pair with design-science DoD: fixed illustration height, no page-wide enter cascades, native 1:1 scroll on sticky pins (see `knowledge-base/design-science-playbook.md`).

**Rule (LO-0120 / LO-0122):** Sticky stage crossfades must keep the **current/active slide sharp** until the next slide is meaningfully in the sticky band. Drive blur/opacity from **relative sticky progress**: incoming blurs into view then clears; outgoing **fades** (opacity). Never mark the current slide outgoing-blurred while the next is still off-screen below the band.

**Rule (LO-0121):** Marketing “appear” stills that only tilt feel stiff. Prefer a **throw-on** start state (blur + reduced opacity + slight overscale) settling simultaneously with a modest end tilt (~3°), not tilt-only.

**Rule (LO-0062 / LO-0064):** Provider-backed **Suggested / found imagery** is not done if the UI only shows query copy + “Looking up…” while returning empty. Before review: smoke Suggested on a **signed-in** board with network; “stuck loading” or empty after optimistic copy = not shipped. Degraded empty must be explicit (auth / network / no candidates) — never look “alive” with zero results.

**Rule (LO-0069 / LO-0074):** Degraded **Suggested** copy must distinguish failure modes — reviewers cannot tell a **provider outage** (HTTP 5xx, timeout) from **adapter filter-empty** (e.g. licence slug mismatch dropping every result). Minimum messaging:

| Condition | User-facing intent | Engineering signal |
|-----------|-------------------|-------------------|
| HTTP 5xx / timeout / DNS | “Image search is temporarily unavailable — try again” | Log status + provider id |
| Auth / entitlement short-circuit | “Sign in to see suggestions” (or product equivalent) | Do not call provider |
| 200 with zero after filter | “No images matched your licence rules” **only when filter is intentional**; if unexpected, treat as bug | Log `rejected_count` + top `rejected_reason` |
| Healthy 200 + candidates | Show results; no perpetual “Looking up…” |

Smoke both a **healthy provider response** and a **forced 502** (or stub) before review so copy and telemetry are verified — not only the happy path.

**Rule (LO-0063 / LO-0065):** Imagery **selection** tickets that feed a presentation must include **presentation layout DoD** in the same epic (or a paired ticket before review): placement (e.g. bottom band) + composition quality (e.g. bento / editorial mosaic) — not only the rail picker. A uniform mid-page image list that does not communicate mood fails review for the imagery capability.

**Rule:** `./studio sprint` is blocked until the current sprint is done, review is **approved**, **reuse review is approved**, retro is **complete** (`--complete`), and (for the first sprint) the **milestone roadmap** is approved. Open LO-* tickets **do not** block the next product sprint — train/infuse in parallel (`./studio infusion` is status, not a gate).

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
