# Quinsy Studio — Skill Registry

> Central index of all skills. The agent uses this registry to assign the right skills to a ticket.

---

## Overview

| Team | Skills | Lead Roles (Director) |
|------|--------|----------------------|
| 01 Frontend Experience | 7 Skills | Lead Experience Architect, Frontend Architect, QA Specialist, UI/Interaction Designer |
| 02 Backend Systems | 6 Skills | Senior Fullstack Architect, Backend Architect, Database Specialist |
| 03 Compliance & Legal | 4 Skills | Legal & Privacy Officer |
| 04 Product Strategy & Architecture | 4 Skills | Product Manager, Systems Architect |
| 05 Growth, Marketing & Content | 3 Skills | SEO/AEO Specialist, Growth Manager |
| 06 Product Management & Operating Model | 3 Skills | Product Manager |
| 07 AI & Autonomous Systems | 4 Skills | Autonomous Systems Director |
| 08 Platform & Enterprise Engineering | 4 Skills | Platform Architect |
| 09 Studio Operations & Evolution | 4 Skills | Studio Automation Engineer, Process Guard, Agile Coach |
| 10 Product Design & Experience | 7 Skills | Product Designer, UX Designer, Brand Guardian, Visual Storyteller |
| 11 Growth Design | 2 Skills | Growth Designer |
| **Total** | **49 Skills** | |

---

## External Skills (Skill Package Manager)

> The studio subscribes to best-in-class skills from external repositories
> (`./studio update-skills`). They are ALWAYS subordinate to the internal
> `anti_ai_slop_protocol.md` and Zero-Data Architecture.
> Imported to `.quinsy-studio/external-skills/` (see `INDEX.md`).
> Advancement epic (UX/IA/UI/FE/BE/AI): [process/hq-skill-advancement-sprints.md](../process/hq-skill-advancement-sprints.md) (`LO-0331`–`LO-0339`).

| External Source | Covered Domains | Internal Teams/Skills | Activation |
|----------------|----------------|----------------------|------------|
| `Nutlope/hallmark` | Anti-Slop Design, Macrostructure, Themes | 01 FE: FE-002 Design System, UI/Interaction Designer | `audit`, `redesign`, `study`, Design drafts |
| `bergside/awesome-design-skills` | 67 Design Skills (Corporate, Paper, Glassmorphism, ...) | 01 FE: FE-001, FE-002 | Reference library for UI designs (SKILL.md + DESIGN.md per style) |
| `seb1n/awesome-ai-agent-skills` | Database, Security, Legal/Compliance, SEO, Copywriting, PM, DevOps, API, Design | **All teams** — targeted per skill: | `--skill <name>` |
| `coreyhaines31/marketingskills` | **49 Marketing Skills**: CRO, Copywriting, SEO, AEO (`ai-seo`), Analytics, Growth | 05 Growth: GM-001, GM-002, GM-003 | `product-marketing` (base) → `ai-seo`, `seo-audit`, `schema`, `copywriting`, `cro`, `ab-testing` |
| `gamedev-skills/awesome-gamedev-agent-skills` | 67 Game Dev Skills (Godot, Unity, Unreal, Phaser, PixiJS, three.js, Bevy, pygame, LÖVE, Roblox) | 01 FE / 02 BE (project archetype `game`!) | Router detects engine + task automatically |
| `samir-abis/cookiecomply-skills` | GDPR/Cookie Compliance (Banner, Consent) | 03 Compliance: CL-002 | `cookiecomply` workflow |
| `bloomprotocol/agent-visibility-skill` | GEO/AI-Visibility: llms.txt, JSON-LD, Comparison Pages, AI-Visibility Audit | 05 Growth: GM-002 AEO | `AI-Visibility-Audit`, `llms.txt`, Comparison Pages |
| `obra/superpowers` | Debug, review, avoid-ai-writing | 09 SO-002 / 07 AI-002 | **Not** `executing-plans` |
| `anthropics/skills` | pdf / pptx / xlsx / docx | 09 SO-004 / 10 UX-007 artifacts | Optional export — not product CSS |
| catalog `scroll-experience` (distilled) | Narrative scroll | UX-002 / UX-007 | Playbook — no new ID |
| catalog `theme-factory` (distilled) | HITL theme pick | UX-005 / UX-006 / UX-007 | Map to aesthetic presets + tokens |

### Targeted Skill Mappings (awesome-ai-agent-skills → Studio Skills)

