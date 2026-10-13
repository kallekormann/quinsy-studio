# Agent Context Protocol

> How the IDE agent stays in studio/project scope and recovers from drift.

**HQ skill advancement (LO-0331–0339):** Teams 01/02/07/10 playbooks distilled; IDs **FE-007**, **BE-006**, **AI-004**; tools `./studio ia-audit` and gate-5 `studio_skill_checks`. Plan: [hq-skill-advancement-sprints.md](hq-skill-advancement-sprints.md).

**HQ isolation epic:** `LO-0314`–`LO-0326` shipped — [hq-isolation-sprints.md](hq-isolation-sprints.md). Resume product `./studio execute` in a **product** chat. Do not Read env **values**.

**Same-window multi-project (Cursor only):** [hq-session-binding.md](hq-session-binding.md). When HQ `runtime` is `cursor`, each chat runs `./studio bind <project> --session <conversation_id>` once. Hooks deny sibling reads and sibling git. A bound `execute` does not rewrite `.cursorignore`. Claude Code and the CLI (`runtime` other than `cursor`) keep workspace focus isolation.

## Every turn (before session start)

Run `./studio guard <project> "<verbatim user message>"` first. While implementation is in flight on that project, guard returns `INBOX_ACK`, queues the note, and the agent resumes `./studio execute`. Do not treat the bubble as a new assignment. Drain after `MOVE_DONE`. Exceptions: abort; “back on track”; explicit **gate / approve-design / approve-arch / cadence review** when execute already says `STOP`; `IDEATE` (`ideate`, `incubate`, `ideation`, or a section or dimension name while a session is open) which asks once when the session is waiting for a brief, and otherwise runs `./studio ideate` through the case in that turn and does not call `execute`. Ask a question only when a fact only the human knows would change the problem. If several ideas remain, ask which one to focus on. If one remains, write the case and ask whether it should become the intake PRD. On yes, run approve and promote. On no, reject or park. Do not write the PRD until they say yes. Builder time is not a ceiling: one solo builder, with AI agents for coding and design, ships in chunks of about two months. The first chunk is the MVP. Later chunks stay in the idea. Medicine and clinical care are out of reach. Other trades stay in reach. Do not ask the human to continue between sections. Mid-sprint “looks good” on a **feature** ticket is not HITL.

## Session start

1. Read [`AGENTS.md`](../../AGENTS.md)
2. Run `./studio bootstrap` (new PRD), `./studio adopt <p> --from …` (existing codebase), or `./studio focus <project>`
3. Run `./studio settings` (HQ train ledger) and `./studio settings <project>` (product execute ledger). Estimates are studio load, not host billing.
4. Run `./studio execute <project>` — do the `NEXT` command, then execute again, until `ACTION` is `HITL`. After gate 2b the loop is a design phase, then an architecture phase, then an implementation phase. An empty phase is skipped. Inside a design or architecture phase, write every packet before the batch signature. If the gold path needs an operator click (submit/start a job) and a later unblocked ticket is only notify/revalidate polish, do the click ticket first (LO-0155).
5. If `ACTION` is `INFORM` (inbox drain / reuse brief), do NEXT and loop — do not wait for a signature. Architecture and design are HITL, not inform.
6. If `ACTION` is `INFORM` and the reason is `cost-cap`, **stop**. Do not keep stuffing files. Raise the **named** key in product `docs/studio.settings.local.yaml` (or HQ local yaml for train), then execute continues.
7. If `ACTION` is `STUDIO_LO`, the product loop is idle — infuse in `.quinsy-studio/` now. Mid-sprint gaps: spawn `./studio train` in a **HQ chat** and keep `IMPLEMENT`
8. Mid-execute human messages: `./studio guard` → `INBOX_ACK` (auto-queued). Resume NEXT. Drain after MOVE_DONE
9. `./studio resume <project>` is a human-readable checklist; do not stop after printing it

Do **not** ask “should I continue?” mid-sprint. Loop until HITL. Compact cards only — do not load the whole backlog. **READ only CARD playbooks.** Never open `knowledge-base/learnings/inbox.md` on IMPLEMENT.

**Docker / secrets:** Docker is required for gate, migrate, and boot. Do not Read `.env` values. `./studio env <p> up|migrate|dev --approve` injects named vars from gitignored `projects/<p>/.env` (seeded from the schema and `.env.example`). Production values live in Coolify. Before pinning Compose host ports or `next dev` ports, probe `docker ps` published ports. Operators run multiple stacks. See [host-port-allocation.md](../knowledge-base/host-port-allocation.md).

