# Quinsy Studio — Human-in-the-Loop

> Manche Entscheidungen sind zu wichtig, um sie allein dem Agenten zu überlassen.
> Human-in-the-Loop stellt sicher, dass irreversible Aktionen menschliche Freigabe erhalten.

## Grundprinzip

```
Agent: "Ich kann das nicht allein entscheiden."
Mensch: "Ich entscheide."
Agent: "Umgesetzt."
```

---

## Wann ist HITL nötig?

| Kategorie | Aktionen | HITL? |
|-----------|----------|-------|
| **Budget** | Kosten über X €/Monat | **Ja** |
| **Recht** | Verträge, Lizenzen, DSGVO-Ausnahmen | **Ja** |
| **Irreversibel** | Daten löschen, Production-Deploy, DNS-Änderungen | **Ja** |
| **Sicherheit** | Security-Exceptions, Zugriffsrechte | **Ja** |
| **Architektur** | Große Architektur-Änderungen | **Ja** |
| **Release** | Production-Release | **Ja** |
| **Feature** | Neue Features (inkrementell) | Nein |
| **Bugfix** | Fehlerbehebung | Nein |
| **Doku** | Dokumentation | Nein |

---

## Decision-Record-Template

```markdown
# Decision Record — DR-NNNN

**Status:** pending | approved | rejected
**Datum:** YYYY-MM-DD
**Angefordert von:** <Rolle/Agent>
**Entscheidung durch:** <Mensch>

## Entscheidung
Was soll entschieden werden?

## Kontext
Warum ist diese Entscheidung nötig?

## Optionen

### Option A: <Name>
- Vorteile: ...
- Nachteile: ...
- Kosten: ...

### Option B: <Name>
- Vorteile: ...
- Nachteile: ...
- Kosten: ...

## Empfehlung
Welche Option empfiehlt der Agent und warum?

## Risiken
Was kann schiefgehen?

## Konsequenzen
Was bedeutet die Entscheidung für das Projekt?
```

---

## HITL-Workflow

```
┌─────────────────────────────────────────────────────────┐
│               HUMAN-IN-THE-LOOP WORKFLOW                │
└─────────────────────────────────────────────────────────┘

 1. Agent erkennt HITL- Situation
       │
 2. Decision Record anlegen
       │
 3. Decision Record vorlegen
       │
 4. ┌─────────────────┐
    │  WARTEN AUF     │
    │  ENTSCHEIDUNG   │
    └─────────────────┘
       │
 5. Mensch entscheidet
       │
 6. Decision Record aktualisieren
       │
 7. Entscheidung umsetzen
```

---

## Befehle

```bash
# Decision Record anlegen
./studio decide <project> "<Titel>"

# Übersicht aller Decision Records
./studio decisions <project>

# Decision Record als genehmigt markieren
./studio decide <project> DR-NNNN --approve

# Decision Record als abgelehnt markieren
./studio decide <project> DR-NNNN --reject
```

---

## Decision-Record-Verzeichnis

```
<project>/docs/decisions/
├── README.md              # Übersicht aller DRs
├── DR-0001-...
├── DR-0002-...
```

### README.md

```markdown
# Decision Records

| DR | Titel | Status | Datum | Entscheider |
|----|-------|--------|-------|-------------|
| DR-0001 | ... | approved | YYYY-MM-DD | ... |
| DR-0002 | ... | pending | YYYY-MM-DD | — |

## Legende
- **pending:** Wartet auf Entscheidung
- **approved:** Genehmigt
- **rejected:** Abgelehnt
```

---

## HITL-Beispiele

### Beispiel 1: Deployment-Kosten

```markdown
# Decision Record — DR-0001

**Status:** pending
**Datum:** 2026-08-20
**Angefordert von:** Platform Engineering

## Entscheidung
Soll für das Projekt ein Managed Kubernetes Cluster (€150/Monat) oder ein simpler Docker-Host (€30/Monat) verwendet werden?

## Kontext
Das Projekt erwartet 10k User im ersten Jahr. Performance-Anforderungen sind moderat.

## Optionen

### Option A: Managed Kubernetes
- Vorteile: Auto-Scaling, High Availability
- Nachteile: Komplexität, Kosten
- Kosten: €150/Monat

### Option B: Docker-Host
- Vorteile: Einfach, Günstig
- Nachteile: Manueller Scale-Up
- Kosten: €30/Monat

## Empfehlung
Option B (Docker-Host) — ausreichend für die erwartete Last, spart €1440/Jahr.

## Risiken
- Bei plötzlichem Traffic-Spike: mögliche Ausfallzeit
- Manuelles Skalieren nötig
```

---

### Beispiel 2: Lizenz-Entscheidung

```markdown
# Decision Record — DR-0002

**Status:** pending
**Datum:** 2026-08-20
**Angefordert von:** Product Management

## Entscheidung
Soll eine kommerzielle UI-Lizenz (€500/Jahr) erworben werden oder eine Open-Source-Alternative verwendet werden?

## Kontext
Das Projekt benötigt eine fortgeschrittene Data-Grid-Komponente.

## Optionen

### Option A: Kommerzielle Lizenz
- Vorteile: Support, Features
- Nachteile: Kosten, Vendor Lock-In
- Kosten: €500/Jahr

### Option B: Open-Source
- Vorteile: Kostenlos, Flexibilität
- Nachteile: Weniger Features, kein Support
- Kosten: €0

## Empfehlung
Option B — die benötigten Features sind in der Open-Source-Version verfügbar.

## Risiken
- Bei Bedarf an erweiterten Features: manuelle Implementierung nötig
```

---

## Automatisierte HITL-Erkennung

Der Agent erkennt automatisch HITL-Situationen:

```yaml
# In der Agent-Konfiguration
hitl_triggers:
  - pattern: "kosten.*€[0-9]+"
    category: budget
  - pattern: "daten.*lösch"
    category: irreversibel
  - pattern: "production.*deploy"
    category: release
  - pattern: "vertrag.*unterschrift"
    category: recht
  - pattern: "dsgvo.*ausnahme"
    category: compliance
```

---

## HITL-Report

```markdown
# HITL-Report — Monatlich

## Entscheidungen im Monat

| DR | Titel | Status | Entscheider | Datum |
|----|-------|--------|-------------|-------|
| DR-0001 | ... | approved | Max | 2026-08-15 |
| DR-0002 | ... | rejected | Max | 2026-08-18 |

## Ausstehende Entscheidungen

| DR | Titel | Angefordert | Wartet seit |
|----|-------|-------------|-------------|
| DR-0003 | ... | Agent | 2026-08-20 |

## Statistiken
- Genehmigt: 5
- Abgelehnt: 1
- Ausstehend: 1
- Durchschnittliche Entscheidungszeit: 2 Tage
```

---

## Referenzen

- `.quinsy-studio/process/lifecycle.md` — Phasen
- `.quinsy-studio/process/gates.md` — Gates
- `./studio decide <project> "<Titel>"` — Decision Record anlegen
- `./studio decisions <project>` — Übersicht anzeigen