| External Skill | Studio Skill (replaces/supplements) |
|----------------|--------------------------------------|
| `database-schema-design`, `query-optimization`, `database-migration` | BE-002 Database Design |
| `api-design`, `oauth-2-0-setup`, `webhook-setup` | BE-001 API Design, BE-003 Auth |
| `security-audit`, `threat-modeling`, `dependency-scanning`, `static-application-security-testing` | PE-003 Security Audit |
| `compliance-checklist-generation`, `privacy-policy-drafting`, `terms-of-service-generation` | CL-001 DSGVO, CL-003 Impressum/AGB |
| `seo-optimization`, `customer-research`, `content-strategy` | GM-001 SEO, GM-003 Content |
| `copywriting`, `blog-post-writing`, `technical-writing` | GM-003 Content, SO-004 Docs |
| `ai-seo` (marketing_aeo) | **GM-002 AEO** — be cited in AI Search/LLM responses |
| `seo-audit`, `schema`, `programmatic-seo`, `site-architecture` (marketing_aeo) | GM-001 SEO (pSEO, Schema.org, Link Rot) |
| `competitors`, `comparison` (marketing_aeo/geo_visibility) | GM-002 AEO — comparison/alternative pages |
| `cro`, `ab-testing`, `analytics`, `pricing` (marketing_aeo) | **GD-001 / GD-002** (hypothesis + commercial mechanics); GM-003 only for copy volume |
| `product-marketing`, `customer-research` (marketing_aeo) | PM-001 User Research, GM-003 Content |
| `cookiecomply` (compliance_cookies) | CL-002 Cookie Banner, Consent Management |
| `llms.txt`, `JSON-LD`, `AI-Visibility-Audit` (geo_visibility) | GM-002 AEO, GM-001 SEO |
| `godot-*`, `unity-*`, `unreal-*`, `phaser-*` (gamedev) | Project archetype `game` — Frontend/Backend per engine |
| `project-management` | PM-002 Roadmapping, SO-002 Process |
| `docker-compose-setup`, `ci-cd`, `infrastructure-as-code` | PE-001 Infra, PE-002 CI/CD |
| `frontend-design`, `wireframing`, `accessibility-testing` | FE-001, FE-004 |
| `human-in-the-loop` | SO-002 Process (HITL Gates) |

**Workflow:** Before activating an internal skill file, the agent checks whether an
imported external skill covers the task better → read external SKILL.md →
compare with internal rules → execute.

---

## Studio skill extensions (committed playbooks)

Deep, codebase-aware extensions live in [knowledge-base/skill-extensions/](../knowledge-base/skill-extensions/README.md).  
They **do not add new internal IDs** — they extend existing skills:

| Extension | Internal skill(s) | Team |
|-----------|-------------------|------|
| delight-micro-interactions | UX-002, FE-001 | 10, 01 |
| email-design | GM-003, UX-007 | 05, 10 |
| product-led-growth | GM-003, PS-001 | 05, 04 |
| affiliate-compliance | GM-001 | 05 |
| privacy-legal-compliance | CL-001 | 03 |
| cookie-compliance | CL-002 | 03 |
| tos-architect | CL-003 | 03 |
| compliance-orchestrator | CL-001/002/003 (audit index) | 03 |
| figma-token-handoff | UX-002, UX-005 | 10 |
| motion-transitions | UX-002, UX-005, FE-001, FE-002 | 10, 01 |
| frontend-security-auditor | PE-003, FE-007 | 08, 01 |
| backend-security-auditor | PE-003 | 08, 02 |

Human drafts: `intake/skills/` (gitignored) → promote to `knowledge-base/skill-extensions/` after review.

---

## Skill Assignment by Ticket Content

### When ticket contains → activate skill

#### Frontend (Team 01)

| Trigger Words | Skill | ID |
|---------------|-------|----|
| Component, UI Element, Button, Card, Modal | UI Component Design | FE-001 |
| Design Tokens, Color Palette, Typography, Theme, Dark Mode | Design System | FE-002 |
| Performance, Load Time, Speed, Bundle, Core Web Vitals | Performance Optimization | FE-003 |
| a11y, Accessibility, WCAG, Screenreader | Accessibility | FE-004 |
| PWA, Offline, Service Worker, Manifest, Installable | PWA Implementation | FE-005 |
| Test, Testing, Coverage, Unit-Test, E2E | Frontend Testing | FE-006 |
| Client XSS, CSP, frontend security | Client Security | FE-007 |

#### Product Design & Experience (Team 10)

| Trigger Words | Skill | ID |
|---------------|-------|----|
| User flow, jobs-to-be-done, platform UX | Product Design | UX-001 |
| Interaction, microcopy, form UX, modal states | UX Design | UX-002 |
| Navigation, IA, wayfinding, nav structure | Information Architecture | UX-003 |
| Feature placement, wrong surface, capability home | Information Architecture | UX-003 (+ UX-002 workflow) |
| Persona, usability, mental model, research | UX Research | UX-004 |
| Typography, color, layout, visual hierarchy | Visual UI Design | UX-005 |
| Brand, voice, tone, consistency | Brand Guardian | UX-006 |
| Homepage, landing, storytelling, workflow diagram, scroll | Visual Storyteller | UX-007 |

