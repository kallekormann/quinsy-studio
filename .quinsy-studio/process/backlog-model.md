# Product Backlog Model (Sprint HITL)

> After gate 2 and **milestone roadmap approval**, tickets use a **simple folder model** — not the legacy 9-step Kanban folders.

## Milestones vs sprints

| Layer | Doc | Human gate |
|-------|-----|------------|
| **Milestone** (M0, M1, …) | `docs/phases/M0-*.md` | Roadmap approval; milestone review when all M* tickets done |
| **Sprint** (SPRINT-NN) | `sprints/SPRINT-NN/` | Scope proposal; sprint review |

Tickets carry `milestone: M0` in frontmatter. Sprint planning pulls from the **current milestone** in product backlog (+ blocked / feedback tickets groom approves).

See [milestone-planning.md](milestone-planning.md).

## Folders

| Location | Meaning |
|----------|---------|
| `projects/<p>/backlog/*.md` | **Product backlog** — unscheduled tickets (`status: backlog`, no `sprint:` tag) |
| `projects/<p>/backlog/*.md` + `sprint: SPRINT-NN` | **Sprint planned** — tagged, still in backlog until implementation starts |
| `projects/<p>/backlog/implement/` | **In progress** — current sprint execution |
| `projects/<p>/backlog/done/` | **Completed** |
| `projects/<p>/backlog/blocked/` | **Blocked** — waiting on human |

### Retired folders (legacy)

`open`, `analyze`, `plan`, `design`, `qa`, `review`, `reuse` — migrated to the layout above on `./studio sprint` or `./studio focus`.

**Do not use** `backlog/open/` for new tickets. The product backlog **is** `backlog/` (ticket files at the root of that directory).

## Sprint flow

```
Milestone roadmap approved (docs/phases/)
  → Agent writes active-milestone tickets → product backlog
Product backlog (backlog/*.md, milestone: M0, no sprint tag)
  → ./studio sprint <p>           # proposes scope (scope-proposal.md)
  → Human approves scope
  → ./studio sprint <p> --approve-scope
  → ./studio groom <p> --approve
  → backlog → implement → done   (autonomous mid-sprint)
  → ./studio review --approve
  → retro → next sprint (same milestone)
  → milestone review when all M* tickets done → plan next milestone
```

### Scope proposal

`./studio sprint` writes:

- `sprints/SPRINT-NN/scope-proposal.md` — human-readable proposed tickets + immature list
- `sprints/SPRINT-NN/planning-questions.md` — tickets **not ready** (need design/architecture/engineering input)

**Immature tickets stay in product backlog** until acceptance criteria are specific enough.

**Mid-sprint goal rewrite (LO-0060):** If feedback pulls a replacement ticket into the **current** sprint, update `plan.md` and mark superseded tickets `sprint_deferred: true` (or clear `sprint:`) in the same turn. Do not leave the plan describing the old goal.

**Mid-sprint maturity (LO-0058):** Replacement tickets often skip scope-proposal maturity. Before `implement`, ensure ≥2 specific BDD AC + Scope (design spec when design-track). Groom may still warn `IMMATURE_TICKET` until the body is filled.

Human checklist:

1. Review proposed tickets
2. Decide what to do with immature tickets (defer, clarify, update blueprint)
3. `./studio sprint <p> --approve-scope`
4. `./studio groom <p> --approve`

## Ticket lifecycle (sprint HITL)

```
backlog/  →  implement/  →  done/
```

The 9-step workflow (analyze, plan, design, qa, review, reuse) remains as **quality gates inside implementation** (tests, gate, reuse on `move … done`) — not as folder moves.

## Studio HQ vs project

| World | Backlog path | Folders |
|-------|--------------|---------|
| Studio LO items | `.quinsy-studio/backlog/open/` | open, done, blocked |
| Project tickets | `projects/<p>/backlog/` | backlog root + implement, done, blocked |
