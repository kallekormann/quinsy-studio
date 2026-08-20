# Quinsy Studio — Ticket-Workflow

> Jedes Ticket durchläuft einen strikten 9-Schritte-Workflow.
> Kein Schritt wird übersprungen; jeder Schritt wird dokumentiert.

## Workflow-Übersicht

```
┌─────────────────────────────────────────────────────────────────┐
│                    9-SCHRITTE-TICKET-WORKFLOW                   │
└─────────────────────────────────────────────────────────────────┘

 1. INTAKE          ──▶  Ticket wird erstellt
       │
 2. ANALYSE         ──▶  Anforderungen werden analysiert
       │
 3. PLANUNG         ──▶  Umsetzung wird geplant
       │
 4. DESIGN          ──▶  Design/Architektur wird definiert
       │
 5. IMPLEMENTATION  ──▶  Code wird geschrieben
       │
 6. QA-GATE         ──▶  Qualität wird geprüft
       │
 7. REVIEW          ──▶  Code-Review wird durchgeführt
       │
 8. REUSE-REVIEW    ──▶  Wiederverwendbarkeit wird geprüft
       │
 9. DONE            ──▶  Ticket wird abgeschlossen
```

---

## Die 9 Schritte (Verbindlich)

| # | Schritt | Beschreibung |
|---|---------|-------------|
| 1 | **Aufnahme & Verstehen** | Ticket lesen, Kontext verstehen, Fragen klären |
| 2 | **Zerlegung & Abhängigkeiten** | In Sub-Tasks aufteilen, Abhängigkeiten identifizieren |
| 3 | **Konzeption/Design** | Lösungsansatz definieren, Architektur-Entscheidungen |
| 4 | **Umsetzung (Clean Code, TDD)** | Code schreiben, Tests schreiben, Tests grün |
| 5 | **Selbstprüfung (Tests, Lint, Review)** | Eigenständige Qualitätsprüfung |
| 6 | **QA-Gate** | `./studio gate <project>` muss grün sein |
| 7 | **Doku & ADR-Sync** | Dokumentation aktualisieren, ADRs anlegen/updaten |
| 8 | **Reuse-Review** | Wiederverwendbar? → `./studio promote` + Doku |
| 9 | **Abschluss** | Status `done`, status.json aktualisieren |

**Regel:** Kein Schritt wird übersprungen. Jeder Schritt wird dokumentiert.

---

## Detail-Schritte

### Schritt 1: Aufnahme & Verstehen

```bash
./studio ticket <project> "<Titel>" --phase <N> --priority <P> --estimate <E>
```

| Aspekt | Beschreibung |
|--------|-------------|
| **Aktion** | Ticket erstellen mit allen Metadaten |
| **Output** | `<project>/backlog/open/TICKET-NNN-<slug>.md` |
| **Verantwortlich** | Project Manager |

**Ticket-Template:**
```markdown
---
id: TICKET-NNN
title: <Titel>
status: open
phase: <N>
priority: <P0-P3>
estimate: <S/M/L/XL>
created: YYYY-MM-DD
assignee: <Rolle>
---

# TICKET-NNN — <Titel>

## Akzeptanzkriterien
- [ ] Kriterium 1
- [ ] Kriterium 2
- [ ] Kriterium 3

## Technische Anforderungen
...

## Abhängigkeiten
- ...

## Begründung
Warum ist dieses Ticket wichtig?
```

---

### Schritt 2: Zerlegung & Abhängigkeiten

```bash
./studio move <project> TICKET-NNN analyze --reason "Zerlegung durchgeführt"
```

| Aspekt | Beschreibung |
|--------|-------------|
| **Aktion** | In Sub-Tasks aufteilen, Abhängigkeiten identifizieren |
| **Output** | Ticket mit Sub-Tasks und Abhängigkeiten |
| **Verantwortlich** | Project Manager + Tech Lead |

**Checkliste:**
- [ ] Ticket in Sub-Tasks zerlegt
- [ ] Abhängigkeiten zu anderen Tickets dokumentiert
- [ ] Blockierer identifiziert
- [ ] Schätzungen für Sub-Tasks

---

### Schritt 3: Konzeption/Design

```bash
./studio move <project> TICKET-NNN design --reason "Konzeption abgeschlossen"
```

| Aspekt | Beschreibung |
|--------|-------------|
| **Aktion** | Lösungsansatz definieren, Architektur-Entscheidungen |
| **Output** | Design-Spezifikation, ggf. ADR |
| **Verantwortlich** | Relevante Fachrollen |

**Checkliste:**
- [ ] Lösungsansatz dokumentiert
- [ ] Architektur-Entscheidungen als ADR (falls nötig)
- [ ] UI-Komponenten definiert (falls Frontend)
- [ ] Datenmodell definiert (falls Backend)
- [ ] API-Design definiert (falls API)

---

### Schritt 4: Umsetzung (Clean Code, TDD)

```bash
./studio move <project> TICKET-NNN implement --reason "Implementierung gestartet"
```

| Aspekt | Beschreibung |
|--------|-------------|
| **Aktion** | Code schreiben (Test-First!) |
| **Output** | Lauffähiger Code mit Tests |
| **Verantwortlich** | Backend Systems / Frontend Experience |