**Schema migrate:** if you can reach the database, **you run** the project migrate command (sprint work) via Compose `--approve` when that is the path. INFORM the human. Do not HITL “please run migrate.” See [backend_playbook.md](../knowledge-base/backend_playbook.md).

**Greenfield UI kit:** `./studio init` / `design` / `adopt` write `docs/setup/ui-kit.md` and put kit peers in the app `package.json`.

Active project is stored in `.quinsy-studio/.active-project.json`.

## Sibling isolation

The IDE workspace is Studio HQ, so every `projects/<name>/` tree is on disk. After `./studio focus <project>` (also reapplied on `execute` and `verify-worlds`):

- Sibling folders are listed in a local `.cursorignore` so Read/Grep/Glob should not see them
- A generated Cursor rule names the **only** allowed product tree
- Guard returns `cross_project` if the request names a sibling folder
- Project `pre-commit` refuses a wrong git toplevel and staged `projects/` symlinks
- HQ pre-commit refuses `projects/` in the studio repo
- `parallel.max_projects` (default 5) leases `./studio execute`. Focus will not clobber another live lease unless `--force`

Do not use Shell to `ls`/`cp`/`git` a sibling. Never merge two product gits. **One chat per product.**

**Do not switch project scope mid-thread.** Stay on `.active-project.json` unless the human **explicitly** asks to switch (`./studio focus <other>`, “switch to …”, “focus …”, “work on … now” naming that product as the new active scope). Naming a sibling in feedback, contrast, or a mistaken label is **not** a switch — ACK, stay put, or queue a note. Do not `./studio focus` another product on your own.

## Three context layers

| Layer | Scope | Examples |
|-------|-------|----------|
| **Studio meta** | `.quinsy-studio/` | LO-* tickets, process, tools, library |
| **Project** | `projects/<name>/` | PRD, gates, tickets, code |
| **Off-topic** | Neither | Unrelated questions |

Studio HQ must stay **project-agnostic** in docs/tools — see [studio-abstraction.md](studio-abstraction.md). Run `./studio verify-abstraction` after studio edits.

**Browser extension global mode:** see [chrome-mv3-vite-content-scripts.md](../knowledge-base/chrome-mv3-vite-content-scripts.md) DoD item 8 — fan-out + inject-on-miss before armed storage (LO-0157, LO-0159).

## When the user asks something

### 0. Mid-execute inbox (first)

If the previous turn was execute-loop work, `./studio guard` is still the first command. Product chat becomes `inbox_ack`. **Exception (LO-0243):** `HQ-T*`, `LO-NNNN`, `.quinsy-studio`, or “quinsy-studio process” is `studio_meta` — do **not** queue it on the product sprint inbox, and do not resume product `IMPLEMENT`.

### 1. Check active project

(Only for a fresh session, a HITL reply, or after inbox drain.)

```bash
./studio focus <project>    # set + print scope banner
./studio guard <project> "user request text"
```

| Verdict | Agent action |
|---------|--------------|
| `inbox_ack` | Note queued. ACK one line. Resume `./studio execute` (same ACTION). Do not implement the note. |
| `abort` | Stop the current ticket. Drain. Wait. |
| `cross_project` | Request names a sibling `projects/` folder — even mid-execute. Do not Read/copy/git it. Stay on the active project unless the human **explicitly** asks to switch focus. Do not queue as an inbox note. |
| `in_scope` | Proceed; tie work to ticket ID if post-gate-2 |
| `needs_ticket` | Do **not** implement — create `./studio ticket` or ask user |
| `pre_impl` | Redirect to current gate (`./studio resume`) |
| `feedback_only` | Sprint review HITL — capture feedback, do not code |
| `studio_meta` | Studio HQ (`HQ-T*`, `LO-NNNN`, `.quinsy-studio`, process) — not product code and **not** the product sprint inbox |
| `unclear` | Ask one clarifying question |

### 2. Off-topic / interference

If the request is unrelated to active project **and** not studio-meta:

- Acknowledge briefly
- Offer: answer shortly **or** park in `./studio learn "..."` / new ticket
- Do **not** mix off-topic implementation into project files

### 3. Not in backlog / sprint

