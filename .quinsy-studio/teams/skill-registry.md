# Quinsy Studio — Skill Registry

> Central index of all skills. The Product Manager staffs every ticket from this registry with **PM-004 Ticket Staffing** ([ticket-staffing.md](06-product-management-operating-model/skills/ticket-staffing.md)). Code mirror: `studio-tools/skill_matcher.py` (`INTERNAL_SKILLS`, `STAFFING_RULES`) and `ticket_helpers.SKILL_ROLE_MAP`; `test_staffing.py` fails when an ID has no role or no skill file.

---

## Overview

| Team | Skills | Lead Roles (Director) |
|------|--------|----------------------|
| 01 Frontend Experience | 8 Skills | Lead Experience Architect, Frontend Architect, QA Specialist, UI/Interaction Designer |
| 02 Backend Systems | 9 Skills | Senior Fullstack Architect, Backend Architect, Database Specialist |
| 03 Compliance & Legal | 4 Skills + marketing-law extension | Legal & Privacy Officer |
| 04 Product Strategy & Architecture | 4 Skills | Product Manager, Systems Architect |
| 05 Growth, Marketing & Content | 6 Skills | SEO/AEO Specialist, Growth Manager, Content Strategist |
| 06 Product Management & Operating Model | 4 Skills | Product Manager (staffs every ticket) |
| 07 AI & Autonomous Systems | 5 Skills | Autonomous Systems Director |
| 08 Platform & Enterprise Engineering | 7 Skills | Platform Architect, Backend Security Specialist |
| 09 Studio Operations & Evolution | 5 Skills | Studio Automation Engineer, Process Guard, Agile Coach, QA Specialist |
| 10 Product Design & Experience | 9 Skills | Product Designer, UX Designer, Brand Guardian, Visual Storyteller |
| 11 Growth Design | 3 Skills | Growth Designer |
| **Total** | **64 Skills** | |

New in 2026-10 (agency-agents integration, [plan](../process/hq-agency-agents-integration.md)): FE-008, BE-008, BE-009, GM-005, GM-006, PM-004, AI-005, PE-005, PE-006, PE-007, SO-005, UX-009, GD-003. UX-008 is now registered for ticket matching. HQ autonomy program (2026-10): GD-004, GM-007.

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
| `competitors`, `comparison` (marketing_aeo) | GM-002 AEO — comparison/alternative pages |
| `cro`, `ab-testing`, `analytics`, `pricing` (marketing_aeo) | **GD-001 / GD-002** (hypothesis + commercial mechanics); GM-003 only for copy volume |
| `product-marketing`, `customer-research` (marketing_aeo) | PM-001 User Research, GM-003 Content |
| `cookiecomply` (compliance_cookies) | CL-002 Cookie Banner, Consent Management |
| `llms.txt`, `JSON-LD`, `AI-Visibility-Audit` | GM-002 AEO, GM-001 SEO |
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
| backend-security-auditor | PE-003, AI-005 | 08, 02 |
| marketing-law | GM-001, GM-003, GM-005, GM-006, GD-002 (UWG, TDDDG § 25, PAngV § 11) | 03 |

Human drafts: `intake/skills/` (gitignored) → promote to `knowledge-base/skill-extensions/` after review.

---

## Skill Assignment by Ticket Content

Trigger words match **whole words** (short words must stand alone: `ai` does not hit `email`). Triggers find the owner skill. **Companions** come from the staffing signals in PM-004 (security, privacy, a11y, testing, payments, secrets, marketing email) and are checked at `./studio groom`.

### When ticket contains → activate skill

#### Frontend (Team 01)

| Trigger Words | Skill | ID |
|---------------|-------|----|
| Component, UI Element, Button, Card, Modal, Page, Screen, Wizard, Dashboard | UI Component Design | FE-001 |
| Design Tokens, Color Palette, Typography, Theme, Dark Mode | Design System | FE-002 |
| Performance, Load Time, Speed, Bundle, Core Web Vitals | Performance Optimization | FE-003 |
| a11y, Accessibility, WCAG, Screenreader (companion on every UI ticket) | Accessibility | FE-004 |
| PWA, Offline, Service Worker, Manifest, Installable | PWA Implementation | FE-005 |
| Test, Testing, Coverage, Unit-Test, E2E, Playwright (companion on every UI ticket) | Frontend Testing | FE-006 |
| Client XSS, CSP, frontend security | Client Security | FE-007 |
| i18n, Translation, Localization, Multilingual, Language switch | i18n and Localization | FE-008 |

