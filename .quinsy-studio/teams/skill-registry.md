# Quinsy Studio — Skill Registry

> Zentraler Index aller Skills. Der Agent nutzt diese Registry, um die richtigen Skills einem Ticket zuzuordnen.

---

## Übersicht

| Team | Skills | Lead-Rollen (Director) |
|------|--------|------------------------|
| 01 Frontend Experience | 6 Skills | Lead Experience Architect, Frontend Architect, QA Specialist, UI/Interaction Designer |
| 02 Backend Systems | 5 Skills | Senior Fullstack Architect, Backend Architect, Database Specialist |
| 03 Compliance & Legal | 4 Skills | Legal & Privacy Officer |
| 04 Product Strategy & Architecture | 4 Skills | Product Manager, Systems Architect |
| 05 Growth, Marketing & Content | 3 Skills | SEO/AEO Specialist, Growth Manager |
| 06 Product Management & Operating Model | 3 Skills | Product Manager |
| 07 AI & Autonomous Systems | 3 Skills | Autonomous Systems Director |
| 08 Platform & Enterprise Engineering | 4 Skills | Platform Architect |
| 09 Studio Operations & Evolution | 4 Skills | Studio Automation Engineer, Process Guard, Agile Coach |
| **Gesamt** | **36 Skills** | |

---

## Externe Skills (Skill-Package-Manager)

> Das Studio abonniert Best-in-Class Skills aus externen Repositories
> (`./studio update-skills`). Sie sind IMMER dem internen
> `anti_ai_slop_protocol.md` und der Zero-Data-Architecture untergeordnet.
> Importiert nach `.quinsy-studio/external-skills/` (siehe `INDEX.md`).

| Externe Quelle | Abgedeckte Domains | Interne Teams/Skills | Aktivierung |
|----------------|--------------------|----------------------|-------------|
| `Nutlope/hallmark` | Anti-Slop-Design, Macrostructure, Themes | 01 FE: FE-002 Design System, UI/Interaction Designer | `audit`, `redesign`, `study`, Design-Entwürfe |
| `bergside/awesome-design-skills` | 67 Design-Skills (Corporate, Paper, Glassmorphism, ...) | 01 FE: FE-001, FE-002 | Referenz-Bibliothek bei UI-Entwürfen (SKILL.md + DESIGN.md pro Stil) |
| `seb1n/awesome-ai-agent-skills` | Database, Security, Legal/Compliance, SEO, Copywriting, PM, DevOps, API, Design | **alle Teams** — gezielt per Skill: | `--skill <name>` |
| `coreyhaines31/marketingskills` | **49 Marketing-Skills**: CRO, Copywriting, SEO, AEO (`ai-seo`), Analytics, Growth | 05 Growth: GM-001, GM-002, GM-003 | `product-marketing` (Basis) → `ai-seo`, `seo-audit`, `schema`, `copywriting`, `cro`, `ab-testing` |
| `gamedev-skills/awesome-gamedev-agent-skills` | 67 Game-Dev-Skills (Godot, Unity, Unreal, Phaser, PixiJS, three.js, Bevy, pygame, LÖVE, Roblox) | 01 FE / 02 BE (Projekt-Archetyp `game`!) | Router erkennt Engine + Task automatisch |
| `samir-abis/cookiecomply-skills` | DSGVO/Cookie-Compliance (Banner, Consent) | 03 Compliance: CL-002 | `cookiecomply`-Workflow |
| `bloomprotocol/agent-visibility-skill` | GEO/AI-Visibility: llms.txt, JSON-LD, Vergleichsseiten, AI-Visibility-Audit | 05 Growth: GM-002 AEO | `AI-Visibility-Audit`, `llms.txt`, Comparison Pages |

### Gezielte Skill-Mappings (awesome-ai-agent-skills → Studio-Skills)

