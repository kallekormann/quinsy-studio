# Skill: Secrets Hygiene

> Keeps credentials out of code, bundles, images, logs and git history, and makes every secret rotatable. A committed secret counts as leaked from the commit time. Removing it from the code is not the fix; rotating it at the provider is.

## Metadata

```
skill_id: PE-006
name: Secrets Hygiene
team: 08-platform-enterprise-engineering
lead_role: Platform Architect
support_roles: [Backend Security Engineer, DevOps Engineer]
phases: [1, 3, 4, 5, 7]
activation_triggers:
  - Ticket adds or renames an environment variable, API key, webhook secret or third-party account
  - Ticket touches env.schema.json, .env.example, Dockerfile, Compose files or Coolify settings
  - Before ./studio ship <p> --to main
  - Any suspected leak (key in a commit, log, screenshot or chat)
pairs_with: [PE-003, PE-005, PE-007, AI-005, PE-002]
```

## When to load

- Gate 1: write the first `docs/security/secrets-inventory.md` from the threat model's `secret` data classes.
- Any ticket that adds a variable or an external service.
- Before every `./studio ship <p> --to main --approve`.
- Immediately on a suspected leak (then also load PE-007).

## Rules

### 1. Names in files, values out of files

- Names and purpose go in `env.schema.json` and `.env.example`. `.env.example` has empty values or obvious placeholders (`changeme-local`), never a real value.
- Desktop values live in gitignored `projects/<p>/.env`. Production values live in Coolify environment variables. Nowhere else: not in Compose files, not in `next.config.mjs`, not in docs, not in tickets.
- The agent does not Read, Grep or print `.env` values. Values reach containers only through `./studio env <p> up|migrate|dev --approve`.
- `.gitignore` covers `.env`, `.env.*` except `.env.example`, `*.pem`, `*.key`.

### 2. Nothing secret reaches the browser

- `NEXT_PUBLIC_*` values are inlined into the client bundle at build time. Only values designed to be public may use the prefix (site URL, Stripe publishable key, analytics site id).
- A server secret is never imported into a `"use client"` file or a module it imports.
- Check: grep the built `.next/static` output for each secret name's value pattern after `next build` (gate check `client_env_leak`).

### 3. Fail loudly when a secret is missing

- No `process.env.X || ''`, `|| 'secret'`, `?? 'changeme'` or `os.getenv("X", "default")` for secrets.
- Use a `requireEnv(name)` helper that throws with the variable name and the `./studio env` hint.
- One allowed exception: during `next build` (`process.env.NEXT_PHASE === 'phase-production-build'`) the helper may return `''`, because Coolify builds without runtime secrets. The Payload template's `payload.config.ts` shows the pattern.
- Gate check `insecure_env_fallback` flags fallbacks on names listed as secrets in `env.schema.json`.

### 4. Images never carry secrets

- No `ARG` or `ENV` with a secret in any Dockerfile. No `COPY .env`. `.dockerignore` lists `.env*`.
- In Coolify, secrets are runtime variables. Do not tick "Build Variable" for a secret; build args are stored in image metadata and build logs.
- Check: `docker history --no-trunc <image>` shows no secret names with values (gate check `docker_secret_leak`).

### 5. Secrets stay out of logs, URLs and errors

- Never log a token, password, cookie, `Authorization` header, webhook secret or full request body. Log ids and event names.
- Never put a token in a query string; reset and magic links use one-time tokens that expire.
- Error responses to clients carry no stack, no DSN, no env dump.

### 6. One credential per purpose and environment

- Local, dev and production use different values. A shared value means one leak burns every environment.
- Third-party keys are scoped to the least permission the provider offers (restricted Stripe keys, bucket-scoped R2 tokens).
- `PAYLOAD_SECRET` is long and random (for example `openssl rand -hex 32`), unique per environment.

### 7. Keep a secrets inventory

`docs/security/secrets-inventory.md`, one row per secret. Columns: Name, Purpose, Owner (person), Where stored (`.env` local / Coolify app / Coolify service), Environments, Rotation (cadence or "on leak"), Revocation path (provider page or API), Last rotated. Never a value, never a prefix or suffix of a value.

### 8. Scan history before main

Before `ship --to main`, run a secret scanner over the full git history of the product repo (for example gitleaks: `gitleaks git` on v8.19+, `gitleaks detect` on older versions). A hit blocks the ship until the secret is rotated (rule 9). Tune false positives with an allowlist file in the repo, not by skipping the scan.

### 9. Leak response order

1. Rotate at the provider: revoke the exposed value, issue a new one. This is the fix.
2. Put the new value in Coolify and local `.env` via `./studio env … --approve`; redeploy.
3. Check provider logs for use during the exposure window (commit time to revocation).
4. Rewrite git history only after rotation, and only with the human's approval (history rewrite is HITL).
5. Add the pattern to the scanner allowlist rules or a new gate check.
6. If the key gave access to personal data and was used, it is a breach: hand off to PE-007.

## Workflow

1. Read `env.schema.json` and `.env.example` (names only).
2. For each new variable: add name + purpose to `env.schema.json`, empty entry to `.env.example`, row to the inventory.
3. Wire it through `requireEnv` on the server side only.
4. Tell the human which named value to add; inject with `./studio env <p> … --approve`.
5. Run gate checks `secret_scan`, `client_env_leak`, `insecure_env_fallback`, `docker_secret_leak` (level 2).
6. Before main: history scan (rule 8), inventory complete, no shared values across environments.

## Deliverables

- Updated `env.schema.json`, `.env.example`, `.gitignore`, `.dockerignore`.
- `docs/security/secrets-inventory.md`.
- A rotation runbook section in the inventory: per provider, the exact page or API call to revoke and reissue.

## Done evidence (receipt)

Receipt section `## Security` with PASS / FAIL / N/A per item:

- `secret_scan` (working tree) — PASS / FAIL
- `client_env_leak` — PASS / FAIL, list of `NEXT_PUBLIC_` names and why each is public
- `insecure_env_fallback` — PASS / FAIL
- `docker_secret_leak` — PASS / FAIL / N/A
- Inventory updated — path and new row names
- History scan (only before `ship --to main`) — tool, version, result

## Anti-patterns

- `const key = process.env.STRIPE_SECRET_KEY || ''` in runtime code.
- `NEXT_PUBLIC_OPENAI_API_KEY`.
- A real value in `.env.example` "for convenience".
- `ARG DATABASE_URL` in the Dockerfile so `next build` can reach the database.
- Marking a leak resolved after deleting the line.
- One `PAYLOAD_SECRET` for local and production.

## Handoff

- To PE-007: any leak where the credential was used or reached personal data.
- To PE-002: the four level-2 checks and the history scan in the ship path.
- To PE-003: inventory and scan results as audit evidence at phase 5.
- To the human: the list of named values to set in Coolify (names only).

## References

- CWE-798 (hard-coded credentials), CWE-312 (cleartext storage), CWE-532 (sensitive data in logs).
- OWASP Secrets Management Cheat Sheet.
- Next.js docs: environment variables and the `NEXT_PUBLIC_` prefix.
- `studio-templates/env.schema.json`, `studio-templates/payload/app/src/payload.config.ts`.
- Source: agency-agents `security/security-secrets-credential-engineer.md` (MIT), rewritten for Compose and Coolify.
