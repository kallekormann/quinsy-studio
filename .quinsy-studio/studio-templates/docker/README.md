# Docker Base Template

This directory contains the studio's **base docker template** with the essentials
(PostgreSQL, Redis, optional app service). During project setup it is copied into
the project folder as the foundation and extended there per project.

## Flow (Base → Project)

1. **Studio holds the essentials:** `docker-compose.yml`, `.env.example` — generic,
   parameterized with `{{PROJECT_NAME}}`.
2. **Project setup copies the base:** `./studio env <project> init` (or
   `python3 .quinsy-studio/studio-tools/init_project_env.py <project>`)
   → result: `projects/<name>/docker/docker-compose.yml` + `.env.example`
   with the real project name.
3. **Project extends ONLY in the project folder:** additional services (Mailpit, MinIO,
   queue workers), build contexts, custom volumes belong in
   `projects/<name>/docker/` — the template stays generic.

## Running (from quinsy-studio root)

```bash
./studio env <project> up --approve   # inject named vars from projects/<project>/.env
./studio env <project> status
./studio env <project> down
```

`up`, `migrate`, and `dev` refuse without `--approve`. The first approved `up` creates gitignored `projects/<project>/.env` from `env.schema.json` plus `.env.example` and `docker/.env.example` when those exist. Existing values and comments stay. Compose receives `--env-file` pointing at that file. Logs print **names only**. Production values live in Coolify, not in a project `.env` on the VPS.

Compose file sets `name: <project>` and `container_name: <project>-postgres` so containers are **not** prefixed `docker-`.

## Supabase local (projects using Supabase CLI)

This template is **generic Postgres**. **Do not leave host `5432` / `6379` if those ports are already published** on the machine (normal when several project stacks run). Probe, then set `POSTGRES_HOST_PORT` / `REDIS_HOST_PORT` in the **project** `docker/.env`. Procedure: [host-port-allocation.md](../../knowledge-base/host-port-allocation.md).

Supabase-local projects use the **Supabase stack** on **unclaimed** host ports (defaults 54321–54323 are often taken). Not legacy `db:migrate` against port 54320.

| Task | Command (in project repo) |
|------|---------------------------|
| Start Supabase | `npx supabase start` or project `npm run supabase:start` |
| Apply migrations | `npm run db:migrate:supabase` (not `db:migrate` on 54320) |
| Env | Copy from `supabase status` → `.env.local` |

Document the project's migrate script in `docs/architecture/` at gate 1. Agents: load `.env.local` before `psql` / connection tests.

## Placeholders

| Placeholder        | Replaced by        |
|--------------------|--------------------|
| `{{PROJECT_NAME}}` | project name       |

## Rules

- **NEVER** commit project-specific config into the template.
- **No** fixed passwords/secrets in the template (only dev defaults, overridable via `.env`).
- If a project needs an improvement that is *universally* useful
  (e.g. a healthcheck, a new base service) → update the template
  (global loop), not just the project (local loop).
