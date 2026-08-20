# Skill: Roadmapping

> Now/Next/Later, RICE/MoSCoW, Abhängigkeiten, Stakeholder-Alignment

## Metadata

```
skill_id: PM-002
name: Roadmapping
team: 06-product-management-operating-model
lead_role: Product Manager
support_roles: [Product Strategist, Systems Architect]
phases: [1, 3, 7]
activation_triggers:
  - Ticket enthält "Roadmap", "Priorisierung", "Planning"
  - Phase 1: Erste Roadmap wird erstellt
  - Phase 3: Sprint-Roadmap
  - Phase 7: Nächste Iteration
```

---

## Verhaltensregeln

### 1. Roadmap-Format

```markdown
Now (0-3 Monate):
  - Kritische Features für Launch
  - Quick Wins (hoher Impact,低 Aufwand)
  - Bug-Fixes die Users stören

Next (3-6 Monate):
  - Growth-Features
  - Monetarisierung
  - Performance-Optimierung

Later (6-12 Monate):
  - Enterprise Features
  - Internationalisierung
  - Advanced Analytics
```

### 2. Priorisierung

```markdown
RICE Score:
  Reach × Impact × Confidence / Effort

  Reach:     Wie viele User betrifft es? (pro Quartal)
  Impact:    Wie stark ist der Impact? (0.25, 0.5, 1, 2, 3)
  Confidence: Wie sicher sind wir? (100%, 80%, 50%)
  Effort:    Aufwand in Person-Monaten

MoSCoW:
  Must:     Ohne kein MVP
  Should:   Wichtig aber verzögerbar
  Could:    Nice-to-have
  Won't:    Nicht in diesem Release
```

### 3. Abhängigkeiten

```markdown
Für jede Epic/Feature:
  - Vorherige Abhängigkeiten (was muss zuerst sein?)
  - Nachfolgende Abhängigkeiten (was braucht das Feature?)
  - Cross-Team Abhängigkeiten
  - Externe Abhängigkeiten (APIs, Services)

Darstellung:
  - Dependency Map
  - Critical Path identifizieren
  - Blockierer frühzeitig erkennen
```

### 4. Stakeholder-Alignment

```markdown
Regelmäßiges Update:
  - Was wurde geliefert?
  - Was ist als nächstes?
  - Was sind die Risiken?
  - Brauchen wir Entscheidungen?

Format:
  - Executive Summary (1 Seite)
  - Feature-Status (Tabelle)
  - Risiken und Blocker
  - Nächste Schritte
```

---

## Anti-Patterns

### ❌ Verboten

```markdown
- Alles ist "Priority 1"
  - Keine Abhängigkeiten dokumentiert
  - Roadmap ohne Zeitfenster
  - Kein Stakeholder-Update
  - Feature-Factory ( Outputs statt Outcomes)
```

### ✅ Stattdessen

```markdown
- Klare Priorisierung (RICE/MoSCoW)
  - Abhängigkeiten dokumentiert
  - Now/Next/Later mit Zeitfenster
  - Regelmäßige Stakeholder-Updates
  - Outcome-basierte Roadmap
```

---

## Referenzen

- `.quinsy-studio/process/iterative-delivery.md` — Sprint/Grooming
- `.quinsy-studio/process/lifecycle.md` — Phasen
