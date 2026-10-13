# Skill: Database Design

> PostgreSQL, JSONb, EAV, GIN indexes, migrations

**Playbook:** [backend_playbook.md](../../../knowledge-base/backend_playbook.md) (DB / migrate). Agent runs migrate when reachable.

One working copy, one Postgres: the Compose Postgres that `@payloadcms/db-postgres` uses. Do not start a second database beside it. Payload owns the schema of its collections and the `users` table. Users are the Payload `users` collection; reference them with a Payload `relationship` field, not a foreign key to an outside auth provider.

## Metadata

```
skill_id: BE-002
name: Database Design
team: 02-backend-systems
lead_role: Database Specialist
support_roles: [Backend Architect, Backend Engineer]
phases: [2, 3, 4]
activation_triggers:
  - Ticket contains "database", "schema", "migration", "query"
  - Phase 2: data model is designed
  - Phase 4: migrations are implemented
  - Performance problem with database queries
```

---

## Behavior rules

### 1. Schema design

Most tables are Payload collections. Design them as collections and fields; Payload generates the tables, join tables (`_rels`, `_locales`, arrays) and timestamps. Write raw tables only for data Payload does not model well (counters, reporting rollups, vectors) and name them in the architecture doc.

```markdown
Standard rules:
  - 3NF (third normal form) as starting point
  - Timestamps: Payload adds createdAt / updatedAt; raw tables add created_at, updated_at
  - Soft delete only where the PRD needs restore or audit (status field or deleted_at);
    hard delete is right for personal data on erasure (CL-004)
  - Relationships through Payload relationship fields; raw tables use foreign keys
  - Validation in Payload field `validate` plus a CHECK constraint on raw tables
```

**ID type rule.** Payload's Postgres adapter uses serial integer IDs by default; `idType: 'uuid'` in `postgresAdapter({ idType })` switches every collection to UUIDs. Gate 1 picks one and the architecture doc records it. Do not mix: raw tables that reference collections use the same type. Changing `idType` after data exists is a migration project with HITL, not a ticket.

**Public identifiers.** Serial IDs reveal counts and are guessable. Access rules (BE-007) are the protection; never rely on an ID being hard to guess. When an ID shows in a public URL, use a `slug` or a random `publicId` field with a unique index.

### 2. Migrations

Payload migrations are the only schema migration path: `payload migrate:create <name>`, then `payload migrate`. Local development may `push`; production sets `push: false`. Locally you run them as sprint work: `./studio env <p> migrate` (agent-run, INFORM; no signature). In production, `compose.prod.yml` runs `migrate` before `start` on every deploy, and an out-of-band migration is the one production step that waits for the human: `./studio ops <p> migrate --prod --approve`. Inspect the schema without a signature through `./studio ops <p> db --sql='\\dt'`.

```markdown
Rules:
  - Migrations are versioned files in the repo, reviewed like code
  - Never edit a migration that has run anywhere shared
  - Data migrations (backfills) separate from schema migrations
  - Each migration has a working down(), tested locally: migrate → migrate:down → migrate
  - Production rollback is forward-fix (rule 2a), not migrate:down
  - **The agent applies pending migrations** when it has DB access (local or VPS). Inform the human. Do not ask the human to run migrate as sprint work.
  - Destructive reset (`migrate:fresh`, `migrate:reset`, drop) is HITL — never on the operator volume without explicit ask
  - Receipt `## Risk & rollback` names the migration, its lock behavior and the forward-fix
```

### 2a. Expand / contract and forward-fix

A deploy runs old and new code against one database for a short time. Every schema change must work with both.

```markdown
Expand → migrate → contract (separate releases):
  1. Expand: add the new column/table, nullable or with a constant default. Old code ignores it.
  2. Deploy code that writes both old and new (or only new, reading both).
  3. Backfill in bounded batches, each its own transaction, safe to re-run
     (UPDATE … WHERE new_col IS NULL AND id BETWEEN $lo AND $hi).
  4. Enforce: add CHECK … NOT VALID, then VALIDATE CONSTRAINT in a separate step;
     SET NOT NULL only after validation.
  5. Contract in a later release: drop the old column once no deployed code reads it.

Renames are add-new + copy + drop-old, never RENAME on a live column.

Lock budget on every DDL in production:
  SET LOCAL lock_timeout = '1s'; SET LOCAL statement_timeout = '5s';
  On timeout the migration fails and is retried; it must not queue traffic.
  Indexes on large tables: CREATE INDEX CONCURRENTLY (outside a transaction;
  drop an INVALID leftover before retrying).

