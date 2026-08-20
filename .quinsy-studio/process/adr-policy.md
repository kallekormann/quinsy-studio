# Quinsy Studio — ADR-Regelwerk

> Jede architektonische Entscheidung wird als Architecture Decision Record (ADR) dokumentiert.
> ADRs sind das Gedächtnis des Projekts — sie erklären das "Warum" hinter dem "Was".

## Grundprinzip

```
Keine Entscheidung ohne Dokumentation.
Keine Dokumentation ohne Begründung.
Keine Begründung ohne Alternative.
```

---

## Wann wird ein ADR angelegt?

| Situation | ADR Pflicht? |
|-----------|-------------|
| Technologie-Wechsel (z.B. Framework, DB) | **Ja** |
| Architektur-Muster (z.B. Monolith → Microservices) | **Ja** |
| API-Design-Entscheidung | **Ja** |
| UI/UX-Grundsatzentscheidung | **Ja** |
| Security-Architektur | **Ja** |
| Deployment-Strategie | **Ja** |
| Code-Convention (neue Regel) | Empfohlen |
| Bugfix mit Architektur-Auswirkung | Empfohlen |
| Kleiner Bugfix ohne Auswirkung | Nein |

---

## ADR-Template

Jedes ADR folgt diesem Template:

```markdown
# ADR-XXXX: [Titel der Entscheidung]

**Status:** proposed | accepted | deprecated | superseded
**Datum:** YYYY-MM-DD
**Entscheider:** [Rolle / Name]
**Betroffene Phasen:** [Phase(n)]

## Kontext
Was ist die Situation? Welches Problem soll gelöst werden?

## Entscheidung
Was wurde entschieden?

## Begründung
Warum wurde diese Entscheidung getroffen?

## Alternativen
Welche Alternativen wurden erwogen?

### Alternative A: [Name]
- Vorteile: ...
- Nachteile: ...

### Alternative B: [Name]
- Vorteile: ...
- Nachteile: ...

## Konsequenzen
Was bedeutet diese Entscheidung für das Projekt?

### Positiv
- ...

### Negativ
- ...

### Risiken
- ...

## Metriken
Wie wird der Erfolg dieser Entscheidung gemessen?

## Follow-up
Welche nächsten Schritte ergeben sich?
```

---

## ADR-Nummerierung

```
ADR-0001, ADR-0002, ADR-0003, ...
```

- fortlaufend
- nie recyceln
- Superseded-ADRs behalten ihre Nummer

---

## ADR-Status

| Status | Bedeutung |
|--------|-----------|
| `proposed` | Vorgeschlagen, noch nicht entschieden |
| `accepted` | Angenommen, gilt als verbindlich |
| `deprecated` | Nicht mehr gültig (durch neues ADR ersetzt) |
| `superseded` | Ersetzt durch ADR-XXXX |

---

## Speicherort

```
<project>/docs/adr/
├── README.md              # Übersicht aller ADRs
├── ADR-0001-...
├── ADR-0002-...
└── ...
```

### ADR-README.md

```markdown
# Architecture Decision Records

| ADR | Titel | Status | Datum |
|-----|-------|--------|-------|
| ADR-0001 | [Titel] | accepted | YYYY-MM-DD |
| ADR-0002 | [Titel] | proposed | YYYY-MM-DD |

## Legende
- **accepted:** Verbindliche Entscheidung
- **proposed:** Noch in Diskussion
- **deprecated:** Nicht mehr gültig
- **superseded:** Ersetzt durch neueres ADR
```

---

## ADR-Workflow

```bash
# Neues ADR anlegen
./studio adr <project> "<Titel>"

# ADR-Datei wird erstellt mit:
# - Template
# - Nächste freie Nummer
# - Status: proposed

# ADR bearbeiten
# 1. Datei manuell ausfüllen
# 2. Status auf "accepted" setzen
# 3. Commit mit ADR-Referenz
```

---

## ADR-Review

Jedes ADR wird mindestens einmalig geprüft:

1. **Erstellung:** Project Manager legt ADR an
2. **Review:** Betroffene Rollen prüfen
3. **Entscheidung:** Mensch oder Project Manager (je nach Gewicht)
4. **Archivierung:** ADR wird committed

---

## ADR-Pflichten je Phase

| Phase | ADR-Pflicht |
|-------|-------------|
| Phase 0 | Archetyp, Komplexitäts-Level |
| Phase 1 | Go/No-Go, Technologie-Stack |
| Phase 2 | Alle Architektur-Entscheidungen |
| Phase 3 | Design-System-Grundsatz |
| Phase 4 | Bei Abweichung von Phase-2-ADR |
| Phase 5 | — |
| Phase 6 | Deployment-Strategie |
| Phase 7 | Optimierungs-Entscheidungen |

---

## Anti-Patterns

### ❌ Kein ADR für Architects-Entscheidung
```bash
# Schlecht:
"Wir nutzen jetzt PostgreSQL statt MySQL"
# (Keine Dokumentation warum)

# Gut:
# ADR-0003: Wechsel zu PostgreSQL
# Status: accepted
# Begründung: JSONb-Support, bessere Full-Text-Search, ...
```

### ❌ ADR ohne Alternativen
```markdown
# Schlecht:
## Entscheidung: Wir nutzen Next.js
## Begründung: Weil es gut ist

# Gut:
## Alternativen
### A: Next.js - Vorteile: SSR, React-Ökosystem, Vercel-Integration
### B: Remix - Vorteile: Web-Standards, simples Loader-Modell
### C: Astro - Vorteile: Insel-Architektur, Performance
## Entscheidung: Next.js (wegen SSR + Large-Scale-Features)
```

### ❌ Veraltetes ADR nicht markieren
```markdown
# Schlecht:
ADR-0001: "Wir nutzen jQuery" (nie aktualisiert)

# Gut:
ADR-0001: "Wir nutzen jQuery"
Status: superseded (durch ADR-0015: React Migration)
```

---

## Referenzen

- `docs/adr/README.md` — ADR-Übersicht im Projekt
- `.quinsy-studio/process/lifecycle.md` — Phasen, in denen ADRs entstehen
- `./studio adr <project> "<Titel>"` — ADR anlegen
