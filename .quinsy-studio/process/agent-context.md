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
- Emergency scope change: user explicitly approves; log in `docs/phases/revisions.md`

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

When sprint tickets are done, pause for human review — never ticket sprint-review ideas directly:

```bash
./studio review <project>
./studio feedback <project> "..."
./studio clarify <project> FB-001 --approve
./studio ticket <project> "..." --from-feedback FB-001
./studio review <project> --approve
```

See [human-in-the-loop.md](human-in-the-loop.md#sprint-cadence-hitl-after-gate-2).
