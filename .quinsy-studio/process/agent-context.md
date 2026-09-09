# Agent Context Protocol

> How the IDE agent stays in studio/project scope and recovers from drift.

## Every turn (before session start)

Run `./studio guard <project> "<verbatim user message>"` first. While implementation is in flight on that project, guard returns `INBOX_ACK`, queues the note, and the agent resumes `./studio execute`. Do not treat the bubble as a new assignment. Drain after `MOVE_DONE`. Exceptions: abort; “back on track”; explicit gate / design / review approval.

## Session start

1. Read [`AGENTS.md`](../../AGENTS.md)
2. Run `./studio bootstrap` (new PRD), `./studio adopt <p> --from …` (existing codebase), or `./studio focus <project>`
3. Run `./studio settings` (merged policy + estimated usage). Defaults cover a **medium project**.
4. Run `./studio execute <project>` — do the `NEXT` command, then execute again, until `ACTION` is `HITL`
5. If `ACTION` is `INFORM` (inbox drain / reuse brief), do NEXT and loop — do not wait for a signature. Architecture and design are HITL, not inform.
6. If `ACTION` is `INFORM` and the reason is `cost-cap`, **stop**. Do not keep stuffing files. The human raises the **named** yaml key in `studio.settings.local.yaml`, then execute continues.
7. If `ACTION` is `STUDIO_LO`, the product loop is idle — infuse in `.quinsy-studio/` now. Mid-sprint gaps: spawn `./studio train` and keep `IMPLEMENT`
8. Mid-execute human messages: `./studio guard` → `INBOX_ACK` (auto-queued). Resume NEXT. Drain after MOVE_DONE
9. `./studio resume <project>` is a human-readable checklist; do not stop after printing it

Do **not** ask “should I continue?” mid-sprint. Loop until HITL. Compact cards only — do not load the whole backlog.

**Docker / local URLs:** before pinning Compose host ports or `next dev` ports, probe `docker ps` published ports. Operators run multiple stacks. See [host-port-allocation.md](../knowledge-base/host-port-allocation.md).

Active project is stored in `.quinsy-studio/.active-project.json`.

## Sibling isolation

The IDE workspace is Studio HQ, so every `projects/<name>/` tree is on disk. After `./studio focus <project>` (also reapplied on `execute` and `verify-worlds`):

- Sibling folders are listed in a local `.cursorignore` so Read/Grep/Glob should not see them
- A generated Cursor rule names the **only** allowed product tree
- Guard returns `cross_project` if the request names a sibling folder
- Project `pre-commit` refuses a wrong git toplevel and staged `projects/` symlinks

Do not use Shell to `ls`/`cp`/`git` a sibling. Switch products with `./studio focus <other>` in a new session — never merge two product gits.

## Three context layers

| Layer | Scope | Examples |
|-------|-------|----------|
| **Studio meta** | `.quinsy-studio/` | LO-* tickets, process, tools, library |

Studio HQ must stay **project-agnostic** in docs/tools — see [studio-abstraction.md](studio-abstraction.md). Run `./studio verify-abstraction` after studio edits.
| **Project** | `projects/<name>/` | PRD, gates, tickets, code |
| **Off-topic** | Neither | Unrelated questions |

## When the user asks something

### 0. Mid-execute inbox (first)

If the previous turn was execute-loop work, `./studio guard` is still the first command — it returns `inbox_ack` and queues the note. Skip the rest of this section until after drain.

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
| `cross_project` | Request names a sibling `projects/` folder — even mid-execute. Do not Read/copy/git it. `./studio focus` to switch. Do not queue as an inbox note. |
| `in_scope` | Proceed; tie work to ticket ID if post-gate-2 |
| `needs_ticket` | Do **not** implement — create `./studio ticket` or ask user |
| `pre_impl` | Redirect to current gate (`./studio resume`) |
| `feedback_only` | Sprint review HITL — capture feedback, do not code |
| `studio_meta` | Studio backlog only — not project code |
| `unclear` | Ask one clarifying question |

### 2. Off-topic / interference

If the request is unrelated to active project **and** not studio-meta:

- Acknowledge briefly
- Offer: answer shortly **or** park in `./studio learn "..."` / new ticket
- Do **not** mix off-topic implementation into project files

### 3. Not in backlog / sprint

After gate 2:

- **No code** without a ticket
- Sprint-review ideas: `./studio feedback` → `clarify` → `ticket --from-feedback` (never direct ticket)
- Scoped new work: `./studio ticket <project> "..."` → groom → sprint
- Emergency scope change: user explicitly approves; log in `docs/phases/revisions.md` or the active milestone doc

## Team allocation (every ticket)

Before implementing, verify **team + skills** match ticket type — auto-match from `./studio ticket` is not enough.

See [ticket-team-allocation.md](ticket-team-allocation.md) for the mapping table.

- **UI design-track tickets:** Team `10-product-design-experience` + UX skills + [aesthetic preset](.quinsy-studio/knowledge-base/aesthetic-presets/README.md); **§2 Context & placement** required ([contextual-ia-playbook.md](.quinsy-studio/knowledge-base/contextual-ia-playbook.md)); human `./studio approve-design` before implement
- **UI implement:** `01-frontend-experience` + `FE-001`, `FE-002` (and `FE-004` for contrast/a11y)
- **API / email / integrations:** `02-backend-systems` + relevant `BE-*` skills
- At groom: human or agent corrects wrong auto-assignment (e.g. email → backend, not AI)

## Milestones (post gate 2)

1. Agent drafts `docs/phases/README.md` + milestone outlines (M0, M1, …)
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

Until gate 2 is approved, guard blocks implementation requests and redirects to pre-impl artifacts.

## Library loop (gate 2)

On design approval, base UI flows to studio-library (see `library_promotion.py`):

- Tokens merged → `studio-library/ui/tokens/`
- Atoms/molecules/organisms → `studio-library/ui/components/`
- Sticker sheet → `studio-library/ui/sticker-sheet/`

Projects **consume** library via `./studio sync <project>`; they **feed** library on gate 2.

## Sprint HITL (after gate 2)

**Mid-sprint:** agent implements autonomously — do not ask the human for direction between tickets.

**Sprint review:** when all sprint tickets are `done`, pause for human review — never ticket sprint-review ideas directly. **Never implement review feedback in code** — only `./studio feedback` → clarify → ticket for the **next** sprint.

```bash
./studio review <project>
./studio feedback <project> "..."
./studio clarify <project> FB-001 --approve
./studio ticket <project> "..." --from-feedback FB-001
./studio review <project> --approve
./studio groom <project> && ./studio retro <project> && ./studio sprint <project>
```

`./studio move … implement` is blocked during sprint review and after review until the next sprint is groomed.
