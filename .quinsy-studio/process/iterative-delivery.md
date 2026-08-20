# Quinsy Studio — Iterative Delivery

> Ab Phase 3 wird iterativ gearbeitet. Sprints, Grooming und das Backlog-Board sind die Triebwerke.

## Grundprinzip

```
Iterativ = planen → bauen → prüfen → lernen → wiederholen
```

Kein Sprint ist identisch; jeder Sprint lernt aus dem vorherigen.

---

## Sprint-Zyklus

```
┌─────────────────────────────────────────────────────────┐
│                    SPRINT-ZYKLUS                        │
└─────────────────────────────────────────────────────────┘

 ┌──────────────┐
 │   SPRINT     │ ◀──────────────────────────────┐
 │   START      │                                │
 └──────┬───────┘                                │
        │                                        │
        ▼                                        │
 ┌──────────────┐                                │
 │   GROOMING   │                                │
 │   (Board)    │                                │
 └──────┬───────┘                                │
        │                                        │
        ▼                                        │
 ┌──────────────┐                                │
 │   TICKETS    │                                │
 │   BEARBEITEN │                                │
 └──────┬───────┘                                │
        │                                        │
        ▼                                        │
 ┌──────────────┐                                │
 │   QA-GATE    │                                │
 └──────┬───────┘                                │
        │                                        │
        ▼                                        │
 ┌──────────────┐                                │
 │   RETRO      │ ──── Learning Items ──────────┘
 │   + REVIEW   │
 └──────────────┘
```

---

## Sprint-Struktur

Jeder Sprint hat:
- **Name:** `SPRINT-01`, `SPRINT-02`, ...
- **Dauer:** variabel (je nach Projekt)
- **Fokus:** ein oder mehrere Features
- **Ziel:** klare Definition von Done

### Sprint-Verzeichnis

```
<project>/sprints/
├── SPRINT-01/
│   ├── plan.md          # Sprint-Planung
│   ├── summary.md       # Sprint-Zusammenfassung
│   ├── grooming.md      # Grooming-Protokoll
│   └── retro.md         # Retrospektive
├── SPRINT-02/
│   └── ...
```

---

## Sprint-Planung

```bash
./studio sprint <project>
```

Erstellt `sprints/SPRINT-NN/plan.md` mit Template:

```markdown
# Sprint-Planung — SPRINT-NN

**Ziel:** <Was soll in diesem Sprint erreicht werden?>
**Start:** YYYY-MM-DD
**Ende:** YYYY-MM-DD
**Kapazität:** <realistische Einschätzung>

## Tickets in diesem Sprint

| Ticket | Titel | Phase | Priorität | Geschätzt |
|--------|-------|-------|-----------|-----------|
| TICKET-NNN | ... | 4 | P1 | M |

## Abhängigkeiten
- ...

## Risiken
- ...

## Definition of Done
- [ ] Alle Tickets im Status "done"
- [ ] QA-Test grün
- [ ] Anti-Slop-Audit: 0 Error
- [ ] Retrospektive durchgeführt
- [ ] Summary geschrieben
```

---

## Grooming

```bash
./studio groom <project>
```

Das Grooming ist die wöchentliche Board-Besprechung:

### Grooming-Agenda

1. **Blockierte Tickets prüfen**
   - Kann der Blocker behoben werden?
   - Soll das Ticket geschlossen werden?

2. **Priorisierung**
   - Sind die Prioritäten noch aktuell?
   - Sollen Tickets umsortiert werden?

3. **Abhängigkeiten**
   - Gibt es neue Abhängigkeiten?
   - Sind Abhängigkeiten aufgelöst?

4. **Kapazität**
   - Ist der Sprint realistisch geplant?
   - Sollen Tickets verschoben werden?

5. **Neue Tickets**
   - Gibt es neue Anforderungen?
   - Sollen sie als Tickets angelegt werden?

### Grooming-Protokoll

```markdown
# Grooming-Protokoll — SPRINT-NN

**Datum:** YYYY-MM-DD
**Teilnehmer:** Project Manager, ...

## Blockierte Tickets
| Ticket | Grund | Aktion |
|--------|-------|--------|
| ... | ... | ... |

## Priorisierungsänderungen
| Ticket | Neue Priorität | Grund |
|--------|---------------|-------|
| ... | ... | ... |

## Neue Tickets
| Ticket | Titel | Priorität |
|--------|-------|-----------|
| ... | ... | ... |

## Kapazitätsanpassungen
- ...

## Nächste Schritte
- ...
```

