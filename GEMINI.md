# Quinsy Studio — Gemini CLI

Follow **[AGENTS.md](AGENTS.md)**. Same `./studio` loop as Cursor. Do not dump the backlog.

**Every turn:** `./studio guard <p> "<verbatim>"`. On `INBOX_ACK`, the note is queued — resume the same ACTION. Only abort preempts.

Session start: `./studio verify-worlds` → `./studio settings` → `./studio focus <project>` → `./studio execute <project>` until HITL.

Honor the COST line on execute. On `INFORM cost-cap`, stop stuffing files — tell the human to raise the **named** key in product `docs/studio.settings.local.yaml` or HQ `.quinsy-studio/studio.settings.local.yaml`.

Keys stay in Gemini CLI (`GEMINI_API_KEY` or Google login). Never write API keys into studio settings.

**Docker is required.** Do not Read `.env` **values**. Inject with `./studio env <p> up|migrate|dev --approve`. One chat per product; `focus --force` only to steal isolation. HQ train is a **separate** session.

Product LLM names in `env.schema.json` are not the coding-agent key.

UI kit peers and agent-run migrations: see `AGENTS.md`.
