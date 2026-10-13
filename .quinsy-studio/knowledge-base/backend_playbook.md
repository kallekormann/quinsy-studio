# Backend Playbook

> Domain-driven design (DDD), SOLID, JSONb EAV structures — the global backend standards.

## Core principle

```
Secure. Scalable. Maintainable.
Every decision is documented.
```

## Implementer rules (Do / Don’t / fail)

| Topic | Do | Don’t | Implement-fail |
|-------|----|-------|----------------|
| API (BE-001) | Resource nouns, explicit error envelope, version at the boundary | Hide breaking changes in a 200 HTML page | Client cannot tell 4xx vs 5xx |
| DB (BE-002) | Agent runs migrate when the DB is reachable; INFORM | Ask the human to migrate as sprint work | `migrate:fresh` on operator data |
| Auth (BE-003) | Server checks authorization on every mutating route | Trust a client role flag | Unauthenticated write |
| Errors (BE-004) | Typed errors; no swallowed catch | Empty `catch {}` | User sees a blank 500 with no log |
| Integrations (BE-005) | Timeouts, retries with bound, secrets in `.env` not `NEXT_PUBLIC_` | Vendor SDK on the hot path without a circuit | Paid-vendor key in the client bundle |
| Jobs (BE-006) | Idempotency keys, outbox, worker queues listed | Fire-and-forget writes that must fan out | Job cannot retry; worker missing the queue name |
| Indexes / FKs (BE-002) | Index what you filter; FKs or documented equivalent | Unbounded scans on operator lists | List GET omits fields the inspector shows |

Durable **agent** workflows (checkpoints, orchestrator) are **AI-003**, not this spine. CI is **PE-002**.

## Receipt lines (API, auth, data, security, infrastructure)

When the ticket skills include `BE-*` or `PE-001`, `## Architecture skill` cannot be `n/a`. The section must state:

- Route, service, and data access are separate. The handler does not embed the query.
- Authorization is enforced on the server for that object.
- Queries are parameterized. Bodies are allow-listed.
- A retried write names an idempotency key, or says why repeat is safe.
- Errors omit stack traces. The expensive path has a rate limit or quota, or the receipt says it is internal-only.
- Outbound calls have a timeout.
- Logs are structured, carry a request id, and omit secrets.
- Infrastructure is declared (Compose or the project IaC). Every long-running service has a health check. Temp and upload directories have an owner and a cleanup. A console-only change is drift, written back or reverted.

**Handoff:** API contract + error envelope + example payload in `docs/` or OpenAPI — FE must not guess field names (`backend-to-frontend-handoff`).

**Evidence bullets** below are studio scars (Compose, Laravel, Filament). They do not replace the spine.

---

## Architecture

### Domain-driven design (DDD)

