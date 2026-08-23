# Agent Context Protocol

> How the IDE agent stays in studio/project scope and recovers from drift.

## Session start

1. Read [`AGENTS.md`](../../AGENTS.md)
2. Run `./studio bootstrap` or `./studio focus <project>`
3. Run `./studio resume <project>` — execute listed actions only

Active project is stored in `.quinsy-studio/.active-project.json`.

## Three context layers

| Layer | Scope | Examples |
|-------|-------|----------|
| **Studio meta** | `.quinsy-studio/` | LO-* tickets, process, tools, library |
| **Project** | `projects/<name>/` | PRD, gates, tickets, code |
| **Off-topic** | Neither | Unrelated questions |

## When the user asks something

### 1. Check active project

```bash
./studio focus <project>    # set + print scope banner
./studio guard <project> "user request text"
```

| Verdict | Agent action |
|---------|--------------|
| `in_scope` | Proceed; tie work to ticket ID if post-gate-2 |
| `needs_ticket` | Do **not** implement — create `./studio ticket` or ask user |
| `pre_impl` | Redirect to current gate (`./studio resume`) |
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

- **UI design-track tickets:** Team `10-product-design-experience` + UX skills; human `./studio approve-design` before implement
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
