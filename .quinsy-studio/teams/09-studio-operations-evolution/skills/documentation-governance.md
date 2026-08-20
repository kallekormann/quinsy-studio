# Skill: Documentation Governance

> Strikte Trennung Studio/Projekt, CHANGELOG-Pflege, README-Aktualität, Wissenstransfer

## Metadata

```
skill_id: SO-004
name: Documentation Governance
team: 09-studio-operations-evolution
lead_role: Documentation Writer
support_roles: [Process Guard]
phases: [6, 7]
activation_triggers:
  - Ticket enthält "Doku", "Documentation", "README", "CHANGELOG"
  - Phase 6: Dokumentation wird aktualisiert
  - Phase 7: Release-Doku
  - /studio evolve Befehl
```

---

## Verhaltensregeln

### 1. Strikte Trennung Studio/Projekt

```markdown
Studio-HQ (.quinsy-studio/):
  - Enthält NUR universell anwendbare Inhalte
  - Keine projektspezifischen Details
  - Playbooks, Tools, Templates, Skills

Projekt (projects/[name]/):
  - Enthält NUR projektspezifische Inhalte
  - Lokale Learnings
  - Projekt-spezifische Doku
  - Status, Tickets, Sprints

Regel:
  - Studio-Dateien dürfen KEINE Projekt-Referenzen enthalten
  - Projekt-Dateien dürfen Studio-Inhalte REFERENZIEREN (nicht kopieren)
```

### 2. CHANGELOG-Pflege

```markdown
Format (Keep a Changelog):
  ## [Version] - YYYY-MM-DD
  ### Added
  - Neues Feature
  ### Changed
  - Geändertes Feature
  ### Fixed
  - Bug-Fix
  ### Removed
  - Entferntes Feature

Wann aktualisieren:
  - Bei jeder Promotion
  - Bei jeder Tool-Änderung
  - Bei jeder Prozess-Änderung
  - Bei jedem Release
```

### 3. README-Pflege

```markdown
Für jede Komponente:
  - Kurze Beschreibung
  - Installation/Setup
  - Nutzung
  - Referenzen
  - Aktualität: Bei jeder Änderung

Stardard-READMEs:
  - .quinsy-studio/README.md (Studio-HQ)
  - Jedes Team-README.md
  - Jedes Skill-README.md (im Skill selbst)
```

### 4. Wissenstransfer

```markdown
Sicherstellen:
  - Neue Team-Mitglieder finden alle Infos
  - Entscheidungen sind dokumentiert (ADRs)
  - Learnings sind zugänglich
  - Prozesse sind beschreiben

Tools:
  - ADRs für Architektur-Entscheidungen
  - Learning Logs für Erkenntnisse
  - Decision Records für HITL-Entscheidungen
```

---

## Anti-Patterns

### ❌ Verboten

```markdown
- Studio-Dateien mit Projekt-Referenzen
  - Veraltete READMEs
  - Kein CHANGELOG
  - Dokumentation nur als Optional
```

### ✅ Stattdessen

```markdown
- Strikte Trennung Studio/Projekt
  - Regelmäßige README-Updates
  - CHANGELOG bei jeder Änderung
  - Dokumentation als Pflicht
```

---

## Referenzen

- `.quinsy-studio/process/learning-loop.md` — Dual-Loop Learning
- `CHANGELOG.md` — Studio-Changelog
- `README.md` — Studio-README
