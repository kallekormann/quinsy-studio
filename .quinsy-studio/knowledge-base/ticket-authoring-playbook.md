# Ticket authoring playbook

> Tickets are a **contract for the implementer**, including small/fast models. If the ticket is ambiguous, the model will invent. Write the contract; do not hope for judgment.

Compact product tickets (Target / Scope / AC) stay the default. At **groom**, expand any ticket a small model will implement so the sections below are present. XL tickets are never groomed into a sprint — split them.

## Six failure modes (and ticket-level antidotes)

| ID | Failure | Antidote (author this; do not leave it to the implementer) |
|----|---------|-----------------------------------------------------------|
| F1 | Invention under ambiguity | **Verbatim artifacts** — literal DDL, function signatures, enum values, CSS variable names, copy strings. Never “a status enum” or “the usual columns.” |
| F2 | Wrong location | **Exact paths per Plan step** — one file (or one directory with a glob) per step. No “update the API layer.” |
| F3 | Declaring done without verifying | **Verify** — literal shell/test commands and the **expected output** (or assertion). “Tests pass” is not a command. |
| F4 | Scope drift | **Do not touch** — list files/dirs owned by parallel tickets or out of this slice. |
| F5 | Context loss | **Size cap** — ≤8 files, ≤400 lines of planned change, **no XL**. Split instead of stuffing. |
| F6 | Silent assumption | **Stop and ask if** — named triggers that escalate instead of inventing (missing table, unclear name, conflicting spec). |

## Required sections (groomed / small-model tickets)

1. **Target** — one outcome sentence.
2. **Read first** — ≤5 files the implementer must open before editing.
3. **Plan** — one step per file (or one directory with a stated glob).
4. **Verbatim artifacts** — paste the names, SQL, types, and strings that must appear unchanged.
5. **Verify** — commands + expected output.
6. **AC** — ≥2 specific Given/When/Then (not “works as described”).
7. **Do not touch** — named paths.
8. **Stop and ask if** — named triggers.
9. **Out of scope** — what this ticket must not start.

## Sizing

| Estimate | Files | Planned loc | Action |
|----------|-------|-------------|--------|
| S | 1–3 | ≤150 | One implementer, one session |
| M | ≤6 | ≤400 | Default max for a small-model ticket |
| L | ≤8 | ≤400 | Split if the eighth file is a new concern |
| XL | >8 or >400 | — | **Forbidden in sprint.** Split; the earlier ticket writes shared names verbatim |

## Shared names across tickets

If two tickets must agree on a name (table, enum, CSS variable, route, env key), the **earlier ticket writes it verbatim** and the **later ticket quotes that artifact**. Do not let both invent.

## Frontmatter

```yaml
executable_by: composer   # composer | opus | human
estimate: M                # never XL in a sprint
```

- `composer` — contract complete (all sections above). Small/fast models may implement.
- `opus` — needs judgment (architecture, ambiguous product call). Still include Verify and Do not touch.
- `human` — HITL-only (credentials, destructive ops, design approval). Do not assign to a model as IMPLEMENT.

See also `process/ticket-team-allocation.md` (groom checklist) and `process/ticket-workflow.md` (compact vs groomed body).