| Externer Skill | Studio-Skill (ersetzt/ergänzt) |
|----------------|-------------------------------|
| `database-schema-design`, `query-optimization`, `database-migration` | BE-002 Database Design |
| `api-design`, `oauth-2-0-setup`, `webhook-setup` | BE-001 API Design, BE-003 Auth |
| `security-audit`, `threat-modeling`, `dependency-scanning`, `static-application-security-testing` | PE-003 Security Audit |
| `compliance-checklist-generation`, `privacy-policy-drafting`, `terms-of-service-generation` | CL-001 DSGVO, CL-003 Impressum/AGB |
| `seo-optimization`, `keyword-research`, `content-strategy` | GM-001 SEO, GM-003 Content |
| `copywriting`, `blog-post-writing`, `technical-writing` | GM-003 Content, SO-004 Doku |
| `ai-seo` (marketing_aeo) | **GM-002 AEO** — in AI-Search/LLM-Antworten zitiert werden |
| `seo-audit`, `schema`, `programmatic-seo`, `site-architecture` (marketing_aeo) | GM-001 SEO (pSEO, Schema.org, Link-Rot) |
| `competitors`, `comparison` (marketing_aeo/geo_visibility) | GM-002 AEO — Vergleichs-/Alternativen-Seiten |
| `cro`, `ab-testing`, `analytics`, `pricing` (marketing_aeo) | GM-003 Growth — Cost of Experimentation, Ghost of Experiments Past |
| `product-marketing`, `customer-research` (marketing_aeo) | PM-001 User Research, GM-003 Content |
| `cookiecomply` (compliance_cookies) | CL-002 Cookie Banner, Consent-Management |
| `llms.txt`, `JSON-LD`, `AI-Visibility-Audit` (geo_visibility) | GM-002 AEO, GM-001 SEO |
| `godot-*`, `unity-*`, `unreal-*`, `phaser-*` (gamedev) | Projekt-Archetyp `game` — Frontend/Backend je Engine |
| `project-management` | PM-002 Roadmapping, SO-002 Prozess |
| `docker-compose-setup`, `ci-cd`, `infrastructure-as-code` | PE-001 Infra, PE-002 CI/CD |
| `frontend-design`, `wireframing`, `accessibility-testing` | FE-001, FE-004 |
| `human-in-the-loop` | SO-002 Prozess (HITL-Gates) |

**Workflow:** Vor Aktivierung einer internen Skill-Datei prüft der Agent, ob ein
importierter externer Skill die Aufgabe besser abdeckt → externe SKILL.md lesen →
mit internen Regeln abgleichen → ausführen.

---

## Skill-Zuordnung nach Ticket-Inhalten

### Wenn Ticket enthält → Skill aktivieren

#### Frontend (Team 01)

| Trigger-Wörter | Skill | ID |
|----------------|-------|----|
| Komponente, Component, UI-Element, Button, Card, Modal | UI Component Design | FE-001 |
| Design Tokens, Farbpalette, Typografie, Theme, Dark Mode | Design System | FE-002 |
| Performance, Ladezeit, Speed, Bundle, Core Web Vitals | Performance Optimization | FE-003 |
| a11y, Barrierefreiheit, Accessibility, WCAG, Screenreader | Accessibility | FE-004 |
| PWA, Offline, Service Worker, Manifest, Installierbar | PWA Implementation | FE-005 |
| Test, Testing, Coverage, Unit-Test, E2E | Frontend Testing | FE-006 |

#### Backend (Team 02)

| Trigger-Wörter | Skill | ID |
|----------------|-------|----|
| API, Endpoint, REST, GraphQL, HTTP | API Design | BE-001 |
| Database, Schema, Migration, Query, SQL, Postgres | Database Design | BE-002 |
| Auth, Login, JWT, Session, RBAC, OAuth | Authentication & Authorization | BE-003 |
| Error, Exception, Fehlerbehandlung, Retry, Logging | Error Handling | BE-004 |
| Integration, Webhook, Stripe, SendGrid, Payment | Third-Party Integrations | BE-005 |

#### Compliance (Team 03)

| Trigger-Wörter | Skill | ID |
|----------------|-------|----|
| DSGVO, GDPR, Datenschutz, Privacy | DSGVO Compliance | CL-001 |
| Cookie, Consent, Banner, Tracking | Cookie Banner | CL-002 |
| Impressum, AGB, Nutzungsbedingungen, Widerruf | Impressum & AGB | CL-003 |
| Zero-Data, Datenminimierung, Löschkonzept, AVV | Zero-Data Architecture | CL-004 |

#### Strategy (Team 04)