```
┌─────────────────────────────────────────────────────────┐
│                    DDD STRUCTURE                        │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  ┌─────────────┐     ┌─────────────┐                   │
│  │   Domain    │────▶│ Application │                   │
│  │   layer     │     │   layer     │                   │
│  └─────────────┘     └──────┬──────┘                   │
│                             │                           │
│                      ┌──────▼──────┐                   │
│                      │ interface   │                   │
│                      │   layer     │                   │
│                      └──────┬──────┘                   │
│                             │                           │
│                      ┌──────▼──────┐                   │
│                      │infrastructure│                   │
│                      │   layer     │                   │
│                      └─────────────┘                   │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

### Separation of concerns

This is a workflow requirement on every feature.

A page, route handler, or component does not embed the query, the storage call, or the business rule. Those live in an application service. The service does not know about HTTP or the screen. Infrastructure (database, Redis, object storage, the encoder) is reached only from that service. A change to where a file is stored does not rewrite the note screen. A change to the screen does not rewrite the query.

### Layers

| Layer | Responsible | Contains |
|-------|-------------|----------|
| **Domain** | business logic | entities, value objects, aggregates, domain events |
| **Application** | orchestration | use cases, DTOs, application services |
| **Interface** | communication | API controllers, CLI, message handlers |
| **Infrastructure** | technical implementation | DB, external APIs, file system |

### Local development & migrations

| Stack | Migrate command | Notes |
|-------|-----------------|-------|
| Studio docker template | `./studio env <project> migrate --approve` | Postgres, then `payload migrate` in the app container |
| Local-first canvas | See [local-first-sync-playbook.md](local-first-sync-playbook.md) | Continuous sync, not one-time migration |

Agents: read project `package.json` scripts and `env.schema.json` / `*.env.example` (**names**) before running migrate. Do not Read `.env` **values**. **You run** `./studio env <project> migrate --approve` (or the project migrate command inside Compose) when you can reach the database. That is sprint work. Tell the human it ran (one INFORM line). Do **not** paste migrate steps for the operator to execute instead of you.

**No access** (no DSN, no container, production without deploy credentials) → say so once and stop; that is HITL / tech-veto, not a fake “please run migrate.”

**Pending migrations before API smoke (LO-0227):** A 500 on a list/inbox API after Compose up often means **pending schema**, not a product bug. Apply the project’s migrate command **inside the app container** (or documented RUNBOOK one-liner) before treating the endpoint as broken. Do not skip migrate because CLI tinker looks healthy.

**Self-hosted Postgres pooler (LO-0168):** transaction poolers (often `:54332`) may require **tenant username** and **SNI / TLS server name** matching the pooler host. Do not treat a failed `psql` to that port as “migrations cannot run.” Apply DDL **inside the database container** (`docker exec … psql` / `artisan migrate` on the app that talks to the primary), not via the pooler as a naive `localhost:54332` without tenant/SNI.

**Host ports:** before writing Compose published ports or local URLs, probe what is already bound. See [host-port-allocation.md](host-port-allocation.md) (LO-0066). Do not reuse another project’s 5432 / 6379 / 3000 / 54321–54323.

**Laravel `artisan serve` in Docker:** `ServeCommand` strips most process env from the PHP child (Compose `DB_*`, vendor base URLs, session driver) unless you pass `--no-reload`. CLI `php artisan` in the same container still sees full env, so tinker can look healthy while HTTP 500s. Use `php artisan serve --host=0.0.0.0 --port=8000 --no-reload`, or `php -S` which inherits the container environment.

**Compose recreate after queue/env/volume edits (LO-0156):** `up -d` of the HTTP process does not refresh already-running queue workers or the public app. Recreate those services so new `--queue=` flags, bind mounts, and shared secrets are live. Container-to-container calls use the Compose service hostname and internal port, not the published `localhost` port the browser uses.

**Billing / paid-vendor env contract (LO-0163):** ship the **server-only secret names** and host-panel (e.g. Coolify) env contract in the **same ticket** as the checkout/webhook feature. Prefer non-`NEXT_PUBLIC_` keys for API secrets. A static public checkout URL is not a substitute when the product needs variant/API checkout. Document expected env keys in `.env.example` and the deploy runbook in that ticket’s DoD.

**Host-panel env aliases (LO-0200):** PaaS UIs often paste vendor names (`NEXT_PUBLIC_*_KEY`, unprefixed `VENDOR_STORE_ID`). Application code should **read aliases for the same secret** (canonical server key first, then known aliases) so deploy does not require renaming every key in the panel. Do **not** keep API secrets as `NEXT_PUBLIC_*` long-term — accept the alias in the server resolver, then migrate the panel to the server-only name. Never commit live keys into `NEXT_PUBLIC_` client bundles as the intended contract.

**PHPUnit vs operator database (LO-0112 / LO-0115 / LO-0145):** `RefreshDatabase` / `migrate:fresh` against the Compose tenant Postgres wipes live domains, kits, and seed. Feature tests that need Postgres must use a throwaway database/schema, or transactions that cannot run `migrate:fresh` on the operator volume. Do not treat a green constraint test as permission to reset the human’s local stack. **`phpunit.xml` `force` is not enough** when Compose injects `DB_*` into the PHP process — the test `TestCase` must pin the isolated test database name in process env **before** the application boots.

**PHPUnit vs Compose queue (LO-0255):** The same leak applies to `QUEUE_CONNECTION`. Compose often injects `redis`/`database`; phpunit.xml `sync` without `force="true"` plus a TestCase env pin means `ShouldQueue` jobs are pushed to Redis and never run. Pin `QUEUE_CONNECTION=sync` in the test bootstrap the same way as `DB_DATABASE`.

**Worker `--queue` vs topology (LO-0257 / LO-0258):** The Compose worker `command` `--queue=` list must include every queue name the app topology routes jobs to (not only `default` or one named queue). Dispatching to a topology queue the worker does not listen on looks like a silent hang. YAML edits do not refresh a running worker — recreate that service (LO-0156).

**Graph mentions need persisted ids (LO-0256):** Derived knowledge-graph `mentions` (document → entity) must use stable foreign keys already stored on content blocks. Do not mint entities from display names. If payloads have no id, ship coverage/`covers` and assert mention count `0` rather than inventing rows.

**Filament operator home (LO-0141):** set panel `homeUrl` to the primary resource **index** (the list of existing records), not an empty dashboard. Header `StatsOverviewWidget`s are lazy by default — set `protected static bool $isLazy = false` so counts render on first paint, not after `x-intersect`.

**Operator idea queues (LO-0146):** If operators must feed a writer or synthesis loop, the idea queue is a **product admin surface**, not IDE chat. Markdown briefing files can seed a first corpus; they are not the ongoing operator inbox.

**Seeded corpus vs next wave (LO-0147):** A first compiled or seeded set of pages is not the ongoing backlog. Later corpus work consumes the **shared idea queue** (or admin briefs), not a silent rewrite of the seeded titles.

---

## SOLID principles

| Principle | Description | Implementation |
|-----------|-------------|----------------|
| **S**ingle Responsibility | one class = one responsibility | small, focused classes |
| **O**pen/Closed | open for extension, closed for modification | interfaces, strategy pattern |
| **L**iskov Substitution | subtypes are replaceable | clean inheritance |
| **I**nterface Segregation | no fat interfaces | many small interfaces |
| **D**ependency Inversion | abstractions instead of concretions | dependency injection |

### Implementation

```typescript
// ✅ SOLID
interface UserRepository {
  findById(id: string): Promise<User | null>;
  save(user: User): Promise<void>;
}

