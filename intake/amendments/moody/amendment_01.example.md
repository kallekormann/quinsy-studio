# Amendment brief — Example title (replace when copying)

> **Project:** moody  
> **Amendment ID:** (assigned on intake → `AM-001`)  
> **Author:** {{your name}}  
> **Date:** {{YYYY-MM-DD}}  
> **Status:** draft  
>
> **Drop path:** `intake/amendments/moody/amendment_01.md`  
> **Then tell the agent:** *"Run amendment intake for moody amendment_01"*
>
> **Do not fill milestones here** — the studio derives new/updated phases after analysis.

---

## 1. Executive summary

<!-- 2–4 sentences: what is this amendment about, in plain language? -->

## 2. Why now

<!-- What changed? User feedback, market, competitor, technical unlock, strategic pivot. -->

| Trigger | Detail |
|---------|--------|
| Primary driver | |
| Evidence (optional) | links, quotes, metrics |
| Urgency | now / next quarter / before launch |

## 3. Vision & concept

<!-- The studio needs enough narrative to weave this into the running product. Write like a short product brief, not a ticket. -->

### 3.1 North-star statement

<!-- One paragraph: the future state if this amendment succeeds. -->

### 3.2 Core concept

<!-- What is the big idea? Name it if helpful (e.g. "Agency client rooms", "AI palette director"). -->

### 3.3 Who benefits

| Audience | How they benefit |
|----------|------------------|
| Primary user | |
| Secondary user | |
| Business | |

### 3.4 Key scenarios (story-level)

<!-- 3–5 short scenarios. "As a … I want … so that …" is fine but keep them conceptual. -->

1. 
2. 
3. 

### 3.5 Product principles (for this amendment)

<!-- Rules the studio should follow when designing/building this direction. -->

- 
- 

### 3.6 Relationship to current Moody

<!-- How does this connect to infinite canvas, boards, teams, share, export, collab today? What stays? What evolves? -->

## 4. Scope boundaries

### 4.1 In scope (directional)

<!-- Capabilities or outcomes you want — still not implementation detail. -->

- 
- 

### 4.2 Out of scope

<!-- Explicitly excluded — prevents scope creep during analysis. -->

- 
- 

### 4.3 Non-goals

<!-- Things that might sound related but are deliberately not part of this amendment. -->

- 

## 5. Success picture

<!-- How do we know this worked? Qualitative + measurable if you have them. -->

| Signal | Target (optional) |
|--------|---------------------|
| User outcome | |
| Business outcome | |
| Technical outcome | |

## 6. Constraints & dependencies

| Type | Notes |
|------|-------|
| Must work with existing collab / teams / share | |
| Legal / privacy | |
| Performance / offline | |
| Depends on other work | e.g. billing, new infra |
| Budget / timeline gut feel | |

## 7. Open questions for the studio

<!-- What should the analysis answer? The agent will respond in `docs/amendments/AM-NNN/`. -->

1. 
2. 
3. 

---

## 8. Team selection

<!-- Check every team that should participate in analysis or delivery. The studio assigns lead vs support per artifact. -->

### Core delivery teams

- [ ] **01 — Frontend Experience** — UI implementation, canvas, performance, a11y, PWA  
- [ ] **02 — Backend Systems** — APIs, data, auth, integrations, email  
- [ ] **10 — Product Design & Experience** — UX, IA, visual design, brand, design specs  

### Strategy, product & growth

- [ ] **04 — Product Strategy & Architecture** — vision fit, ADRs, tech evaluation, feasibility  
- [ ] **05 — Growth, Marketing & Content** — SEO, AEO, landing copy, content strategy  
- [ ] **06 — Product Management & Operating Model** — research, roadmap, operating model  

### Compliance, platform & AI

- [ ] **03 — Compliance & Legal** — GDPR, cookies, terms, zero-data  
- [ ] **07 — AI & Autonomous Systems** — LLM features, anti-slop, automation  
- [ ] **08 — Platform & Enterprise Engineering** — infra, CI/CD, security, monitoring  

### Studio meta

- [ ] **09 — Studio Operations & Evolution** — process, tooling, documentation governance  

---

## 9. Skill selection

