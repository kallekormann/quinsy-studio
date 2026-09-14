# Quinsy Studio — Claude Code

Follow **[AGENTS.md](AGENTS.md)**. Same `./studio` loop as Cursor. Do not dump the backlog.

**Every turn:** `./studio guard <p> "<verbatim>"`. On `INBOX_ACK`, the note is queued — resume the same ACTION. Only abort preempts.

Session start: `./studio verify-worlds` → `./studio settings` → `./studio focus <project>` → `./studio execute <project>` until HITL.

Honor the COST line on execute. On `INFORM cost-cap`, stop stuffing files — raise the **named** key in product `docs/studio.settings.local.yaml` or HQ `.quinsy-studio/studio.settings.local.yaml` (`ledger=` on COST).

Keys stay in Claude Code / Anthropic login. Never write API keys into studio settings.

Product LLM keys (if a project uses Gemini, etc.) live in that project's `.env`, not here.

UI kit peers and agent-run migrations: see `AGENTS.md`.