**Regeln:**
- ✅ Test-First (TDD)
- ✅ Clean Code / SOLID
- ✅ Spezifische Error-Handling
- ✅ Kein AI-Slop
- ✅ Dokumentation
- ❌ Kein Code ohne Ticket
- ❌ Kein Commit ohne grüne Tests

---

### Schritt 5: Selbstprüfung (Tests, Lint, Review)

```bash
# Tests ausführen
pnpm test
# Linting
pnpm lint
# Build
pnpm build
```

| Aspekt | Beschreibung |
|--------|-------------|
| **Aktion** | Eigenständige Qualitätsprüfung |
| **Output** | Alle Checks grün |
| **Verantwortlich** | Implementierender Agent |

**Checkliste:**
- [ ] Alle Tests grün
- [ ] Keine Linting-Errors
- [ ] Build erfolgreich
- [ ] Code-Review (selbst oder Peer)
- [ ] Kein AI-Slop (Anti-Slop-Check)

---

### Schritt 6: QA-Gate

```bash
./studio gate <project> --level 5
```

| Aspekt | Beschreibung |
|--------|-------------|
| **Aktion** | Formales QA-Gate ausführen |
| **Output** | Gate-Status (grün/rot) |
| **Verantwortlich** | QA Specialist, Anti-Slop Auditor |

**Regel:** `./studio gate <project>` muss grün sein, bevor Ticket als done markiert wird.

**Bei Fehler:** Ticket geht zurück zu Schritt 4 (Umsetzung)

---

### Schritt 7: Doku & ADR-Sync

```bash
# falls nötig:
./studio adr <project> "<Titel>"
```

| Aspekt | Beschreibung |
|--------|-------------|
| **Aktion** | Dokumentation aktualisieren, ADRs anlegen/updaten |
| **Output** | Aktualisierte Doku, ggf. neue ADRs |
| **Verantwortlich** | Implementierender Agent |

**Checkliste:**
- [ ] Betroffene Definitions-Dateien aktualisiert
- [ ] READMEs aktuell
- [ ] ADRs angelegt (falls Architektur-Entscheidung)
- [ ] Decision Records aktualisiert (falls HITL)

---

### Schritt 8: Reuse-Review

```bash
# falls wiederverwendbar:
./studio promote <project> <asset-path>
```

| Aspekt | Beschreibung |
|--------|-------------|
| **Aktion** | Prüfen ob Code/Design wiederverwendbar ist |
| **Output** | Reuse-Entscheidung, ggf. Promotion zu Studio-Library |
| **Verantwortlich** | Project Manager |

**Checkliste:**
- [ ] Ist diese Lösung für andere Projekte nützlich?
- [ ] Könnte es eine generische Komponente werden?
- [ ] Ist es eine bewährte Lösung?
- [ ] Soll es zur Studio-Library promoted werden?

**Bei Promotion:**
```bash
./studio promote <project> <asset-path>
# Z.B.: ./studio promote nudge ui/components/button
```

---

### Schritt 9: Abschluss → Status `done`

```bash
./studio move <project> TICKET-NNN done --reason "Alle 9 Schritte abgeschlossen"
```

| Aspekt | Beschreibung |
|--------|-------------|
| **Aktion** | Ticket abschließen, Status aktualisieren |
| **Output** | Ticket in `backlog/done/` verschoben, status.json aktualisiert |
| **Verantwortlich** | Project Manager |

**Abschluss-Checkliste:**
- [ ] Alle 9 Schritte dokumentiert
- [ ] Alle Akzeptanzkriterien erfüllt
- [ ] QA-Gate grün
- [ ] Doku aktuell
- [ ] Status.json aktualisiert
- [ ] Commit durchgeführt

---

## Ticket-Status

```
open ──▶ analyze ──▶ plan ──▶ design ──▶ implement ──▶ qa ──▶ review ──▶ reuse ──▶ done
                                                                      
         blocked ◀── (bei Problemen) ──▶ (zurück zu vorherigem Schritt)
```

| Status | Bedeutung |
|--------|-----------|
| `open` | Ticket erstellt, wartet auf Analyse |
| `analyze` | Wird analysiert |
| `plan` | Implementierung wird geplant |
| `design` | Design/Architektur wird definiert |
| `implement` | Code wird geschrieben |
| `qa` | Qualität wird geprüft |
| `review` | Code-Review |
| `reuse` | Reuse-Review |
| `done` | Abgeschlossen |
| `blocked` | Blockiert (warten auf Entscheidung/Input) |

---

## Blockierte Tickets

Wenn ein Ticket blockiert ist:

```bash
./studio move <project> TICKET-NNN blocked --reason "Wartet auf ADR-Entscheidung"
```

- Blockierungsgrund wird dokumentiert
- Ticket wird bei Grooming besprochen
- Bei Grooming wird geprüft ob Blocker behoben werden kann

---

## Referenzen

- `.quinsy-studio/process/lifecycle.md` — Phasen
- `.quinsy-studio/process/gates.md` — QA-Gate im Detail
- `.quinsy-studio/process/anti-slop.md` — Anti-Slop-Audit
- `.quinsy-studio/process/iterative-delivery.md` — Sprint/Board/Grooming
- `./studio ticket <project> "<Titel>"` — Ticket erstellen
- `./studio move <project> <id> <status>` — Status wechseln
