# Skill: Database Design

> Schema-Design, Migrationen, Normalisierung, Indexierung, Query-Optimierung

## Metadata

```
skill_id: BE-002
name: Database Design
team: 02-backend-systems
lead_role: Database Specialist
support_roles: [Backend Architect, Backend Engineer]
phases: [2, 3, 4]
activation_triggers:
  - Ticket enthält "Database", "Schema", "Migration", "Query"
  - Phase 2: Datenmodell wird entworfen
  - Phase 4: Migrationen werden implementiert
  - Performance-Problem mit Datenbank-Queries
```

---

## Verhaltensregeln

### 1. Schema-Design

```markdown
Standard-Regeln:
  - 3NF (Third Normal Form) als Ausgangspunkt
  - UUIDs für externe IDs (nicht Auto-Increment)
  - Timestamps: created_at, updated_at
  - Soft Delete: deleted_at (statt physikalisches Löschen)
  - Foreign Keys für Integrität
  - CHECK Constraints für Validierung

Tabellen-Struktur:
  id: UUID (PK)
  created_at: TIMESTAMP
  updated_at: TIMESTAMP
  deleted_at: TIMESTAMP (nullable, für Soft Delete)
  ... spezifische Felder
```

### 2. Migrationen

```markdown
Regeln:
  - Jede Migration ist reversibel (up + down)
  - Migrationen sind versioniert
  - Keine Breaking Changes in bestehenden Migrationen
  - Daten-Migrationen separat von Schema-Migrationen
  - Immer testen: migrate → rollback → migrate

Naming:
  20260820_create_users_table
  20260821_add_email_index_to_users
  20260822_create_orders_table
```

### 3. Indexierung

```markdown
Index erstellen für:
  - Foreign Keys (immer!)
  - Häufig gefilterte Spalten
  - Sortierung in Listen-Ansichten
  - UNIQUE Constraints
  - composite index für häufige Multi-Column-Queries

Nicht indexieren:
  - Spalten mit wenigen eindeutigen Werten (Boolean, Status)
  - Sehr große Text-Spalten (stattdessen Full-Text Search)
  - Spalten die selten abgefragt werden
```

### 4. Query-Optimierung

```markdown
Tools:
  - EXPLAIN ANALYZE für Query-Plan
  - pg_stat_statements für Langsam-Query-Erkennung

Optimierungen:
  - N+1 Queries vermeiden (eager loading / JOIN)
  - SELECT nur benötigte Spalten (kein SELECT *)
  - Pagination für große Listen
  - Caching für häufige Reads
  - Batch Inserts/Updates für viele Einträge
```

### 5. JSONb (Supabase/PostgreSQL)

```markdown
Wann JSONb:
  - EAV-Modelle für flexible Attribute
  - Metadaten die sich经常 ändern
  - Konfigurations-Objekte

GIN-Index für JSONb:
  CREATE INDEX idx_metadata ON table USING GIN (metadata);

Query:
  SELECT * FROM table WHERE metadata @> '{"key": "value"}';
```

---

## Anti-Patterns

### ❌ Verboten

```markdown
- Auto-Increment statt UUID für externe IDs
- Keine Foreign Keys (Integrität!)
- SELECT * in Produktions-Code
- N+1 Queries
- Fehlende Index auf Foreign Keys
- Keine Migration-Strategie
- Hardcoded DB-Credentials
```

### ✅ Stattdessen

```markdown
- UUIDs für externe Referenzen
- Foreign Keys mit ON DELETE/UPDATE
- Explizites SELECT mit benannten Spalten
- Eager Loading / JOINs
- Index auf alle FKs und häufige Query-Spalten
- Versionierte Migrationen
- Environment Variables / Secrets Management
```

---

## Externe Skill-Unterstützung

> Vor der Umsetzung die importierten Best-in-Class-Skills laden (`./studio update-skills`):

- **`all_domains/database/database-schema-design`** — normalisiertes Schema-Design. **Primäre Referenz.**
- **`all_domains/database/query-optimization`** — Langsame Queries optimieren (EXPLAIN, Indizes)
- **`all_domains/database/database-migration`** — Migrations-Planung + Ausführung
- **`all_domains/database/database-backup`** — Backup-Strategien

Ablauf: Schema entwerfen → `database-schema-design` prüfen → Migration planen → Query-Performance validieren.

## Referenzen

- `.quinsy-studio/knowledge-base/backend_playbook.md` — Backend-Regeln
- `.quinsy-studio/process/adr-policy.md` — ADR für DB-Entscheidungen
- `.quinsy-studio/studio-library/packages/` — Wiederverwendbare Packages