| Trigger-Wörter | Skill | ID |
|----------------|-------|----|
| Strategie, Vision, Roadmap, Monetarisierung | Product Strategy | PS-001 |
| ADR, Architektur, Tech-Stack, Build vs Buy | Architecture Decisions | PS-002 |
| Evaluation, Framework, Library, Migration | Technology Evaluation | PS-003 |
| Machbarkeit, Feasibility, Risiko, Scope | Feasibility Analysis | PS-004 |

#### Growth (Team 05)

| Trigger-Wörter | Skill | ID |
|----------------|-------|----|
| SEO, Sichtbarkeit, Ranking, Google, Schema.org | SEO Optimization | GM-001 |
| AEO, AI Search, ChatGPT, Perplexity, Vergleich | AEO | GM-002 |
| Content, Blog, Social, Newsletter, Tone of Voice | Content Strategy | GM-003 |

#### Product Management (Team 06)

| Trigger-Wörter | Skill | ID |
|----------------|-------|----|
| Research, Interview, Survey, Usability | User Research | PM-001 |
| Roadmap, Priorisierung, Planning, MoSCoW | Roadmapping | PM-002 |
| Operating Model, Team-Struktur, Prozess, OKR | Operating Model | PM-003 |

#### AI (Team 07)

| Trigger-Wörter | Skill | ID |
|----------------|-------|----|
| AI, LLM, GPT, Claude, Prompt, KI-Integration | AI Integration | AI-001 |
| Anti-Slop, Slop, AI-Code, Code-Qualität | Anti-Slop Audit | AI-002 |
| CI/CD, Pipeline, Automatisierung, GitHub Actions | Automation Pipelines | AI-003 |

#### Platform (Team 08)

| Trigger-Wörter | Skill | ID |
|----------------|-------|----|
| Infrastructure, Docker, Cloud, Deploy, CDN | Infrastructure | PE-001 |
| CI/CD, Pipeline, GitHub Actions, Build | CI/CD Pipelines | PE-002 |
| Security, OWASP, Penetration, Vulnerability | Security Audit | PE-003 |
| Monitoring, Alerting, Uptime, Sentry | Monitoring & Observability | PE-004 |

#### Game Development (Querschnitt — externer Skill)

| Trigger-Wörter | Skill | ID |
|----------------|-------|----|
| Game, Godot, Unity, Unreal, Platformer, Phaser, three.js, pygame, Spiel | Game Development (extern) | GM-004 |

> GM-004 aktiviert den **gamedev-Router** (`.quinsy-studio/external-skills/gamedev/router/`),
> der Engine + Task automatisch erkennt und die passenden Skills lädt (z.B. `godot-2d-movement` + `platformer`).
> Entspricht dem Projekt-Archetyp `game`.

#### Studio Operations (Team 09)

| Trigger-Wörter | Skill | ID |
|----------------|-------|----|
| Studio Tools, Python, Tooling, Wartung | Studio Tooling Maintenance | SO-001 |
| Prozess, Sprint-Disziplin, Optimierung, Metriken | Process Optimization | SO-002 |
| Learning, Retro, Knowledge, Promotion, Dual-Loop | Dual-Loop Learning | SO-003 |
| Doku, Documentation, README, CHANGELOG | Documentation Governance | SO-004 |

---

## Skill-Zuordnung nach Phase

| Phase | Typische Skills |
|-------|----------------|
| **Phase 0** (Intake) | PS-001, PS-004, PM-001, CL-001, SO-004 |
| **Phase 1** (Validierung) | PS-001, PS-003, PS-004, PM-001, PE-001, GM-001, SO-004 |
| **Phase 2** (Architektur) | PS-002, BE-001, BE-002, FE-002, CL-001, CL-004, AI-001, PE-001, PE-003, GM-001, SO-002 |
| **Phase 3** (Sprint Setup) | PM-002, FE-001, FE-002, FE-005, BE-001, CL-002, GM-003, PE-001, PE-002, AI-001, SO-002 |
| **Phase 4** (Implementierung) | FE-001, FE-003, FE-004, FE-005, FE-006, BE-001, BE-002, BE-003, BE-004, BE-005, CL-002, CL-003, AI-001, AI-002, PE-002, PE-003, SO-001 |
| **Phase 5** (QA) | FE-003, FE-004, FE-006, BE-003, CL-001, CL-002, AI-002, PE-003, PE-004, GM-001, GM-002, PM-001, SO-002 |
| **Phase 6** (Knowledge Harvesting) | **SO-003 (Dual-Loop)**, SO-001, SO-002, SO-004, PE-004, PM-003 |
| **Phase 7** (Deployment) | PE-001, PE-002, PE-004, GM-001, GM-002, GM-003, PS-001, PM-002, PM-003, SO-001, SO-004 |