When the blueprint says `Payload: in`, Team 01 styles `(marketing)` and `(app)` and reads [payload-playbook.md](../knowledge-base/payload-playbook.md). `/admin` stays Payload's UI.

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
| Design direction, direction critique (gate 2a), anti-slop design | Anti-Slop Design & UX | UX-008 |
| UI parity, finish gate, shipped screen vs signed mock | UI Finish Gate | UX-009 |

When the blueprint says `Payload: in`, Team 10 specs the marketing and app surfaces in [payload-playbook.md](../knowledge-base/payload-playbook.md). Do not restyle `/admin` in the design phase. A ticket that moves content in from another CMS also loads `teams/02-backend-systems/skills/cms-migration/SKILL.md`.

#### Growth Design (Team 11)

| Trigger Words | Skill | ID |
|---------------|-------|----|
| A/B, hypothesis, experiment, conversion, CRO, variant | Hypothesis & experiment design | GD-001 |
| Landing, pricing table/page, checkout, cart, PDP, PLP, catalog | Commercial surface mechanics | GD-002 |
| Persona walkthrough, five-second test (commercial design packets) | Persona walkthrough | GD-003 |
| Growth loop, Referral, Invite, Share link, Activation, Upgrade path | In-product growth loops | GD-004 |

Ticket `team` stays **10** when GD is paired. See [design-team-canon-ledger.md](../knowledge-base/design-team-canon-ledger.md).

**External (reference, not duplicated):** `.quinsy-studio/external-skills/design-agent/` → `ux-*`, `taste-skill`, `brandkit`

**Aesthetic presets (studio-owned, optional):** `.quinsy-studio/knowledge-base/aesthetic-presets/` — 17 presets; Team 10 may footnote via [aesthetic-presets.md](../teams/10-product-design-experience/skills/aesthetic-presets.md). Uniqueness in `design/DESIGN.md` is the source of truth.

#### Backend (Team 02)

| Trigger Words | Skill | ID |
|---------------|-------|----|
| API, Endpoint, REST, GraphQL, HTTP | API Design | BE-001 |
| Database, Schema, Migration, Query, SQL, Postgres | Database Design | BE-002 |
| Auth, Login, JWT, Session, RBAC, OAuth, Sign-up, Password | Authentication & Authorization | BE-003 |
| Error, Exception, Error Handling, Retry, Logging | Error Handling | BE-004 |
| Integration, Webhook, SendGrid, Email, SMTP | Third-Party Integrations | BE-005 |
| Queue, Worker, Outbox, BullMQ, Background job, Cron | Jobs and Delivery | BE-006 |
| Payload, Collection, Local API, CMS, Localization | Payload | BE-007 |
| Payment, Billing, Checkout, Subscription, Stripe, Lemon Squeezy, Refund | Payments and Billing | BE-008 |
| PDF, Invoice, XRechnung, ZUGFeRD, E-Rechnung, GoBD | Document Generation | BE-009 |
| WordPress, Contentful, Strapi, Sanity, Webflow, CMS migration | CMS migration (only that ticket) | cms-migration |

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
| Technology evaluation, framework choice, library choice | Technology Evaluation | PS-003 |
| Feasibility, Risk assessment, Spike | Feasibility Analysis | PS-004 |

#### Growth (Team 05)

| Trigger Words | Skill | ID |
|---------------|-------|----|
| SEO, Visibility, Ranking, Google, Schema.org | SEO Optimization | GM-001 |
| AEO, AI Search, ChatGPT, Perplexity, Comparison | AEO | GM-002 |
| Content strategy, Editorial, Blog, Social media, Tone of Voice, Copywriting | Content Strategy | GM-003 |
| Launch, Product Hunt, Show HN, Community, Press release, Reddit, LinkedIn | Launch and Community | GM-005 |
| Newsletter, Lifecycle email, Drip, Welcome email, Double opt-in | Lifecycle Email | GM-006 |
| Positioning, Core message, Tagline, Value proposition, Persona page, Hero copy | Positioning & Messaging | GM-007 |

