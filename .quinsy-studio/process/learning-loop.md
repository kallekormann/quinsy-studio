# Quinsy Studio — Learning Loop

> Das Studio lernt aus seinen Fehlern. Jeder Mistake wird analysiert und in Verbesserungen umgewandelt.

## Grundprinzip

```
Fehler → Learning Item → Meta-Retro → Verbesserung → CHANGELOG
```

---

## Learning-Items erfassen

```bash
./studio learn "<Titel>" --signal <Signal> --source <Quelle>
```

### Signale

| Signal | Beschreibung | Aktion |
|--------|-------------|--------|
| `gate-fail` | Gate-Prüfung fehlgeschlagen | Gate-Kriterien überprüfen |
| `rework` | Arbeit musste wiederholt werden | Prozess-Schritt analysieren |
| `tooling-gap` | Tooling fehlte oder war unzureichend | CLI/Tooling erweitern |
| `design-gap` | Design-Spezifikation war unzureichend | Design-Process verbessern |
| `process-gap` | Prozess-Schritt war unklar | Process-Docs aktualisieren |
| `knowledge-gap` | Wissen fehlte | Team-Skill erweitern |
| `sloppy-code` | AI-Slop erkannt | Anti-Slop-Regeln verschärfen |
| `slow-gate` | Gate-Check dauerte zu lang | Gate-Optimierung |

### Learning-Item-Format

```markdown
---
id: LO-NNNN
title: <Titel>
status: open | in-progress | done
signal: <Signal>
source: <Quelle>
priority: P0-P3
created: YYYY-MM-DD
updated: YYYY-MM-DD
---

# LO-NNNN — <Titel>

## Beobachtung
Was ist passiert / was fehlt?

## Auswirkung
Welche Folge hatte das (Rework, Unsicherheit, Qualitätsrisiko)?

## Vorschlag
Wie soll Prozess / Skill / Tooling verbessert werden?

## Status
- [ ] Im Meta-Retro besprochen
- [ ] Umgesetzt (CHANGELOG.md-Eintrag, Version aktualisiert)
```

---

## Learning-Items auflisten

```bash
./studio learn-list
```

Zeigt alle offenen Learning Items.

---

## Meta-Retrospektive

```bash
./studio retro <project>
```

### Ablauf

1. **Learning Items sammeln**
   - Offene LOs aus `./studio learn-list`
   - Feedback aus Sprint-Retros
   - Gate-Fehler-Analyse

2. **Skill-Review**
   - Jeder Team-Skill wird geprüft
   - Qualitätssignale sammeln
   - Verbesserungen identifizieren

3. **Entscheidungen**
   - Was wird geändert?
   - Was wird beibehalten?
   - Priorisierung

4. **Action Items**
   - Konkrete Änderungen
   - Owner zuweisen
   - Deadline setzen

5. **CHANGELOG**
   - Jede Änderung wird dokumentiert
   - Version aktualisieren

### Retro-Template

```markdown
# Meta-Retro — YYYY-MM-DD

## Eingegangene Learning Items
- LO-0000: ...

## Skill-Review
| Skill | Qualitätssignal | Aktion |
|-------|-----------------|--------|
| ... | ... | ... |

## Entscheidungen
- ... (jede Änderung → CHANGELOG.md-Eintrag)

## Action Items
- [ ] ... (Owner: ...)
- [ ] ... (Owner: ...)
```

---

## CHANGELOG pflegen

Jede Änderung am Studio wird im CHANGELOG dokumentiert:

```markdown
## [1.1.0] — 2026-08-21

### Geändert
- Gate-Check optimiert (30% schneller)
- Anti-Slop-Regeln verschärft (neue Regel: C5)

### Hinzugefügt
- Neuer Befehl: `./studio audit <project>`
- Team-Skill 07: Anti-Slop-Sektion erweitert

### Behoben
- Gate-History Bug behoben
```

---

## Integration

Der Learning Loop ist ein ** kontinuierlicher Prozess**:

```
┌─────────────────────────────────────────────────────────┐
│                 LEARNING LOOP                           │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  1. Arbeiten                                            │
│     └─▶ Fehler passieren                               │
│                                                         │
│  2. Learning Item anlegen                               │
│     └─▶ `./studio learn \"...\" --signal ...`          │
│                                                         │
│  3. Meta-Retro                                          │
│     └─▶ `./studio retro <project>`                     │
│                                                         │
│  4. Verbesserung umsetzen                               │
│     └─▶ Process/Tool/Skill anpassen                    │
│                                                         │
│  5. CHANGELOG aktualisieren                             │
│     └─▶ Version bump                                   │
│                                                         │
│  6. Zurück zu 1                                         │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

---

## Referenzen

- `.quinsy-studio/process/iterative-delivery.md` — Sprint/Retro
- `.quinsy-studio/process/gates.md` — Gate-Definitionen
- `CHANGELOG.md` — Änderungshistorie
