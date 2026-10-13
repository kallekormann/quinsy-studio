# Setup

## What you install

You need Node.js 20 or newer, Git, and Docker Desktop. Docker is required to boot a product, run migrations, and pass a gate. There is no fallback that prints secret values into the chat.

```bash
git clone <this-repo>
cd quinsy-studio
./studio install
./studio verify-worlds
./studio verify-abstraction
```

`./studio install` adds the UI packages the studio library expects. `node_modules/` is not in git. Optional extra skill packages: `./studio install --with-skills`.

Open the repo at the **studio root** (the folder that contains `./studio` and `.quinsy-studio/`). Do not open only `projects/<name>/`.

## Where things live

| What | Where | Whose git |
|------|--------|-----------|
| Studio process, skills, library, this manual | `.quinsy-studio/` | The studio repo |
| The `./studio` command | `studio` at the repo root | The studio repo |
| A product | `projects/<name>/` | That product's own repo |
| Research notes before a product exists | `ideation/` | Not committed |
| A product definition you drop in by hand | `intake/` | Not committed |

Studio git never stores a product. Product git never stores the studio. `./studio verify-worlds` checks that split.

## Which app you use

Open the same folder in Cursor, Claude Code, or a terminal agent. API keys stay in that app. They are never written into studio settings.

The studio reads one switch, `runtime`, in `.quinsy-studio/studio.settings.yaml`:

| Value | What you get |
|-------|----------------|
| `cursor` | Several products in one Cursor window. Each chat binds its own product. See [Several products at once](03-several-products.md). |
| anything else | One workspace focus at a time. `./studio focus <project>` hides the other products. Claude Code and a plain CLI use this. |

A missing `runtime` key is treated as `cursor`. To turn the Cursor multi-chat behavior off, set `runtime` to another value, for example `claude` or `cli`. There is no second switch.

## Secrets

Agents may read **names** of environment variables (`env.schema.json`, `.env.example`). They must not read **values** from `.env` or `.env.local`.

| File | Who fills it | What it is |
|------|----------------|------------|
| `projects/<name>/.env` | You, on your machine | Local Docker values. Gitignored. |
| `projects/<name>/.env.local` | You | Production access names (SSH, Coolify). Gitignored. |
| Coolify | You, in the host | Production values. Nothing from `.env` is copied to the server by the studio. |

`./studio env <project> prod --explain` lists the production names and whether each one is set. It does not print the values.

`./studio env <project> up` starts the local stack. The agent may run that. You do not have to migrate by hand on your machine.

## After setup

Pick one row in [The path](04-the-path.md) and open a chat. Say the sentence. The agent runs the commands.
