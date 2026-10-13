# Skills

Sixty-four skills. The owner is the first id on the ticket. Companions are the rest. This page is the map. The file the agent reads is under `.quinsy-studio/teams/<team>/skills/`.

## 01 — Frontend

| ID | Skill | Why it is included |
|----|--------|--------------------|
| FE-001 | UI components | Buttons, cards, modals, pages. Build from the library, not from scratch. |
| FE-002 | Design system | Tokens, type, color, theme. The project kit from gate 2b. |
| FE-003 | Performance | Load time and bundle size. |
| FE-004 | Accessibility | Companion on every UI ticket. |
| FE-005 | PWA | Offline, installable. |
| FE-006 | Frontend testing | Companion on every UI ticket. |
| FE-007 | Client security | XSS, content security policy. |
| FE-008 | i18n | Language switch and localized fields. |

## 02 — Backend

| ID | Skill | Why it is included |
|----|--------|--------------------|
| BE-001 | API design | REST and GraphQL contracts. |
| BE-002 | Database design | Schema, queries, migrations. |
| BE-003 | Auth | Login, session, roles. On a web app this is Payload Users, not a second auth system. |
| BE-004 | Error handling | Retries and logging. |
| BE-005 | Integrations | Webhooks, email, other vendors. |
| BE-006 | Jobs | Queues and workers. A long job is enqueued, not run inside the request. |
| BE-007 | Payload | Collections, local API, admin. Loaded when the blueprint says Payload is in. |
| BE-008 | Payments | Stripe and Lemon Squeezy. Pull the `billing` package. |
| BE-009 | Documents | Invoices and structured documents. |

A ticket that moves content in from another CMS also loads the cms-migration skill. It is not a standing team member.

## 03 — Compliance

| ID | Skill | Why it is included |
|----|--------|--------------------|
| CL-001 | Privacy | Personal data, minimization, deletion. |
| CL-002 | Cookies | Consent before tracking. |
| CL-003 | Terms | Impressum, terms, cancellation. |
| CL-004 | Zero data | What the product must not store. |

## 04 — Strategy

| ID | Skill | Why it is included |
|----|--------|--------------------|
| PS-001 | Product strategy | Vision, scope, monetization. |
| PS-002 | Architecture decisions | ADRs, build versus buy. Gate 1. |
| PS-003 | Technology evaluation | Framework and library choice. |
| PS-004 | Feasibility | Spikes and risk. |

## 05 — Growth and content

| ID | Skill | Why it is included |
|----|--------|--------------------|
| GM-001 | SEO | Search, schema, site structure. |
| GM-002 | AEO | Being cited by answer engines. |
| GM-003 | Content | Editorial, tone, copy volume. |
| GM-005 | Launch | Community and the first public post. |
| GM-006 | Lifecycle email | Welcome and drip. Marketing law comes with it. |
| GM-007 | Positioning | The sentence the product is willing to repeat. |

GM-004 is the game router. It loads only when the archetype is a game.

## 06 — Product management

| ID | Skill | Why it is included |
|----|--------|--------------------|
| PM-001 | User research | Interviews and the gap between what people do and what the product assumes. |
| PM-002 | Roadmapping | Milestones and priority. |
| PM-003 | Operating model | How the team is shaped. |
| PM-004 | Ticket staffing | On every ticket. Owner first, then companions. |

## 07 — AI

| ID | Skill | Why it is included |
|----|--------|--------------------|
| AI-001 | AI integration | The product calls a model. |
| AI-002 | Anti-slop audit | Generated code and copy still have to meet the bar. |
| AI-003 | Automation pipelines | Durable jobs and agent workflows. |
| AI-004 | Eval and context | Whether the model output is good enough to ship. |
| AI-005 | AI-code security | Companion when auth, access, or a model can be talked into the wrong thing. |

## 08 — Platform

| ID | Skill | Why it is included |
|----|--------|--------------------|
| PE-001 | Infrastructure | Docker, Coolify, the VPS. |
| PE-002 | CI/CD | Pipelines. |
| PE-003 | Security audit | Companion on auth and access. |
| PE-004 | Monitoring | Uptime and errors in production. |
| PE-005 | Threat modeling | Trust boundaries. |
| PE-006 | Secrets | Names in schema, values never in chat. |
| PE-007 | Incidents | Outage, backup, restore. |

## 09 — Studio operations

| ID | Skill | Why it is included |
|----|--------|--------------------|
| SO-001 | Studio tooling | The `./studio` command itself. |
| SO-002 | Process | Gates, sprints, the human stops. |
| SO-003 | Dual-loop learning | Harvest and infusion. See [Studio learning](09-hq-learning.md). |
| SO-004 | Documentation | This manual, READMEs, changelogs. |
| SO-005 | Release reality check | A fresh walk of the dev build before the cadence brief. |

The ideation desk is a Team 09 skill too. It runs the research loop, not a product ticket.

## 10 — Product design

| ID | Skill | Why it is included |
|----|--------|--------------------|
| UX-001 | Product design | Jobs to be done and the platform shape. |
| UX-002 | UX design | Interaction, forms, states, motion. |
| UX-003 | Information architecture | Where a feature lives. Placement before layout. |
| UX-004 | UX research | Personas and mental models. |
| UX-005 | Visual UI | Hierarchy, type, color. |
| UX-006 | Brand | Voice and consistency. |
| UX-007 | Visual storyteller | Marketing narrative and workflow explainers. |
| UX-008 | Anti-slop design | Gate 2a. The direction has to be this product, not a default theme. |
| UX-009 | Finish gate | Shipped screen versus the signed mock, including the click-through. |

## 11 — Growth design

Loaded beside Team 10. The ticket team stays 10.

| ID | Skill | Why it is included |
|----|--------|--------------------|
| GD-001 | Experiments | A hypothesis before a variant. |
| GD-002 | Commercial surfaces | Landing, pricing, checkout, catalog, product page. |
| GD-003 | Persona walkthrough | A five-second read of a commercial packet. |
| GD-004 | Growth loops | Invite, share, activation, upgrade. |