Forward-fix:
  A bad migration in production is fixed by a new migration, not by down().
  down() after new writes can lose data. Write the forward-fix plan before deploy.
```

### 2b. Backups and restore drill

A backup counts only after a restore has worked. PE-001 owns the backup job and the restore drill (restore the latest dump into a throwaway Compose Postgres, run `payload migrate:status` and a smoke query set, record the time taken). Before a migration that drops or rewrites data, confirm the last restore drill passed and take a fresh dump. Name both on the receipt.

### 3. Indexing

```markdown
Create an index for:
  - Foreign keys (always!)
  - Frequently filtered columns
  - Sorting in list views
  - UNIQUE constraints
  - composite index for frequent multi-column queries

Don't index:
  - Columns with few distinct values (boolean, status)
  - Very large text columns (use full-text search instead)
  - Columns that are rarely queried
```

### 4. Query optimization

```markdown
Tools:
  - EXPLAIN (ANALYZE, BUFFERS) on the real query against realistic row counts
  - pg_stat_statements for slow-query detection
  - Read the plan: Seq Scan on a large table in a hot path, estimated vs actual rows
    far apart, or a sort spilling to disk → fix before merge

Payload queries:
  - Set `depth` explicitly (0 or 1 in lists); default depth populates every relationship
  - Use `select` to return only needed fields
  - Always paginate (`limit`, `page`); never `pagination: false` on user-facing lists
  - Add `index: true` on fields used in `where` or `sort`; `unique: true` where it is unique
  - N+1: one `find` with `where: { id: { in: ids } }`, not a find per row in a loop or a hook

Raw SQL:
  - SELECT only needed columns (no SELECT *)
  - Partial index for a common filter (WHERE status = 'published')
  - Composite index ordered as the query filters then sorts
  - Batch inserts/updates for many entries
  - Caching for frequent reads only with a named invalidation (revalidateTag / afterChange)
```

### 4a. Connections

Payload holds one pool per app container. With more replicas or a worker, add the `pooler` profile (session mode) and keep the total under Postgres `max_connections`. Never open a connection per request.

### 5. JSONb (PostgreSQL)

```markdown
When to use JSONb:
  - EAV models for flexible attributes
  - Metadata that changes often
  - Configuration objects

GIN index for JSONb:
  CREATE INDEX idx_metadata ON table USING GIN (metadata);

Query:
  SELECT * FROM table WHERE metadata @> '{"key": "value"}';
```

---

## Anti-patterns

### ❌ Forbidden

```markdown
- A second database or ORM beside Payload (Prisma, a Supabase project, a second users table)
- Mixing serial and UUID IDs across collections and raw tables
- Guessable IDs as the only protection of a resource
- No foreign keys on raw tables (integrity!)
- SELECT * in production code; Payload finds with default depth in lists
- N+1 queries
- Missing index on foreign keys and filtered fields
- RENAME or DROP of a column that deployed code still reads
- migrate:down as the production rollback
- Hardcoded DB credentials
```

### ✅ Instead

```markdown
- Payload collections and Payload migrations
- One idType, chosen at gate 1
- Access rules + slug or publicId for public URLs
- Foreign keys with ON DELETE/UPDATE on raw tables
- Explicit select and depth
- One batched query
- Index on all FKs and frequent query columns
- Expand → migrate → contract
- Forward-fix migration
- Environment variable names in env.schema.json; values via ./studio env … --approve
```

---

## External skill support

> Before implementation load the imported best-in-class skills (`./studio update-skills`):

- **`all_domains/database/database-schema-design`** — normalized schema design. **Primary reference.**
- **`all_domains/database/query-optimization`** — optimize slow queries (EXPLAIN, indexes)
- **`all_domains/database/database-migration`** — migration planning + execution
- **`all_domains/database/database-backup`** — backup strategies

Flow: design the schema → check with `database-schema-design` → plan the migration → validate query performance.

## References

- `.quinsy-studio/knowledge-base/backend_playbook.md` — backend rules
- `.quinsy-studio/knowledge-base/payload-playbook.md` — Payload owns schema, auth and migrations
- `teams/02-backend-systems/skills/payload/` (BE-007) — adapters, queries, `idType`
- `teams/08-platform-enterprise-engineering/skills/infrastructure.md` (PE-001) — backups and restore drill
- `.quinsy-studio/process/adr-policy.md` — ADR for DB decisions
- PostgreSQL docs: `ALTER TABLE` lock levels, `CREATE INDEX CONCURRENTLY`, `EXPLAIN`