---

## Backlog-Board

Das Board zeigt alle Tickets ihres aktuellen Status:

```bash
./studio board <project>
```

### Board-Ansicht

```
┌─────────────┬─────────────┬─────────────┬─────────────┬─────────────┐
│    OPEN     │  IN PROGRESS│    QA       │   REVIEW    │    DONE     │
├─────────────┼─────────────┼─────────────┼─────────────┼─────────────┤
│ TICKET-008  │ TICKET-007  │ TICKET-006  │ TICKET-005  │ TICKET-001  │
│ TICKET-009  │             │             │             │ TICKET-002  │
│ TICKET-010  │             │             │             │ TICKET-003  │
│ TICKET-011  │             │             │             │ TICKET-004  │
└─────────────┴─────────────┴─────────────┴─────────────┴─────────────┘
```

### Board-Filter

```bash
./studio board <project> --phase 4
./studio board <project> --priority P0
./studio board <project> --assignee "frontend"
```

---

## Ticket-Bewegung

```bash
# Ticket in nächsten Status verschieben
./studio move <project> TICKET-NNN <status> [--reason "Grund"]

# Beispiele
./studio move nudge TICKET-007 implement --reason "Implementierung gestartet"
./studio move nudge TICKET-007 qa --reason "QA gestartet"
./studio move nudge TICKET-007 done --reason "Alle Kriterien erfüllt"
```

**Regel:** Jede Bewegung wird dokumentiert (Status-Änderung + Grund).

---

## Sprint-Review

Am Ende jedes Sprints:

```markdown
# Sprint-Review — SPRINT-NN

## Erreicht
- [x] TICKET-001: ...
- [x] TICKET-002: ...

## Nicht erreicht ( verschoben)
- [ ] TICKET-003: ... (Grund: ...)

## Metriken
- Geplant: 5 Tickets
- Geschafft: 3 Tickets
- Quote: 60%
- Durchschnittliche Dauer: 2 Tage/Ticket

## Velocity
- SPRINT-01: 3 Tickets
- SPRINT-02: 4 Tickets (+1)
- Trend: 📈
```

---

## Retrospektive

Nach jedem Sprint:

```bash
./studio retro <project>
```

### Retro-Template

```markdown
# Retrospektive — SPRINT-NN

## Was lief gut? 🟢
- ...

## Was lief schlecht? 🔴
- ...

## Was können wir verbessern? 🟡
- ...

## Learning Items
| Item | Signal | Quelle | Aktion |
|------|--------|--------|--------|
| ... | ... | ... | ... |

## Action Items
- [ ] ... (Owner: ...)
- [ ] ... (Owner: ...)
```

---

## Learning Items

```bash
./studio learn "<Titel>" --signal <Signal> --source <Quelle>
```

### Learning-Signale

| Signal | Bedeutung |
|--------|-----------|
| `gate-fail` | Gate-Prüfung fehlgeschlagen |
| `rework` | Arbeit musste wiederholt werden |
| `tooling-gap` | Tooling fehlte oder war unzureichend |
| `design-gap` | Design-Spezifikation war unzureichend |
| `process-gap` | Prozess-Schritt war unklar |
| `knowledge-gap` | Wissen fehlte |

### Learning-Item-Template

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

## Status-Datei

Jedes Projekt hat eine `status.json`:

```json
{
  "name": "nudge",
  "phase": "5",
  "gate": "4",
  "gate_status": "bestanden",
  "created": "2026-08-19",
  "last_update": "2026-08-19",
  "archetype": "saas-application",
  "current_sprint": "SPRINT-01",
  "active_ticket": "TICKET-007",
  "velocity": {
    "SPRINT-01": 3,
    "SPRINT-02": 4
  },
  "gate_history": [
    {
      "gate": 0,
      "status": "grün",
      "passed_at": "2026-08-19T10:00:00Z"
    }
  ]
}
```

---

## Referenzen

- `.quinsy-studio/process/ticket-workflow.md` — 9-Schritte-Ticket-Workflow
- `.quinsy-studio/process/gates.md` — Gate-Definitionen
- `.quinsy-studio/process/lifecycle.md` — Phasen-Überblick
- `./studio sprint <project>` — Sprint anlegen
- `./studio groom <project>` — Grooming durchführen
- `./studio board <project>` — Board anzeigen
- `./studio move <project> <id> <status>` — Ticket bewegen
- `./studio learn "<Titel>"` — Learning Item anlegen
- `./studio retro <project>` — Retrospektive starten
