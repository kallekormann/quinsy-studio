# Skill: Feasibility Analysis

> Machbarkeitsprüfung, Risikoanalyse, Kapazitätsplanung, Scope-Definition

## Metadata

```
skill_id: PS-004
name: Feasibility Analysis
team: 04-product-strategy-architecture
lead_role: Systems Architect
support_roles: [Product Manager, Backend Architect]
phases: [0, 1]
activation_triggers:
  - Ticket enthält "Machbarkeit", "Feasibility", "Risiko", "Scope"
  - Phase 0: Neues Projekt wird evaluiert
  - Phase 1: Scope wird definiert
  - Komplexe Feature-Anforderung
```

---

## Verhaltensregeln

### 1. Machbarkeitsprüfung

```markdown
Dimensionen:
  - Technisch: Ist es machbar?
  - Wirtschaftlich: Lohnt sich der Aufwand?
  - Zeitlich: Ist der Zeitplan realistisch?
  - Ressourcen: Haben wir die Skills?
  - Legal: Ist es rechtlich erlaubt?

Für jede Dimension:
  - Status: ✅ machbar / ⚠️ risikobehaftet / ❌ nicht machbar
  - Begründung
  - Risiken
  - Empfehlung
```

### 2. Risikoanalyse

```markdown
Pro Risiko:
  - Beschreibung
  - Eintrittswahrscheinlichkeit (1-5)
  - Auswirkung (1-5)
  - Risiko-Score (W × A)
  - Gegenmaßnahme
  - Verantwortlicher

Risiko-Matrix:
  5×5 = 25 (kritisch)
  4×4 = 16 (hoch)
  3×3 = 9 (mittel)
  2×2 = 4 (niedrig)
  1×1 = 1 (minimal)
```

### 3. Scope-Definition

```markdown
MoSCoW-Priorisierung:
  Must:     Ohne diese Features kein MVP
  Should:   Wichtig aber verzögerbar
  Could:    Nice-to-have
  Won't:    Nicht in diesem Release

Scope-Checks:
  - Passt es ins Zeitbudget?
  - Sind die Abhängigkeiten geklärt?
  - Gibt es Quick Wins?
  - Was kann weggelassen werden ohne Wertverlust?
```

### 4. Kapazitätsplanung

```markdown
Für jede Phase:
  - Benötigte Rollen
  - Geschätzte Stunden
  - Abhängigkeiten
  - Risiko-Puffer (20-30%)

Team-Verfügbarkeit:
  - Wer ist wann verfügbar?
  - Gibt es Abhängigkeiten zu anderen Projekten?
  - Urlaub / Feiertage
```

---

## Anti-Patterns

### ❌ Verboten

```markdown
- "Das schaffen wir schon" ohne Analyse
- Kein Risiko-Plan
- Unrealistische Zeitpläne
- Scope Creep ohne Priorisierung
- Kein Rollback-Plan
```

### ✅ Stattdessen

```markdown
- Strukturierte Machbarkeitsprüfung
- Risiko-Matrix mit Gegenmaßnahmen
- Realistische Zeitpläne mit Puffer
- MoSCoW-Priorisierung
- Rollback-Plan für jede Phase
```

---

## Referenzen

- `.quinsy-studio/process/lifecycle.md` — Phasen
- `.quinsy-studio/process/project-archetypes.md` — Archetypen