#### Product Management (Team 06)

| Trigger Words | Skill | ID |
|---------------|-------|----|
| User research, Interview, Survey, Usability | User Research | PM-001 |
| Roadmap, Prioritization, MoSCoW, Milestone plan | Roadmapping | PM-002 |
| Operating Model, Team Structure, OKR | Operating Model | PM-003 |
| Every ticket at creation and groom; staffing, skill assignment | Ticket Staffing | PM-004 |

#### AI (Team 07)

| Trigger Words | Skill | ID |
|---------------|-------|----|
| AI, LLM, GPT, Claude, Prompt, AI Integration | AI Integration | AI-001 |
| Anti-Slop, Slop, AI Code, Code Quality | Anti-Slop Audit | AI-002 |
| Durable workflow, orchestrator, Inngest, Temporal, infusion, agent job | Automation Pipelines | AI-003 |
| Eval, RAG, context window, prompt cache | Eval and Context | AI-004 |
| Prompt injection, overrideAccess, access control; companion on auth/access/LLM tickets | AI-Code Security Audit | AI-005 |

#### Platform (Team 08)

| Trigger Words | Skill | ID |
|---------------|-------|----|
| Infrastructure, Docker, Cloud, Deploy, CDN, Coolify, VPS | Infrastructure | PE-001 |
| CI/CD, Pipeline, GitHub Actions, Project setup | CI/CD Pipelines | PE-002 |
| Security, OWASP, Vulnerability, XSS, CSRF, IDOR; companion on auth/access tickets | Security Audit | PE-003 |
| Monitoring, Alerting, Uptime, Sentry | Monitoring & Observability | PE-004 |
| Threat model, Trust boundary, STRIDE, Multi-tenant | Threat Modeling | PE-005 |
| Secret, API key, Credential, Env var, Key rotation | Secrets Hygiene | PE-006 |
| Incident, Outage, Runbook, Postmortem, Backup, Restore, Data breach | Incident, Reliability and Breach Response | PE-007 |

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
| Studio tools, Studio tooling, Python | Studio Tooling Maintenance | SO-001 |
| Process, Sprint Discipline, Optimization, Metrics | Process Optimization | SO-002 |
| Learning, Retro, Knowledge, Promotion, Dual-Loop | Dual-Loop Learning | SO-003 |
| Docs, Documentation, README, CHANGELOG | Documentation Governance | SO-004 |
| Reality check, Release readiness, Go-live (after `ship --to dev`) | Release Reality Check | SO-005 |

---

## Skill Assignment by Phase

| Phase | Typical Skills |
|-------|----------------|
| **Phase 0** (Intake) | PS-001, PS-004, PM-001, CL-001, SO-004 |
| **Phase 1** (Validation) | PS-001, PS-003, PS-004, PM-001, PE-001, GM-001, SO-004 |
| **Phase 2** (Architecture) | PS-002, BE-001, BE-002, BE-007, FE-002, CL-001, CL-004, AI-001, PE-001, PE-003, **PE-005** (threat model, threat delta), GM-001, SO-002 |
| **Phase 3** (Sprint Setup) | PM-002, **PM-004** (staff every ticket), FE-001, FE-002, FE-005, BE-001, CL-002, GM-003, PE-001, PE-002, AI-001, SO-002 |
| **Phase 4** (Implementation) | FE-001, FE-003, FE-004, FE-005, FE-006, FE-007, BE-001, BE-002, BE-003, BE-004, BE-005, BE-006, BE-007, CL-002, CL-003, AI-001, AI-002, AI-003, AI-004, PE-002, PE-003, SO-001 |
| **Phase 5** (QA) | FE-003, FE-004, FE-006, BE-003, CL-001, CL-002, AI-002, AI-005, PE-003, PE-004, UX-009, **SO-005** (reality check before cadence review), GM-001, GM-002, PM-001, SO-002 |
| **Phase 6** (Knowledge Harvesting) | **SO-003 (Dual-Loop)**, SO-001, SO-002, SO-004, PE-004, PM-003 |
| **Phase 7** (Deployment) | PE-001, PE-002, PE-004, GM-001, GM-002, GM-003, PS-001, PM-002, PM-003, SO-001, SO-004 |

