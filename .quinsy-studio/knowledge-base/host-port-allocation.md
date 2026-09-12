# Host port allocation (local Docker and dev servers)

Operators run **more than one project stack** on the same machine. Published host ports collide even when Compose `name:` prefixes container names.

Do **not** ship `5432:5432`, `6379:6379`, `3000:3000`, or Supabase CLI defaults (`54321`–`54323`) without probing. Those bindings are often already taken.

This is an agent rule, not a new `./studio` command.

## When it applies

- Writing or copying `docker-compose.yml`
- `./studio env <project> init` follow-up (template defaults are not a reservation)
- Pinning `next dev`, Filament, Mailpit, MinIO, or Supabase local URLs
- Gate 1 architecture notes that list local URLs

## Probe (before pinning)

```bash
docker ps --format '{{.Names}}\t{{.Ports}}'
```

On macOS, also:

```bash
lsof -nP -iTCP -sTCP:LISTEN
```

Pick host ports that do not appear. Prefer a **project offset** (for example 15xxx / 16xxx) over “the textbook port.”

## How to pin

1. Host ports live in the **project** `docker/.env` (or `.env.example`), not hardcoded in the studio template.
2. Compose maps `${POSTGRES_HOST_PORT}:5432` (container port stays standard; host port moves).
3. List the chosen host ports in project `RUNBOOK.md` (Postgres, Redis, HTTP apps, Supabase API/DB/Studio if used).
4. App env (`DATABASE_URL`, `REDIS_URL`, `NEXT_PUBLIC_*`) must use those host ports on the host, and internal Compose DNS on the overlay network.
5. Human smoke for UI tickets uses the **RUNBOOK compose URL**, not a guessed port. Do not hard-code another product’s host port into studio HQ.

Do not stop or rebind another project’s containers to free a default port.

## Related

- LO-0026: Next.js **dev** port collision / stale `.next` (review 500) is a different failure; this file is **Compose and long-running stacks**.
- [backend_playbook.md](backend_playbook.md) — migrate commands still use the **project** ports, not 54320-by-habit.