---

## Skill-Zuordnung nach Archetyp

| Archetyp | Bevorzugte Skills |
|----------|-------------------|
| **saas-application** | FE-001, FE-002, FE-005, BE-001, BE-002, BE-003, CL-001, PS-001, PE-001, SO-003 |
| **e-commerce** | FE-001, BE-001, BE-005, CL-001, CL-002, GM-001, PS-001, SO-003 |
| **content-platform** | FE-001, FE-002, BE-001, GM-001, GM-002, GM-003, PS-001, SO-003 |
| **enterprise-tool** | BE-001, BE-003, PE-003, PS-002, CL-004, SO-003 |
| **mobile-first** | FE-001, FE-005, FE-003, PE-001, SO-003 |
| **game** | FE-001, FE-003, BE-002, PE-001 + **extern: gamedev (Router)** |

---

## Skill-Aktivierungs-Workflow

```
1. Ticket lesen
     │
2. Trigger-Wörter erkennen
     │
3. Skills aus Registry zuordnen (max. 5 pro Ticket)
     │
4. Phasen-Kontext prüfen
     │
5. Archetyp prüfen
     │
6. Lead-Rolle bestimmen (aus Team-README)
     │
7. Support-Rollen bestimmen
     │
8. Skill-Dateien laden (.quinsy-studio/teams/[team]/skills/)
     │
9. Nach Skill-Regeln arbeiten
     │
10. Learning → Local oder Global Loop (Phase 6)
```

---

## Skill-Dateien (Pfade)

```
.quinsy-studio/teams/
├── 01-frontend-experience/
│   ├── README.md
│   └── skills/
│       ├── ui-component-design.md
│       ├── design-system.md
│       ├── performance-optimization.md
│       ├── accessibility.md
│       ├── pwa-implementation.md
│       └── frontend-testing.md
├── 02-backend-systems/
│   ├── README.md
│   └── skills/
│       ├── api-design.md
│       ├── database-design.md
│       ├── authentication-authorization.md
│       ├── error-handling.md
│       └── third-party-integrations.md
├── 03-compliance-legal/
│   ├── README.md
│   └── skills/
│       ├── dsgvo-compliance.md
│       ├── cookie-banner-implementation.md
│       ├── impressum-agb.md
│       └── zero-data-architecture.md
├── 04-product-strategy-architecture/
│   ├── README.md
│   └── skills/
│       ├── product-strategy.md
│       ├── architecture-decisions.md
│       ├── technology-evaluation.md
│       └── feasibility-analysis.md
├── 05-growth-marketing-content/
│   ├── README.md
│   └── skills/
│       ├── seo-optimization.md
│       ├── aeo-answer-engine-optimization.md
│       └── content-strategy.md
├── 06-product-management-operating-model/
│   ├── README.md
│   └── skills/
│       ├── user-research.md
│       ├── roadmapping.md
│       └── operating-model.md
├── 07-ai-autonomous-systems/
│   ├── README.md
│   └── skills/
│       ├── ai-integration.md
│       ├── anti-slop-audit.md
│       └── automation-pipelines.md
├── 08-platform-enterprise-engineering/
│   ├── README.md
│   └── skills/
│       ├── infrastructure.md
│       ├── ci-cd-pipelines.md
│       ├── security-audit.md
│       └── monitoring-observability.md
├── 09-studio-operations-evolution/
│   ├── README.md
│   └── skills/
│       ├── studio-tooling-maintenance.md
│       ├── process-optimization.md
│       ├── dual-loop-learning.md
│       └── documentation-governance.md
└── skill-registry.md  ← DIESE DATEI
```
