# Skill: Anti-Slop Audit

> AI-Code-Erkennung, Code-Qualitätsprüfung, Anti-Pattern-Detection

## Metadata

```
skill_id: AI-002
name: Anti-Slop Audit
team: 07-ai-autonomous-systems
lead_role: Process Guard
support_roles: [AI Architect, QA Specialist]
phases: [4, 5]
activation_triggers:
  - Ticket enthält "Anti-Slop", "Slop", "AI-Code", "Qualität"
  - Phase 5: QA-Gate prüft Anti-Slop
  - Reuse-Review: Code wird zur Library promoted
  - Verdacht auf AI-generierten Code
```

---

## Verhaltensregeln

### 1. Anti-Slop-Checkliste

```markdown
Code-Pattern-Erkennung:
  - Übermäßige Kommentare (jede Zeile kommentiert)
  - Redundante Variablen
  - Unnötige Imports
  - Übermäßige Error-Handling-Blöcke
  - TODO-Kommentare ohne Kontext
  - Übermäßige Log-Aufrufe
  - Unnötige Delay/Fake-Daten
  - Redundante Validierung
```

### 2. Text-Pattern (AI-Floskeln)

```markdown
Schwarze Liste:
  - "In today's digital landscape"
  - "Revolutionize" / "Revolutionary"
  - "Seamless" / "Seamlessly"
  - "Empower" / "Empowering"
  - "Leverage" / "Leveraging"
  - "Cutting-edge" / "State-of-the-art"
  - "Furthermore" / "Moreover"
  - "It's worth noting that"
  - "Delve" / "Delving"
  - "Tapestry" / "Multifaceted"
  - "Game-changer"
  - "Unlock the potential"
```

### 3. Qualitäts-Prüfung

```markdown
Für jede Code-Datei:
  - Komplexe Funktionen (>50 Zeilen)?
  - Maximale Verschachtelung (>3 Ebenen)?
  - Zu viele Parameter (>5)?
  - Fehlende Typisierung?
  - Dead Code?
  - Performance-Issues (N+1, fehlende Indices)?
```

### 4. Audit-Workflow

```markdown
Schritt 1: Statischer Check
  - Linting (ESLint, Prettier)
  - Type-Check (TypeScript)
  - Complexity-Analyse

Schritt 2: Pattern-Matching
  - AI-Floskeln in Kommentaren/Strings
  - Übermäßige Log-Aufrufe
  - Redundanter Code

Schritt 3: Review
  - Code-Sinnhaftigkeit prüfen
  - Performance prüfen
  - Sicherheit prüfen

Schritt 4: Report
  - Fehler (muss gefixt werden)
  - Warnungen (sollte gefixt werden)
  - Vorschläge (könnte verbessert werden)
```

### 5. Integration in QA-Gate

```markdown
./studio gate <project> --anti-slop

Output:
  ✅ Anti-Slop: 0 Errors, 3 Warnings
  ❌ Anti-Slop: 5 Errors (müssen gefixt werden)

Regel: 0 Anti-Slop Errors für Gate-Pass
```

---

## Anti-Patterns

### ❌ Verboten

```markdown
- AI-generierter Code ohne Review
  - Übermäßige TODO-Kommentare
  - Redundanter Code wird nicht bereinigt
  - Anti-Slop-Check nur optional
  - Kein Anti-Slop im QA-Gate
```

### ✅ Stattdessen

```markdown
- Jeder Code wird geprüft
  - Klare, nützliche Kommentare
  - Redundanter Code wird entfernt
  - Anti-Slop als Pflicht-Check im QA-Gate
  - Pattern-Detection in CI/CD
```

---

## Referenzen

- `.quinsy-studio/knowledge-base/anti_ai_slop_protocol.md` — Anti-Slop-Regeln
- `.quinsy-studio/process/gates.md` — Anti-Slop im Gate 5
- `studio-tools/validate_anti_slop.py` — Automatisierter Check
