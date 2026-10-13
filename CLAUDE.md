# Quinsy Studio — Claude Code

Follow **[AGENTS.md](AGENTS.md)**. Same `./studio` loop as Cursor. Do not dump the backlog.

**Every turn:** `./studio guard <p> "<verbatim>"`. On `INBOX_ACK`, the note is queued — resume the same ACTION. Only abort preempts.

Session start: `./studio verify-worlds` → `./studio settings` → `./studio focus <project>` → `./studio execute <project>` until HITL.

Honor the COST line on execute. On `INFORM cost-cap`, stop stuffing files — raise the **named** key in product `docs/studio.settings.local.yaml` or HQ `.quinsy-studio/studio.settings.local.yaml` (`ledger=` on COST).

Keys stay in Claude Code / Anthropic login. Never write API keys into studio settings.

**Docker is required.** Do not Read `.env` / `.env.local` **values** — names only (`env.schema.json`). Local inject `./studio env <p> up|migrate|dev` is agent-run INFORM. Production: `./studio env <p> prod --explain` lists the `.env.local` names for the human; `./studio ops <p> …` runs deploy/logs/status/db/cleanup; only `migrate --prod --approve` and destructive steps wait. One chat per product (`parallel.max_projects`, default 5). Session bind (`./studio bind`) is Cursor-only (`runtime: cursor` in HQ settings). This Claude Code session keeps workspace `focus` / `execute` isolation. `./studio focus` will not clobber a live lease unless `--force`. HQ train is a **separate** session; product execute INFORM open LO counts and must not steal the chat for `STUDIO_LO` mid-project. HITL is gates 0/1/2a/2b, milestone roadmap and reviews, `approve-design --phase`, `ship --to main`, production migration, tech-veto — not a morning brief. Architecture, cadence review, local env and ops are INFORM.

Product LLM **names** belong in `env.schema.json`; **values** belong in gitignored `projects/<p>/.env` on the desktop and in Coolify in production, not in this file.

UI kit peers and agent-run migrations: see `AGENTS.md`.
