# Docker Base Template

This directory contains the studio's **base docker template**: Postgres with pgvector, and optional profiles for Redis, PgBouncer, MinIO, and the Python embedding worker. The Payload app is a second Compose file written into the project after gate 1. During project setup the base is copied into the project folder.

## Flow (Base → Project)

1. **Studio holds the essentials:** `docker-compose.yml`, `.env.example` — generic,
   parameterized with `{{PROJECT_NAME}}`.
2. **Project setup copies the base:** `./studio env <project> init` (or
   `python3 .quinsy-studio/studio-tools/init_project_env.py <project>`)
   → result: `projects/<name>/docker/docker-compose.yml` + `.env.example`
   with the real project name.
3. **Project extends ONLY in the project folder:** `payload-app.compose.yml` is written there after gate 1. Further services belong in `projects/<name>/docker/`. The template stays generic. `./studio env init` does not overwrite a Compose file that already exists.

## Running (from quinsy-studio root)

```bash
./studio env <project> up --approve   # inject named vars from projects/<project>/.env
./studio env <project> status
./studio env <project> down
```

`up`, `migrate`, and `dev` refuse without `--approve`. The first approved `up` creates gitignored `projects/<project>/.env` from `env.schema.json` plus `.env.example` and `docker/.env.example` when those exist. Existing values and comments stay. Compose receives `--env-file` pointing at that file. Logs print **names only**. Production values live in Coolify, not in a project `.env` on the VPS.

Compose file sets `name: <project>` and `container_name: <project>-postgres` so containers are **not** prefixed `docker-`.

## Payload local

`./studio env <project> up --approve` starts Postgres. After gate 1 signs `Payload: in`, the same command also starts the app container (`next dev` inside Docker, not on the host). `./studio env <project> migrate --approve` runs `payload migrate` in that container. Production Coolify runs migrate, then `node server.js`.

Do not publish host `5432` / `6379` / `3000` if those ports are already taken. Probe, then set `POSTGRES_HOST_PORT` / `REDIS_HOST_PORT` / `APP_HOST_PORT`. See [host-port-allocation.md](../../knowledge-base/host-port-allocation.md).

| Profile | Starts | When |
|---------|--------|------|
| (none) | Postgres, and the Payload app when `payload-app.compose.yml` exists | Always |
| `redis` | Redis 7 | Cache, rate limit, or the Python queue. Payload jobs do not need it |
| `pooler` | PgBouncer, session mode | Connection pressure. Local app traffic uses Postgres directly |
| `minio` | MinIO | Local stand-in for Cloudflare R2. Same `@payloadcms/storage-s3` adapter |
| `rag` | Python embedding worker, plus Redis | Long work. Vectors go in pgvector on this Postgres |

Turn a profile on from the blueprint `Profiles:` line, or `./studio env <project> up --approve --profile minio`.

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
