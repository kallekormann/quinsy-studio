# Quinsy Studio — Claude Code

Follow **[AGENTS.md](AGENTS.md)**. Same `./studio` loop as Cursor. Do not dump the backlog.

**Every turn:** `./studio guard <p> "<verbatim>"`. On `INBOX_ACK`, the note is queued — resume the same ACTION. Only abort preempts.

Session start: `./studio verify-worlds` → `./studio settings` → `./studio focus <project>` → `./studio execute <project>` until HITL.

Honor the COST line on execute. On `INFORM cost-cap`, stop stuffing files — raise the **named** key in product `docs/studio.settings.local.yaml` or HQ `.quinsy-studio/studio.settings.local.yaml` (`ledger=` on COST).

Keys stay in Claude Code / Anthropic login. Never write API keys into studio settings.

**Docker is required.** Do not Read `.env` **values** — names only (`env.schema.json`). Inject with `./studio env <p> up|migrate|dev --approve`. One chat per product (`parallel.max_projects`, default 5). `./studio focus` will not clobber a live lease unless `--force`. HQ train is a **separate** session; product execute INFORM open LO counts and must not steal the chat for `STUDIO_LO` mid-project. HITL is packet sign-off or env `--approve`, not a morning brief.

Product LLM **names** belong in `env.schema.json`; **values** in the host secret store, not this file.

UI kit peers and agent-run migrations: see `AGENTS.md`.
