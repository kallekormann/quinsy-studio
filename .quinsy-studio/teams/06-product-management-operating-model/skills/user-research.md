# Skill: User Research

> Problem-Interviews, Solution-Interviews, Surveys, Usability-Tests, Analytics

## Metadata

```
skill_id: PM-001
name: User Research
team: 06-product-management-operating-model
lead_role: Product Manager
support_roles: [UI/Interaction Designer, Growth Manager]
phases: [0, 1, 3, 5, 7]
activation_triggers:
  - Ticket enthält "Research", "Interview", "Survey", "Usability"
  - Phase 0: Problem wird validiert
  - Phase 1: Lösung wird validiert
  - Phase 5: Usability wird getestet
  - Phase 7: Optimierung basiert auf Feedback
```

---

## Verhaltensregeln

### 1. Problem-Interviews

```markdown
Ziel: Problem verstehen, nicht Lösung verkaufen

Struktur (15-30 Min):
  1. Kontext: "Erzählen Sie von..."
  2. Problem: "Was ist dabei frustrierend?"
  3. Aktuelle Lösung: "Wie lösen Sie das heute?"
  4. Wert: "Was würden Sie dafür bezahlen?"
  5. Abschluss: "Gibt es noch etwas?"

Regeln:
  - 80% Zuhören, 20% Fragen
  - Keine Lösung vorschlagen
  - Follow-up Fragen stellen
  - Emotionen und Zitate notieren
```

### 2. Solution-Interviews

```markdown
Ziel: Lösung testen, nicht Features verkaufen

Struktur:
  1. Konzept zeigen (nichts erklären)
  2. "Was verstehen Sie?"
  3. "Wie würden Sie das nutzen?"
  4. "Was fehlt?"
  5. "Würden Sie dafür bezahlen?"

Regeln:
  - Prototyp zeigen (nicht erzählen)
  - Geduld haben (Nutzer denken lassen)
  - Verwirrung = Design-Problem
```

### 3. Surveys

```markdown
Wann: Quantitatives Feedback zu vielen Usern

Struktur:
  - Max. 10 Fragen
  - Mix aus Multiple Choice + Open
  - Likert-Skala (1-5 oder 1-7)
  - Demografie am Ende

Regeln:
  - Keine suggestiven Fragen
  - Keine Doppel-Fragen
  - Testen mit 3 Leuten vorher
  - Anreiz für Teilnahme
```

### 4. Usability-Tests

```markdown
Struktur (30-45 Min):
  1. Kontext: "Stellen Sie sich vor..."
  2. Aufgabe: "Bitte finden Sie..."
  3. Laut Denken: "Was denken Sie gerade?"
  4. Follow-up: "Warum haben Sie...?"

Regeln:
  - 5 User = 80% der Probleme
  - Keine Hilfestellung
  - Protokollieren: wo scheitert der User?
  - Severity rating: kritisch / mittel / niedrig
```

### 5. Analytics

```markdown
Tools: Plausible / PostHog / Google Analytics

Metriken:
  - Pageviews, Unique Visitors
  - Bounce Rate
  - Time on Page
  - Conversion Rate
  - User Flows (wo gehen User hin?)
  - Drop-off Points (wo brechen User ab?)

Für Entscheidungen:
  - Quantitative Daten (Analytics) +
  - Qualitative Daten (Interviews) =
  - Fundierte Entscheidung
```

---

## Anti-Patterns

### ❌ Verboten

```markdown
- Feature-Requests als User Needs interpretieren
  - Nur quantitative Daten (keine Interviews)
  - Leading Questions ("Stimmen Sie zu, dass...")
  - Nur 1-2 User testen
  - Lösung in Interviews verraten
```

### ✅ Stattdessen

```markdown
- "Five Whys" für tieferes Verständnis
  - Mix aus qualitativ und quantitativ
  - Offene Fragen stellen
  - Min. 5 User für Usability-Tests
  - Problem verstehen, nicht Lösung verkaufen
```

---

## Referenzen

- `.quinsy-studio/process/lifecycle.md` — Phasen
- `.quinsy-studio/knowledge-base/design_playbook.md` — UX-Heuristiken
