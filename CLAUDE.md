# Quinsy Studio — Claude Code

Follow **[AGENTS.md](AGENTS.md)**. Same `./studio` loop as Cursor. Do not dump the backlog.

Session start: `./studio verify-worlds` → `./studio settings` → `./studio focus <project>` → `./studio execute <project>` until HITL.

Honor the COST line on execute. On `INFORM cost-cap`, stop stuffing files — tell the human to raise the **named** key in `.quinsy-studio/studio.settings.local.yaml`.

Keys stay in Claude Code / Anthropic login. Never write API keys into studio settings.

Product LLM keys (if a project uses Gemini, etc.) live in that project's `.env`, not here.
