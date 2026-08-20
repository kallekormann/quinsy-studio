# Skill: Studio Tooling Maintenance

> Wartung, Refactoring und Verbesserung der Python-Tools im Studio-HQ

## Metadata

```
skill_id: SO-001
name: Studio Tooling Maintenance
team: 09-studio-operations-evolution
lead_role: Studio Automation Engineer
support_roles: [Platform Architect]
phases: [6, 7]
activation_triggers:
  - Ticket enthält "Studio Tools", "Python", "Tooling", "Wartung"
  - /studio-evolution Befehl
  - Phase 6: Learning Loop identifiziert Tooling-Verbesserungen
  - Performance-Probleme bei Studio-Tools
```

---

## Verhaltensregeln

### 1. Python-Tools pflegen

```markdown
Dateien in .quinsy-studio/studio-tools/:
  - validate_anti_slop.py    → Anti-Slop-Erkennung
  - run_qa_gate.py           → QA-Gate-Orchestrierung
  - generate_ticket_manifest.py → Ticket-Generierung
  - sync_global_assets.py    → Asset-Promotion
  - init_project_env.py      → Projekt-Initialisierung
  - requirements.txt         → Dependencies

Regelmäßige Wartung:
  - Dependencies updaten (weekly)
  - Security-Scans
  - Performance-Benchmarks
  - Unit-Tests schreiben/aktualisieren
```

### 2. Refactoring-Regeln

```markdown
Beim Refactoring:
  - API backward-compatible halten
  - CHANGELOG.md eintragen
  - README.md aktualisieren
  - Tests aktualisieren
  - Keine Breaking Changes ohne Version-Bump
```

### 3. Monitoring

```markdown
Was tracken:
  - Ausführungszeit pro Tool
  - Erfolgsrate
  - Häufigkeit der Nutzung
  - Fehler-Logs
```

---

## Anti-Patterns

### ❌ Verboten

```markdown
- Breaking Changes ohne Versionierung
  - Keine Tests für geänderte Tools
  - Dependencies nicht updaten
  - Debug-Code in Production
```

### ✅ Stattdessen

```markdown
- Semantic Versioning
  - Tests vor jedem Deploy
  - Regelmäßige Dependency-Updates
  - Sauberer Production-Code
```

---

## Referenzen

- `.quinsy-studio/studio-tools/` — Python-Automation
- `.quinsy-studio/process/learning-loop.md` — Learning Loop
