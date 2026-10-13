# Changelog — Quinsy Studio

All changes to Quinsy Studio are documented here.

## [Unreleased] — 2026-09-30

- Desktop secrets live in gitignored `projects/<p>/.env`. `./studio env … --approve` passes that file to Compose. Production stays in Coolify.
- After gate 2b, each cycle is a design phase, then an architecture phase, then an implementation phase. An empty phase is skipped.

Detail: [.quinsy-studio/CHANGELOG.md](.quinsy-studio/CHANGELOG.md) · [.quinsy-studio/GETTING_STARTED.md](.quinsy-studio/GETTING_STARTED.md)

## [1.16.0] — 2026-09-22

### HQ isolation (LO-0314–LO-0326)

- Secrets as **names** (`env.schema.json`); values in the host secret store; `./studio env … --approve`
- Docker required for gate / migrate / boot; execute leases (`parallel.max_projects`); one chat per product
- Sequential `approve --gate N`; execute CARD **CONSTITUTION**; INFORM open HQ learning counts; HQ train in a separate session

Detail: [.quinsy-studio/CHANGELOG.md](.quinsy-studio/CHANGELOG.md) · [hq-isolation-sprints.md](.quinsy-studio/process/hq-isolation-sprints.md)

## [1.12.0] — 2026-08-25

### STUDIO-SPRINT-01 — Design discipline & studio abstraction

- ✅ **Contextual IA** — `contextual-ia-playbook.md`, `workflow-definition-playbook.md`, design spec §2 Context & placement
- ✅ **`ia-feature-placement`** ticket type; UX-003 expanded; `approve-design` placement warning
- ✅ **`./studio verify-abstraction`** — scan studio HQ for hard-coded client project names
- ✅ **Amendment intake** — generic `studio-templates/amendment_01.example.md` (`acme-app`); docs use `<project>` placeholders
- ✅ **Docs** — `README.md`, `.quinsy-studio/README.md`, `GETTING_STARTED.md` updated for session ritual, design HITL, abstraction policy
- ✅ Learning items **LO-0006**, **LO-0007** (design-gap + studio abstraction)

Detail: [.quinsy-studio/CHANGELOG.md](.quinsy-studio/CHANGELOG.md) · [STUDIO-SPRINT-01](.quinsy-studio/sprints/STUDIO-SPRINT-01/README.md)

## [1.9.3] — 2026-08-24

### Sprint planning & learning loop

- ✅ **`assess_ticket_maturity`** — reads `phase` from ticket frontmatter (not body); feedback tickets still require `**Scope:**` in body
- ✅ **HITL** — retro step: agent must fill project `retro.md` + meta-retro (not template-only); maturity rules documented
- ✅ **Meta-retro** — populated `meta-retro-2026-08-24.md`; backfill note on 2026-08-23 shell
- ✅ **Learning items** — LO-0002 … LO-0005 from SPRINT-25 (ticket maturity, Supabase migrations, local-first sync, retro fill-in)

## [1.9.2] — 2026-08-21

### Studio library: Supabase auth boilerplate (LO-0001)

- ✅ **`packages/auth` v2.0.0** — Next.js App Router + `@supabase/ssr`: client, server, middleware, callback, RBAC, Resend welcome, `sync-supabase-env.mjs`, Supabase/Mailpit templates (promoted from a product)
- ✅ **`ui/components/auth-login/`** — generic `AuthLoginForm` molecule (sign-in, sign-up, magic link)
- ✅ Registry aliases: `supabase-auth`, `supabase`, `auth-login`
- ✅ Learning item **LO-0001** (library-gap, a product sprint)

## [1.9.1] — 2026-08-20

### Docker env runs compose with project name

- ✅ `./studio env <project> up|down|status|logs` **executes** `docker compose -p <project>` (no longer print-only)
- ✅ Auto-creates `docker/.env` from `.env.example` on first `up`
- ✅ Studio template: `name: {{PROJECT_NAME}}` + `container_name: {{PROJECT_NAME}}-*` so containers are not prefixed `docker-`

## [1.9.0] — 2026-08-20

### Milestone execution planning (post gate 2)

- ✅ **Execution planning** after design: `docs/phases/` milestone roadmap (M0, M1, …)
- ✅ Human approves roadmap before sprints; **tickets for active milestone only** (not full dump at gate 2)
- ✅ **Milestone review** when all milestone tickets done — before next milestone backlog + sprints
- ✅ Sprint HITL unchanged within a milestone (scope proposal → groom → autonomous implement → review)
- ✅ New project scaffold: `docs/phases/README.md` + `revisions.md`
- ✅ Docs: [milestone-planning.md](.quinsy-studio/process/milestone-planning.md); updates to lifecycle, HITL, backlog-model, iterative-delivery, AGENTS.md, README, GETTING_STARTED, operations manual