#### Growth Design (Team 11)

| Trigger Words | Skill | ID |
|---------------|-------|----|
| A/B, hypothesis, experiment, conversion, CRO, variant | Hypothesis & experiment design | GD-001 |
| Landing, pricing table/page, checkout, cart, PDP, PLP, catalog | Commercial surface mechanics | GD-002 |

Ticket `team` stays **10** when GD is paired. See [design-team-canon-ledger.md](../knowledge-base/design-team-canon-ledger.md).

**External (reference, not duplicated):** `.quinsy-studio/external-skills/design-agent/` → `ux-*`, `taste-skill`, `brandkit`

**Aesthetic presets (studio-owned, optional):** `.quinsy-studio/knowledge-base/aesthetic-presets/` — 17 presets; Team 10 may footnote via [aesthetic-presets.md](../teams/10-product-design-experience/skills/aesthetic-presets.md). Uniqueness in `design/DESIGN.md` is the source of truth.

#### Backend (Team 02)

| Trigger Words | Skill | ID |
|---------------|-------|----|
| API, Endpoint, REST, GraphQL, HTTP | API Design | BE-001 |
| Database, Schema, Migration, Query, SQL, Postgres | Database Design | BE-002 |
| Auth, Login, JWT, Session, RBAC, OAuth | Authentication & Authorization | BE-003 |
| Error, Exception, Error Handling, Retry, Logging | Error Handling | BE-004 |
| Integration, Webhook, Stripe, SendGrid, Payment | Third-Party Integrations | BE-005 |
| Queue, Worker, Outbox, BullMQ, Background job | Jobs and Delivery | BE-006 |

#### Compliance (Team 03)

| Trigger Words | Skill | ID |
|---------------|-------|----|
| DSGVO, GDPR, Privacy | DSGVO Compliance | CL-001 |
| Cookie, Consent, Banner, Tracking | Cookie Banner | CL-002 |
| Impressum, AGB, Terms of Service, Cancellation | Impressum & AGB | CL-003 |
| Zero-Data, Data Minimization, Deletion Concept, DPA | Zero-Data Architecture | CL-004 |

#### Strategy (Team 04)

| Trigger Words | Skill | ID |
|---------------|-------|----|
| Strategy, Vision, Roadmap, Monetization | Product Strategy | PS-001 |
| ADR, Architecture, Tech Stack, Build vs Buy | Architecture Decisions | PS-002 |
| Evaluation, Framework, Library, Migration | Technology Evaluation | PS-003 |
| Feasibility, Risk, Scope | Feasibility Analysis | PS-004 |

#### Growth (Team 05)

| Trigger Words | Skill | ID |
|---------------|-------|----|
| SEO, Visibility, Ranking, Google, Schema.org | SEO Optimization | GM-001 |
| AEO, AI Search, ChatGPT, Perplexity, Comparison | AEO | GM-002 |
| Content, Blog, Social, Newsletter, Tone of Voice | Content Strategy | GM-003 |

#### Product Management (Team 06)

| Trigger Words | Skill | ID |
|---------------|-------|----|
| Research, Interview, Survey, Usability | User Research | PM-001 |
| Roadmap, Prioritization, Planning, MoSCoW | Roadmapping | PM-002 |
| Operating Model, Team Structure, Process, OKR | Operating Model | PM-003 |

#### AI (Team 07)

| Trigger Words | Skill | ID |
|---------------|-------|----|
| AI, LLM, GPT, Claude, Prompt, AI Integration | AI Integration | AI-001 |
| Anti-Slop, Slop, AI Code, Code Quality | Anti-Slop Audit | AI-002 |
| Durable workflow, orchestrator, Inngest, Temporal, infusion, agent job | Automation Pipelines | AI-003 |
| Eval, RAG, context window, prompt cache | Eval and Context | AI-004 |

#### Platform (Team 08)

| Trigger Words | Skill | ID |
|---------------|-------|----|
| Infrastructure, Docker, Cloud, Deploy, CDN | Infrastructure | PE-001 |
| CI/CD, Pipeline, GitHub Actions, Build | CI/CD Pipelines | PE-002 |
| Security, OWASP, Penetration, Vulnerability | Security Audit | PE-003 |
| Monitoring, Alerting, Uptime, Sentry | Monitoring & Observability | PE-004 |

#### Game Development (Cross-cutting — External Skill)

| Trigger Words | Skill | ID |
|---------------|-------|----|
| Game, Godot, Unity, Unreal, Platformer, Phaser, three.js, pygame | Game Development (external) | GM-004 |

