# Changelog — Quinsy Studio

Alle Änderungen am Quinsy Studio werden hier dokumentiert.

## [1.3.0] — 2026-08-20

### Strikte Ticket-Architektur (Projekt- + Studio-Ebene)

Tickets waren zu vage (ein Satz + flache Checkboxen). Neues Schema für ALLE Tickets:

- ✅ **Rollenzuweisung:** `assignee_role` (Director-Level) wird aus Skills abgeleitet (z.B. Login → Backend Architect (Director))
- ✅ **Context & Value:** Ist-Zustand vs. Soll-Zustand statt vager Problembeschreibung
- ✅ **Strikte Constraints:** Exakte Modifikationspfade, Regeln (keine externen Packages ohne ADR), zwingende Playbook-Referenz
- ✅ **BDD-Akzeptanzkriterien:** Given / When / Then statt Implementierungs-Beschreibung
- ✅ **Definition of Done:** Messbare Abschluss-Kriterien

#### Umsetzung
- ✅ `ticket_helpers.py` (neu) — gemeinsames Schema: Skill→Rolle-Mapping, Playbook-Mapping, BDD-Builder, Markdown-Renderer
- ✅ `generate_ticket_manifest.py` — Setup-Tickets + Feature-Tickets mit neuem Schema; ID-Kollisionsfix beibehalten
- ✅ `studio.py` — `cmd_ticket` (Projekt) + `cmd_learn` (Studio, Typ `studio-evolution`) auf neues Schema
- ✅ `ticket_template.md` — Template mit Rolle, Ist/Soll, Constraints, BDD, DoD

#### Bugfixes (durch Schema-Test gefunden)
- ✅ Feature-Extraktion: `(.+?)`-Regex matchte nur 1 Zeichen → Name wurde verworfen (jetzt: Doppelpunkt-Split)
- ✅ Template-Platzhalter (`_Noch nicht definiert_`) wurden als Features extrahiert → gefiltert
- ✅ `{project}`/`{signal}`-Platzhalter in f-Strings waren nicht aufgelöst

## [1.2.0] — 2026-08-20

### Externe Skill-Quellen erweitert (Skill-Package-Manager)
- ✅ 4 neue verifizierte Quellen: `coreyhaines31/marketingskills` (49 Skills inkl. ai-seo/AEO), `gamedev-skills/awesome-gamedev-agent-skills` (67 Skills + Router), `samir-abis/cookiecomply-skills` (DSGVO), `bloomprotocol/agent-visibility-skill` (GEO)
- ✅ `skill-dependencies.json` auf 7 Domains erweitert, alle importiert (29 externe Skill-Quellen auf Disk)
- ✅ Skill-Registry: Neue Quellen + gezielte Skill-Mappings (ai-seo→GM-002, cookiecomply→CL-002, seo-audit→GM-001, ...) + Archetyp `game`

### Externe Skills in Teams eingearbeitet
- ✅ AEO (GM-002): ai-seo, schema, geo_visibility, competitors
- ✅ SEO (GM-001): seo-audit, programmatic-seo, site-architecture
- ✅ Design System (FE-002) + UI Components (FE-001): hallmark, design_awesome
- ✅ Cookie Banner (CL-002): cookiecomply
- ✅ Content (GM-003): copywriting, product-marketing, customer-research
- ✅ Database (BE-002): database-schema-design, query-optimization
- ✅ Security (PE-003): security-audit, threat-modeling, SAST/DAST

### Skill-Matching-Test
- ✅ `test_skill_matching.py` — 7 Beispiel-Tickets → interne + externe Skills, verifiziert Quellen auf Disk
- ✅ Neue interne Skill GM-004 (Game Development) mit gamedev-Router-Trigger
- ✅ Ergebnis: 7/7 Tickets gematcht, 29/29 externe Quellen verifiziert
- ✅ Learning Item LO-0001 (Game-Dev-Lücke) als Nachweis des Learning Loops

## [1.1.0] — 2026-08-20

### Ordner-Konsolidierung (alles unter .quinsy-studio/)
- ✅ `studio-library/` → `.quinsy-studio/studio-library/` (Pfade in studio.py, sync_global_assets.py aktualisiert)
- ✅ `templates/docker/` → `.quinsy-studio/studio-templates/docker/` (Basis-Docker-Template)
- ✅ Orphan `studio-tools/` (alte studio.py) und leeres `templates/` entfernt
- ✅ `studio` Wrapper bleibt als CLI-Entry-Point (delegiert an .quinsy-studio/studio-tools/)