class CreateUserUseCase {
  constructor(private userRepo: UserRepository) {}
  
  async execute(data: CreateUserDTO): Promise<User> {
    const user = User.create(data);
    await this.userRepo.save(user);
    return user;
  }
}

// ❌ NOT SOLID
class UserService {
  async createUser(data: any) {
    const db = new Database(); // violates dependency inversion
    await db.query('INSERT INTO users...'); // violates SRP
  }
}
```

---

## PostgreSQL / Payload

### Database design

```sql
-- Enums (type safety)
CREATE TYPE user_role AS ENUM ('admin', 'user', 'viewer');
CREATE TYPE task_status AS ENUM ('open', 'in_progress', 'done');

-- Tables
CREATE TABLE users (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  email TEXT UNIQUE NOT NULL,
  role user_role NOT NULL DEFAULT 'user',
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- Indexes
CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_users_role ON users(role);
```

### JSONb EAV structures

```sql
-- Flexible attribute system
CREATE TABLE product_attributes (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  product_id UUID NOT NULL REFERENCES products(id),
  attribute_key TEXT NOT NULL,
  attribute_value JSONB NOT NULL,
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- GIN index for JSONb
CREATE INDEX idx_product_attributes_value 
  ON product_attributes USING GIN(attribute_value);

-- Query
SELECT * FROM product_attributes 
WHERE attribute_value @> '{"color": "red"}';
```

### Migrations

```bash
./studio env <project> migrate --approve
```

That runs `payload migrate` inside the app container. Local development may push schema. Production does not. Read [payload-playbook.md](payload-playbook.md).

---

## API design

### RESTful resources

```
GET    /api/v1/users          # list
GET    /api/v1/users/:id      # detail
POST   /api/v1/users          # create
PATCH  /api/v1/users/:id      # update
DELETE /api/v1/users/:id      # delete
```

### Response format

```typescript
// success
{
  "data": { ... },
  "meta": { "page": 1, "total": 100 }
}

// error
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Email is invalid",
    "details": { "email": "Must be a valid email address" }
  }
}
```

### Versioning

```
/api/v1/...  # main version
/api/v2/...  # breaking changes
```

---

## Authentication

### JWT + refresh token

```typescript
// login
const accessToken = jwt.sign({ userId: user.id }, SECRET, { expiresIn: '15m' });
const refreshToken = jwt.sign({ userId: user.id }, REFRESH_SECRET, { expiresIn: '7d' });