---

## Skill Assignment by Archetype

| Archetype | Preferred Skills |
|-----------|-------------------|
| **saas-application** | FE-001, FE-002, FE-005, BE-001, BE-002, BE-003, BE-007, BE-008, CL-001, CL-003, PS-001, PE-001, PE-005, PE-006, SO-003 |
| **e-commerce** | FE-001, BE-001, BE-007, BE-008, BE-009, CL-001, CL-002, CL-003, GM-001, GD-002, PS-001, SO-003 |
| **content-platform** | FE-001, FE-002, BE-001, BE-007, GM-001, GM-002, GM-003, PS-001, SO-003 |
| **enterprise-tool** | BE-001, BE-003, PE-003, PS-002, CL-004, SO-003 |
| **mobile-first** | FE-001, FE-005, FE-003, PE-001, SO-003 |
| **game** | FE-001, FE-003, BE-002, PE-001 + **external: gamedev (Router)** |

---

## Skill Activation Workflow

```
1. Read ticket (Target, Scope, AC — not only the title)
     │
2. Detect trigger words → owner skill            (./studio ticket)
     │
3. PM-004 staffing: add companions with a reason  (## Staffing; max. 8 per ticket)
     │
4. Check phase context (design / architecture / implementation)
     │
5. Check archetype
     │
6. Lead role from the owner skill; support roles from companions
     │
7. ./studio groom refuses SKILLS_MISSING / SKILL_UNKNOWN / STAFFING_GAP
     │
8. execute CARD lists the skill files; agent reads them before coding
     │
9. Work according to skill rules; receipt shows each skill's Done evidence
     │
10. Learning → Local or Global Loop (Phase 6); retro names teams never staffed
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
│       ├── client-security.md
│       └── i18n-localization.md          (FE-008)
├── 02-backend-systems/
│   ├── README.md
│   └── skills/
│       ├── api-design.md
│       ├── database-design.md
│       ├── authentication-authorization.md
│       ├── error-handling.md
│       ├── third-party-integrations.md
│       ├── jobs-and-delivery.md
│       ├── payments-billing.md           (BE-008)
│       ├── document-generation.md        (BE-009)
│       ├── payload/SKILL.md              (BE-007, vendored)
│       └── cms-migration/SKILL.md
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
│       ├── content-strategy.md
│       ├── game-development.md
│       ├── launch-community.md           (GM-005)
│       ├── lifecycle-email.md            (GM-006)
│       └── positioning-messaging.md      (GM-007)
├── 06-product-management-operating-model/
│   ├── README.md
│   └── skills/
│       ├── user-research.md
│       ├── roadmapping.md
│       ├── operating-model.md
│       └── ticket-staffing.md            (PM-004)
├── 07-ai-autonomous-systems/
│   ├── README.md
│   └── skills/
│       ├── ai-integration.md
│       ├── anti-slop-audit.md
│       ├── automation-pipelines.md
│       ├── eval-and-context.md
│       └── ai-code-security-audit.md     (AI-005)
├── 08-platform-enterprise-engineering/
│   ├── README.md
│   └── skills/
│       ├── infrastructure.md
│       ├── ci-cd-pipelines.md
│       ├── security-audit.md
│       ├── monitoring-observability.md
│       ├── threat-modeling.md            (PE-005)
│       ├── secrets-hygiene.md            (PE-006)
│       └── incident-response.md          (PE-007)
├── 09-studio-operations-evolution/
│   ├── README.md
│   └── skills/
│       ├── studio-tooling-maintenance.md
│       ├── process-optimization.md
│       ├── dual-loop-learning.md
│       ├── documentation-governance.md
│       ├── ideation-desk.md
│       └── release-reality-check.md      (SO-005)
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
│       ├── visual-storyteller.md
│       ├── anti-slop-design-ux.md        (UX-008)
│       └── ui-finish-gate.md             (UX-009)
├── 11-growth-design/
│   ├── README.md
│   └── skills/
│       ├── hypothesis-experiment-design.md
│       ├── commercial-surface-mechanics.md
│       ├── persona-walkthrough.md        (GD-003)
│       └── in-product-growth-loops.md    (GD-004)
└── skill-registry.md  ← THIS FILE
```