<!-- Check skills the studio should load during analysis and when writing tickets. Max ~5 per ticket at implement time; here you flag all that may be needed across the amendment. -->

### Team 01 — Frontend Experience

- [ ] **FE-001** UI Component Design  
- [ ] **FE-002** Design System / tokens / themes  
- [ ] **FE-003** Performance optimization  
- [ ] **FE-004** Accessibility (WCAG)  
- [ ] **FE-005** PWA / offline  
- [ ] **FE-006** Frontend testing  

### Team 02 — Backend Systems

- [ ] **BE-001** API design  
- [ ] **BE-002** Database / schema / migrations  
- [ ] **BE-003** Auth / RBAC / OAuth  
- [ ] **BE-004** Error handling / observability  
- [ ] **BE-005** Third-party integrations (Stripe, email, …)  

### Team 03 — Compliance & Legal

- [ ] **CL-001** DSGVO / GDPR  
- [ ] **CL-002** Cookie / consent  
- [ ] **CL-003** Impressum / terms  
- [ ] **CL-004** Zero-data architecture  

### Team 04 — Product Strategy & Architecture

- [ ] **PS-001** Product strategy  
- [ ] **PS-002** Architecture decisions (ADRs)  
- [ ] **PS-003** Technology evaluation  
- [ ] **PS-004** Feasibility analysis  

### Team 05 — Growth, Marketing & Content

- [ ] **GM-001** SEO  
- [ ] **GM-002** AEO / AI search visibility  
- [ ] **GM-003** Content strategy / copy  

### Team 06 — Product Management

- [ ] **PM-001** User research  
- [ ] **PM-002** Roadmapping / prioritization  
- [ ] **PM-003** Operating model  

### Team 07 — AI & Autonomous Systems

- [ ] **AI-001** AI / LLM integration  
- [ ] **AI-002** Anti-slop audit  
- [ ] **AI-003** Automation pipelines  

### Team 08 — Platform & Enterprise Engineering

- [ ] **PE-001** Infrastructure / Docker / deploy  
- [ ] **PE-002** CI/CD  
- [ ] **PE-003** Security audit  
- [ ] **PE-004** Monitoring / observability  

### Team 09 — Studio Operations

- [ ] **SO-001** Studio tooling maintenance  
- [ ] **SO-002** Process optimization  
- [ ] **SO-003** Dual-loop learning  
- [ ] **SO-004** Documentation governance  

### Team 10 — Product Design & Experience

- [ ] **UX-001** Product design / user flows  
- [ ] **UX-002** UX design / interaction / microcopy  
- [ ] **UX-003** Information architecture  
- [ ] **UX-004** UX research  
- [ ] **UX-005** Visual UI design  
- [ ] **UX-006** Brand guardian  
- [ ] **UX-007** Visual storyteller / marketing surfaces  

---

## 10. Optional references

<!-- Links, screenshots, competitors, internal docs — anything that grounds the vision. -->

| Reference | URL / path | Notes |
|-----------|------------|-------|
| | | |

---

## What the studio produces (after you submit)

You do **not** write milestones or tickets. On `./studio amend moody <this-file>`, the agent creates:

```
projects/moody/docs/amendments/AM-001-<slug>/
├── source.md                    # copy of this brief
├── 01-vision-synthesis.md         # consolidated narrative + PRD fit
├── 02-requirements-addendum.md  # new FR/NFR, personas, journeys
├── 03-milestone-roadmap.md      # NEW/updated M* phases (replaces guessing M6 timing)
├── 04-ui-ux-concept.md          # Team 10 — flows, IA, concept mocks direction
├── 05-frontend-architecture.md  # Team 01 — components, routes, state, library impact
├── 06-backend-architecture.md   # Team 02 — APIs, data, integrations
├── 07-tooling-and-process.md    # Team 08/09 — CI, env, studio scripts if needed
├── 08-adrs/                     # Team 04 — only if decisions required
├── 09-tickets-draft.md          # groomed stubs with team + skills + milestone tags
└── 10-approval-checklist.md     # human sign-off before backlog materialize
```

Human approves → tickets move to `backlog/` → **then** sprint planning (M6 billing waits until roadmap is re-approved).