> GM-004 activates the **gamedev router** (`.quinsy-studio/external-skills/gamedev/router/`),
> which automatically detects engine + task and loads matching skills (e.g., `godot-2d-movement` + `platformer`).
> Corresponds to project archetype `game`.

#### Studio Operations (Team 09)

| Trigger Words | Skill | ID |
|---------------|-------|----|
| Studio Tools, Python, Tooling, Maintenance | Studio Tooling Maintenance | SO-001 |
| Process, Sprint Discipline, Optimization, Metrics | Process Optimization | SO-002 |
| Learning, Retro, Knowledge, Promotion, Dual-Loop | Dual-Loop Learning | SO-003 |
| Docs, Documentation, README, CHANGELOG | Documentation Governance | SO-004 |

---

## Skill Assignment by Phase

| Phase | Typical Skills |
|-------|----------------|
| **Phase 0** (Intake) | PS-001, PS-004, PM-001, CL-001, SO-004 |
| **Phase 1** (Validation) | PS-001, PS-003, PS-004, PM-001, PE-001, GM-001, SO-004 |
| **Phase 2** (Architecture) | PS-002, BE-001, BE-002, FE-002, CL-001, CL-004, AI-001, PE-001, PE-003, GM-001, SO-002 |
| **Phase 3** (Sprint Setup) | PM-002, FE-001, FE-002, FE-005, BE-001, CL-002, GM-003, PE-001, PE-002, AI-001, SO-002 |
| **Phase 4** (Implementation) | FE-001, FE-003, FE-004, FE-005, FE-006, FE-007, BE-001, BE-002, BE-003, BE-004, BE-005, BE-006, CL-002, CL-003, AI-001, AI-002, AI-003, AI-004, PE-002, PE-003, SO-001 |
| **Phase 5** (QA) | FE-003, FE-004, FE-006, BE-003, CL-001, CL-002, AI-002, PE-003, PE-004, GM-001, GM-002, PM-001, SO-002 |
| **Phase 6** (Knowledge Harvesting) | **SO-003 (Dual-Loop)**, SO-001, SO-002, SO-004, PE-004, PM-003 |
| **Phase 7** (Deployment) | PE-001, PE-002, PE-004, GM-001, GM-002, GM-003, PS-001, PM-002, PM-003, SO-001, SO-004 |

---

## Skill Assignment by Archetype

| Archetype | Preferred Skills |
|-----------|-------------------|
| **saas-application** | FE-001, FE-002, FE-005, BE-001, BE-002, BE-003, CL-001, PS-001, PE-001, SO-003 |
| **e-commerce** | FE-001, BE-001, BE-005, CL-001, CL-002, GM-001, PS-001, SO-003 |
| **content-platform** | FE-001, FE-002, BE-001, GM-001, GM-002, GM-003, PS-001, SO-003 |
| **enterprise-tool** | BE-001, BE-003, PE-003, PS-002, CL-004, SO-003 |
| **mobile-first** | FE-001, FE-005, FE-003, PE-001, SO-003 |
| **game** | FE-001, FE-003, BE-002, PE-001 + **external: gamedev (Router)** |

---

## Skill Activation Workflow

```
1. Read ticket
     │
2. Detect trigger words
     │
3. Assign skills from registry (max. 5 per ticket)
     │
4. Check phase context
     │
5. Check archetype
     │
6. Determine lead role (from team README)
     │
7. Determine support roles
     │
8. Load skill files (.quinsy-studio/teams/[team]/skills/)
     │
9. Work according to skill rules
     │
10. Learning → Local or Global Loop (Phase 6)
```

---

## Skill Files (Paths)

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
│       ├── frontend-testing.md
│       └── client-security.md
├── 02-backend-systems/
│   ├── README.md
│   └── skills/
│       ├── api-design.md
│       ├── database-design.md
│       ├── authentication-authorization.md
│       ├── error-handling.md
│       ├── third-party-integrations.md
│       └── jobs-and-delivery.md
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
│       ├── automation-pipelines.md
│       └── eval-and-context.md
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
├── 10-product-design-experience/
│   ├── README.md
│   ├── agents/
│   │   ├── design-brand-guardian.md
│   │   ├── design-ux-researcher.md
│   │   └── design-visual-storyteller.md
│   └── skills/
│       ├── product-design.md
│       ├── ux-design.md
│       ├── information-architecture.md
│       ├── ux-research.md
│       ├── visual-ui-design.md
│       ├── aesthetic-presets.md
│       ├── brand-guardian.md
│       └── visual-storyteller.md
├── 11-growth-design/
│   ├── README.md
│   └── skills/
│       ├── hypothesis-experiment-design.md
│       └── commercial-surface-mechanics.md
└── skill-registry.md  ← THIS FILE
```