## [1.8.0] — 2026-08-20

### Product backlog layout + sprint scope approval

- ✅ **Product backlog** = `projects/<p>/backlog/*.md` (replaces confusing `backlog/open/`)
- ✅ Sprint folders simplified: `backlog/` → `implement/` → `done/` (+ `blocked`)
- ✅ Legacy folders (`analyze`, `plan`, `design`, `qa`, `review`, `reuse`, `open`) auto-migrated on `./studio sprint`
- ✅ `./studio sprint` writes **scope proposal** — does not tag tickets until human approves
- ✅ `./studio sprint <p> --approve-scope` — human gate before groom/implement
- ✅ Immature tickets flagged in `scope-proposal.md` + `planning-questions.md` (stay in product backlog)
- ✅ Docs: [backlog-model.md](.quinsy-studio/process/backlog-model.md)

## [1.7.2] — 2026-08-20

### Feedback dedupe, backlog-first tickets, sprint planning maturity

- ✅ `./studio feedback` dedupes similar items per sprint (`--force` to override)
- ✅ `--from-feedback` tickets go to **backlog without sprint tag**; `./studio sprint` assigns mature tickets
- ✅ Sprint planning prioritizes feedback-sourced backlog tickets; defers immature with `planning-questions.md`
- ✅ Groom validation: `IMMATURE_TICKET` when acceptance criteria are too generic
- ✅ Docs: feedback → backlog → sprint planning flow in [human-in-the-loop.md](.quinsy-studio/process/human-in-the-loop.md)

## [1.7.1] — 2026-08-20

### Sprint review feedback — capture only, never implement

- ✅ `./studio guard` returns `feedback_only` during sprint review for product/polish requests
- ✅ `./studio feedback` warns: do NOT implement mid-review — clarify → ticket → next sprint
- ✅ `./studio repo <p> link <url>` — link project git remote (project world)
- ✅ Docs + resume: explicit rule — review feedback is backlog-only until next sprint

## [1.7.0] — 2026-08-20

### Sprint review boundary (autonomous execution)

- ✅ **Mid-sprint:** agent implements all groomed sprint tickets without human checkpoints
- ✅ **Sprint review:** human involvement when all sprint tickets are `done` (`./studio review` → `--approve`)
- ✅ **Blocked:** `./studio move … implement` during review pending or after review until next sprint
- ✅ **Blocked:** `./studio sprint` until review approved + retro complete
- ✅ `./studio guard` returns `sprint_review` / `sprint_closed` for direction-change requests mid-sprint
- ✅ `./studio resume` and focus banner show autonomous vs review-pending mode
- ✅ Docs: [human-in-the-loop.md](.quinsy-studio/process/human-in-the-loop.md), [iterative-delivery.md](.quinsy-studio/process/iterative-delivery.md), [AGENTS.md](AGENTS.md)

## [1.6.0] — 2026-08-20

### Sprint human-in-the-loop (review, feedback, clarify)

- ✅ `./studio review <p>` — sprint review brief (`sprints/SPRINT-NN/review.md`); `--approve` / `--reject`
- ✅ `./studio feedback <p> "..."` — capture raw human feedback (not a ticket)
- ✅ `./studio clarify <p> FB-001` — clarify feedback → executable draft; `--approve`
- ✅ `./studio ticket <p> "..." --from-feedback FB-001` — ticket only after clarification
- ✅ `./studio feedback-list <p>` — feedback queue status
- ✅ `./studio retro <p>` — project sprint `retro.md` (was studio meta-retro only)
- ✅ `./studio resume` surfaces **sprint review pending** when all sprint tickets are done
- ✅ `sprint_hitl.py` + docs: [human-in-the-loop.md](.quinsy-studio/process/human-in-the-loop.md), [iterative-delivery.md](.quinsy-studio/process/iterative-delivery.md)

## [1.5.0] — 2026-08-20

### Pre-implementation: three human gates (0, 1, 2)

- ✅ Gate **0** — PRD + definitions approval before architecture
- ✅ Gate **1** — architecture blueprint (`docs/architecture/`, ADRs)
- ✅ Gate **2** — design (Next.js prototype, sticker sheet, tokens); **tickets generated here**
- ✅ `./studio blueprint`, `./studio design --scope journey|core-views`, `./studio revise`

