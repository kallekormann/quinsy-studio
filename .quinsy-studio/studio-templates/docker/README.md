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
./studio env <project> up      # docker compose -p <project> up -d
./studio env <project> status
./studio env <project> down
```

Compose file sets `name: <project>` and `container_name: <project>-postgres` so containers are **not** prefixed `docker-`.

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
