# Studio HQ skill advancement — sprint plan

> Source catalog: [davila7/claude-code-templates](https://github.com/davila7/claude-code-templates) (`cli-tool/components/skills/`, plus attributed repos).  
> **Index (2026-09-24):** 30 categories, **892** `SKILL.md` files. First pass sampled categories; second pass listed **every skill name** (not every file body). Distill from names + our team CARD, then read the SKILL.md at implement time.  
> **Not a product milestone.** Tickets: `LO-0331`–`LO-0339` in `.quinsy-studio/backlog/open/`.  
> This chat stays `studio_meta`. Do not queue on a product sprint inbox.

**Policy**

1. **Cite → distill → CARD.** Infuse Do/Don’t/implement-fail (or spec-fail) into existing playbooks. Prefer that over new skill IDs.
2. **Never** `npx claude-code-templates` the whole tree (~910 `SKILL.md`). Subscribe **named upstream repos** only.
3. Catalog files are **reference**, not authority. Anti-slop, library-first, sequential gates, secrets-as-names, and packet HITL win.
4. **Python tools** enforce what CARD already claims. They do not invent a second design language.
5. Do not import `executing-plans` (batch then wait). Studio loop is `./studio execute` until HITL.

**How to run**

1. Implement one LO at a time in an HQ session: playbook/skill/tool + tests + CHANGELOG → move LO to `backlog/done/`.
2. Product execute INFORM open LO counts; infuse with `./studio train` in HQ — do not steal IMPLEMENT.

---

## Selected catalog (in) vs dump (out)

| Include (read, then distill) | Path / repo | Why |
|------------------------------|-------------|-----|
| `frontend-design`, `ui-design-system`, `tailwind-patterns`, **`scroll-experience`**, **`theme-factory`** | `creative-design/` | UI + tokens + scroll + **HITL theme pick** — UX-005 / UX-006 / UX-007; map to aesthetic presets + tokens, do not dump catalog hex into the product app |
| `accessibility-auditor` | `creative-design/` | Spec-fail + FE-004 |
| `figma-implement-design` | `creative-design/` | Handoff only — extension, not a new UX ID |
| `ux-researcher-designer` | `creative-design/` | Overlaps UX-004 — steal methods, not a second research team |
| `nextjs-app-router-patterns`, `react-best-practices`, `web-performance-optimization` | `web-development/` | FE-001 / FE-003 |
| `playwright-skill` | `utilities/` | FE-006 |
| `zod-validation-expert` | `web-development/` | Forms/API client — FE-001 + BE-001 |
| `postgres-schema-design`, `supabase-postgres-best-practices` | `database/` | BE-002 |
| `api-design-principles`, `api-patterns` | `development/` | BE-001 |
| `context-window-management`, `agent-evaluation`, `autonomous-agent-patterns` | `ai-research/` | AI-001 / new AI-004 |
| **`workflow-automation`** | `workflow-automation/` | Durable agent jobs — AI-003 (not PE-002 CI). Related reads: `inngest`, `n8n`, `trigger-dev` |
| `deslop` | `sentry/` | AI-002 |
| `debugging-strategies`, `code-review-excellence`, `avoid-ai-writing` | [obra/superpowers](https://github.com/obra/superpowers) | SO-002 / AI-002 |
| Official `pdf`, `pptx`, `xlsx`, `docx` | [anthropics/skills](https://github.com/anthropics/skills) | SO-004 / UX-007 optional |

### Second pass (full name index — fold into existing LOs, no extra IDs)

These were **missed or under-weighted** in the first selected table. Read the SKILL.md when implementing the mapped LO.

| Fold into | Catalog skills (names) |
|-----------|------------------------|
| **LO-0332** Team 10 | **`scroll-experience`** (required), **`theme-factory`** (required), `mobile-design`, `web-design-guidelines`, `mermaid-diagrams`, `c4-architecture`, `canvas-design`, `figma` (plus `figma-implement-design`), `ui-ux-pro-max` **as anti-pattern reference only** (presets win), `premium-web-design` only for commercial-web class |
| **LO-0335** FE | `react-state-management`, `tanstack-query-expert`, `zustand-store-ts`, `react-component-performance`, `react-patterns`, `react-ui-patterns`, `react-useeffect`, `nextjs-best-practices`, `frontend-dev-guidelines`, `cc-skill-frontend-patterns`, `core-web-vitals`, `progressive-web-app`, `i18n-localization`, `playwright` / `playwright-e2e-builder` / `e2e-testing-patterns`, `javascript-testing-patterns`, `typescript-expert`, `design-system-starter`, `tailwind-design-system` |
| **LO-0336** BE | `bullmq-specialist`, `database-optimizer`, `postgresql-optimization`, `database-migration`, `postgres-best-practices`, `laravel-expert`, `nodejs-backend-patterns`, `saas-multi-tenant`, `domain-driven-design`, `openapi-to-typescript`, `graphql` (Don’t: no GraphQL skill ID unless archetype needs it), `stripe-integration`, `event-sourcing-architect` (reference), `backend-to-frontend-handoff-docs` |
| **LO-0337** AI | **`workflow-automation`** (required), `llm-evaluation`, `rag-implementation` / `rag-engineer`, `llm-app-patterns`, `prompt-engineering-patterns`, `prompt-caching`, `eval-genius`, `safety-alignment-nemo-guardrails`, `observability-langsmith` / `langfuse` (observability, not vendor lock); related: `inngest`, `n8n-workflow-patterns`, `trigger-dev` |
| **LO-0334 / PE-003** (defensive only) | `api-security-best-practices`, `secrets-management`, `security-threat-model` / `threat-modeling-expert`, `sast-configuration`, `supply-chain-guard`, `top-web-vulnerabilities`, `cc-skill-security-review` — **not** pentest/Metasploit catalogs |
| **Team 11** (distill into growth-mechanics with 0332) | `form-cro`, `page-cro`, `signup-flow-cro`, `onboarding-cro`, `paywall-upgrade-cro`, `analytics-tracking` |
| **Team 03** (later epic, not 0331–0339 implement) | `gdpr-dsgvo-expert`, `data-privacy-compliance` — read vs privacy-legal-compliance **before** subscribe |
| **SO-002 / 0331** | `systematic-debugging`, `verification-before-completion`, `tdd-workflow`, `code-review-checklist`, `receiving-code-review`, `requirements-clarity`, `skill-creator` |
| **PE-002 / PE-004** (later) | `github-actions-templates`, `observability-engineer` |
| **Root** | `design-to-code` → same as Figma extension |

| Exclude | Reason |
|---------|--------|
| Whole `development/` (230) as a **blob** | CARD overflow — **named** rows above are in |
| `scientific/` (136), `career/` (21), `sports/`, `doordash/`, `railway/`, `curviate/`, `pocketbase/`, `open-banking-io/` | Not agency default craft |
| `security/` pentest / Metasploit / privilege-escalation / sqlmap / burp **attack** skills | PE-003 is **defensive** |
| `shadcn` as source of truth | Studio-library + Radix kit |
| `executing-plans`, `finishing-a-development-branch` as studio loop | Conflicts with execute-until-HITL |
| Bright Data `web-data/scrape` MCP as default | Secrets / vendor |
| 400+ persona **agents**; `senior-*` role packs | Ticket → team skill IDs already |
| `ai-research` training/Megatron/Unsloth/fine-tune zoo | We ship **product** agents, not foundation-model training |
| `video/` (Sora, Remotion) unless a ticket is motion-export | Optional later for UX-007 |
| ISO/FDA/QMS enterprise-comms | Not CL-001 unless the product is a medical device |

---

## Vetting: Quinsy skill vs selected catalog

Verdict: **keep** (already stronger) · **distill** (playbook + thin skill pointer) · **new ID** · **tool** (Python) · **skip**.

### Team 10 — UX, IA, UI (product design)

| Quinsy | Selected catalog | Verdict | Enhancement |
|--------|------------------|---------|-------------|
| UX-001 Product design | `ux-researcher-designer` (partial), Garrett/Cooper already in canon | **keep + distill** | Steal JTBD/posture checklists; no new ID. Spec-fail: no goal in §1. |
| UX-002 Interaction | `frontend-design` (states), form patterns in catalog | **distill** | Empty/loading/error/success matrix already required — add catalog form anti-patterns as Don’t. Tool: mock-state filenames already in `design_ticket_helpers.py`. |
| UX-003 IA | *no dedicated IA skill in aitmpl* (nav buried in frontend-design) | **keep + tool** | We are ahead. Tool: wrap `design_math.ia_nav_audit` as `./studio ia-audit` and require top-level count + depth in spec §2. |
| UX-004 Research | `ux-researcher-designer` | **distill** | Mental-model interview prompts into `ux-research-playbook.md`. Do not duplicate Team 06 PM-001. |
| UX-005 Visual UI | `ui-design-system`, `tailwind-patterns`, `frontend-design`, **`theme-factory`** | **distill** | Contrast already in `design_math.py`. Distill type-scale / 60-30-10 as spec-fail. **Theme-factory process:** show repertoire → **HITL pick** → apply one cohesive palette+type pair. Product UI: map the pick onto **one aesthetic preset** or `project-brand-only`, then **tokens** — do not paste catalog hex (“Ocean Depths”) into app CSS. |
| UX-006 Brand | `brand-guidelines-*`; **`theme-factory` HITL** | **distill process only** | Logo still HITL. Theme-factory wait-for-selection matches Brand Guardian: never auto-apply a surprise palette. |
| UX-007 Storyteller | Anthropic `pptx` / `pdf`; **`scroll-experience`**; **`theme-factory`** | **distill** | Marketing/story pages: scroll as narrative (beats, sticky, reveal). Spec-fail: scroll hijack; hide content behind motion; desktop-only parallax. Pair FE-003 (no CLS/jank) + FE-004 (`prefers-reduced-motion`). No GSAP as a default kit. **Slides/PDF/report artifacts:** theme-factory 10 packs + custom-on-HITL; WCAG contrast on hex. |
| UX-008 Anti-slop design | `avoid-ai-writing`, `sentry/deslop` | **distill** | Copy clichés → anti-slop-design-ux. |
| Aesthetic presets | `design_awesome` already subscribed; **`theme-factory` as picker ritual** | **keep + distill** | 17 studio presets remain the product-UI source of truth. Theme-factory **does not replace** them. It adds: explicit choice, pairing (color+type together), artifact themes for UX-007. |
| *(missing)* Figma handoff | `figma-implement-design` | **extension** | `skill-extensions/figma-token-handoff.md` under UX-002/005. Not UX-009. |
| *(missing)* Delight ID | catalog motion skills | **skip new ID** | Delight stays on every design CARD via UX-002 (canon). `scroll-experience` is **not** UX-009 — load from UX-002/007 + delight playbook. |

### Team 01 — Frontend + design *application*

| Quinsy | Selected catalog | Verdict | Enhancement |
|--------|------------------|---------|-------------|
| FE-001 Compose kit | `react-best-practices`, `zod-validation-expert` | **distill + tool** | App-router/data-fetch Don’ts. Tool: fail `native <select>` / missing kit peers (extend gate). |
| FE-002 Apply tokens | `ui-design-system`, `tailwind-patterns`, **not** `shadcn` | **distill + tool** | Tool: warn hardcoded `#hex` / `rgb()` in product UI when tokens exist. |
| FE-003 Performance | `web-performance-optimization` | **distill** | LCP/INP/CLS playbook bullets; no new ID. |
| FE-004 a11y | `accessibility-auditor`, `development/accessibility` | **distill** | Spec-fail contrast already; add name/role/value Don’ts. |
| FE-005 PWA | — | **keep** | No catalog gap. Load only when ticket says PWA. |
| FE-006 Testing | `playwright-skill` | **distill** | Default-flow already required. Distill locator/role queries — not a second QA team. |
| *(role, no ID)* Client security | OWASP plugin examples (defensive) | **new ID FE-007** | Thin CARD: XSS/CSP/token storage; always-on with FE-001. Playbook: existing `frontend-security-auditor.md`. |

### Team 02 — Backend

| Quinsy | Selected catalog | Verdict | Enhancement |
|--------|------------------|---------|-------------|
| BE-001 API | `api-design-principles`, `api-patterns` | **distill** | Error envelopes already. Add idempotency + pagination Don’ts. |
| BE-002 Database | `postgres-schema-design`, `supabase-postgres-best-practices` | **distill** | Migrate-via-`--approve` already. Distill index/FK Don’ts. |
| BE-003 Auth | catalog oauth skills (all_domains already) | **keep** | Server-side auth spine exists. |
| BE-004 Errors | — | **keep** | Stronger than catalog. |
| BE-005 Integrations | — | **distill lightly** | Timeouts + no `NEXT_PUBLIC_` secrets (isolation). |
| *(role, no ID)* Jobs / sync | — | **new ID BE-006** | Thin: queues, outbox, partner sync. Spine in `backend_playbook.md`. |

### Team 07 — AI autonomous

| Quinsy | Selected catalog | Verdict | Enhancement |
|--------|------------------|---------|-------------|
| AI-001 Integration | `autonomous-agent-patterns`, `ai-agents-architect` | **distill** | Replace generic provider list with adapter + eval + user-visible surface (already LO-0017). |
| AI-002 Anti-slop | `deslop`, `avoid-ai-writing` | **distill** | Point at `validate_anti_slop.py` (already a tool). |
| AI-003 Automation pipelines | **`workflow-automation`** (n8n / Temporal / Inngest patterns) | **distill + retarget** | CI/CD stays **PE-002**. AI-003 = (1) studio train/infusion loop **and** (2) **durable agent workflows**: sequential / parallel / orchestrator-worker, checkpoints, idempotency, timeouts, backoff, observability. **Don’t** default n8n — pick platform with an ADR. Queues/outbox stay **BE-006**. |
| *(missing)* Eval / RAG / context | `agent-evaluation`, `context-window-management` | **new ID AI-004** | Thin CARD + `ai_automation_playbook` sections. Tool: AI-ticket receipt heading `Eval` required on AI-001/004 implement. |

### Other teams (not this epic’s implement focus)

Compliance, growth, growth-design, platform security, studio ops: **no wholesale catalog**. Optional later: defensive OWASP examples under PE-003; superpowers review under SO-002 (LO-0331 import covers files).

---

## Python tools (selected skills)

Existing (keep, wire harder): `validate_anti_slop.py`, `design_math.py` (`ia_nav_audit`, contrast), `design_ticket_helpers.py` (spec §2 / all-state), `ui_kit_peers.py`, `run_qa_gate.py`.

| New / extend | Enforces | CLI |
|--------------|----------|-----|
| `studio_ia_audit.py` | UX-003 nav limits | `./studio ia-audit <p> <TICKET>` |
| Token literal warn in `run_qa_gate.py` | FE-002 | gate level 5 **warn** (not red on generated Konva if allowlisted) |
| Native-control scan | FE-001 implement-fail | gate level 5 **warn** → **red** after one sprint of false-positive tuning |
| `ai_eval_receipt.py` | AI-004 | `move … done` refuses AI tickets without Eval heading |
| FE-007 / security auditor | already markdown | CARD load only in LO-0335 |

Do **not** scrape Figma via Bright Data. Handoff extension is tokens + HTML mocks we already require.

---

## Sprints

### HQ-SKILL-01 — Subscribe (no dump)

| ID | Est. | Title |
|----|------|--------|
| LO-0331 | M | Subscribe superpowers + Anthropic document skills; conflict-matrix those sources; refuse aitmpl blob install |

### HQ-SKILL-02 — Design (UX / IA / UI / systems)

| ID | Est. | Title |
|----|------|--------|
| LO-0332 | L | Distill selected design catalog into Team 10 playbooks; **`scroll-experience`** + **`theme-factory`**; Figma handoff as extension; no UX-009 |
| LO-0333 | M | IA: `./studio ia-audit` must wrap `ia_nav_audit` and fail approve-design when nav counts are missing or over limit |

### HQ-SKILL-03 — Frontend

| ID | Est. | Title |
|----|------|--------|
| LO-0334 | M | Design-system application: token-literal warn on gate 5; FE-002 playbook; never treat shadcn as kit |
| LO-0335 | L | Distill Next/React/Playwright into frontend playbook; add thin FE-007 client security on every UI implement CARD |

### HQ-SKILL-04 — Backend

| ID | Est. | Title |
|----|------|--------|
| LO-0336 | L | Distill postgres/API catalog into backend playbook; add thin BE-006 jobs and delivery |

### HQ-SKILL-05 — AI autonomous

| ID | Est. | Title |
|----|------|--------|
| LO-0337 | L | Distill eval/context catalog; add thin AI-004; retarget AI-003 from CI/CD to durable agent workflows (`workflow-automation`) |

### HQ-SKILL-06 — Tools + CARD

| ID | Est. | Title |
|----|------|--------|
| LO-0338 | L | Skill-advancement Python checks (IA already 0333; tokens, native select, AI eval receipt) + unit tests |
| LO-0339 | S | Registry, CARD playbook lists, GETTING_STARTED: new IDs + subscribed sources |

**After HQ-SKILL-06:** product chats keep IMPLEMENT; HQ train infuses remaining LOs.

**Execute steps (file-level):** [hq-skill-advancement-implementation.md](hq-skill-advancement-implementation.md)

---

## Out of scope

- Installing the aitmpl CLI into operator machines as the studio source of truth.
- New Team 12.
- Offensive security skills.
- Changing product app code in `projects/`.
- Morning-brief dashboards.