After gate 2b:

- **No code** without a ticket
- **Wire the prototype.** After gate 2b, `app/` is the copy and `design/prototype/` stays the visual baseline. Implementation makes that copy work, then may enhance behavior, UI, interaction, and information architecture. See `docs/design/baseline.md`.
- **Separation of concerns.** A page or route handler does not embed the query, the storage call, or the business rule. Those live in a service. Infrastructure sits behind that service. See the backend playbook.
- **Harvest generic work.** Realtime, collaboration, object storage, and authentication leave a `./studio library promote` or a `./studio learn` on the receipt. Project look stays in the project. See the learning loop.
- Sprint-review ideas: `./studio feedback` → `clarify` → `ticket --from-feedback` (never direct ticket)
- Scoped new work: `./studio ticket <project> "..."` → groom → sprint
- Emergency scope change: user explicitly approves; log in `docs/phases/revisions.md` or the active milestone doc

## Team allocation (every ticket)

Before implementing, verify **team + skills** match ticket type — auto-match from `./studio ticket` is not enough.

See [ticket-team-allocation.md](ticket-team-allocation.md) for the mapping table.

- **UI design-track tickets:** Team `10-product-design-experience` + UX skills; aesthetic preset is optional; **write** `docs/design-specs/<TICKET>.md` + in-context token mocks (all states) **before** asking for `./studio approve-design`. A missing file is not HITL.
- **UI implement (non-design):** `01-frontend-experience` + `FE-001`, `FE-002` — stay on gate-2b project tokens + Headless library; missing primitives → design-track ticket
- **UI implement:** `01-frontend-experience` + `FE-001`, `FE-002` (and `FE-004` for contrast/a11y)
- **API / email / integrations:** `02-backend-systems` + relevant `BE-*` skills
- At groom: human or agent corrects wrong auto-assignment (e.g. email → backend, not AI)

## Milestones (post gate 2b)

1. Agent drafts `docs/phases/README.md` and one outline per version the PRD needs (M0, M1, M2, …). There is no fixed count.
2. Human approves roadmap before sprints or milestone tickets
3. Agent populates product backlog for **active milestone only** (`milestone: M0` in ticket frontmatter)
4. Sprints run within the milestone; sprint review unchanged
5. When all milestone tickets are `done` → **milestone review** before next milestone planning

See [milestone-planning.md](../.quinsy-studio/process/milestone-planning.md).

## Drift recovery

When conversation wanders, user says:

> **"Back on track"** / **"Resume project"** / **"Studio focus"**

Agent runs:

```bash
./studio focus <project>
./studio resume <project>
```

Then continues **only** the first action in the resume list.

## Human gates block implementation

Until gate 2b is approved, guard blocks implementation requests and redirects to pre-impl artifacts.

Gate 1 for a web project needs `Payload: in` in the blueprint, or `Payload: out` plus an ADR that opts out. After that signature, `./studio execute` writes `apps/web` when Payload is in. Follow [payload-playbook.md](../knowledge-base/payload-playbook.md). Do not add a second auth system, ORM, or content-translation package.

## Library loop (after 2b)

Gate 2b does **not** merge project UI into studio-library. Headless primitives stay studio-owned. Pull library → adapt brand in the project.

**Vendored admin shells (LO-0177 / LO-0178):** Reuse the shell’s Kanban, data table, Dialog, and Empty primitives before drawing a custom grid or a three-field inline create form. **Add** a new entity → full Dialog; **inspect** existing → Sheet.

## Sprint HITL (after gate 2b)

**Mid-sprint:** agent implements autonomously — do not ask the human for direction between tickets.

**Cadence review:** when `implementation_sprints_since_review` reaches `cost.human_review_every_sprints` (default 2), push **`origin/dev`** if a remote exists (`./studio ship --to dev`), then pause for human review. Off-cadence, receipts + gate 5 + per-ticket **commits** are enough. Never ticket review ideas directly. **Never implement review feedback in code**. Production/`main` push is HITL only.

```bash
./studio review <project>
./studio feedback <project> "..."
./studio clarify <project> FB-001 --approve
./studio ticket <project> "..." --from-feedback FB-001
./studio review <project> --approve
./studio groom <project> && ./studio retro <project> && ./studio sprint <project>
```

`./studio move … implement` is blocked during sprint review and after review until the next sprint is groomed.
