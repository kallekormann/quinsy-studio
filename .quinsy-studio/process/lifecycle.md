# Quinsy Studio — 7-Phase Lifecycle

> Der verbindliche Ablauf von Intake bis Deployment. Der Agent arbeitet autonom — **nur** an den Human-Gates stoppt er und wartet auf Freigabe.

## Architektur-Prinzip

```
Studio (Meta-Ebene)     ──▶  existiert autark, verbessert sich selbst
Projekt (Ausführungsebene) ──▶  wird vom Studio ausgeführt, Local Loop
```

---

## Übersicht

```
┌─────────────────────────────────────────────────────────────────────────┐
│                        7-PHASE LIFECYCLE                               │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  Phase 1: Intake & PRD Processing                                       │
│     └─▶ PRD einlesen, Meilensteine/Tickets, Repo/Docker init           │
│                                                                         │
│  ═══════════════ HUMAN-GATE 1 ═══════════════                          │
│                                                                         │
│  Phase 2: Architecture & Design Blueprinting                           │
│     └─▶ ADRs, UI-Specs basierend auf Playbooks                         │
│                                                                         │
│  ═══════════════ HUMAN-GATE 2 ═══════════════                          │
│                                                                         │
│  Phase 3: Sprint Setup & Backlog Grooming                              │
│     └─▶ Tickets in Sprint-Ordner verschieben                           │
│                                                                         │
│  Phase 4: Autonomous Sprint Execution                                  │
│     └─▶ Code schreiben, lokales Testen im Docker-Container             │
│                                                                         │
│  Phase 5: Comprehensive QA & Compliance Gate                           │
│     └─▶ validate_anti_slop.py + run_qa_gate.py                         │
│                                                                         │
│  Phase 6: Dual-Loop Knowledge Harvesting                               │
│     └─▶ Retro: Local Learnings (Projekt) + Global Evolution (Studio)   │
│                                                                         │
│  Phase 7: Deployment & Iteration                                       │
│     └─▶ Zero-Downtime Deployment, Monitoring                           │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## Phase 1: Intake & PRD Processing

**Ziel:** PRD verstehen, Projektstruktur aufsetzen, Tickets generieren.

| Aspekt | Beschreibung |
|--------|-------------|
| **Input** | PRD (`projects/[name]/docs/prd.md`) |
| **Output** | Validiertes PRD, generierte Tickets, Repo + Docker init |
| **Rollen (Lead)** | Product Manager, Systems Architect |
| **Rollen (Support)** | Legal/Privacy Officer (Early-Check) |
| **Human-Gate** | Nein — Agent arbeitet autonom |

### Ablauf

1. PRD einlesen und auf Vollständigkeit prüfen
2. `docs/definitions/` befüllen (00-index bis 11-assumptions)
3. Archetyp bestimmen und Archetyp-Checkliste ausfüllen
4. `./studio init <project> --archetype <type>`
5. `./studio env <project> init` — Docker-Compose + Git
6. `./studio repo <project> create` — GitHub-Repo (nur mit Freigabe)
7. Tickets generieren: `generate_ticket_manifest.py`
8. Erste ADRs anlegen für Grundsatzentscheidungen
9. `status.json` initialisieren
10. Gate 0 prüfen

### Gate 0 (intern)

- [ ] PRD validiert und vollständig
- [ ] Definitions-Dokumente befüllt
- [ ] Archetyp bestimmt
- [ ] Mindestens 1 ADR vorhanden
- [ ] Repo + Docker initialisiert

---

## ═══════════════ HUMAN-GATE 1 ═══════════════

> **Agent stoppt.** User muss Architecture & Design Blueprint freigeben.
> 
> **Was der Agent vorlegt:**
> - System-Architektur (Tech-Stack, Deployment)
> - UI-Specs (Design Tokens, Komponenten-Hierarchie)
> - ADRs für alle Grundsatzentscheidungen
> - DSGVO-Compliance-Check
>
> **User entscheidet:**
> - Architecture Blueprint Approve / Reject / Request Changes
> 
> **Erst nach Freigabe:** Phase 3 startet.

---

## Phase 2: Architecture & Design Blueprinting

**Ziel:** Systemarchitektur, UI-Spezifikation, Datenmodell, API-Kontrakte.

| Aspekt | Beschreibung |
|--------|-------------|
| **Input** | Validiertes PRD, Gate 0 |
| **Output** | Architecture Blueprint, UI-Spec, ADRs |
| **Rollen (Lead)** | Systems Architect, Backend Architect, Frontend Architect |
| **Rollen (Support)** | Database Specialist, Security Engineer |
| **Human-Gate** | **JA — HUMAN-GATE 1** |

### Ablauf

1. Tech-Stack finalisieren (basierend auf Archetyp-Checkliste)
2. System-Architektur entwerfen
3. Datenmodell definieren (ER-Diagramm, Migration-Strategie)
4. API-Kontrakte spezifizieren
5. UI-Specs erstellen (Design Tokens, Komponenten, Layouts)
6. Sicherheits-Architektur definieren
7. DSGVO-Compliance-Check
8. Alle Entscheidungen als ADR dokumentieren
9. Architecture Blueprint zusammenstellen
10. **WARTEN AUF HUMAN-GATE 1**

---

## Phase 3: Sprint Setup & Backlog Grooming

**Ziel:** Tickets in Sprints organisieren, Kapazität planen.

| Aspekt | Beschreibung |
|--------|-------------|
| **Input** | Genehmigter Architecture Blueprint |
| **Output** | Erster Sprint mit zugeordneten Tickets |
| **Rollen (Lead)** | Product Manager, Backlog Owner |
| **Rollen (Support)** | Systems Architect |
| **Human-Gate** | Nein — Agent arbeitet autonom |

### Ablauf

1. `./studio sprint <project>` — Sprint anlegen
2. Tickets priorisieren (RICE, MoSCoW)
3. Abhängigkeiten identifizieren
4. Kapazität schätzen
5. Tickets dem Sprint zuordnen
6. `plan.md` ausfüllen
7. Blocked-Review durchführen
8. Grooming-Protokoll schreiben
9. Gate 3 prüfen

---

## Phase 4: Autonomous Sprint Execution

**Ziel:** Code schreiben, lokales Testen, iterative Lieferung.

| Aspekt | Beschreibung |
|--------|-------------|
| **Input** | Sprint mit zugeordneten Tickets |
| **Output** | Implementierter Code mit lokalen Tests |
| **Rollen (Lead)** | Frontend Engineer, Backend Engineer |
| **Rollen (Support)** | Database Specialist, QA Specialist |
| **Human-Gate** | Nein — Agent arbeitet autonom |

### Ablauf pro Ticket (9-Schritte)

1. Aufnahme & Verstehen
2. Zerlegung & Abhängigkeiten
3. Konzeption/Design
4. Umsetzung (Clean Code, TDD)
5. Selbstprüfung (Tests, Lint, Review)
6. QA-Gate (`./studio gate <project>`)
7. Doku & ADR-Sync
8. Reuse-Review (`./studio promote`)
9. Abschluss → Status `done`

### Regeln

- **Kein Code ohne Ticket**
- **Test-First (TDD)**
- **Clean Code / SOLID**
- **Anti-Slop beachten**
- **Docker-Container für lokales Testen**

---

## Phase 5: Comprehensive QA & Compliance Gate

**Ziel:** Formales QA, Security-Audit, Anti-Slop-Audit, DSGVO-Check.

| Aspekt | Beschreibung |
|--------|-------------|
| **Input** | Implementierter Code |
| **Output** | QA-Report, Security-Audit, Anti-Slop-Bericht |
| **Rollen (Lead)** | QA Specialist, Security Engineer, Legal/Privacy Officer |
| **Rollen (Support)** | AI-Autonomous-Systems (Anti-Slop) |
| **Human-Gate** | Nein — Agent arbeitet autonom |

### Ablauf

1. `validate_anti_slop.py` ausführen
2. `run_qa_gate.py` ausführen
3. Security-Scan (OWASP, Dependencies)
4. DSGVO-Compliance-Check
5. Performance-Tests (Core Web Vitals)
6. Barrierefreiheits-Check (a11y)
7. Anti-Slop-Audit: 0 Error-Verstöße
8. Gate 5 muss grün sein
9. QA-Report generieren

---

## Phase 6: Dual-Loop Knowledge Harvesting

**Ziel:** Lernen aus dem Sprint — strikte Trennung Local vs. Global.

| Aspekt | Beschreibung |
|--------|-------------|
| **Input** | Sprint-Erfahrung, QA-Ergebnisse |
| **Output** | Local Learnings + Global Studio Evolution |
| **Rollen (Lead)** | Process Guard, Platform Architect |
| **Rollen (Support)** | Documentation Writer, Agile Coach |
| **Human-Gate** | Nein — Agent arbeitet autonom |

### Ablauf

1. Sprint-Retrospektive durchführen
2. Learning Items sammeln (`./studio learn`)
3. **Local Loop:** Projektspezifische Learnings → `projects/[name]/docs/local_learnings.md`
4. **Global Loop:** Universelle Verbesserungen → `.quinsy-studio/knowledge-base/`
5. Playbooks aktualisieren (Global Loop)
6. Python-Tools optimieren (Global Loop)
7. CHANGELOG aktualisieren
8. `./studio retro <project>`

---

## Phase 7: Deployment & Iteration

**Ziel:** Produktivumgebung deployen, Monitoring, nächste Iteration planen.

| Aspekt | Beschreibung |
|--------|-------------|
| **Input** | QA-geprüfter Code |
| **Output** | Live-System, Monitoring, nächste Sprint-Planung |
| **Rollen (Lead)** | Platform Architect, Backend Security & Infrastructure |
| **Rollen (Support)** | Growth Manager, Data Analyst |
| **Human-Gate** | Nein — aber Deployment-Freigabe empfohlen |

### Ablauf

1. Staging-Deployment
2. Smoke-Tests
3. Production-Deployment (Zero-Downtime)
4. Monitoring & Alerting einrichten
5. Release-Notes
6. Nächsten Sprint planen
7. Zurück zu Phase 3/4 (iterativ)

---

## Gate-Definitionen

| Gate | Phase | Prüfpunkte |
|------|-------|------------|
| **Gate 0** | Phase 1 (intern) | PRD, Definitions, Archetyp, ADRs, Repo |
| **HUMAN-GATE 1** | Phase 2→3 | Architecture Blueprint — **User-Freigabe** |
| **Gate 3** | Phase 3 (intern) | Sprint geplant, Tickets zugeordnet |
| **Gate 5** | Phase 5 (intern) | QA, Security, Anti-Slop, DSGVO — alles grün |

---

## Dual-Loop Integration

```
┌─────────────────────────────────────────────────────────────────────────┐
│                     DUAL-LOOP INTEGRATION                               │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  LOCAL LOOP (Projekt-Welt)           GLOBAL LOOP (Studio-Welt)         │
│  ─────────────────────────           ──────────────────────────         │
│  • Projektspezifische Bugs           • Universelle Playbooks            │
│  • Nischen-Erkenntnisse              • Python-Tooling-Updates           │
│  • Workarounds                       • Anti-Slop-Regel-Updates          │
│  • Ablage: projects/[name]/          • Ablage: .quinsy-studio/          │
│    docs/local_learnings.md             knowledge-base/                   │
│                                                                         │
│  ⚠️ Beeinflusst NICHT andere         ✅ Gilt für ALLE zukünftigen       │
│     Projekte                            Projekte                         │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## Referenzen

- `.quinsy-studio/process/gates.md` — Gate-Definitionen im Detail
- `.quinsy-studio/process/learning-loop.md` — Dual-Loop Learning
- `.quinsy-studio/process/ticket-workflow.md` — 9-Schritte-Ticket-Workflow
- `.quinsy-studio/knowledge-base/` — Playbooks & Protokolle
- `studio-tools/` — Python-Automation
