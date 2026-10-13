# Foundation

A website or web app runs on Payload inside one Next.js app, `apps/web`. That app is written after you sign gate 1, on the next execute. It is not created when the folder is first made.

The blueprint says `Payload: in`, or `Payload: out` with an ADR that opts out. Gate 1 refuses a web project that has neither. A game or an API service may omit the line.

| Piece | Where it lives |
|-------|----------------|
| Marketing pages | `apps/web/src/app/(marketing)` |
| Signed-in product | `apps/web/src/app/(app)` |
| Admin and REST | `apps/web/src/app/(payload)` — `/admin` and `/api` |
| Auth, content, jobs | Payload. Users is an auth collection. Do not add a second auth system, ORM, or content-translation package. |
| Email | Resend, when the key is set |
| Payments | The `billing` package. Pull it. |
| Database | Postgres in Docker locally. A Coolify database in production. |
| Uploads | Local disk in dev. Object storage in production. |
| Long work | A worker. A Payload job only enqueues it. |
| Locales | One default unless the blueprint lists more. Payload localizes the fields. |

Desktop, a browser extension, and mobile call the API. They do not embed Payload.

The how-to the agent reads is [payload-playbook.md](../knowledge-base/payload-playbook.md). Skill BE-007 is on the card when Payload is in. Team 10 specs the marketing and app surfaces. Team 10 does not restyle `/admin`.

## Secrets

| Where | What |
|-------|------|
| `env.schema.json` and `*.env.example` | Names. Safe to read. |
| `projects/<project>/.env` | Local values. Gitignored. The agent injects them with `./studio env`. It does not print them. |
| `projects/<project>/.env.local` | Production access names: host, Coolify, the production database URL. `./studio env <project> prod --explain` says which names are set and what they are for. It does not print values. |
| Coolify | Production values. There is no project `.env` on the server. |

`./studio env <project> up`, `migrate`, and `dev` are agent-run. You are told they ran. A production migration and any destructive reset wait for you.

## Production

`docker/compose.prod.yml` is the production-shaped stack. Coolify installs from `package.json` and migrates before the new container serves traffic. `./studio ship` only pushes git.

`./studio ship <project> --to dev` is the agent, before a cadence brief. `./studio ship <project> --to main --approve` is you. It refuses when the readiness check fails.

The agent can deploy, read logs, and check status with `./studio ops`. Those lines land in the product's `docs/ops/ops-log.md`.
