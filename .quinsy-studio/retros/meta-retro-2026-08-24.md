# Meta-Retro — 2026-08-24

## Project: moody (SPRINT-25)

- Retro: [projects/moody/sprints/SPRINT-25/retro.md](../../projects/moody/sprints/SPRINT-25/retro.md)
- Shipped: MOOD-0069–0072 (team permissions, home grouping, collaborator share policy)
- Review: 6 feedback items; 5 ticketed for SPRINT-26

## Learnings (SPRINT-25)

| Theme | Observation | Studio action |
|-------|-------------|---------------|
| **Ticket maturity** | Feedback-derived tickets were flagged immature despite full BDD; planner required `**Scope:**` in markdown body | Fixed `assess_ticket_maturity` to read `phase` from frontmatter; document `**Scope:**` in ticket template |
| **DB / Docker** | Agents suggested `psql $DATABASE_URL` without loading `.env.local`; moody uses Supabase on 54322 not legacy 54320 | `db:migrate:supabase` script + docker README (moody); session checklist |
| **Local-first sync** | One-time migration gate left new boards local-only; share broke | Product pattern: sync on create, open, login, online — document in agent-context for canvas apps |
| **Empty retros** | `./studio retro` only writes templates; agent skipped fill-in | Process update: agent must complete retro + meta-retro before sprint planning |

## Incoming learning items

- **LO-0002** — Mature feedback tickets need explicit Scope in body (process-gap)
- **LO-0003** — Supabase local migrations vs legacy `db:migrate` (tooling-gap)
- **LO-0004** — Local-first apps need continuous cloud metadata sync (process-gap)
- **LO-0005** — Agent must populate sprint retro and meta-retro (process-gap)

## Action items

- [x] Fix sprint maturity phase check (frontmatter) — `sprint_planning.py`
- [x] Regenerate SPRINT-26 scope with matured MOOD-0074–0078
- [ ] Human: approve SPRINT-26 scope
- [ ] Add ticket template note for `**Scope:**` when `--from-feedback` (LO-0002)