### AI embedding & hardening

- ✅ [`AGENTS.md`](AGENTS.md) — IDE agent contract
- ✅ [`.cursor/rules/quinsy-studio.mdc`](.cursor/rules/quinsy-studio.mdc)
- ✅ `./studio bootstrap`, `./studio focus`, `./studio resume`, `./studio guard`, `./studio verify-worlds`
- ✅ [process/worlds.md](.quinsy-studio/process/worlds.md), [process/agent-context.md](.quinsy-studio/process/agent-context.md)
- ✅ `projects/` + `intake/` gitignored; per-project `.git` on init

### Studio library system

- ✅ [library_registry.md](.quinsy-studio/studio-library/library_registry.md) + `library_registry.json`
- ✅ `./studio library list|pull|promote|suggest|promote-design`
- ✅ `promote-library` — UI tokens, atoms/molecules/organisms, page-types, sticker sheet; `--force` + version bump
- ✅ Functional stubs: auth, billing (Stripe/Lemon Squeezy), feature-gating, Button, comparison page-type
- ✅ Reuse warnings on `./studio move … done`; library-first hint on `implement`

## [1.4.0] — 2026-08-20

### Workflow & tooling (summary)

- ✅ Unified ticket IDs, skill_matcher, intake fail-fast, init merge
- ✅ Sprint auto-assign, board columns, German PRD intake
- ✅ E2E reference flow documented

## [1.3.0] — 2026-08-20

### Strict Ticket Architecture (Project + Studio Level)

Tickets were too vague (one sentence + flat checkboxes). New schema for ALL tickets:

- ✅ **Role Assignment:** `assignee_role` (Director-level) derived from skills (e.g., Login → Backend Architect (Director))
- ✅ **Context & Value:** Current state vs. desired state instead of vague problem description
- ✅ **Strict Constraints:** Exact modification paths, rules (no external packages without ADR), mandatory playbook reference
- ✅ **BDD Acceptance Criteria:** Given / When / Then instead of implementation description
- ✅ **Definition of Done:** Measurable completion criteria

#### Implementation
- ✅ `ticket_helpers.py` (new) — shared schema: skill→role mapping, playbook mapping, BDD builder, markdown renderer
- ✅ `generate_ticket_manifest.py` — setup tickets + feature tickets with new schema; ID collision fix retained
- ✅ `studio.py` — `cmd_ticket` (project) + `cmd_learn` (studio, type `studio-evolution`) on new schema
- ✅ `ticket_template.md` — template with role, current/desired state, constraints, BDD, DoD

#### Bugfixes (found through schema testing)
- ✅ Feature extraction: `(.+?)` regex matched only 1 character → name was discarded (now: colon split)
- ✅ Template placeholders (`_Not yet defined_`) were extracted as features → filtered out
- ✅ `{project}`/`{signal}` placeholders in f-strings were not resolved

## [1.2.0] — 2026-08-20

### External Skill Sources Expanded (Skill Package Manager)
- ✅ 4 new verified sources: `coreyhaines31/marketingskills` (49 skills incl. ai-seo/AEO), `gamedev-skills/awesome-gamedev-agent-skills` (67 skills + router), `samir-abis/cookiecomply-skills` (GDPR), `bloomprotocol/agent-visibility-skill` (GEO)
- ✅ `skill-dependencies.json` expanded to 7 domains, all imported (29 external skill sources on disk)
- ✅ Skill registry: new sources + targeted skill mappings (ai-seo→GM-002, cookiecomply→CL-002, seo-audit→GM-001, ...) + `game` archetype

### External Skills Integrated into Teams
- ✅ AEO (GM-002): ai-seo, schema, geo_visibility, competitors
- ✅ SEO (GM-001): seo-audit, programmatic-seo, site-architecture
- ✅ Design System (FE-002) + UI Components (FE-001): hallmark, design_awesome
- ✅ Cookie Banner (CL-002): cookiecomply
- ✅ Content (GM-003): copywriting, product-marketing, customer-research
- ✅ Database (BE-002): database-schema-design, query-optimization
- ✅ Security (PE-003): security-audit, threat-modeling, SAST/DAST

### Skill Matching Test
- ✅ `test_skill_matching.py` — 7 sample tickets → internal + external skills, verified sources on disk
- ✅ New internal skill GM-004 (Game Development) with gamedev router trigger
- ✅ Result: 7/7 tickets matched, 29/29 external sources verified
- ✅ Learning item LO-0001 (game-dev gap) as proof of the learning loop