### Docker-Basis-Template (Base → Project)
- ✅ `.quinsy-studio/studio-templates/docker/` mit docker-compose.yml, .env.example, README
- ✅ `./studio env <project> init` kopiert Template in den Projektordner und parametrisiert `{{PROJECT_NAME}}`
- ✅ `init_project_env.py` nutzt ebenfalls das Template (kein Hardcode mehr)

### Skill-Package-Manager (externe Skills)
- ✅ `.quinsy-studio/skill-dependencies.json` — abonnierte Quellen (hallmark, awesome-design-skills, awesome-ai-agent-skills)
- ✅ `import_external_skills.py` — importiert Skills via git clone nach `.quinsy-studio/external-skills/`
- ✅ `./studio update-skills` — Command zum Abonnieren/Aktualisieren
- ✅ Skill-Registry um External-Skills-Mapping erweitert (Domain → Team → Skill)

## [1.0.0] — 2026-08-20

### Rebuild des gesamten Studio-Systems

Nach einem vollständigen Verlust aller Studio-Dateien wurde das gesamte System neu aufgebaut.

#### Process-Dokumente (.quinsy-studio/process/)
- ✅ `lifecycle.md` — 8-Phasen-Lebenszyklus
- ✅ `gates.md` — Detaillierte Gate-Definitionen
- ✅ `adr-policy.md` — ADR-Regelwerk
- ✅ `anti-slop.md` — Anti-Slop-Audit
- ✅ `ticket-workflow.md` — 9-Schritte-Ticket-Workflow
- ✅ `iterative-delivery.md` — Sprint/Grooming/Board
- ✅ `human-in-the-loop.md` — HITL-Entscheidungen
- ✅ `project-archetypes.md` — Projekt-Archetypen

#### Team-Skills (.quinsy-studio/teams/)
- ✅ `01-frontend-experience/` — UI/UX, Design System, Performance
- ✅ `02-backend-systems/` — API, Datenbanken, Auth
- ✅ `03-compliance-legal/` — DSGVO, Datenschutz, Impressum
- ✅ `04-product-strategy-architecture/` — Strategie, Architektur, ADRs
- ✅ `05-growth-marketing-content/` — SEO, AEO, Content, Growth
- ✅ `06-product-management-operating-model/` — PM, User Research, Roadmap
- ✅ `07-ai-autonomous-systems/` — KI-Integration, Anti-Slop, Automatisierung
- ✅ `08-platform-enterprise-engineering/` — Infrastruktur, DevOps, Security

#### Studio CLI (studio-tools/)
- ✅ `studio.py` — Python CLI mit allen Befehlen
- ✅ `./studio` — Wrapper-Script

**Befehle:**
- `./studio status <project>`
- `./studio gate <project> [--level N] [--anti-slop]`
- `./studio adr <project> "<Titel>"`
- `./studio ticket <project> "<Titel>"`
- `./studio board <project>`
- `./studio move <project> <id> <status>`
- `./studio sprint <project>`
- `./studio groom <project>`
- `./studio set-phase <project> <phase> --gate <n>`
- `./studio decide <project> "<Titel>"`
- `./studio decisions <project>`
- `./studio env <project> init|up|down|status|logs`
- `./studio repo <project> create|status`
- `./studio learn "<Titel>" --signal <s>`
- `./studio learn-list`
- `./studio retro <project>`
- `./studio promote <project> <asset>`
- `./studio init <project> --archetype <type>`

#### Studio Library (studio-library/)
- ✅ `ui/tokens/` — Design-Tokens (JSON, CSS)
- ✅ `ui/components/button/` — Button-Komponente
- ✅ `ui/page-types/comparison/` — Vergleichs-Seitentyp
- ✅ `packages/auth/` — Authentifizierung
- ✅ `packages/billing/` — Abrechnung
- ✅ `packages/feature-gating/` — Feature-Flags
- ✅ `manifest.json` — Asset-Registry

#### Templates
- ✅ `templates/docker/` — Docker-Compose + .env

---

## Status

**System-Status:** ✅ Operativ
**Version:** 1.0.0
**Letztes Update:** 2026-08-20

---

## Bekannte Einschränkungen

- Anti-Slop-Audit ist noch ein Stub (keine echte Code-Analyse)
- Docker-Commands sind noch nicht vollständig implementiert
- GitHub-Integration (gh CLI) noch nicht angebunden
