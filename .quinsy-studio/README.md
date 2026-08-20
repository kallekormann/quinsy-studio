# Quinsy Studio — Betriebsanleitung

> Das Studio-HQ: eine hochgradig autonome, self-learning Software-Entwicklungs- und
> Growth-Agentur auf Director-Niveau. Dieses Dokument beschreibt, wie du das Studio
> **bedienst**, wie du **Skills erweiterst**, wie du den **Prozess optimierst** und
> wie der **Dual-Loop** dafür sorgt, dass das Studio aus Projekten lernt.

---

## Inhaltsverzeichnis

1. [Was ist Quinsy Studio?](#1-was-ist-quinsy-studio)
2. [Ordnerstruktur](#2-ordnerstruktur)
3. [Schnellstart: Projekt starten (5 Minuten)](#3-schnellstart-projekt-starten)
4. [Wo liegt was? (Templates, PRD, Tickets)](#4-wo-liegt-was)
5. [Der Studio-Prozess (Dual-Speed)](#5-der-studio-prozess)
6. [Alle CLI-Befehle](#6-alle-cli-befehle)
7. [Skills verwalten (intern + extern)](#7-skills-verwalten)
8. [Den Prozess optimieren (Learning Loop)](#8-den-prozess-optimieren)
9. [Der Dual-Loop: Studio lernt aus Projekten](#9-der-dual-loop)
10. [Studio-Library: wiederverwendbare Assets](#10-studio-library)
11. [Qualitätssicherung & Gates](#11-qualitätssicherung)
12. [Troubleshooting](#12-troubleshooting)

---

## 1. Was ist Quinsy Studio?

Quinsy Studio ist ein **Dateisystem-basiertes Betriebssystem für Software-Projekte**.
Es besteht aus:

- **Prozess-Dokumenten** (`process/`) — Lifecycle, Gates, Anti-Slop, Ticket-Workflow
- **Teams & Skills** (`teams/`) — 9 Teams, 37 interne Skills + Skill-Registry
- **Knowledge Base** (`knowledge-base/`) — Playbooks (Design, Frontend, Backend, Compliance, AI)
- **Studio-Tools** (`studio-tools/`) — Python-CLI mit allen Befehlen
- **Studio-Templates** (`studio-templates/`) — PRD, Ticket, ADR, Docker-Basis
- **Studio-Library** (`studio-library/`) — wiederverwendbare Assets (UI, Packages, Tokens)
- **Externe Skills** (`external-skills/`) — importierte Best-in-Class Skill-Pakete

Das Studio arbeitet im **Dual-Speed-Modus**:
- **CORE** — für neue Plattformen & komplexe Systeme (6 Phasen mit Human-Gates)
- **LEAN** — für Iterationen & Features in bestehenden Projekten (4 Phasen)

---

## 2. Ordnerstruktur

```
quinsy-studio/
├── .quinsy-studio/                 ← DAS STUDIO (alles hier drin)
│   ├── process/                    # Prozess-Dokumente (Lifecycle, Gates, Anti-Slop)
│   ├── teams/                      # 9 Teams × Skills + skill-registry.md
│   │   ├── 01-frontend-experience/
│   │   ├── 02-backend-systems/
│   │   ├── 03-compliance-legal/
│   │   ├── 04-product-strategy-architecture/
│   │   ├── 05-growth-marketing-content/
│   │   ├── 06-product-management-operating-model/
│   │   ├── 07-ai-autonomous-systems/
│   │   ├── 08-platform-enterprise-engineering/
│   │   └── 09-studio-operations-evolution/
│   ├── knowledge-base/             # Playbooks (Design, Frontend, Backend, Compliance, AI, Anti-Slop)
│   ├── studio-tools/               # Python-CLI (studio.py + alle Tools)
│   ├── studio-templates/           # PRD, Ticket, ADR, Docker-Basis, Learning-Logs
│   ├── studio-library/             # Wiederverwendbare Assets (ui/, packages/, tokens)
│   ├── external-skills/            # Importierte Skill-Pakete (hallmark, marketing, ...)
│   ├── backlog/                    # NUR Studio-Verbesserungen (LO-*)
│   ├── retros/                     # Retrospektiven & Audits
│   └── skill-dependencies.json     # Abonnierte externe Skill-Quellen
├── projects/                       # ALLE Kundenprojekte (je eigenes Backlog, Docker)
│   └── <projekt>/                  # status.json, docs/, backlog/, sprints/, docker/, design/
├── intake/                         # Rohe Projekt-Ideen (Markdown)
├── studio                          # CLI-Wrapper (delegiert an .quinsy-studio/studio-tools/)
├── README.md                       # Projekt-README (diese Datei ist .quinsy-studio/README.md)
└── CHANGELOG.md
```

**Wichtige Trennung:**
- **Studio-Welt** (`.quinsy-studio/`) — Prozess, Skills, Templates, Library, Learning
- **Projekt-Welt** (`projects/<name>/`) — Tickets, ADRs, Sprints, Docker, Code

---

## 3. Schnellstart: Projekt starten

### Schritt 1: PRD-Template holen

```bash
cp .quinsy-studio/studio-templates/prd_template.md intake/mein-projekt.md
```

Das Template liegt unter **`.quinsy-studio/studio-templates/prd_template.md`**.
Alternativ kannst du auch eine lose Idee nach `intake/` legen — das Studio strukturiert
sie beim Intake automatisch.

### Schritt 2: Projekt initialisieren

```bash
./studio init mein-projekt --archetype saas-application
```

Verfügbare Archetypen: `saas-application`, `e-commerce`, `content-platform`,
`mobile-first`, `enterprise-tool`, `game`, `api-service`, `internal-tool`.

### Schritt 3: Intake verarbeiten (PRD → Tickets)

```bash
./studio intake mein-projekt intake/mein-projekt.md
```

Das Studio:
1. Liest das PRD ein
2. Erkennt den Archetyp automatisch
3. Generiert das strukturierte PRD nach `projects/mein-projekt/docs/intake/prd.md`
4. Erstellt Tickets in `projects/mein-projekt/backlog/open/`

### Schritt 4: Projekt starten

```bash
./studio start mein-projekt --mode core    # oder: --mode lean
```

### Schritt 5: Konzept & Design (Human-Gate 1)

```bash
./studio concept mein-projekt              # erstellt DESIGN.md, wartet auf Freigabe
./studio approve mein-projekt --gate 1     # nach Review freigeben
```

### Schritt 6: Sprints & Tickets

```bash
./studio sprint mein-projekt               # SPRINT-01 anlegen
./studio ticket mein-projekt "Feature X"   # Ticket erstellen
./studio move mein-projekt TICK-0001 implement   # Ticket bewegen
./studio board mein-projekt                # Board anzeigen
```

### Schritt 7: QA-Gate

```bash
./studio gate mein-projekt --level 5       # Anti-Slop + Skill-Matching + Tests
```

### Schritt 8: Docker-Umgebung (optional)

```bash
./studio env mein-projekt init             # kopiert Basis-Template → Projektdocker
./studio env mein-projekt up               # Postgres + Redis starten
```

---

## 4. Wo liegt was?

| Was | Wo? |
|-----|-----|
| **PRD-Template** | `.quinsy-studio/studio-templates/prd_template.md` |
| **PRD (bearbeitet)** | `projects/<name>/docs/intake/prd.md` |
| **Rohe Idee/Input** | `intake/<name>.md` |
| **Tickets** | `projects/<name>/backlog/open|done|blocked/` |
| **ADRs** | `projects/<name>/docs/adr/` |
| **Decision Records** | `projects/<name>/docs/decisions/` |
| **Sprints** | `projects/<name>/sprints/SPRINT-NN/` |
| **Design-Blueprint** | `projects/<name>/design/DESIGN.md` |
| **Docker (projektspezifisch)** | `projects/<name>/docker/` |
| **Docker-Basis-Template** | `.quinsy-studio/studio-templates/docker/` |
| **Status (Phase/Gate)** | `projects/<name>/status.json` |
| **Studio-Learning-Items** | `.quinsy-studio/backlog/open/LO-*.md` |
| **Retros** | `.quinsy-studio/retros/` |
| **Studio-Library** | `.quinsy-studio/studio-library/` |

---

## 5. Der Studio-Prozess (Dual-Speed)

### CORE-Modus (neue Plattformen, komplexe Systeme)

| Phase | Aktion | Artefakt | Gate |
|-------|--------|----------|------|
| **1. Clean Intake** | PRD einlesen, Archetyp, Tickets | `docs/intake/prd.md`, Tickets | — |
| **2. Concept & Design** | ADRs, DESIGN.md, Architektur | `design/DESIGN.md`, ADRs | **HUMAN-GATE 1** |
| **3. Sprint Planning** | Tickets groomen, Sprint | `sprints/SPRINT-01/` | — |
| **4. Autonomous Sprints** | Tickets abarbeiten | Code im Projekt | — |
| **5. QA & Review** | Anti-Slop, Tests, Skill-Matching | QA-Report | Gate 5 |
| **6. Dual-Loop Reflektion** | Learnings + Assets extrahieren | `docs/local_learnings.md`, Library | — |
| **7. Deployment** | Release | — | — |

### LEAN-Modus (Features, Iterationen)

| Phase | Aktion |
|-------|--------|
| **1. Ticket Drop** | Ticket direkt in Backlog |
| **2. Quick Align** | Kurzer Lösungsweg → **HUMAN-GATE 1** (Go/No-Go) |
| **3. Execute & QA** | Sofortige Umsetzung + Tests |
| **4. Fast Sync** | Commit + Global-Asset-Abgleich |

---

## 6. Alle CLI-Befehle

```bash
# Projektmanagement
./studio init <project> --archetype <type>     # Projekt anlegen
./studio start <project> --mode [core|lean]    # Prozess starten
./studio status <project>                      # Stand anzeigen
./studio board <project>                       # Backlog-Board

# Intake & Konzept
./studio intake <project> <input-file>         # PRD verarbeiten → Tickets
./studio concept <project>                     # Design-Phase (Gate 1)
./studio approve <project> --gate <n>          # Human-Gate freigeben

# Sprints & Tickets
./studio sprint <project>                      # Sprint anlegen
./studio ticket <project> "Titel"              # Ticket erstellen
./studio move <project> <id> <status>          # Ticket bewegen
./studio groom <project>                       # Grooming

# Qualität
./studio gate <project> [--level N]            # QA-Gate (inkl. Skill-Matching)
./studio adr <project> "Titel"                 # Architektur-Entscheidung
./studio decide <project> "Titel"              # Decision Record (HITL)
./studio decisions <project>                   # Decisions anzeigen

# Umgebung
./studio env <project> init|up|down|status     # Docker (Basis-Template)
./studio repo <project> create|status          # GitHub-Repo (mit Freigabe!)

# Learning & Studio-Evolution
./studio learn "Titel" --signal <s>            # Learning Item
./studio learn-list                            # Learning Items anzeigen
./studio retro <project>                       # Retrospektive
./studio sync <project>                        # Assets → Studio-Library
./studio promote <project> <asset>             # Asset manuell promoven
./studio update-skills                         # Externe Skills aktualisieren
```

---

## 7. Skills verwalten

### Interne Skills (`.quinsy-studio/teams/`)

Jedes Team hat einen `README.md` (Rollen) und `skills/` (ein Markdown pro Skill).
Jeder Skill enthält: **Metadata** (ID, Trigger-Wörter, Phasen, Rollen), **Verhaltensregeln**,
**Anti-Patterns** und **Referenzen**.

**Skill-Registry:** `.quinsy-studio/teams/skill-registry.md` — der zentrale Index.
Der Agent ordnet jedem Ticket über Trigger-Wörter die passenden Skills zu
(max. 5 pro Ticket).

**Neuen internen Skill anlegen:**
1. Datei `teams/<team>/skills/<name>.md` erstellen (Schema aus bestehenden Skills kopieren)
2. Skill in `skill-registry.md` eintragen (Trigger-Wörter, Phasen, Archetyp)
3. Test ausführen: `python3 .quinsy-studio/studio-tools/test_skill_matching.py`

### Externe Skills (Skill-Package-Manager)

Das Studio abonniert Best-in-Class-Skills aus externen Repositories:

```json
// .quinsy-studio/skill-dependencies.json
{
  "design":         "github:Nutlope/hallmark@main",
  "marketing_aeo":  "github:coreyhaines31/marketingskills@main",
  "gamedev":        "github:gamedev-skills/awesome-gamedev-agent-skills@main",
  "compliance":     "github:samir-abis/cookiecomply-skills@main",
  "geo":            "github:bloomprotocol/agent-visibility-skill@main",
  "all_domains":    "github:seb1n/awesome-ai-agent-skills@main"
}
```

**Ablauf:**
```bash
./studio update-skills               # alle Quellen importieren/aktualisieren
./studio update-skills --list        # deklarierte Quellen anzeigen
./studio update-skills design        # nur eine Domain
```

Importiert wird nach `.quinsy-studio/external-skills/<domain>/`.
Danach `INDEX.md` prüfen und die Konflikt-Matrix
(`knowledge-base/external_skills_conflict_matrix.md`) aktualisieren.

**Wichtig:** Externe Skills sind IMMER dem internen Anti-Slop-Protocol und der
Zero-Data-Architecture untergeordnet. Sie sind Werkzeuge, keine Autorität.

---

## 8. Den Prozess optimieren

Das Studio optimiert sich über **Learning Items** (LO-*):

```bash
./studio learn "Gate-Check dauert zu lange" --signal tooling-gap
./studio learn-list
```

Signale: `tooling-gap`, `process-gap`, `design-gap`, `quality-risk`, `conflict`, ...

**Ablauf (Meta-Loop):**
1. **Signal erkennen** — Gate-Fail, Rework, Tooling-Lücke, Design-Lücke
2. **Learning Item anlegen** (`./studio learn ...`)
3. **Retrospektive** (`./studio retro <project>`) — LO-Items besprechen
4. **Entscheidung** — Prozess-Doc, Skill-Datei oder Python-Tool verbessern
5. **CHANGELOG-Eintrag** — Änderung dokumentieren
6. **Testen** — `test_skill_matching.py` + `./studio gate <project>`

**Prozess-Dokumente direkt bearbeiten:**
- `process/lifecycle.md` — Phasen
- `process/gates.md` — Gate-Definitionen
- `process/ticket-workflow.md` — 9-Schritte
- `process/human-in-the-loop.md` — HITL-Entscheidungen
- `knowledge-base/` — Playbooks

---

## 9. Der Dual-Loop: Studio lernt aus Projekten

### Loop 1: Local Project Loop (Projekt-Welt)

Projektspezifische Erkenntnisse bleiben **im Projekt** gefangen:
- ADRs → `projects/<name>/docs/adr/`
- Learnings → `projects/<name>/docs/local_learnings.md`
- Schema-Entscheidungen → `docs/definitions/`

Diese beeinflussen **nicht** die Arbeitsweise des Studios in anderen Projekten.

### Loop 2: Global Studio Evolution (Studio-Welt)

Universell anwendbare Erkenntnisse werden **ins Studio befördert**:

1. **Assets** → `./studio sync <project>` oder `./studio promote <project> <pfad>`
   → landen in `.quinsy-studio/studio-library/` (UI-Komponenten, Services, Helpers, Packages)
2. **Prozess** → Process Guard aktualisiert Playbooks in `knowledge-base/`
3. **Skills** → Skill-Dateien werden verbessert
4. **Templates** → Studio-Templates werden erweitert

**Auswahlkriterium (was wird promoted?):**
- ✅ In 2+ Projekten identisch verwendet
- ✅ Projekt-agnostisch (kein Kunden-Branding)
- ✅ Qualitätsgeprüft (Anti-Slop + Tests grün)
- ❌ Projektspezifische Hacks, Workarounds, Nischen-Logik

**Beispiel:**
```bash
# Komponente aus Projekt in Studio-Library übernehmen
./studio promote mein-projekt ui/components/button

# Oder automatisch scannen + extrahieren
./studio sync mein-projekt
```

Das nächste Projekt startet dann direkt mit der verbesserten Studio-Version.

---

## 10. Studio-Library

Die wiederverwendbaren Assets liegen in `.quinsy-studio/studio-library/`:

```
studio-library/
├── ui/
│   ├── tokens/          # Design Tokens (design-tokens.json + .css)
│   ├── components/      # UI-Komponenten (button, ...)
│   └── page-types/      # Seitentypen (comparison, ...)
├── packages/            # Backend-Packages (auth, billing, feature-gating)
├── design/              # Design-Richtlinien
└── manifest.json        # Asset-Registry (Name, Quelle, Typ)
```

**Regeln:**
- Assets werden NUR via `./studio promote` / `./studio sync` hinzugefügt (Global Loop)
- Jedes Asset hat eine README + Qualitätsnachweis
- Keine projektspezifischen Secrets oder Branding in Library-Assets

---

## 11. Qualitätssicherung

| Check | Wann | Wie |
|-------|------|-----|
| **Anti-Slop-Audit** | Jeder Commit | `python3 .quinsy-studio/studio-tools/validate_anti_slop.py .` |
| **QA-Gate** | Vor jedem Release | `./studio gate <project> --level 5` |
| **Skill-Matching-Test** | Bei jedem QA-Gate + Registry-Änderung | `python3 .quinsy-studio/studio-tools/test_skill_matching.py` |
| **Konflikt-Matrix** | Nach `update-skills` | `knowledge-base/external_skills_conflict_matrix.md` |
| **Gate-Exit-Kriterien** | Je Gate | `process/gates.md` |

**QA-Gate Level:**
- Level 0–1: Struktur + Status
- Level 2: Linting
- Level 3: Type-Check
- Level 4: Tests
- Level 5: Build + Audit + Anti-Slop + **Skill-Matching**

---

## 12. Troubleshooting

| Problem | Lösung |
|---------|--------|
| `./studio` nicht gefunden | `chmod +x studio` (einmalig) |
| Externe Skills fehlen | `./studio update-skills` (braucht git) |
| Ticket-ID-Duplikate | `rm projects/<name>/.ticket_counter` (wird neu aufgebaut) |
| QA-Gate rot bei npm_audit | Lockfile fehlt → `npm i --package-lock-only` im Projekt |
| Skill-Matching-Test rot | Registry-Trigger prüfen → `teams/skill-registry.md` |
| Docker-Template fehlt | Liegt unter `studio-templates/docker/` — nicht löschen |
| Studio-Dateien verloren | **Git sichern!** `.gitignore` beachten (externe Skills regenerierbar) |

---

## Weiterführende Dokumentation

- `process/lifecycle.md` — 7-Phasen-Lifecycle
- `process/gates.md` — Gate-Definitionen
- `process/adr-policy.md` — ADR-Regeln
- `process/human-in-the-loop.md` — HITL
- `teams/skill-registry.md` — Skill-Index
- `knowledge-base/anti_ai_slop_protocol.md` — Anti-Slop
- `knowledge-base/external_skills_conflict_matrix.md` — Skill-Konflikte
- `CHANGELOG.md` — Versionshistorie
