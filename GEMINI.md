# Quinsy Studio — Gemini CLI

Follow **[AGENTS.md](AGENTS.md)**. Same `./studio` loop as Cursor. Do not dump the backlog.

**Every turn:** `./studio guard <p> "<verbatim>"`. On `INBOX_ACK`, the note is queued — resume the same ACTION. Only abort preempts.

Session start: `./studio verify-worlds` → `./studio settings` → `./studio focus <project>` → `./studio execute <project>` until HITL.

Honor the COST line on execute. On `INFORM cost-cap`, stop stuffing files — tell the human to raise the **named** key in `.quinsy-studio/studio.settings.local.yaml`.

Keys stay in Gemini CLI (`GEMINI_API_KEY` or Google login). Never write API keys into studio settings.

Product LLM keys in a project `.env` are not the coding-agent key.