// refresh
app.post('/refresh', async (req, res) => {
  const { refreshToken } = req.body;
  const payload = jwt.verify(refreshToken, REFRESH_SECRET);
  const newAccessToken = jwt.sign({ userId: payload.userId }, SECRET, { expiresIn: '15m' });
  res.json({ accessToken: newAccessToken });
});
```

### RBAC

```typescript
type Role = 'admin' | 'user' | 'viewer';
type Permission = 'read' | 'write' | 'delete';

const rolePermissions: Record<Role, Permission[]> = {
  admin: ['read', 'write', 'delete'],
  user: ['read', 'write'],
  viewer: ['read'],
};

function hasPermission(role: Role, permission: Permission): boolean {
  return rolePermissions[role].includes(permission);
}
```

---

## Error handling

```typescript
// custom error classes
class AppError extends Error {
  constructor(
    public code: string,
    message: string,
    public statusCode: number = 500
  ) {
    super(message);
  }
}

class ValidationError extends AppError {
  constructor(message: string, public details: Record<string, string>) {
    super('VALIDATION_ERROR', message, 400);
  }
}

// global error handler
app.use((err, req, res, next) => {
  if (err instanceof AppError) {
    return res.status(err.statusCode).json({
      error: { code: err.code, message: err.message, details: err.details }
    });
  }
  
  // unknown error
  console.error(err);
  res.status(500).json({
    error: { code: 'INTERNAL_ERROR', message: 'An internal error occurred' }
  });
});
```

---

## Testing

### Unit tests

```typescript
describe('CreateUserUseCase', () => {
  it('should create a user', async () => {
    const repo = new InMemoryUserRepository();
    const useCase = new CreateUserUseCase(repo);
    
    const user = await useCase.execute({ email: 'test@example.com' });
    
    expect(user.email).toBe('test@example.com');
  });
});
```

### Integration tests

```typescript
describe('POST /api/users', () => {
  it('should create a user', async () => {
    const response = await request(app)
      .post('/api/users')
      .send({ email: 'test@example.com' });
    
    expect(response.status).toBe(201);
    expect(response.body.data.email).toBe('test@example.com');
  });
});
```

---

## External provider adapters — licence codes (LO-0067 / LO-0072)

Stock-media APIs (e.g. [Openverse](https://api.openverse.org/)) expose **provider-native licence slugs**, not SPDX display strings. The Openverse `license` query parameter and result fields use short codes such as `by`, `by-sa`, `by-nc`, `by-nc-sa`, `by-nd`, `by-nc-nd`, `cc0`, `pdm`, `nc-sampling+`, and `sampling+` — **not** `cc-by` / `cc-by-sa` prefixes.

### Adapter contract

| Layer | Responsibility |
|-------|----------------|
| **Provider slug** | Exact string from the API (`by`, `by-sa`, …) — treat as opaque, case-sensitive |
| **Canonical enum** | Internal stable id (may map `by` → `CC_BY`) for business rules and filtering |
| **Display label** | Human string (`CC BY 4.0`) — never used for allowlist matching |

### Rules

1. **Allowlists match provider slugs first.** If the adapter only accepts `cc-by` but the API returns `by`, every result is silently dropped — the UI looks like “no matches” while the network path is healthy.
2. **Normalize at the boundary.** One function maps provider slug → canonical enum; downstream code never branches on display strings or guesses prefixes.
3. **Version is separate.** Openverse also returns `license_version` (e.g. `4.0`). Slug + version compose the attribution URL — do not embed version inside the slug.
4. **Fixture from OpenAPI.** Copy licence values from the provider’s published schema/examples into adapter unit tests; do not invent `cc-*` forms from memory.
5. **Degraded telemetry.** Log `provider_slug`, `mapped`, and `rejected_reason` at debug level so a mapper bug is distinguishable from an HTTP outage (see HITL LO-0069 / LO-0074).

```typescript
// ✅ Boundary normalizer — provider slug is source of truth
const OPENVERSE_SLUGS = new Set([
  'by', 'by-sa', 'by-nc', 'by-nc-sa', 'by-nd', 'by-nc-nd',
  'cc0', 'pdm', 'nc-sampling+', 'sampling+',
]);

