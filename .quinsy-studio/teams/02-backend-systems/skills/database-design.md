# Skill: Database Design

> PostgreSQL, JSONb, EAV, GIN indexes, migrations

**Playbook:** [backend_playbook.md](../../../knowledge-base/backend_playbook.md) (DB / migrate). Agent runs migrate when reachable.

One working copy, one Postgres. Do not start a second `supabase start` database beside Compose Postgres. Store `auth_user_id` as the hook for the hosted Auth `sub`.

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

```markdown
Standard rules:
  - 3NF (third normal form) as starting point
  - UUIDs for external IDs (not auto-increment)
  - Timestamps: created_at, updated_at
  - Soft delete: deleted_at (instead of physical deletion)
  - Foreign keys for integrity
  - CHECK constraints for validation

Table structure:
  id: UUID (PK)
  created_at: TIMESTAMP
  updated_at: TIMESTAMP
  deleted_at: TIMESTAMP (nullable, for soft delete)
  ... specific fields
```

### 2. Migrations

```markdown
Rules:
  - Every migration is reversible (up + down)
  - Migrations are versioned
  - No breaking changes in existing migrations
  - Data migrations separate from schema migrations
  - Always test: migrate → rollback → migrate
  - **The agent applies pending migrations** when it has DB access (local or VPS). Inform the human. Do not ask the human to run migrate as sprint work.
  - Destructive reset (`migrate:fresh`, drop) is HITL — never on the operator volume without explicit ask

Naming:
  20260820_create_users_table
  20260821_add_email_index_to_users
  20260822_create_orders_table
```

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
  - EXPLAIN ANALYZE for the query plan
  - pg_stat_statements for slow-query detection

Optimizations:
  - Avoid N+1 queries (eager loading / JOIN)
  - SELECT only needed columns (no SELECT *)
  - Pagination for large lists
  - Caching for frequent reads
  - Batch inserts/updates for many entries
```

### 5. JSONb (Supabase/PostgreSQL)

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
- Auto-increment instead of UUID for external IDs
- No foreign keys (integrity!)
- SELECT * in production code
- N+1 queries
- Missing index on foreign keys
- No migration strategy
- Hardcoded DB credentials
```

### ✅ Instead

```markdown
- UUIDs for external references
- Foreign keys with ON DELETE/UPDATE
- Explicit SELECT with named columns
- Eager loading / JOINs
- Index on all FKs and frequent query columns
- Versioned migrations
- Environment variables / secrets management
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
- `.quinsy-studio/process/adr-policy.md` — ADR for DB decisions