## [1.1.0] — 2026-08-20

### Folder Consolidation (everything under .quinsy-studio/)
- ✅ `studio-library/` → `.quinsy-studio/studio-library/` (paths in studio.py, sync_global_assets.py updated)
- ✅ `templates/docker/` → `.quinsy-studio/studio-templates/docker/` (base Docker template)
- ✅ Orphaned `studio-tools/` (old studio.py) and empty `templates/` removed
- ✅ `studio` wrapper remains as CLI entry point (delegates to .quinsy-studio/studio-tools/)

### Docker Base Template (Base → Project)
- ✅ `.quinsy-studio/studio-templates/docker/` with docker-compose.yml, .env.example, README
- ✅ `./studio env <project> init` copies template to project folder and parameterizes `{{PROJECT_NAME}}`
- ✅ `init_project_env.py` also uses the template (no more hardcoded values)

### Skill Package Manager (External Skills)
- ✅ `.quinsy-studio/skill-dependencies.json` — subscribed sources (hallmark, awesome-design-skills, awesome-ai-agent-skills)
- ✅ `import_external_skills.py` — imports skills via git clone to `.quinsy-studio/external-skills/`
- ✅ `./studio update-skills` — command for subscribing/updating
- ✅ Skill registry extended with external skills mapping (domain → team → skill)

## [1.0.0] — 2026-08-20

### Complete Studio System Rebuild

After a complete loss of all studio files, the entire system was rebuilt from scratch.

#### Process Documents (.quinsy-studio/process/)
- ✅ `lifecycle.md` — 8-phase lifecycle
- ✅ `gates.md` — Detailed gate definitions
- ✅ `adr-policy.md` — ADR rules
- ✅ `anti-slop.md` — Anti-slop audit
- ✅ `ticket-workflow.md` — 9-step ticket workflow
- ✅ `iterative-delivery.md` — Sprint/Grooming/Board
- ✅ `human-in-the-loop.md` — HITL decisions
- ✅ `project-archetypes.md` — Project archetypes

#### Team Skills (.quinsy-studio/teams/)
- ✅ `01-frontend-experience/` — UI/UX, Design System, Performance
- ✅ `02-backend-systems/` — API, Databases, Auth
- ✅ `03-compliance-legal/` — GDPR, Data Protection, Imprint
- ✅ `04-product-strategy-architecture/` — Strategy, Architecture, ADRs
- ✅ `05-growth-marketing-content/` — SEO, AEO, Content, Growth
- ✅ `06-product-management-operating-model/` — PM, User Research, Roadmap
- ✅ `07-ai-autonomous-systems/` — AI Integration, Anti-Slop, Automation
- ✅ `08-platform-enterprise-engineering/` — Infrastructure, DevOps, Security

#### Studio CLI (studio-tools/)
- ✅ `studio.py` — Python CLI with all commands
- ✅ `./studio` — Wrapper script

**Commands:**
- `./studio status <project>`
- `./studio gate <project> [--level N] [--anti-slop]`
- `./studio adr <project> "<title>"`
- `./studio ticket <project> "<title>"`
- `./studio board <project>`
- `./studio move <project> <id> <status>`
- `./studio sprint <project>`
- `./studio groom <project>`
- `./studio set-phase <project> <phase> --gate <n>`
- `./studio decide <project> "<title>"`
- `./studio decisions <project>`
- `./studio env <project> init|up|down|status|logs`
- `./studio repo <project> create|status`
- `./studio learn "<title>" --signal <s>`
- `./studio learn-list`
- `./studio retro <project>`
- `./studio promote <project> <asset>`
- `./studio init <project> --archetype <type>`

#### Studio Library (studio-library/)
- ✅ `ui/tokens/` — Design tokens (JSON, CSS)
- ✅ `ui/components/button/` — Button component
- ✅ `ui/page-types/comparison/` — Comparison page type
- ✅ `packages/auth/` — Authentication
- ✅ `packages/billing/` — Billing
- ✅ `packages/feature-gating/` — Feature flags
- ✅ `manifest.json` — Asset registry

#### Templates
- ✅ `templates/docker/` — Docker Compose + .env

---

## Status

**System Status:** ✅ Operational
**Version:** 1.0.0
**Last Updated:** 2026-08-20

---

## Known Limitations

- Anti-slop audit is still a stub (no real code analysis)
- Docker commands are not yet fully implemented
- GitHub integration (gh CLI) not yet connected