function toCanonicalLicence(providerSlug: string): CanonicalLicence | null {
  if (!OPENVERSE_SLUGS.has(providerSlug)) return null;
  return SLUG_TO_CANONICAL[providerSlug]; // e.g. by → CC_BY
}
```

---

## Stock imagery — provider priority (LO-0075)

When integrating multiple stock-media providers for **Suggested** / discovery rails:

1. **Primary aggregator first.** Prefer a licence-broad meta-catalog (e.g. Openverse) as the default path — one adapter covers many sources with consistent slugs.
2. **Fix mapper before adding providers.** If Suggested is empty on a healthy HTTP 200, suspect adapter filtering (licence slug mismatch) before blaming the primary API or adding fallbacks.
3. **Fallback providers are last resort.** Only evaluate direct APIs (e.g. Unsplash, Pexels) when: (a) the primary adapter maps correctly, (b) the primary returns healthy responses, and (c) Suggested is still empty for product-valid queries.
4. **Do not stack providers to mask bugs.** A second provider that “works” while the primary silently filters everything hides mapper and copy failures until review.

**Board column ids (LO-0180):** When a job (or similar) machine is wired to an API, persist **native column ids** on the reused board. A UI translation layer (demo column ids mapped onto domain states) is a bootstrap only — do not keep it as the contract.

---

## References

- `.quinsy-studio/knowledge-base/anti_ai_slop_protocol.md` — backend slop rules
- `.quinsy-studio/teams/02-backend-systems/` — backend team
- `.quinsy-studio/teams/08-platform-enterprise-engineering/` — infrastructure team

## Deltas

- **PB-20260925-001** helpful=0 harmful=0 :: Do not enqueue HQ skill-catalog work on the product sprint inbox. Route it to the studio LO and train queue. Product execute INFORM the open HQ LO count. Infuse those jobs in a HQ session; STUDIO_LO only when the product loop is idle.
- **PB-20260922-001** helpful=0 harmful=0 :: When a persisted image URL fails reachability, queue public-photo research on the same gold path as persist. Do not wait for a generation vendor.
- **PB-20260916-005** helpful=0 harmful=0 :: Per-tenant third-party API credentials are encrypted rows in the database, scoped to the tenant. An admin surface must not read them from process .env.
- **PB-20260916-004** helpful=5 harmful=0 :: A list GET must return every attribute the inspector is supposed to show. Do not ship a write path whose corresponding list omits those fields.
- **PB-20260916-003** helpful=1 harmful=0 :: Operator-authorized jobs skip the exploration weekly cap. Re-check monthly and kill-switch caps on every LLM complete; do not add a daemon. After the operator raises a limit, the next call picks up available budget.
- **PB-20260916-002** helpful=0 harmful=0 :: Lifecycle folder queries (awaiting approval, in progress, done) must exclude dismissed rows. Filtering dismissed only on the Dismissed folder still lists trashed items in the other lifecycle views.
- **PB-20260916-001** helpful=0 harmful=0 :: Empty production pipeline maps activity or trace status to idle, not in_progress. Defaulting unknown or empty rows to in_progress lies to the operator.
- **PB-20260915-002** helpful=2 harmful=0 :: Bootstrap plans that need catalog items queue research as an operator Inbox request, not a ticket-id hint in the UI.
- **PB-20260915-001** helpful=0 harmful=0 :: Cache-bust after a write belongs on the plane that holds the secret (admin worker, server action, route handler). A client module cannot see admin-only env; Saved can look true while the public host stays stale. Pull write-side-revalidate; never use NEXT_PUBLIC_ as the secret source.
- **PB-20260914-004** helpful=0 harmful=0 :: Compose worker --queue must list every topology queue jobs are dispatched on; default or a single named queue is not enough.
- **PB-20260914-003** helpful=0 harmful=0 :: Changing Compose queue-worker command or --queue flags requires recreating that service; up -d of the HTTP process leaves the old worker command running.
- **PB-20260914-002** helpful=1 harmful=0 :: Derived graph mentions use persisted entity foreign keys on content blocks; if ids are absent, mention count stays 0 — do not mint entities from display names.
- **PB-20260914-001** helpful=0 harmful=0 :: PHPUnit TestCase must pin QUEUE_CONNECTION=sync when Compose injects redis/database; phpunit.xml without force is not enough (same class of leak as DB_DATABASE).
