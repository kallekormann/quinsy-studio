# Quinsy Studio

> Das autonome, selbstlernende Entwicklungs-Operating-System für KI-Agenten.

## Überblick

Quinsy Studio ist ein Framework für autonome Softwareentwicklung mit KI-Agenten. Es definiert:

- **8 Phasen** von Konzeption bis Monitoring
- **8 Teams** mit spezialisierten Rollen
- **Qualitäts-Gates** die jeden Schritt prüfen
- **Anti-Slop-Audit** für AI-generierten Code
- **Self-Learning** durch Retros und Learning Items
- **Human-in-the-Loop** für irreversible Entscheidungen

## Schnellstart

```bash
# 1. Projekt initialisieren
./studio init mein-projekt --archetype saas-application

# 2. Status prüfen
./studio status mein-projekt

# 3. Ticket erstellen
./studio ticket mein-projekt "Erste Feature" --phase 3 --priority P1

# 4. Board anzeigen
./studio board mein-projekt

# 5. Ticket bewegen
./studio move mein-projekt MEIN-0001 implement --reason "Implementierung gestartet"

# 6. Gate prüfen
./studio gate mein-projekt --level 5

# 7. ADR anlegen
./studio adr mein-projekt "Architektur-Entscheidung"

# 8. Sprint starten
./studio sprint mein-projekt

# 9. Grooming durchführen
./studio groom mein-projekt

# 10. Learning Item anlegen
./studio learn "Gate-Check dauert zu lange" --signal tooling-gap

# 11. Asset promoven
./studio promote mein-projekt ui/components/button

# 12. Retrospektive starten
./studio retro mein-projekt
```

## Projektstruktur

```
quinsy-studio/
├── .quinsy-studio/
│   ├── process/           # Prozess-Dokumente
│   │   ├── lifecycle.md
│   │   ├── gates.md
│   │   ├── adr-policy.md
│   │   ├── anti-slop.md
│   │   ├── ticket-workflow.md
│   │   ├── iterative-delivery.md
│   │   ├── human-in-the-loop.md
│   │   └── project-archetypes.md
│   ├── teams/             # Team-Skills
│   │   ├── 01-frontend-experience/
│   │   ├── 02-backend-systems/
│   │   ├── 03-compliance-legal/
│   │   ├── 04-product-strategy-architecture/
│   │   ├── 05-growth-marketing-content/
│   │   ├── 06-product-management-operating-model/
│   │   ├── 07-ai-autonomous-systems/
│   │   └── 08-platform-enterprise-engineering/
│   ├── backlog/           # Tickets (nur Studio-Verbesserungen LO-*)
│   │   ├── open/
│   │   ├── done/
│   │   └── blocked/
│   ├── retros/            # Retrospektiven
│   ├── studio-library/    # Wiederverwendbare Assets
│   │   ├── ui/ (tokens, components, page-types)
│   │   ├── packages/ (auth, billing, feature-gating)
│   │   └── manifest.json
│   ├── studio-tools/      # Python-Tooling (alle Scripts)
│   ├── studio-templates/  # Blau-pausen (PRD, Ticket, ADR, Docker-Basis)
│   │   └── docker/        # Basis-Docker-Template → Projekt-Kopie
│   ├── knowledge-base/    # Playbooks
│   ├── external-skills/   # Importierte Best-in-Class Skills (update-skills)
│   └── skill-dependencies.json
├── projects/              # Projekte (inkl. eigenem backlog/, docker/)
│   ├── nudge/
│   └── quinsy-affiliate-engine/
├── studio                 # CLI-Wrapper (delegiert an .quinsy-studio/studio-tools/)
├── CHANGELOG.md
└── README.md
```

## Dokumentation

### Process
- [Lifecycle](.quinsy-studio/process/lifecycle.md) — 7 Phasen (Dual-Speed: CORE/LEAN)
- [Gates](.quinsy-studio/process/gates.md) — Qualitäts-Checks
- [ADR Policy](.quinsy-studio/process/adr-policy.md) — Architektur-Entscheidungen
- [Anti-Slop](.quinsy-studio/process/anti-slop.md) — Code-Qualität
- [Ticket Workflow](.quinsy-studio/process/ticket-workflow.md) — 9-Schritte
- [Iterative Delivery](.quinsy-studio/process/iterative-delivery.md) — Sprints
- [Human-in-the-Loop](.quinsy-studio/process/human-in-the-loop.md) — Entscheidungen
- [Project Archetypes](.quinsy-studio/process/project-archetypes.md) — Projekt-Typen

### Teams
- [Frontend Experience](.quinsy-studio/teams/01-frontend-experience/README.md)
- [Backend Systems](.quinsy-studio/teams/02-backend-systems/README.md)
- [Compliance & Legal](.quinsy-studio/teams/03-compliance-legal/README.md)
- [Product Strategy & Architecture](.quinsy-studio/teams/04-product-strategy-architecture/README.md)
- [Growth, Marketing & Content](.quinsy-studio/teams/05-growth-marketing-content/README.md)
- [Product Management & Operating Model](.quinsy-studio/teams/06-product-management-operating-model/README.md)
- [AI & Autonomous Systems](.quinsy-studio/teams/07-ai-autonomous-systems/README.md)
- [Platform & Enterprise Engineering](.quinsy-studio/teams/08-platform-enterprise-engineering/README.md)

### Studio Library
- [Design Tokens](.quinsy-studio/studio-library/ui/tokens/)
- [Button Component](.quinsy-studio/studio-library/ui/components/button/)
- [Comparison Page Type](.quinsy-studio/studio-library/ui/page-types/comparison/)
- [Auth Package](.quinsy-studio/studio-library/packages/auth/)
- [Billing Package](.quinsy-studio/studio-library/packages/billing/)
- [Feature Gating Package](.quinsy-studio/studio-library/packages/feature-gating/)

### Externe Skills (Skill-Package-Manager)
- [Skill Dependencies](.quinsy-studio/skill-dependencies.json) — abonnierte Quellen
- [External Skills Index](.quinsy-studio/external-skills/INDEX.md) — importierte Pakete
- `./studio update-skills` — alle externen Skills abonnieren/aktualisieren

## CLI-Befehle

```bash
./studio --help
```

## Archetypen

| Archetyp | Beschreibung |
|----------|-------------|
| `saas-application` | B2C/B2B SaaS-Produkt |
| `ecommerce` | Online-Shop |
| `content-platform` | Content-Management |
| `marketplace` | Zweiseitiger Markt |
| `internal-tool` | Interne Dashboards |
| `api-service` | Backend-API |
| `mobile-app` | Mobile Anwendung |
| `prototype` | Schneller Prototyp |

## Qualitäts-Regeln

1. **Kein Code ohne Ticket** — Jede Zeile Code braucht ein Ticket
2. **Gate = Pflicht** — Kein Gate wird übersprungen
3. **Anti-Slop** — AI-Code muss geprüft werden
4. **ADRs** — Alle Entscheidungen werden dokumentiert
5. **Self-Learning** — Fehler werden analysiert und vermieden
6. **HITL** — Irreversible Entscheidungen brauchen menschliche Freigabe

## CHANGELOG

Siehe [CHANGELOG.md](CHANGELOG.md) für alle Änderungen.

---

**Version:** 1.0.0
**Stand:** 2026-08-20
