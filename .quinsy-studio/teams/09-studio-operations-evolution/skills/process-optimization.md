# Skill: Process Optimization

> Sprint-Disziplin, Studio-Abläufe, Metriken, Anti-Patterns im Prozess

## Metadata

```
skill_id: SO-002
name: Process Optimization
team: 09-studio-operations-evolution
lead_role: Process Guard
support_roles: [Agile Coach]
phases: [3, 5, 6, 7]
activation_triggers:
  - Ticket enthält "Prozess", "Sprint-Disziplin", "Optimierung"
  - Phase 3: Sprint-Setup wird geprüft
  - Phase 5: QA-Gate identifiziert Prozess-Lücken
  - Phase 6: Retro identifiziert Verbesserungen
  - /studio-evolution Befehl
```

---

## Verhaltensregeln

### 1. Sprint-Disziplin

```markdown
Was prüfen:
  - Werden alle 9 Schritte des Ticket-Workflows eingehalten?
  - Wird TDD tatsächlich angewendet?
  - Wird Anti-Slop-Audit durchgeführt?
  - Werden Gates eingehalten?
  - Wird dokumentiert?

Bei Verstößen:
  - Ticket geht zurück zum fehlenden Schritt
  - Learning wird protokolliert
  - Prozess-Lücke wird geschlossen
```

### 2. Studio-Metriken

```markdown
Was tracken:
  - Sprint-Velocity (Story Points pro Sprint)
  - Ticket-Durchlaufzeit (Intake → Done)
  - Gate-Pass-Rate (erstes Mal bestanden)
  - Anti-Slop-Error-Rate
  - Learning-Items pro Sprint
  - Local vs. Global Learnings Ratio

Ziel:
  - Velocity stabil oder steigend
  - Durchlaufzeit sinkend
  - Gate-Pass-Rate > 80%
  - Anti-Slop-Error-Rate < 5%
```

### 3. Anti-Patterns im Prozess

```markdown
Erkennung:
  - Tickets die im "implement" hängen (>3 Tage)
  - Steps die übersprungen werden
  - Gates die nicht durchlaufen werden
  - Fehlende Dokumentation
  - Kein Learning aus Fehlern

Gegenmaßnahmen:
  - Automatische Erinnerungen
  - Stricter Gate-Checks
  - Prozess-Verbesserungen im Global Loop
```

---

## Anti-Patterns

### ❌ Verboten

```markdown
- Prozess wird nicht geprüft
  - Metriken werden nicht getrackt
  - Verstöße werden nicht dokumentiert
  - Keine Verbesserungen aus Lernings
```

### ✅ Stattdessen

```markdown
- Regelmäßige Prozess-Checks
  - Metriken-Dashboard
  - Verstöße → Learning → Verbesserung
  - Iterative Prozess-Optimierung
```

---

## Qualitätssicherung: Skill-Matching-Test

Der Skill-Matching-Test verifiziert, dass Tickets korrekt auf interne UND externe Skills
gemappt werden (`.quinsy-studio/studio-tools/test_skill_matching.py`):

```bash
python3 .quinsy-studio/studio-tools/test_skill_matching.py
```

**Ausführen nach:**
- Neuen Trigger-Wörtern / Skill hinzugefügt
- Neuer externer Skill-Dependency
- Änderung an der Skill-Registry

**Testfälle (7):** Design-System, SEO/AEO, Cookie-Compliance, Database, Security, Game-Dev, Copywriting.
Erwartung: `7/7` Tickets gematcht, `29/29` externe Quellen auf Disk.

## Referenzen

- `.quinsy-studio/process/lifecycle.md` — Phasen
- `.quinsy-studio/process/ticket-workflow.md` — 9-Schritte-Workflow
- `.quinsy-studio/process/iterative-delivery.md` — Sprint/Grooming
