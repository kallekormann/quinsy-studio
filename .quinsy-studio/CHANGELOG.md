## 2026-10-13 — The manual is the reference

`.quinsy-studio/docs/` now covers the concept, the three loops (reason, input, output), the product loop and its gates, studio learning and why a training chat exists, every command, and all eleven teams with their skills. The repo README, `.quinsy-studio/README.md`, and Getting Started point at those chapters. The process specs stay where the agent reads them.

## 2026-10-13 — User manual

`.quinsy-studio/docs/` is the book: setup, the three loops, how to bind a Cursor chat without looking up an id, the path from a direction to a studio lesson, what each command does, and what to do when the agent stops. The repo README, Getting Started, the operations manual, and the studio overview point at it.

## 2026-10-13 — Cursor session bind for one window, many products

HQ `runtime: cursor` is the switch. Each Cursor chat binds one product. Claude Code and the CLI keep workspace focus isolation.

### Added

- **`./studio bind <project> --session <id>`** (`studio_agent_sessions.py`). The id is Cursor's `conversation_id` (`session_id` on `sessionStart` is the same value). `--show` and `--clear` are per session. A non-cursor HQ runtime refuses and writes nothing.
- **Leases** record `session_id`. A second session cannot execute a product the first session already holds. Two sessions can execute two products. A bound Cursor `execute` / `focus` does not rewrite the sibling block in `.cursorignore`.
- **Hooks** `.cursor/hooks.json` and `.cursor/hooks/session_bind.py`: deny sibling reads and sibling `git` for a bound chat, deny `.env` / `.pem`, inject `--session` onto `./studio bind|execute|guard|focus`. When HQ runtime is not `cursor`, every hook allows the call. `sessionStart` tells an unbound chat to bind and does not guess a project.
- **Guard** returns `SESSION_BOUND` when the named project is not this chat's binding. `verify-worlds` checks the hook files exist and does not re-hide siblings while runtime is `cursor`.

## 2026-10-13 — Opened HQ epic: session-scoped binding (not built yet)

Same-window multi-product work still shares one `.cursorignore` and one active project. The fix is specified, not implemented.

### Added

- **Epic** `process/hq-session-binding.md`. Tickets `LO-0419`–`LO-0424` in `backlog/open/`: record the Cursor hook session id, `./studio bind`, session leases that do not rewrite global isolation, deny hooks for sibling reads and git, guard + manuals, then a two-session dry run. Cursor only — the switch is HQ `runtime: cursor` in `.quinsy-studio/studio.settings.yaml`, not a new key. Claude Code and the CLI keep today's `focus` / `execute` isolation. If the hook payload has no stable session id, multi-project mode stays off.

## 2026-10-13 — Interactive design mocks: always a running prototype

A design mock is now an interactive prototype in the product app, not a folder of screenshots. The human reviews the running route; the implementation sprint ports the mock code.

### Added

- **Interactivity gate.** `design_mocks_interactive_error` (design_ticket_helpers): approve-design refuses mocks without a `'use client'` page with wired handlers, without scenario states reachable in the running route (`?state=` / `useSearchParams` / `data-state` / `mock-scenario-panel`), or — when §2d is not `motion: off` — without wired transitions. Static per-state frames fail.
- **`mock-scenario-panel`** studio-library primitive (`ui/components/mock-scenario-panel/`): dev-only floating state switcher driven by `?state=`, so the human clicks through scenario states and Playwright captures each state by URL. Registered in manifest and registry.
- **Spec §2e Interaction walkthrough** (design-spec-template): the review script — mock route URL plus ordered `do X → expect Y` steps (3 minimum, naming §2d transitions). Checked by `design_spec_interaction_walkthrough_error`.
- **`./studio mock <p> <T>`**: verifies the interactive mock packet and prints the review script (dev-server hint, route URLs with `?state=` variants, §2e walkthrough). `approve-design` prints the same block before the signature — the human reviews the running route, screenshots are the record.
- **Handoff.** The execute IMPLEMENT CARD on a ticket with a signed design adds the mock route dir + spec to READ and informs that the mock code is the reference implementation (port interactions, transitions, wiring — do not rebuild from screenshots). The UX-009 finish gate gains a `## Behavior` table: every §2e step run on the shipped surface against the signed mock route; a missing table or a HOLD row blocks PASS (`qa_review.py`).

### Changed

- Design CARDs, `design_deliverables_status`, `design_playbook.md`, `ticket-team-allocation.md`, UX-005 / UX-009 / UX-001 skills, `AGENTS.md`, `.cursor/rules/quinsy-studio.mdc`: mocks are interactive prototypes; screenshots are the record, never the deliverable.
- Tests: interactivity gate, walkthrough checker, finish-gate behavior rows (`test_design_ticket_helpers.py`, `test_design_loop.py`).

## 2026-10-13 — HQ autonomy program: PM, Engineering, Design, Growth (LO-0395 … LO-0418)

The human now stops on product and design decisions and on irreversible production steps. Everything else runs from the agent seat and INFORMs. Program: `process/hq-autonomy-program.md`. Matrix: `process/human-in-the-loop.md#when-is-hitl-needed`.

### Added

- **Milestones (PM).** `knowledge-base/milestone-coverage-checklist.md` (21 areas, when each is required, owner skills) and `studio-templates/phases/milestone.md`. `./studio milestone <p> plan|review|approve|list` writes the active milestone's tickets, writes `docs/phases/M<n>-review.md` when every ticket is done, and lets the human re-plan, re-order, or open a design sprint before the next milestone. `approve --milestones` refuses roadmaps with coverage gaps; `sprint` refuses without an approved roadmap and active milestone. Execute carries a PM CARD (PM-002, PM-004, PS-002) at roadmap and milestone boundaries. PM-002 rewritten to the skill template.
- **Done bar (Engineering).** `move … done` runs the full bar on every ticket and refuses a ticket whose sprint does not match. UI tickets make `skill_application` a hard check; a new `ui_motion` level-5 check requires §2d motion tokens and a `prefers-reduced-motion` path in product UI and fails a second animation layer (`gate_ui_checks.py`). QA verdicts carry `Reviewer: <id>` that must differ from the implementing context (`./studio whoami`, `implement-start` event). Receipts list every CARD skill file and playbook under `## Skills read` with the rule applied; a file not on the CARD or a blank rule fails. Reality check `NEEDS WORK` files bug tickets instead of asking.
- **Production path (Engineering).** `studio-templates/docker/compose.prod.yml` (no data ports, restart, bounded logs, built image, migrate before start, healthcheck) is copied by `env init`. `./studio ops <p> readiness|deploy|logs|status|migrate --prod|db|cleanup [--dry-run]` with one log line per run in `docs/ops/ops-log.md`; only `migrate --prod --approve`, `db --reset`, `cleanup --prune-volumes` wait for the human. `env.schema.json` gains the `prod` group (`VPS_SSH_HOST`, `VPS_SSH_USER`, `VPS_SSH_KEY_PATH`, `VPS_COMPOSE_DIR`, `COOLIFY_URL`, `COOLIFY_TOKEN`, `COOLIFY_APP_UUID`, `PROD_DATABASE_URL`) stored in gitignored `projects/<p>/.env.local`; `./studio env <p> prod --explain` tells the human which names to fill and what each does, without ever printing a value. `ship --to main` refuses on a readiness FAIL. PE-001, PE-007, BE-002 updated.
- **Design loop (Design).** `approve-design <p> <T> --reject --reason hierarchy|density|motion|copy|flow|uniqueness|a11y|brand`, `feedback`/`clarify --design-reason <code>`, and a finish-gate HOLD (`Reason:` line) write `docs/design-specs/pushback-log.md` and harvest into `knowledge-base/learnings/design/` (`design_feedback.py`; new topics `interaction.md`, `craft.md`; harvest kind `craft`). Retro gets a `## Design` section with counts per code. Design specs need `## 7b. Catalog applied` with PB-/LO- ids (or `catalog: none` with a reason). UX-001, UX-002, UX-003, UX-004, UX-005, UX-006, UX-008 rewritten to the skill template; UX-006/008/009 load their playbooks.
- **Growth.** Skills GD-004 In-product growth loops (`teams/11-growth-design/skills/in-product-growth-loops.md`) and GM-007 Positioning & messaging (`teams/05-growth-marketing-content/skills/positioning-messaging.md`), registered in matcher, roles, playbooks, registry; staffing adds GM-007 on commercial surfaces and proposes GD-004 on signup/share/invite/upgrade flows. `docs/definitions/12-positioning.md` is a gate-0 requirement; `02-personas.md` is a task-segment table; the PRD template gains a Positioning section. `knowledge-base/growth-content-playbook.md`; in-product loops section in `growth-mechanics-playbook.md`; Payload content-engine collections in `payload-playbook.md`; templates `studio-templates/growth/growth-loop-map.md`, `persona-page-set.md`, `seo-foundation-pack.md`, `content-engine-pack.md`; anti-slop rule 2.4 (feature-list pages are slop).
- **Autonomy.** `approve-arch --phase` and per-ticket `approve-arch` are agent-signed VERIFY steps with a tech-veto window. Cadence review is `./studio review <p> --inform`: the brief is written, the stop closes, feedback arrives through `feedback`/`clarify`. Local `env up|migrate|dev` runs without `--approve` (accepted as a no-op). Guard classifies HQ work that mentions ideation as `STUDIO_META`, not `IDEATE`. `verify-worlds` checks loop separation (`loop_separation_issues`: `.gitignore` lists `projects/`, `intake/`, `ideation/`; no build folders in `ideation/`; no HQ or desk folders inside a product; no product or desk folders inside HQ).

### Changed

- Human stops are gates 0/1/2a/2b, milestone roadmap and reviews, `approve-design --phase`, `ship --to main --approve`, production migration and destructive data steps, tech-veto, abort. `AGENTS.md`, `CLAUDE.md`, `.cursor/rules/quinsy-studio.mdc`, `README.md`, `GETTING_STARTED.md`, `process/studio-overview.md`, `process/human-in-the-loop.md` say so.
- Tests: `test_studio_milestones.py`, `test_done_bar.py`, `test_studio_ops.py`, `test_design_feedback.py`, `test_growth_skills.py`, `test_hq_autonomy.py`; cadence and env tests assert the INFORM contract.

## 2026-10-13 — HQ holds no product references; gate-2b mocks land in the Payload app

### Fixed

- **Gate 2b materialize on Payload projects.** `materialize_baseline` copied the signed mock pages into a stray `projects/<p>/app/`. It now prefers `apps/web/src/app/(app)/` when `apps/web/package.json` exists. `design/prototype/` stays as the reference that `docs/design/baseline.md` names.

### Changed

- **No product references anywhere studio git commits.** `verify-abstraction` scans every tracked and untracked-but-not-ignored file outside `projects/`, `intake/` and `ideation/`, every text suffix, with no provenance exemption. It matches product folder names, including names glued to hyphens (`--name`, `name-spark`), and product ticket IDs (first four letters of the folder, uppercased). Policy: `process/studio-abstraction.md`.
- **Provenance stays in the product.** Harvest, `library promote` and `sync_global_assets` no longer write the source project or ticket into the learnings inbox, `manifest.json`, titles or CHANGELOGs. The product's own `docs/library-promotions.json` keeps that record. Existing manifest fields, inbox Source lines and playbook Signal lines were stripped.
- **Product surface names** come from a product-local `docs/portability-nouns.txt` instead of a list in HQ code. Vendored folders the anti-slop gate should skip go in the product's `docs/anti-slop-ignore.txt`; the hard-coded product folder ignore is gone.
- Examples, help text and tests use `demo` / `DEMO-0001` or `acme-app` instead of real products.
- **`design-md-repo`**: the default system is `soft-ui`. The product brand system is removed.
- **Library assets made neutral.** `canvas-export` watermark falls back to `Preview`; products pass their name as `text`. `sendMailpitEmail` takes `fromName`. `celebration` class and attribute names are `celebration-*`. `AvatarStack` uses `--accent-secondary`. Ticket IDs and brand names are gone from component comments, and `ui/docs/shadcn-coverage.md` is rewritten against shadcn only.

### Removed

- `studio-library/packages/capture-types/` and `studio-library/ui/components/emotion-strip/` (one product's domain types and chrome). Products that pulled them keep their copies.

## 2026-10-13 — Agency integration closed: launch pack, CLI rules, bloomprotocol retired (LO-0391, LO-0392, LO-0393)

### Added

- **Launch playbook** (`knowledge-base/launch-playbook.md`): when a launch exists, the T-21 to T+7 timeline, and what the studio enforces. Templates `studio-templates/growth/launch-plan.md` and `launch-ticket-pack.md` give eight staffed launch tickets (plan, landing page, waitlist, analytics, lifecycle email, legal review, pre-ship, results). GM-005 loads the playbook with marketing-law. `test_launch_pack.py` runs every draft through PM-004 staffing, so the pack cannot drift from the staffing rules.
- **CLI rules for `./studio`** in SO-001 rule 4: help line in both help blocks, exit code 1 on refusal, refusals name the next command, no prompts, `execute` output is a contract, idempotent writes, secrets as names only, two worlds, pass and fail fixtures for every check. `test_cli_help.py` checks that every dispatched command has help in both blocks and every help line has a handler.
- LO-0394: migrate the 47 skill files that still warn on template sections.

### Changed

- **Staffing:** "UTM register" and "risk register" no longer trigger the account-registration companions (PE-003, CL-001).
- **Help:** `decisions` and `update-skills` were missing from the module help in `studio.py`.

### Removed

- **bloomprotocol `agent-visibility-skill`** (`geo_visibility`). It bundled an MCP server for paid agent missions with wallet provisioning and sent URLs to a third-party API. GM-002 already owns llms.txt, crawler policy and the citation audit. Removed from `skill-dependencies.json`, README, matcher, registry and GM-002; the conflict matrix keeps a "retired" note.

S5 (LO-0391) was verified complete: BE-008, BE-009, FE-008, the BE-007 admin layout, the private-page caching rule, BE-002 reliability, BE-003 identity and the AI-001/AI-004 cost rules were all in place.

## 2026-10-13 — Design workflow: imagery rules, must-fail microcopy, clarify fields (LO-0390)

### Changed

- **UX-007 Visual Storyteller** is rewritten to the skill template and gains generated-imagery rules. Every image has a job and a brief in spec §5 `### Imagery`. People in images match the PRD personas and are never given names or quotes, because a generated customer is a fake testimonial. Product screens are captures of the running app, never generated. Words are never baked into a generated image. Every image is logged in `docs/design-specs/imagery.md` with source, licence or model, alt text, and the AI label required by EU AI Act Art. 50(4). New triggers: hero image, illustration, imagery, generated image, OG image, stock photo.
- **Anti-slop gate**: microcopy is now a gate **error**, not a warning. It fails whimsy interjections, "magic" wait copy, forced praise, celebration emoji, and error lines that break the UX-002 rubric, in English and German. A spec line that quotes a bad example as a rule is skipped. Playbook §2.2b lists the patterns.
- **`./studio clarify`** takes `--severity blocker|major|minor|polish` (required before `--approve`) and `--verbatim "..."`. The human's words stay unedited, separate from the agent's reading of them. Recurring feedback from earlier sprints is found automatically and listed. A ticket made from feedback carries the quotes, severity and recurrence, and severity sets its priority (P0–P3) unless one was given.

### Added

- `studio-tools/fixtures/anti-slop/microcopy-must-fail.txt` and `microcopy-must-pass.txt`; tests `test_anti_slop_microcopy.py`, `test_feedback_clarify.py`.

## 2026-10-12 — Trustworthy done bar: receipts, QA review, security and quality checks, finish gate, reality check (LO-0387–LO-0389)

Rows L1–L14 of `process/hq-agency-agents-integration.md`.

### Changed

- **Receipts (L1, L6).** Untouched stub text counts as empty. Every result line under Skill QA, A11y, API proof and Evidence is PASS, FAIL or NOT TESTED; FAIL blocks done, NOT TESTED needs a reason, PASS needs a path or a command. Cited files in AC coverage, Evidence, API proof and citations must exist, and so must every screenshot. The stub only adds the sections the ticket needs: Security and Scope always, Evidence and A11y on UI, API proof for BE-001/003/007, Threat delta for PE-005, Risk & rollback for migrations, auth and infra.
- **Gate (L4, L5).** Smoke without `smoke-routes.json`, or with `QUINSY_SKIP_SMOKE`, reports NOT TESTED instead of passing. Level 2 adds `secret_scan`, `client_env_leak`, `insecure_env_fallback` and `docker_secret_leak`. Level 5 adds `payload_access`, `local_api_override`, `webhook_signature`, `npm_audit_policy`, `a11y_axe`, `e2e_hygiene` and `api_contract`; `llm_sink`, `sensitive_log`, `security_headers` and `perf_budget` warn. `.env` files are never opened. A finding is waived only by a row in `docs/security/exceptions.md` with an expiry date.
- **Failure loop (L3).** The debug file is Issue / Expected / Actual / Evidence / Fix / Files, and the next attempt fixes only those. Red gates, QA FAILs and finish-gate HOLDs share 3 attempts; two identical failures escalate early. Escalation writes `sprints/SPRINT-NN/escalations/<T>.md` and moves the ticket to `blocked`; siblings continue. The human is asked only when every remaining ticket is blocked.
- **Architecture (L7, L8).** Gate 1 needs `threat-model.md` (System, Data map, Trust boundaries, STRIDE, Requirements, Tenant model, Change log), `data-map.md`, `secrets-inventory.md` and `docs/workflows/REGISTRY.md`. An architecture packet cannot claim `threat delta: none` when it touches a webhook, upload, endpoint, role, tenant, job or collection. A flow ticket links a `WORKFLOW-*.md` with TC-nn cases and cites one.
- **Design packets (L9).** `approve-design` needs a five-second test at 390 and 1440 on every packet, and the GD-003 persona walkthrough appendix on commercial ones. The design-spec template has the table.
- **Gate 0 (L10).** `prd.md` ends with `## Gate 0 frame`: press release, non-goals, a Metric / Baseline / Target / Window table (`unknown` allowed, blanks not, at least one target) and a three-reason pre-mortem. Only the frame block counts, not headings inside inlined source files.
- **`ship --to main` (L12)** refuses on a secret in git history, an incomplete secrets inventory, a missing `docs/ops/incident-runbook.md`, an expired security exception, or a database port not bound to `127.0.0.1`.
- **Retro (L14).** `retro.md` opens with loop metrics from `execution-log.json`: first-pass gate rate overall and per failing check, average retries, QA fails, finish holds and blocked tickets.
- Templates: the Payload app ships a `.dockerignore` and security headers (CSP, HSTS, nosniff, Referrer-Policy, frame and permissions policy); the Docker compose template binds ports to `127.0.0.1`.

### Added

- `./studio qa <p> <T> [--verdict PASS|FAIL]` (L2): execute step `QA_REVIEW` after a green gate. A fresh-context reviewer writes `sprints/SPRINT-NN/qa/<T>.md`, defaulting to FAIL without proof. Move done refuses without a QA PASS after the last green gate.
- `./studio qa <p> <T> --finish [PASS|HOLD]` (L9): the UX-009 finish gate on tickets with signed mock shots. `qa/<T>-finish-gate.md` compares every mock state with a shipped capture at 1440 and 390, with a Keep list; HOLD is a QA fail.
- `./studio reality-check <p>` (L11): execute step `REALITY_CHECK` after `ship --to dev` and before the cadence review, tied to the commit SHA. FAILED files bug tickets and keeps building instead of asking for sign-off.
- `./studio lint-skills [--strict]` (L13) and `knowledge-base/skill-template.md`. Drift between `skill_matcher`, `SKILL_ROLE_MAP`, the skill files, team prefixes, staffing rules and `skill-registry.md` is an error; missing template sections warn (48 older skill files today).
- Modules `receipt_checks`, `qa_review`, `security_checks`, `quality_checks`, `architecture_checks`, `ship_checks`, `reality_check`, `retro_metrics`, `lint_skills`; tests `test_loop_trust`, `test_security_gate`, `test_design_loop`.

## 2026-10-12 — Ticket staffing (PM-004); 13 new skills from the agency-agents review

### Changed

- Skill triggers match whole words. Short triggers must stand alone, so `ai` no longer hits `email`, `detail` or `main`, `test` no longer hits `latest`, and `form` no longer hits `format`. Noisy triggers were narrowed (PE-002 `build`, PS-004 `scope`, GM-003 `content`).
- The Product Manager staffs every ticket (PM-004). `./studio ticket` adds companion skills from the ticket text and writes `## Staffing` with a reason for each. `./studio groom` treats `SKILLS_MISSING`, `SKILL_UNKNOWN` and `STAFFING_GAP` as errors; `STAFFING_SUGGEST` is info. The required companions are PE-003 + AI-005 (auth, access, tenants, uploads, webhooks, keys), CL-001 (personal data), CL-002 (tracking), PE-006 (secrets), BE-008 + CL-003 (payments), GM-006 (marketing email), and FE-004 + FE-006 (UI). Waive one with `staffing_waive:` and a reason. A ticket carries at most eight skills.
- The execute CARD lists the **skill files** to read, not only team playbooks, and adds a required companion the ticket lacks (`staffed by PM-004`).
- Billing package (`studio-library/packages/billing`): Stripe webhooks refuse a signature timestamp more than 300 s off and accept any `v1` value (key rotation). `createCheckout(planId, email, userId)` sends the Payload user ID (`client_reference_id` / `metadata.user_id`, Lemon Squeezy `custom.user_id`). The README no longer documents a `subscription`/`metering` API that does not exist.
- Skill rewrites:
  - FE-003, FE-004 (BFSG / EN 301 549) and FE-006 rewritten.
  - BE-001 and BE-004 share one error shape. BE-002 drops its Supabase leftovers. BE-003 follows NIST SP 800-63B.
  - PE-001 gets a Coolify/VPS posture checklist. PE-002 uses forward-fix migrations. PE-003 gets a PASS/FAIL/N/A catalog.
  - CL-003 citations updated (§ 18(2) MStV, § 5 DDG). CL-001 gets DPIA and breach decisions. CL-004 gets a data map.
  - GM-001 no longer promises FAQ rich results. GM-002 adds a crawler policy and `llms.txt`.
  - GD-001 adds sample size. GD-002 adds PAngV. UX-002 adds an error-message rubric.
  - The Payload notes and AI-001/AI-004 get updates.
- The archetype table now uses the Payload stack and PWA-first mobile. The Payload playbook notes the Postgres adapter, no caching of private pages, and AI-005 checks.

### Added

- Skills: FE-008 i18n, BE-008 payments and billing, BE-009 document generation, GM-005 launch and community, GM-006 lifecycle email, PM-004 ticket staffing, AI-005 AI-code security audit, PE-005 threat modeling, PE-006 secrets hygiene, PE-007 incident and breach response, SO-005 release reality check, UX-009 UI finish gate, GD-003 persona walkthrough. UX-008 is registered for matching (64 skills).
- `knowledge-base/skill-extensions/marketing-law.md` (UWG, TDDDG § 25, PAngV § 11, reviews, influencer disclosure).
- `test_staffing.py`: trigger matching, companions, groom findings, and every ID has a role and a skill file.

## 2026-10-12 — Real-UI design mocks; agency-agents integration plan

### Changed

- Design mocks must be the real app. A mock is a route in the product app at `app/(design-mocks)/design-mocks/<TICKET>/<state>/page.tsx` that imports the real shell or view and real components, with the design solution woven in. `(design-mocks)/layout.tsx` returns 404 in production. Screenshots of every state, newer than the mock code, go in `docs/design-specs/mocks/<TICKET>/`.
- `approve-design` refuses standalone HTML mocks, mocks without app or shell imports, inline styles, hex or arbitrary colours, and missing or stale screenshots (`design_ticket_helpers.design_mocks_real_ui_error`). The design-spec stub writes the production guard layout.
- Design-spec template §2c, Team 10 README and anti-slop skill, design playbook, compliance checklist, component-creation playbook, motion extension, GETTING_STARTED, human-in-the-loop, AGENTS.md, and the Cursor rule describe real-UI mocks.
- Payload template: `Users` access is admin-or-self with an admin-only `role` field; the first user becomes admin; login lockout. `Media` needs a login. `PAYLOAD_SECRET`, `DATABASE_URL`, and S3 keys fail loudly instead of falling back to `''`, except during `next build`.

### Added

- `process/hq-agency-agents-integration.md`: review of the agency-agents repo by division, 12 new skill IDs, 14 loop changes, fixes, and sprints S0–S7 (`LO-0386` … `LO-0393`).

## 2026-10-12 — Compose `next dev`; MOVE_DONE arbitrary space

### Changed

- Prefer `next dev` in Compose for UI tickets when the app image can boot it. Production `build` + `start` with a named `.next` volume hides bind-mounted source until rebuild (`LO-0384`, `PB-20261012-001`).
- MOVE_DONE flags newly added `[Nrem]` / `[Npx]` classNames. Moving a line counts as added; use a scale utility or keep the original line unchanged (`LO-0385`).

## 2026-10-08 — UUID test keys; parked tickets stay out of implementation

### Changed

- Test helpers that stand in for primary keys must match the column type (UUID when the schema is UUID). Design-track and parked tickets stay out of an implementation sprint until that phase is open (`LO-0383`).

## 2026-10-08 — Hosted type and pipe tables in PDF

### Changed

- When HTML-to-PDF does not implement tables, parse pipe rows in the writer and draw cells (`LO-0381`, `PB-20261008-001`).
- Register every style of a custom PDF face. Host SIL webfonts in the product tree and reuse them in PDF export so a public page does not call a font CDN (`LO-0382`, `PB-20261008-002`).

## 2026-10-07 — A failed export is visible

### Changed

- A failed export shows a notice the member can see. A relationship list is done only when every row is a saved document, not a derived label (`LO-0380`).

## 2026-10-07 — Payload is the web foundation

### Changed

- A web blueprint says `Payload: in` or opts out in an ADR. After gate 1, execute writes `apps/web`. Local boot is Docker Desktop. Production is Coolify. Getting Started, the READMEs, and the playbooks describe that path.
- The Payload and CMS-migration skills are copied from payloadcms/skills. `./studio update-skills payload` refreshes that copy. The app image runs migrate, then the server, and registers S3 storage.
- Login for a new project is the Payload Users collection. `packages/auth` is not pullable. The login form posts to Payload.
- Intake keeps a file, a folder, or several files. The PRD indexes them and keeps the text. The milestone roadmap has as many versions as that material needs.

## 2026-10-07 — Two acceptance lines before a sprint

### Changed

- A behavior the review already specified should start with two concrete acceptance lines (`LO-0379`).

## 2026-10-07 — Dialog for a value, mock before a mark

### Changed

- A control that asks for a value uses the design-system dialog, not a browser prompt. A mark's look is signed in a mock before a build changes how that mark appears (`LO-0378`).

## 2026-10-05 — Close an approved design ticket

### Changed

- When a design ticket is approved, close it. A build ticket must not stay blocked on a design session that does not ship code (`LO-0377`).

## 2026-10-05 — A failed check still restores queued work

### Changed

- A test that marks ready work as queued restores that work when an assertion throws. The restore sits in a finally, not after the assertion (`LO-0376`).

## 2026-10-04 — A signed rail is the frame, and a deferred ticket stays deferred

### Changed

- Do not restyle a second side rail until that surface is signed. The signed rail's width, padding, surface, and left border are the frame (`LO-0373`).
- Leave a deferred ticket deferred. Do not pull that surface into the ticket that is open (`LO-0374`).
- A service the current sprint just built stays in that product until a second product needs it (`LO-0375`).

## 2026-10-04 — Domain services stay in the product

### Changed

- A service built in the current sprint stays in that product until a second product needs the same behavior (`LO-0372`).

## 2026-10-03 — Signed prototype on the first pass, and isolated requeue tests

### Changed

- When a signed prototype is the visual baseline, the first build uses that editor, those controls, and optional modules that start off (`LO-0370`).
- A requeue test uses the rows it created and restores any other rows it marked queued (`LO-0371`).

## 2026-10-02 — Motion skill is internal

### Changed

- Motion no longer depends on an external subscription. The skill is `knowledge-base/skill-extensions/motion-transitions.md`. Dialogs, menus, and tooltips scale with `--motion-scale-*` on open and close.
- `transitions_dev` is removed from `skill-dependencies.json`.

## 2026-10-02 — Motion is the default on UI specs and the studio kit

### Changed

- Subscribed [transitions.dev](https://github.com/Jakubantalik/transitions.dev/tree/main/skills) as `transitions_dev` for Teams 10 and 01. The doctrine is distilled into `knowledge-base/skill-extensions/motion-transitions.md`. The `t-*` recipe collection stays in the subscribed clone. It is not a second kit.
- Design specs need **§2d Motion** before approve-design. The only off switch is HITL `motion: off`, which sets project `--motion-duration-*` to `0ms`.
- Studio-library tokens and core controls (button, menus, dialog, sheet, tooltip, tabs, switch, checkbox, accordion, toast) use that scale so implementation does not re-time them per project.

## 2026-10-01 — Arbitrary Tailwind size classes on added diff lines (LO-0368)

### Changed

- UI receipts scan added `tsx`/`css` lines. Re-emitting an existing `text-[Npx]` className on a rewritten control fails the token check. Leave the original className line untouched, or use a scale class / token (`PB-20261001-001`).

## 2026-09-30 — Mixed-sprint architecture tags and design-spec iframes

### Changed

- Mixed-sprint architecture phase sign-off must not untag tickets that still need implementation (`PB-20260930-002`).
- Design-spec iframe catalogs need the product app listening; connection refused is a stopped server (`PB-20260930-001`).

## 2026-09-30 — Desktop env file and operator guides

### Changed

- `./studio env <p> up|migrate|dev --approve` injects gitignored `projects/<p>/.env`. A missing file is created from the schema plus `.env.example` and `docker/.env.example`. Existing values and comments stay. Production values stay in Coolify.
- Getting Started, both READMEs, and the agent how-tos now describe gates 2a and 2b and the design → architecture → implementation train.

## 2026-09-30 — Sprint phase train after gate 2b

### Changed

- After gate 2b, each cycle is a design phase, then an architecture phase, then an implementation phase. A phase with no tickets is skipped and does not open a sprint.
- Implementation scope accepts only tickets whose design and architecture are already signed. One unsigned ticket does not block a ready sibling.
- A design ticket names `architecture delta: none` or a ticket id before the phase can be signed. `./studio approve-arch <p> <TICKET> --reject` sends an infeasible design to the next cycle.

## 2026-09-30 — Implementation reuse, tokens, story, and receipt lines

### Changed

- UI move-done fails a second Popover, Tooltip, DropdownMenu, Dialog, or Button, a receipt that names no existing component or pulled slug, and a changed file that hardcodes a color or an off-scale space while project tokens exist. A missing role is a new semantic token, then `var(--role)`.
- Generic components carry a behavior contract (keyboard, focus, viewport, states, reduced motion, tokens). The app shell stays mounted; the content region may morph. Pattern: `studio-library/ui/docs/patterns/app-shell.md`.
- Marketing, workflow, and commercial composition specs need a filled `## 5. Story` (arc, one CTA, reduced-motion path) before approve-design.
- `## Design skill` and `## Architecture skill` cannot be `n/a` when the ticket is UI or includes API, auth, data, security, or infrastructure. The architecture section must cover separation, server authorization, parameterized queries, allow-listed bodies, idempotency, no stack traces, rate limit or internal-only, timeouts, structured logs, health checks, temp cleanup, and drift.

## 2026-09-30 — Design baseline and critique before HITL

### Changed

- Gate 2a requires one aesthetic preset as craft substrate plus a product delta, and a separate `design/DIRECTION-CRITIQUE.md`. Execute stays on IMPLEMENT while any rubric line is FAIL. The human signs the identity only after the critique passes.
- Gate 2b requires the studio-library base kit and a shell around the PRD journey (marketing, auth, settings, empty/loading/error). `internal-tool` skips marketing. `api-service` has no UI prototype.
- Approving gate 2b copies prototype mocks into the product app and leaves `design/prototype/` as the visual baseline. A silent rewrite of a pulled control fails move-to-done unless the receipt has an `Enhancement:` line.

## 2026-09-29 — Keep account settings on the existing settings surface (LO-0365)

### Changed

- Keep operator account settings on the existing authenticated settings surface. A later IA ticket that sounds like a new page is not a second settings product. Playbook: `knowledge-base/learnings/design/information-architecture.md` **PB-20260929-001**.



### Changed

- When reuse review flags files under a product `ui/components` kit, record them as project-local. Do not open a studio LO to copy token-bound molecules into studio-library. Playbook: `knowledge-base/learnings/library/components.md` **PB-20260929-001**.

## 2026-09-29 — Catalog AC must not infer design-track; one Postgres per working copy (LO-0361–LO-0362)

### Changed

- When a project has `docs/i18n.md`, catalog AC that mentions a UI string must not infer `ui-composition`. Ticket type stays explicit. Playbook: `knowledge-base/learnings/process/workflow.md` **LO-0361**. Classifier: `design_ticket_helpers.infer_ticket_type` strips that AC before matching `ui`.
- Do not run `supabase start` beside an existing Compose Postgres in the same working copy. Local session comes from the product API; `auth_user_id` hooks the hosted Auth `sub`. Playbook: `knowledge-base/learnings/backend/data.md` **LO-0362**.

## 2026-09-27 — Keep specifications, schemas, and gates portable (LO-0353–LO-0360)

### Changed

- A PRD rewrite must keep the original specification unchanged and must not drop normative details to fit a length cap. Playbook: `knowledge-base/learnings/process/workflow.md` **PB-20260927-001**.
- When a requirement needs a fact the schema cannot store, architecture must add that column instead of shipping the schema alone. Playbook: `knowledge-base/learnings/backend/data.md` **PB-20260927-001**.
- A SaaS blueprint must include a public marketing route group: home, use-case content files, and legal routes when copy comes later. Playbook: `knowledge-base/learnings/design/visual.md` **PB-20260927-001**.
- Subscription checkout must use hosted billing while the price id stays empty and must refuse checkout until that id exists. Playbook: `knowledge-base/learnings/library/packages.md` **PB-20260927-001**.
- A stack and host named in the PRD must win over the archetype default, and that delta must be an ADR. Playbook: `knowledge-base/learnings/process/workflow.md` **PB-20260927-002**.
- Execute leases must expire when the holder process is dead so focus is not blocked by a stale lease. Playbook: `knowledge-base/learnings/process/tooling.md` **PB-20260927-001**.
- Gate feedback must be a gate revision and must not be queued as a sprint inbox note while execute is waiting on a human gate. Playbook: `knowledge-base/learnings/process/workflow.md` **PB-20260927-003**.
- Keep the product UI kit in the product repository. Do not promote project look into studio-library. Playbook: `knowledge-base/learnings/library/packages.md` **PB-20260927-002**.

## 2026-09-27 — Verify vendor webhook signatures before any write (LO-0352)

### Changed

- Verify the provider signature on every vendor webhook before any write. A reachable endpoint is normal. An unsigned request must leave stored data unchanged. Playbook: `knowledge-base/learnings/backend/services.md` **PB-20260927-001**.

## 2026-09-26 — Keep the first marketing screen static (LO-0351)

### Changed

- Keep the first marketing screen static: claim, product visual, and primary CTA readable at rest. Do not pin a multi-viewport scroll film as the opening. Playbook: `knowledge-base/learnings/design/visual.md` **PB-20260926-001**.

## 2026-09-26 — Human design is 2a then 2b; project kit is the handoff (LO-0340–LO-0343)

### Changed

- Split human design into **2a** (discovery interview + signed `DESIGN.md`; blocks prototype) and **2b** (project CSS tokens, coded A/M/O, sticker inventory). `./studio approve --gate 2` is refused. Approving 2b does **not** promote product look into studio-library. Aesthetic presets are optional footnotes. Playbook: `knowledge-base/design-direction-playbook.md`.

## 2026-09-26 — Keep the feature inventory when replacing stacked mocks (LO-0350)

### Changed

- When collapsing stacked mocks into one composition, keep the feature inventory section. A single narrative frame is not permission to delete the inventory. Playbook: `knowledge-base/learnings/process/workflow.md` **PB-20260926-005**.

## 2026-09-26 — Do not `--approve-scope` blocked tickets (LO-0349)

### Changed

- Do not `--approve-scope` tickets that are blocked (unmet dependencies or not ready). Drop them from `proposed` before approve. Playbook: `knowledge-base/learnings/process/workflow.md` **PB-20260926-004**.

## 2026-09-26 — Keep public host routing on the original Host (LO-0348)

### Changed

- Keep public host routing on the original Host header without a path-prefix rewrite. Do not restyle a live public site from a docs-only ticket. Playbook: `knowledge-base/learnings/process/workflow.md` **PB-20260926-003**.

## 2026-09-26 — Keep operator nav and inbox on shipped chrome (LO-0347)

### Changed

- Keep operator nav and inbox work on the shipped chrome. Do not invent a second shell or an in-thread preview frame. Playbook: `knowledge-base/learnings/design/inbox.md` **PB-20260926-002**; skills UX-003 / FE-002.

## 2026-09-26 — Keep composition on the live layout-picker cards (LO-0346)

### Changed

- Keep layout and composition work on the live layout-picker cards. Do not invent a second block-list editor, a second intake inbox, or a one-off product-detail workbench. Playbook: `knowledge-base/learnings/design/inbox.md` **PB-20260926-001**; skills UX-003 / FE-002.

## 2026-09-26 — Do not groom a missing control onto a surface (LO-0345)

### Changed

- Do not groom a control-specific ticket onto a surface that does not already show that control. File a design-track ticket and get the packet signed before the control is in grooming. Playbook: `knowledge-base/learnings/process/workflow.md` **PB-20260926-002**.

## 2026-09-26 — `sprint: none` is unscheduled (LO-0344)

### Fixed

- Planning treats `sprint: none` (and empty) as no sprint tag, not as already assigned. Playbook: `knowledge-base/learnings/process/workflow.md` **PB-20260926-001**.



### Changed

- Ship the shared surface first. Inventory work is its own later ticket. A shell ticket depends only on the shell it renders. Playbook: `knowledge-base/learnings/process/workflow.md` **LO-0343**.

## 2026-09-25 — Off-cadence UI sprints can plan next after retro

### Fixed

- Skill-QA batches (cadence review not due) no longer require `./studio review --approve` before the next sprint. After retro `--complete`, execute proposes `./studio sprint`. Cadence `REVIEW_PENDING` still HITLs.

## 2026-09-25 — Layout sprints must not restyle public magazine chrome or auto-publish (LO-0342)

### Changed

- Layout and composition sprints must not restyle a tenant's public magazine, generate articles, merge properties, or auto-publish. Those actions need their own operator tickets. Playbook: `knowledge-base/learnings/process/workflow.md` **PB-20260925-002**.

## 2026-09-25 — HQ skill-catalog work stays off the product sprint inbox (LO-0341)

### Changed

- Route HQ skill-catalog jobs to the studio LO/train queue. Product execute INFORM the open HQ LO count and must not enqueue those notes on the product sprint inbox. Infuse in a HQ session; `STUDIO_LO` only when the product loop is idle. Playbook: `knowledge-base/learnings/backend/queues.md` **PB-20260925-001**; `knowledge-base/backend_playbook.md`; skills BE-001 / BE-004.

## 2026-09-25 — Command palette intercept is a live-proof gap (LO-0340)

### Changed

- Do not block MOVE_DONE when an IDE command palette steals the browser automation tab and unit contracts already cover the AC. Record the intercept; cite HTTP/API tests. Playbook: `knowledge-base/learnings/process/workflow.md` **PB-20260925-001**.

## 2026-09-24 — `--help` is a flag, not a project

### Fixed

- `./studio gate --help` and `./studio retro --help` print usage. They no longer treat `--help` as a project slug or write `projects/--help/`.
- `save_status` refuses slugs that start with `-` or `.`.

## 2026-09-24 — HQ skill advancement (LO-0331–0339)

### Added

- External subscribes: `obra/superpowers`, `anthropics/skills` (`skill-dependencies.json`). Conflict matrix blocks `executing-plans`, aitmpl blob, Bright Data scrape default, shadcn-as-kit.
- Skills: **FE-007** client security, **BE-006** jobs/delivery, **AI-004** eval/context. AI-003 retargeted to durable workflows (CI stays PE-002).
- Tools: `./studio ia-audit`; gate 5 soft `skill_application` (`studio_skill_checks.py`); `move … done` requires `## Eval` on AI-001/AI-004 receipts.
- Playbooks: scroll-experience, theme-factory HITL, Figma handoff extension, App Router/query/i18n Don’ts, backend jobs spine.

### Changed

- Skill registry total **49**. `approve-design` for `ia-navigation` requires `ia_nav` metrics (≤7 top, depth ≤3).

## 2026-09-24 — HQ skill advancement epic opened (LO-0331–0339)

### Changed

- Plan: [process/hq-skill-advancement-sprints.md](process/hq-skill-advancement-sprints.md). Vet selected claude-code-templates / superpowers / Anthropic skills against Teams 10, 01, 02, 07. Distill into playbooks; add FE-007 / BE-006 / AI-004; Python checkers. Do not install the aitmpl blob.

## 2026-09-23 — Unique network SKU matches only (LO-0330)

### Changed

- First-party catalog rows link to a network SKU only on a unique identity match. Missing or ambiguous matches stay unmatched until the operator picks the SKU.

## 2026-09-23 — Preview origin vs tenant host; inbox page link (LO-0327–0329)

### Changed

- Operator preview links use the configured magazine origin (loopback plus port on local stacks). Tenant chrome is a `host` query param, not the public hostname in the URL.
- Folder filters that join work rows to pages by `page_id` must also resolve the page via the linked brief, or persist `page_id` when the page is created.

## 2026-09-22 — Concurrent execute leases + isolation + guides (LO-0324–0326)

### Changed

- `parallel.max_projects` (default 5) file-leases `.quinsy-studio/.cache/execute-leases/`. A sixth `./studio execute` is queued and does not rewrite isolation. HITL idle or `--release` frees a slot. `./studio focus` will not clobber another live lease unless `--force`. Operator docs (root README, GETTING_STARTED, ops README, AGENTS, CLAUDE, GEMINI, Cursor rules, gates, worlds, HITL): Docker required, secrets as names, one chat per product, HQ train in a separate session.

## 2026-09-22 — Execute constitution, INFORM LOs, sequential gates, packet HITL (LO-0320–0323)

### Changed

- Every execute CARD prints **CONSTITUTION** (worlds, secrets-as-names, packet HITL). In-flight product steps INFORM open HQ LO counts and never switch to `STUDIO_LO`. `approve --gate N` refuses unless gate N-1 is approved (re-approve still allowed). HITL copy points at spec/arch/env packets, not a morning brief.

## 2026-09-22 — Infusion/learn abort on product nouns + HQ lock (LO-0318)

### Changed

- `infusion-delta` add/update refuse project folder names outside provenance and do not write. train-queue, inbox compact, and principle commits take `.quinsy-studio/.cache/hq.lock` (fcntl flock, re-entrant).

## 2026-09-22 — Abstraction verify uses every project folder (LO-0319)

### Changed

- `./studio verify-abstraction` flags any `projects/<name>` token via `list_project_names()`, skipping provenance lines, CHANGELOG, inbox archive, and tests.

## 2026-09-22 — HQ pre-commit refuses `projects/` (LO-0317)

### Changed

- `./studio install` copies `studio-templates/hooks/studio-hq-pre-commit.sh` into the studio `.git/hooks/pre-commit`. Staging `projects/` fails the hook.

## 2026-09-22 — Gate/migrate/dev require Docker (LO-0316)

### Changed

- Missing Docker fails closed with an install URL. No host fallback that prints `.env`. QA/gate stdout is pattern-redacted. `GETTING_STARTED.md` states Docker is required for gate, migrate, and boot.

## 2026-09-22 — Docker env inject is HITL `--approve` (LO-0315)

### Changed

- `./studio env <project> up|migrate|dev` exits non-zero without `--approve` and prints the HITL command (intent only). With `--approve`, Compose gets `--env-file` from the host secret store. Stdout/stderr are redacted; command lines never dump values.

## 2026-09-22 — Secret values stay out of the agent tree (LO-0314)

### Changed

- Cursor ignore always includes a **QUINSY-SECRETS** block (`**/.env`, `projects/*/.env`, host `.secrets/`) for the focused product as well as siblings. Names live in `studio-templates/env.schema.json` and `env.example`. Values belong in `~/Library/Application Support/quinsy-studio/secrets/<project>/` (or XDG). `./studio focus` / `install` rewrite the block.

## 2026-09-22 — HQ isolation epic planned (HQ-ISO-01…04)

### Added

- Four HQ sprints (`LO-0314`–`LO-0326`) so Studio can isolate secrets, require Docker, serialize HQ writes, and run ≥5 product chats. Plan: `process/hq-isolation-sprints.md`. Pause product execute until HQ-ISO-04 is done.

## 2026-09-22 — Legal templates parameterized by property identity (LO-0313)

### Changed

- Default legal templates use the property's public identity, never a hard-coded first-tenant brand string (`LO-0313` process).
- Sprint `--approve-scope` reads `scope-proposal.json` against open `backlog/*.md` only; already-done ids must be dropped from `proposed` first (`PB-20260922-003` process).

## 2026-09-22 — Sole-item canvas re-click stays selected (LO-0301)

### Changed

- Board-canvas selection: re-clicking the only selected item keeps it selected. Clear on empty-canvas click or an explicit deselect control (`PB-20260922-001` frontend).
- Unreachable persisted image URLs queue public-photo research on the same gold path as persist; do not wait for a generation vendor (`PB-20260922-001` backend, LO-0302, LO-0303).
- Tokens libraries list typefaces declared on the kit, not only fonts found on the current board (`PB-20260922-001` design, LO-0304). Canvas/Konva paint already resolves theme hex (`PB-20260916-006`; LO-0306, LO-0308 closed as duplicates).
- Zone placement must select Primary (`PB-20260922-001` IA, LO-0305). A typeface placed in a zone stays Primary until replaced (`PB-20260922-001` gates, LO-0307).
- Font-token cards: eyebrow name, ABC specimen, then a sentence in that face (`PB-20260922-002` design, LO-0309).
- New canvas item types ship CRDT allowlist and persistence enum together (`PB-20260922-001` local-first, LO-0311).



### Changed

- HQ harvest only accepts must/should/never/prefer/generalize principles. Hosts, product tickets, named product surfaces, and `when`/`chrome`/`inbox` cue-only incidents stay in the project local log (`studio_portability`).
- `inbox.md` is the **open queue**. Infused rows archive to `knowledge-base/learnings/archive/`. Durable principles live in `knowledge-base/learnings/<domain>/<topic>.md` with `index.md`. CARD lists the domain README. `./studio learn-find` / `learn-compact`. Dropped `./studio learn` prints the reason instead of "already open".

### Added

- Domain folders: `learnings/{frontend,backend,design,process,library}/` plus topic files written on portable harvest.


### Changed

- Per-tenant third-party API credentials live in encrypted rows, not process `.env` (`PB-20260916-005` backend).

## 2026-09-16 — New domain_id FKs target properties (LO-0312)

### Changed

- After the core rename, new tables with `domain_id` foreign-key `properties`, not the `domains` view (`PB-20260916-007` ticket-workflow).

## 2026-09-16 — Light islands must pin ink (LO-0300)

### Changed

- A forced-light presentation island pins `--ink` (and related text tokens) so inherited theme `text-ink` cannot flip the island pale (`PB-20260916-006` ticket-workflow).

## 2026-09-16 — Canvas 2D APIs never take CSS variables (LO-0299)

### Changed

- Non-DOM canvas stroke, fill, and title text resolve `html.dark` theme colors to hex first. CSS variables never reach the canvas API (`PB-20260916-005` ticket-workflow).

## 2026-09-16 — Canvas paint must resolve theme ink (LO-0298)

### Changed

- Non-DOM canvas paint uses the same dark/light ink as `html.dark`; CSS variables never reach canvas fills unless resolved to hex (`PB-20260916-006` design).

## 2026-09-16 — Catalog list GET must match inspector fields (LO-0297)

### Changed

- List APIs return every attribute the inspector shows; a write path is incomplete if GET omits those fields (`PB-20260916-004` backend).

## 2026-09-16 — Jobs without production orders still need Inbox and Agent (LO-0296)

### Changed

- Tickets whose jobs skip production orders must still define Inbox Done and Agent running/done rows (`PB-20260916-006` HITL).

## 2026-09-16 — Spend ledger is not the Agent view (LO-0295)

### Changed

- A green spend/LLM line is not operator proof of agent work. Jobs without a production order still need an Agent-surface row (`PB-20260916-005` HITL).

## 2026-09-16 — Gold-path chrome and architecture packets (LO-0293, LO-0294)

### Changed

- Gold-path tests for operator chrome must match the live chrome. When a ticket removes a control, update the gold path in the same change (`PB-20260916-004` design).
- `needs_architecture` tickets stay on the production stream until the architecture packet exists and is approved. Execute must not offer IMPLEMENT while `architecture_status` is pending (`PB-20260916-003` ticket-workflow, `PB-20260916-004` HITL).

## 2026-09-16 — MOVE_DONE sprint-complete copy only when the sprint is empty (LO-0292)

### Changed

- `move … done` prints sprint-complete / retro copy only when every sprint ticket is done or cancelled. Remaining tickets continue `./studio execute` (`PB-20260916-003` HITL).

## 2026-09-16 — Zone-sourced kit rails reassemble from current children (LO-0290)

### Changed

- When a canvas zone is the source of truth for a kit or inspector rail, reassemble from current children on add/delete. Do not rematch a stale stored palette (`PB-20260916-003` design).

## 2026-09-16 — Host-scope hang is not API proof (LO-0291)

### Changed

- An automation browser stuck on the fleet empty state on a host-only route is not proof the API failed. Cover AC with tests or curl and record the hang (`PB-20260916-004` gates).

## 2026-09-16 — Review --approve keeps a completed retro (LO-0285)

### Changed

- Review `--approve` must not rewind `retro_status` after `--complete`. Cadence or skill-QA approve after retro is done must not send execute back to fill retro (`PB-20260916-001` HITL).

## 2026-09-16 — Operator go vs exploration caps (LO-0286, LO-0287)

### Changed

- Operator-authorized Approve bypasses exploration or weekly synthesis caps; those caps throttle autonomous work (`PB-20260916-003` gates).
- Gold-path coverage includes the operator-authorized approve path when the autonomous cap is already exhausted (`PB-20260916-001` QA).

## 2026-09-16 — Visible review outcome; image gen is architecture-first (LO-0288, LO-0289)

### Changed

- Operator review Approve shows a visible outcome next to the action; preview URLs are the public reader host, not the admin sign-in wall (`PB-20260916-001` frontend).
- Costly generation stays an architecture packet (cost envelope + prompt/reference) before any vendor (`PB-20260916-002` HITL).

## 2026-09-16 — Lifecycle folders exclude dismissed (LO-0284)

### Changed

- Lifecycle folder queries must exclude dismissed rows; filtering dismissed only on the Dismissed folder still lists trashed items elsewhere (`PB-20260916-002` backend).

## 2026-09-16 — Chrome Share vs canvas; invite previews need cloud URLs (LO-0282, LO-0283)

### Changed

- Chrome actions such as Share belong on the shell that is already painted; a media rail must not offer a stock provider that never returns results (`PB-20260916-001` contextual-ia).
- Hub or invite previews are not done on a local blob URL; resolve the cloud content URL first (`PB-20260916-002` gates).

## 2026-09-16 — Chrome identity is UI review; identity tickets stay feature (LO-0279, LO-0280, LO-0281)

### Changed

- Operator chrome/identity sprints are not backend-only inform review (`PB-20260916-001` design).
- Left-rail demo profiles and app-chrome identity are separate tickets when the operator asks to remove all hardcoded profiles (`PB-20260916-002` design).
- `infer_ticket_type` keeps fixture/identity swaps on the feature stream even if the raw text mentions a menu (`PB-20260916-002` ticket-workflow).

## 2026-09-16 — Receipt honesty, newer feedback first, idle traces (LO-0276, LO-0277, LO-0278)

### Changed

- A hung loading surface is not browser proof of list chrome. Receipt Default flow must name what loaded; if the list never left loading, cite tests and record the hang (`PB-20260916-001` gates).
- Sprint scope sorts `--from-feedback` tickets by newer ticket number first at the same priority so leftover P0 restyle work cannot beat this session's feedback (`PB-20260916-001` ticket-workflow).
- Empty production pipeline maps activity/trace status to idle, not in_progress (`PB-20260916-001` backend).

## 2026-09-15 — Split AC bullets on --from-feedback (LO-0275)

### Changed

- Each Given/When/Then is its own AC bullet so sprint maturity sees two specific criteria (`PB-20260915-001` ticket-workflow).

## 2026-09-15 — Setup finish lands in Inbox (LO-0270, LO-0271, LO-0273, LO-0274)

### Changed

- After the last required wizard step succeeds, enable the primary finish action. Do not leave Finish disabled with an unexplained secondary pipeline link (`PB-20260915-004` HITL).
- Loading and empty states must not render leftover navigation from a previous step. Show a loading label until the next checks exist (`PB-20260915-005` HITL).
- After activate, the only enabled primary action is the operator Inbox. Downstream pipeline views stay secondary until approval (`PB-20260915-006` HITL).
- Editorial catalog forms omit merchant inventory fields the operator never uses (`PB-20260915-007` HITL).

## 2026-09-15 — Bootstrap research via Inbox (LO-0272)

### Changed

- Bootstrap plans that need catalog items queue research as an operator Inbox request, not a ticket-id hint in the UI (`PB-20260915-002` backend).

## 2026-09-15 — Shared host resolver (LO-0267, LO-0269)

### Changed

- Chrome and page lookup must share one host resolver. Do not trust the raw Host header on a preview origin when chrome already resolved the public hostname (`PB-20260915-003` design).
- Host helpers for chrome and for catalog or page lookup must share one tenant key (`PB-20260915-004` design).

## 2026-09-15 — Write-side revalidate (LO-0266, LO-0268)

### Changed

- Cache-bust after a write belongs on the plane that holds the secret. `"use client"` cannot see admin-only env — Saved can look true while the public host stays stale. Pull `write-side-revalidate`; skip `NEXT_PUBLIC_*` as the secret source (`PB-20260915-001` backend, `PB-20260915-002` frontend).
- Same rule in process: do not treat a client Saved click as proof the public host refreshed (`PB-20260915-003` HITL).

## 2026-09-15 — Sprint scope: canvas vs export/MD (LO-0263)

### Changed

- Do not mix canvas chrome with long export/MD deliverable tickets in one implementation sprint; finish gold-path product bugs first (`PB-20260915-001` design).
- Close a canvas-chrome sprint when those tickets are done; keep export/MD work later (`PB-20260915-002` design).
- After production auth or email-link changes, HITL-push the production git branch in the same session the operator can still click the message (`PB-20260915-002` HITL).

## 2026-09-15 — Soft npm_audit + delivery fetch after publish (LO-0261, LO-0262)

### Changed

- Gate-5 `npm_audit` remaining moderate on `@vitest/mocker` (same advisory class) stays a soft warning; MOVE_DONE when hard checks are green (`PB-20260915-002` gates + qa-gate).
- Gold-path publish is not done on WORK/CMS status alone — fetch the public delivery URL and confirm the document assembled (`PB-20260915-001` HITL).

## 2026-09-15 — Root tsc isolation + same-session close (LO-0259, LO-0260)

### Changed

- Public-app root `tsc` must exclude sibling apps; tests that import another app's `@/` belong in that app's graph (`PB-20260915-001` frontend Testing).
- Gate Prettier/`100` anti-slop: format the product tree before MOVE_DONE; named consts after equals (`PB-20260915-001` qa-gate).
- Close the current ticket in the same session the work lands so inbox drain can feed the next sprint (`PB-20260915-001` gates).

## 2026-09-15 — Write-side revalidate (LO-0266)

### Changed

- Cache-bust after a write belongs on the plane that holds the secret. `"use client"` cannot see admin-only env — Saved can look true while the public host stays stale. Pull `write-side-revalidate`; skip `NEXT_PUBLIC_*` as the secret source.

# Quinsy Studio CHANGELOG

## 2026-09-14 — Compose worker queues vs topology (LO-0257, LO-0258)

### Changed

- Worker `--queue=` must include every topology queue jobs are dispatched on (`PB-20260914-004`).
- YAML `--queue` / worker-command edits require recreating that service; HTTP `up -d` leaves the old command running (`PB-20260914-003`, same class as LO-0156).

## 2026-09-14 — QA prettier vs session usage JSON (LO-0254)

### Changed

- Gate Prettier ignores generated product `.studio-session-usage.json`. `ensure_prettierignore_cost_lines` keeps it in `.prettierignore` the same way gitignore lists it.
- Do not treat an unformatted estimate ledger as a ticket prettier fail.

## 2026-09-14 — PHPUnit queue pin + graph mention ids (LO-0255, LO-0256)

### Changed

- Laravel tests must pin `QUEUE_CONNECTION=sync` in TestCase env when Compose injects redis (same leak class as `DB_DATABASE`).
- Derived graph mentions use persisted entity foreign keys; missing ids → mention count 0, never mint entities from display names.
- Routed LO-0255 into `backend_playbook.md` (queue isolation is BE, not IA).

## 2026-09-14 — Guides: HQ vs product load caps and how to size S–XL

### Changed

- Root `README.md` and `GETTING_STARTED.md` explain HQ vs product ledgers, what `context` / step `budget` / `session_token_budget` mean, how to estimate (`chars/4`), and S–XL baselines.

## 2026-09-14 — HQ vs product studio-load ledgers (LO-0253)

### Changed

- HQ `studio.settings.yaml` caps **train / STUDIO_LO** only. Product execute uses `projects/<p>/docs/studio.settings.yaml`.
- `./studio settings <p> --init` writes the product file on existing trees. Adopt/init write it automatically.
- Usage: HQ `.session-usage.json`; product `.studio-session-usage.json` (gitignored). `focus` resets the product counter only.
- `INFORM cost-cap` names the ledger and which local yaml to raise. Estimates are still not host billing.

## 2026-09-14 — Product git: commit per ticket, push `dev` for review (LO-0246)

### Changed

- `MOVE_DONE` commits the **product** repo (`git -C projects/<p>`). Fine-grained revert.
- Before cadence HITL, execute runs `./studio ship <p> --to dev` when `origin` is ahead of `origin/dev`. Never auto-push `main` / production (`./studio ship --to main --approve` is HITL).

## 2026-09-14 — Guides + Cursor Auto-run for MOVE_DONE

### Changed

- Root `README.md`, `.quinsy-studio/README.md`, and `GETTING_STARTED.md` describe `PRODUCTION`, `approve-arch`, cadence review, hygiene sprints, and that `MOVE_DONE` is not studio HITL.
- `.cursor/permissions.json` steers Auto-review to allow `./studio` (including `move … done`). Add `./studio` to the **in-app** terminal allowlist; do not put `terminalAllowlist` only in this file if you want Auto-review.

## 2026-09-14 — Production stream + cadence review (LO-0244)

### Changed

- Tickets that still need design or architecture packets sit on a **production** stream. `./studio execute` returns `ACTION: PRODUCTION` (same loop, not a skipped sidecar). HITL is `./studio approve-design` and `./studio approve-arch`.
- Implementation sprints only pull **ready** tickets. `--approve-scope` is blocked when production work exists and ready backlog is below `cost.production_ready_min` (default 2). Starved pipelines steal execute into PRODUCTION when no ticket is `implement`.
- Human product review is every `cost.human_review_every_sprints` implementation sprints (default 2). Off-cadence `MOVE_DONE` is skill QA on the receipt (Skill QA / Design skill / Architecture skill). Hygiene: `./studio sprint --kind hygiene`.
- `./studio train --purge-empty` closes open train jobs with a blank observation (`closed_reason: empty-observation-invalid`).

## 2026-09-14 — Studio HQ chat is not the product inbox (LO-0243)

### Changed

- Guard returns `studio_meta` for `HQ-T*`, `LO-NNNN`, `.quinsy-studio`, and “quinsy-studio process” even while a product ticket is in flight. Those bubbles are not `./studio note` on the product sprint.

## 2026-09-13 — HQ-T18 ACE cite + train observation

### Changed

- Train jobs must carry an LO **observation**. Harvest enqueues `--from lo --lo`; CARD sidecar no longer omits `--lo`. `./studio train --topic … --lo` **enqueues** (only `--done` closes).
- Dedup + backfill close historic empty-obs duplicates of already-done jobs after portability rewrites.
- Receipt **Playbook citations** + `./studio cite` increment `helpful=` / `harmful=` on infusion-delta bullets at `move … done`.

## 2026-09-13 — HQ loop close, CARD tokens, Team 01/02 canon

### Changed

- Lifecycle docs lead with **gate 0/1/2** (not Phase 1 vs Phase 8). Project-local learnings path is `docs/studio-learnings-local.md`.
- Open LOs **do not** block product sprint. `./studio train --done` / `--lo`; queue cap `cost.train_open_max` (12). `./studio infusion-delta` ADD/UPDATE/REMOVE bullets (no full-file rewrite).
- Implement CARD context **28000** (design stays 40000). CARD: read only listed playbooks; never `learnings/inbox.md` on IMPLEMENT.
- Team 01 README is implement-only (UX/growth/SEO stay 10/11/05). Thin FE skills + `frontend_playbook` Do/Don’t/fail + `qa-gate-playbook.md` (no Team 12).
- Team 02 backend spine + CARD extras. Legal **spec-fail** rows on `compliance_playbook.md`.
- Team 07 owns loop integrity. Agentic-loop playbook lists the real CLI.

## 2026-09-12 — Delight as a layer (no UX-009)

### Changed

- New `knowledge-base/delight-playbook.md` — Norman visceral/behavioral/reflective, Kano (basics first), NN/g deep vs surface, peak–end, IA orientation, buying as service truth. **No new skill ID** (would skip most tickets).
- CARD: UX-002 and GD-002 load the delight playbook. Spec §6b + Growth peak–end row.
- Rewrote `skill-extensions/delight-micro-interactions.md` so it cannot recommend joke loaders or confetti-on-save (anti-slop wins).

## 2026-09-12 — Agentic loop: store + delta merge (LO-0231)

### Changed

- New: `knowledge-base/agentic-loop-playbook.md` — loop closes on a versioned store; ACE Generator/Reflector/Curator; merge is deterministic; LO infusion is a confirmed delta.
- `process/learning-loop.md` cross-references the playbook.

## 2026-09-12 — Ticket contract for small-model execution (LO-0230)

### Changed

- New: `knowledge-base/ticket-authoring-playbook.md` — six failure modes (invention, wrong path, unverified done, scope drift, context loss, silent assumption) each with a ticket-level antidote; required sections; sizing (no XL); `executable_by: composer|opus|human`.
- Groom checklist (`process/ticket-team-allocation.md`) and `ticket-workflow.md` point at the playbook.
- Provenance: derived from scoping a 66-ticket programme for small-model execution (LO-0230).

## 2026-09-12 — Team 10 desk-canon playbooks (Do / Don’t / fail)

### Changed

- New: `product-ux-playbook.md` (Garrett planes, Cooper goals/posture), `interaction-ux-playbook.md` (Nielsen fail table, Wroblewski forms, Cooper IxD, Krug/HIG grammar), `ux-research-playbook.md` (Indi Young).
- Deepened: design-science (visual hierarchy fail lines), contextual-ia (labeling/wayfinding), visual-storytelling, atomic, workflow, brand-guardian.
- CARD: extras per UX skill; compact card lists up to 6 playbooks.

## 2026-09-12 — Team 11 Growth Design + design canon ledger

### Changed

- New **Team 11** (`GD-001` hypothesis/experiments, `GD-002` commercial surfaces). Ticket `team` stays Team 10; GD skills append on landing, pricing, checkout, PLP, PDP.
- Knowledge: `design-team-canon-ledger.md` (10 / 11 / 05 split; books + public sources as distill-not-reprint). `growth-mechanics-playbook.md` for commercial Do/Don’t/fail lines.
- Spec template §6 Growth intent; `approve-design` fails on marketing-page / commercial ticket blob without it.
- CARD playbooks include `growth-mechanics-playbook.md` when GD or UX-007 is loaded.

## 2026-09-12 — UI kit peers on scaffold; agent-run migrations

### Changed

- Every project setup (`init` / `bootstrap` / `design` / `adopt`) writes `docs/setup/ui-kit.md`. Design-prototype `package.json` includes `radix-ui`, `class-variance-authority`, `clsx`, `tailwind-merge`, `lucide-react`, and `@headlessui/react`. Adopt and UI `library pull` merge the same peers into existing app `package.json`s.
- Schema apply is **agent work** when the agent can reach the DB (local Compose, `.env` DSN, documented VPS). Inform the human. Do not ask them to run migrate as sprint work. Destructive reset remains HITL.
- Docs: AGENTS, GETTING_STARTED, READMEs, HITL, backend playbook, brownfield-adopt, lifecycle, ticket-workflow.

## 2026-09-12 — Design-track: write spec+mocks before approve-design

### Changed

- Agents must **write** `docs/design-specs/<TICKET>.md` and `docs/design-specs/mocks/<TICKET>/` HTML before anyone is asked to review. Execute returns IMPLEMENT (write) when the packet is missing — not HITL. `approve-design` **fails** on missing/stub spec, mocks that skip project CSS tokens, orphan artboards, or incomplete states (rest/hover/pressed/disabled/focus; open/closed; empty/loading/error).
- Ticket create drops a spec stub (still not approvable). Docs: design-spec-template, HITL, GETTING_STARTED, AGENTS, README, Team 10.

## 2026-09-12 — Studio-library shadcn kit (themable)

### Changed

- Styled `ui/components/*` kit is shadcn/Radix + CVA, themed via CSS variables (`--primary`, `--background`, …) aliased from studio tokens. Brand-hardcoded Button/Input/Badge/Checkbox/etc. lost the “generic + themable” comparison vs a shadcn kit.
- Headless UI primitives stay under `ui/primitives/headless/`. Headless molecules (`dialog-shell`, `search-command`, Listbox `dropdown`, `segmented-toggle`) remain.
- Not vendored (need `@shadcn/react`): Questionnaire, Message Scroller. Product-specific files were not copied.
- Inventory: `studio-library/ui/docs/shadcn-coverage.md`.

## 2026-09-12 — Design-track HITL; other tickets stay on the system

### Changed

- `approve-design` is HITL again **only** for design-track tickets (major UX/UI/IA). `move … implement` blocks until `design_status: approved`. Feature/styling/bug tickets do **not** wait for ticket ACK.
- Missing component/token/pattern: file a design-track ticket and work it in a **design sprint** — do not invent primitives in a feature ticket (`human-in-the-loop.md`, `design-system-compliance-checklist.md`).
- Execute CARD / guard: still no feature-ticket ACK; `HITL design-approve` restored for design-track.

## 2026-09-12 — Sprint HITL is review only after start

### Changed

- After a sprint has started, execute/guard no longer HITL on per-ticket `approve-design` or “looks good” ticket ACK. Human stop is **UI sprint review** (plus tech-veto, 3× gate fail, abort, `INFORM cost-cap`).
- Design specs stay agent DoD (`design_status: agent-owned`, §2 + §2c). `./studio move … implement` is not blocked on `approve-design`.
- Docs: `human-in-the-loop.md`, `AGENTS.md`, GETTING_STARTED, READMEs, Cursor rules, ticket-team-allocation.

## 2026-09-12 — Onboarding docs match isolation + two-git habit

### Changed

- Root `README.md`, `.quinsy-studio/README.md`, `GETTING_STARTED.md` — `focus`/`isolate` assignment (not a sandbox), `CROSS_PROJECT`, product git via `git -C projects/<name>`, portable HQ LOs only, Team 10 in the team list, ticket-specific design specs before sprint scope, smoke the project RUNBOOK URL.

## 2026-09-12 — Open LO harvest (0206–0230), portability split

### Changed

- `studio-tools/sprint_reuse_review.py` — host `packages/ui` and scoped `@*/ui` are product-local; reuse does not demand promote (LO-0206).
- `process/human-in-the-loop.md` — scope-proposal md/json/execute counts match (LO-0208); human-smoke AC names compose/create path (LO-0223); operator filing stays structured-first (LO-0224).
- `process/ticket-team-allocation.md` — ticket-specific design spec + §2/§2c before sprint scope (LO-0213 / 0218 / 0220 / 0222).
- `knowledge-base/frontend_playbook.md` — shared card organism before a second copy; specimens use library/token styles; print CSS is the PDF source; HTML sticker `</style>` before body (LO-0210 / 0211 / 0212 / 0216 / 0217).
- `knowledge-base/design_playbook.md` — export chrome names filename/format only (LO-0226); list/detail titles truncate (LO-0229).
- `knowledge-base/backend_playbook.md` — pending migrations before treating API 500 as a product bug (LO-0227).
- `knowledge-base/host-port-allocation.md` — smoke on the project RUNBOOK compose URL, never a hardcoded studio port.

### Closed

- Infused: LO-0206, 0208, 0210–0213, 0216–0218, 0220, 0222–0224, 0226, 0227, 0229.
- Removed from HQ backlog (project-local only): LO-0207, 0209, 0214, 0215, 0219, 0221, 0225, 0228, 0230.

## 2026-09-11 — LO-0202–0205 (idle infusion + ticket generator)

### Changed

- `knowledge-base/backend_playbook.md` — LO-0202 closed as duplicate of LO-0200 (host-panel env aliases).
- `process/human-in-the-loop.md` — public `/` with published inventory is the default flow for chrome tickets (LO-0203, LO-0205).
- `knowledge-base/design_playbook.md` — smoke `/` on the RUNBOOK public host port, not only inner slugs (LO-0205).
- `process/ticket-workflow.md` + `studio-tools/ticket_helpers.py` / `studio.py` — `--from-feedback` uses draft AC; skip generic GWT (LO-0204).

### Closed

- LO-0202, LO-0203, LO-0204, LO-0205 infused.


## 2026-09-11 — LO-0200 / LO-0201 idle infusion

### Changed

- `knowledge-base/backend_playbook.md` — accept vendor env aliases in the server resolver; do not leave API secrets as `NEXT_PUBLIC_*` long-term (LO-0200).
- `knowledge-base/design_playbook.md` — selected palette id must drive presentation and PDF, not design-file-only fixes (LO-0201).

### Closed

- LO-0200, LO-0201 infused.


## 2026-09-11 — SPRINT-18 idle infusion (LO-0197–0199)

### Changed

- `process/ticket-team-allocation.md` — `files:` hitting `packages/ui` is not design-track by itself; split visitor-shortlist vs editorial comparison verbs before bulk-select (LO-0197, with LO-0184).
- `process/human-in-the-loop.md` — one listener per published host port: Compose XOR host `npm run dev` (LO-0198, LO-0199).

### Closed

- LO-0197, LO-0198, LO-0199 infused.


## 2026-09-11 — SPRINT-134 retro learnings (LO-0191–0196)

### Changed

- `knowledge-base/frontend_playbook.md` — print unlock for `overflow:hidden` / `h-dvh` shells; selected palette import never invents FALLBACK roles (LO-0191, LO-0192, LO-0194, LO-0196).
- `knowledge-base/design_playbook.md` — plugin HTML icon-only = outline/dimmed, not soft wash (LO-0193).
- `process/human-in-the-loop.md` — print overflow unlock in DoD; gitignored plugin `dist/` needs rebuild+reload for review smoke (LO-0192, LO-0194, LO-0195).

### Closed

- LO-0191, LO-0192, LO-0193, LO-0194, LO-0195, LO-0196 infused.


## 2026-09-11 — SPRINT-133 retro learnings (LO-0187–0190)

### Changed

- `process/human-in-the-loop.md` — print DoD: section wrappers + print-preview page count; plan-only green is not done (LO-0189 / LO-0181).
- `knowledge-base/frontend_playbook.md` — section=page print tree; selected-id bind for palette/kit import-export (LO-0188, LO-0189).
- `knowledge-base/design_playbook.md` + `studio-library/ui/components/button/README.md` — dimmed/outline icon chrome for light+dark (LO-0187, LO-0190).

### Closed

- LO-0187, LO-0188, LO-0189, LO-0190 infused.


## 2026-09-11 — SPRINT-131 retro learnings (LO-0181–0186)

### Changed

- `process/human-in-the-loop.md` — print/PDF receipts need page-count proof (LO-0181); prefer split sprints over 14-ticket polish dumps (LO-0183); bundle plugin shell chrome FBs (LO-0185).
- `process/ticket-team-allocation.md` — do not over-classify chrome polish as design-track (LO-0184).
- `knowledge-base/design_playbook.md` — plugin cold-open shows Login first (LO-0182); moving exports drops leftover helper cards (LO-0186).

### Closed

- LO-0181, LO-0182, LO-0183, LO-0184, LO-0185, LO-0186 infused.


## 2026-09-11 — Sprint-16 learnings (LO-0176–0180)

### Changed

- `process/gates.md` — after a claimed prod-infra fix, next tickets are research + instrumentation (LO-0176).
- `process/agent-context.md` — reuse vendored admin Kanban/table/Dialog/Empty; Add = Dialog, inspect = Sheet (LO-0177, LO-0178).
- `knowledge-base/design-science-playbook.md` — empty states name the previous step and link to it (LO-0179).
- `knowledge-base/backend_playbook.md` — persist native board column ids when wiring the job API (LO-0180).

### Closed

- LO-0176, LO-0177, LO-0178, LO-0179, LO-0180 infused.

## 2026-09-10 — Clear sprint on supersede/cancel (LO-0175)

### Changed

- `process/ticket-workflow.md` / `process/human-in-the-loop.md` — supersede or cancel must clear `sprint:` or `move … cancelled` in the same turn so execute/review cannot pick ghosts.

### Closed

- LO-0175 infused.

## 2026-09-10 — Anti-slop ignores vendored admin shells

### Changed

- `studio-tools/validate_anti_slop.py` — ignore a vendored admin UI the same way as Filament public assets (now listed per product in `docs/anti-slop-ignore.txt`).

## 2026-09-10 — Residual UI needs a render-path ticket (LO-0174)

### Changed

- `process/gates.md` — leftover flicker after a status-only ticket requires a follow-up that changes the render path, not another flag flip.

### Closed

- LO-0174 infused.

## 2026-09-10 — Kit-token Dropdown

### Changed

- `studio-library/ui/components/dropdown/` — Listbox paints from kit CSS variables (`--color-border`, `--color-background`, `--color-foreground`, `--color-muted`, `--color-accent`, `--font-ui`) instead of one product's class names.
- `studio-library/ui/tokens/design-tokens.css` — aliases those kit names onto the canonical surface/text/primary tokens.

## 2026-09-10 — Deployed review push; reuse inform-auto; gutter; pooler (LO-0167–0173)

### Changed

- `process/human-in-the-loop.md` / `process/agent-context.md` — git-deployed sprint review needs a product-repo push after MOVE_DONE (LO-0167, LO-0170); drop accidental `--help` feedback before retro (LO-0173).
- `studio-tools/studio.py` / `sprint_hitl.py` — reuse inform completes when paths are recorded; no `--approve` (LO-0169).
- `studio-library/library_registry.md` — `--record local` on brand UI when the ticket ships (LO-0171).
- `knowledge-base/design_playbook.md` — `scrollbar-gutter: stable` on public chrome (LO-0172).
- `knowledge-base/backend_playbook.md` — pooler tenant/SNI; apply DDL on the primary, not a bare pooler port (LO-0168).

### Closed

- LO-0167, LO-0168, LO-0169, LO-0170, LO-0171, LO-0172, LO-0173 infused.

## 2026-09-09 — Soft npm_audit label; warm Playwright cache (LO-0165, LO-0166)

### Changed

- `studio-tools/run_qa_gate.py` — `npm_audit` soft fails show ⚠️ and “does not fail RESULT” when hard checks pass (LO-0165).
- `process/gates.md` — warm `.quinsy-studio/.cache/playwright/<project>/` via `smoke:install` before smoke-heavy sprints (LO-0166); document npm_audit soft policy.

### Closed

- LO-0165, LO-0166 infused.

## 2026-09-09 — Dual-surface delete; reuse skip product packages; billing env (LO-0158–0164)

### Changed

- `knowledge-base/design_playbook.md` / `chrome-mv3-vite-content-scripts.md` — companion ↔ cloud delete must be bidirectional before “inbox ready” (LO-0158, LO-0160).
- `studio-tools/sprint_reuse_review.py` / `studio-library/library_registry.md` — skip figma-plugin/extension and `.DS_Store`/`dist` as promote noise (LO-0162, LO-0164).
- `knowledge-base/backend_playbook.md` — server-only secrets + host env contract in the same billing ticket (LO-0163).

### Closed

- LO-0158, LO-0160, LO-0162, LO-0163, LO-0164 infused.

## 2026-09-09 — Extension global-arm order; never silent focus switch (LO-0157, LO-0159, LO-0161)

### Changed

- `knowledge-base/chrome-mv3-vite-content-scripts.md` — global mode: fan-out + inject-on-miss before persisting armed storage (LO-0157, LO-0159).
- `process/agent-context.md` — do not `./studio focus` another product unless the human explicitly asks to switch; chat/execute topic mismatch stays on active project (LO-0161).

### Closed

- LO-0157, LO-0159, LO-0161 infused.

## 2026-09-09 — Operator click before job polish; recreate Compose workers (LO-0155, LO-0156)

### Changed

- `process/human-in-the-loop.md` / `process/agent-context.md` — a queued job is not the default flow until the operator control that enqueues it ships; implement that click before notify/revalidate polish when the human is waiting (LO-0155).
- `knowledge-base/backend_playbook.md` — recreate queue workers and the public app after Compose queue/env/volume edits; use the service hostname for container-to-container URLs (LO-0156).

### Closed

- LO-0155, LO-0156 infused.

## 2026-09-09 — Public document matches operator Save (LO-0154)

### Changed

- `process/human-in-the-loop.md` — published Save must be what the public document route serves; no silent fixture fallback when a live record id exists (LO-0154).

### Closed

- LO-0154 infused.

## 2026-09-09 — Public nav DoD + operator edit layout (LO-0151, LO-0152)

### Changed

- `process/human-in-the-loop.md` — public nav lists only published, non-empty destinations (LO-0151). Operator edit: tabs under header actions, ordered map first, one field per row (LO-0152).
- `process/learning-loop.md` — named 404s in a brand masthead stay in the project-local log; the portable rule is empty-destination chrome.

### Closed

- LO-0151, LO-0152 infused.
- LO-0153 closed as duplicate of LO-0150 (project public chrome stays local at reuse).

## 2026-09-09 — Warn that IDE focus is not a product sandbox

### Changed

- `README.md` and `GETTING_STARTED.md` — several products in one workspace can still be seen by the agent; users keep one chat/CLI process per product.

## 2026-09-09 — Ordered admin maps as lists (LO-0149)

### Changed

- `process/human-in-the-loop.md` — ordered named rows (section/nav maps) ship as a table/list, not a stacked card Repeater (LO-0149).

### Closed

- LO-0149 infused.

## 2026-09-09 — Project public chrome stays local (LO-0150)

### Changed

- `studio-library/library_registry.md` — project `packages/ui` masthead/nav/page renderers stay `local` at reuse; do not promote host face into HQ (LO-0150).

### Closed

- LO-0150 infused.

## 2026-09-09 — Sibling project isolation (focus / guard / git)

### Added

- `studio_isolation.py` — `./studio focus`, `./studio isolate`, and `./studio execute` hide other `projects/*` via `.cursorignore` + a generated Cursor rule. Guard returns `CROSS_PROJECT` if the request names a sibling. Execute CARD prints `ISOLATE`. Project `pre-commit` refuses a wrong git toplevel, escaped paths, and `projects/` symlinks.
- `verify-worlds` reapplies isolation for the active project and fails if that project's git toplevel is the wrong repo.

### Changed

- `.gitignore` — `.cursorignore` and `.cursor/rules/quinsy-project-isolation.mdc` are local (regenerated on focus).

## 2026-09-09 — Closed-library editor + visitor preview (LO-0148)

### Changed

- `process/human-in-the-loop.md` — operator editor matches the public block library and visitor template, not a Word/HTML page field (LO-0148).

### Closed

- LO-0148 infused.

## 2026-09-09 — Seeded corpus is not the next-wave backlog (LO-0147)

### Changed

- `knowledge-base/backend_playbook.md` — further corpus work uses the idea queue / admin briefs, not a silent rewrite of the seeded set (LO-0147).

### Closed

- LO-0147 infused.

## 2026-09-08 — Close sprint review when this sprint is done (LO-0144)

### Changed

- `process/human-in-the-loop.md` — do not keep sprint review open for later amendments, consoles, or unwritten skills that are still only feedback (LO-0144).
- `process/lifecycle.md` — Phase 7 review is for shipped sprint tickets (LO-0144).

### Closed

- LO-0144 infused.

## 2026-09-08 — Isolated test DB pin + operator idea queues (LO-0145 / LO-0146)

### Changed

- `process/gates.md` — `phpunit.xml` `force` is not enough inside Compose; TestCase must pin the isolated test database before schema refresh (LO-0145).
- `knowledge-base/backend_playbook.md` — same TestCase pin (LO-0145); operator idea queues belong in product admin, not IDE chat (LO-0146).
- `teams/02-backend-systems/skills/api-design.md` — toolbox: in-product idea queue (LO-0146).
- `teams/02-backend-systems/skills/error-handling.md` — toolbox: do not treat chat paste as the system of record (LO-0146).

### Closed

- LO-0145, LO-0146 infused.

## 2026-09-08 — Upgrade soft-path DoD (LO-0142 / LO-0143)

### Changed

- `studio-library/ui/docs/patterns/upgrade-soft-path.md` — soft-path must surface Free + Upgrade or auto-open upgrade dialog (LO-0142).
- `studio-library/ui/docs/README.md` — index link to upgrade soft-path pattern.
- `knowledge-base/frontend_playbook.md` — cross-link soft-path Account pattern (LO-0142).
- `knowledge-base/skill-extensions/product-led-growth.md` — soft-path Account DoD (LO-0142 / LO-0143).
- `process/gates.md` — free-tier Account assert before soft-path tickets are done (LO-0143).
- `teams/09-…/skills/studio-tooling-maintenance.md` — toolbox TR-0011 (LO-0142/0143).
- `teams/10-…/skills/visual-ui-design.md` — toolbox TR-0012 (LO-0142).
- `teams/01-…/skills/design-system.md` — toolbox TR-0013 (LO-0142).

### Closed

- LO-0142, LO-0143 infused.

## 2026-09-08 — Filament home is the resource list (LO-0141)

### Changed

- `knowledge-base/backend_playbook.md` — admin `homeUrl` to the primary resource index; header stats widgets must not stay lazy (LO-0141).

### Closed

- LO-0141 infused.

## 2026-09-08 — Legal disclosure needs network assert (LO-0139 / LO-0140)

### Changed

- `process/gates.md` — when Privacy forbids pre-auth / anonymous font CDNs, smoke must assert network on marketing **and** anonymous share/presentation surfaces in the same sprint (LO-0139 / LO-0140).

### Closed

- LO-0139, LO-0140 infused.


## 2026-09-08 — Gate uses project Prettier; first-brand chrome stays local (LO-0137–0138)

### Changed

- `studio-tools/run_qa_gate.py` — `npx --no-install` for Prettier, ESLint, `tsc`, and Vitest so QA cannot download a stray formatter (LO-0137).
- `process/gates.md` — document project-local Prettier for QA levels.
- `studio-library/library_registry.md` + `studio-library/packages/README.md` — first-brand public chrome stays in-project; reuse `--record … local` (LO-0138).

### Closed

- LO-0137, LO-0138 infused.

## 2026-09-08 — Gate smoke unrestricted + pre-auth font DoD (LO-0132–0136)

### Changed

- `process/gates.md` — before `move … done`, re-run Playwright smoke outside agent sandboxes; `QUINSY_SKIP_SMOKE` is last-resort only (LO-0132 / LO-0133 / LO-0136).
- `studio-tools/run_qa_gate.py` — skip message reminds agents to re-run smoke unrestricted.
- `knowledge-base/frontend_playbook.md` — pre-auth self-host font DoD covers layout, specimens/iframes, and `ensureGoogleFontLink` skips (LO-0134).
- `knowledge-base/component-creation-playbook.md` — project `ui/` cannot promote into studio-library; edit HQ library or open a studio LO (LO-0135).
- Portability: replaced project-folder names in chrome-mv3 / figma-plugin / frontend playbook provenance lines.

### Closed

- LO-0132–LO-0136 infused.


## 2026-09-08 — Portability gate drops project-incident LOs (LO-0129, LO-0131)

### Fixed

- Harvest no longer opens HQ LOs from long incident sentences, product ticket IDs, or vendor-sprint bullets. Those go to `projects/<p>/docs/studio-learnings-local.md`.
- Guard does not queue short HITL replies (`approved`, `looks good`) or review/amendment approve.

### Changed

- `process/learning-loop.md` — HQ vs project-local examples.
- `process/human-in-the-loop.md` — last ticket `done` → HITL sprint-review immediately.

### Closed

- LO-0129, LO-0131 infused. LO-0127, LO-0128, LO-0130, LO-0132 dropped (project-local, not studio HQ).

## 2026-09-08 — Polish-sprint capacity + motion smoke numbers (LO-0124–0126)

### Changed

- `process/human-in-the-loop.md` — intentional 2-ticket review-polish sprints OK under capacity warn (LO-0124).
- `knowledge-base/design-science-playbook.md` — prototype one sticky section before done (LO-0125).
- `knowledge-base/design_playbook.md` — put cover-range / throw-on numbers in the design spec (LO-0126).

### Closed

- LO-0124–LO-0126 infused.

## 2026-09-08 — Sticky blur timing + appear throw-on DoD (LO-0120–0123)

### Changed

- `process/human-in-the-loop.md` — sticky stages: current stays sharp; incoming blur-in; outgoing fade; throw-on over tilt-only (LO-0120–0122).
- `knowledge-base/design-science-playbook.md` — appear DoD requires start blur/opacity/scale + end tilt degrees (LO-0123).

### Closed

- LO-0120–LO-0123 infused.

## 2026-09-08 — Marketing scroll-story motion DoD (LO-0116–0119)

### Changed

- `process/human-in-the-loop.md` — lock scroll-story motion model in design spec before IMPLEMENT (LO-0116).
- `knowledge-base/design_playbook.md` — sticky stages: prefer blur crossfade over SoftCard chrome + scale-recess (LO-0117).
- `knowledge-base/design-science-playbook.md` — fixed illustration height, no page-wide enter cascades, native sticky scroll (LO-0118, LO-0119).
- Queued train TR-0009 (UX-002), TR-0010 (UX-003).

### Closed

- LO-0116–LO-0119 infused.

## 2026-09-08 — Tailwind v4 `@source` workspace UI; PHPUnit isolation (LO-0110–0115)

### Changed

- `frontend_playbook.md` — Tailwind v4 `@import` does not scan sibling UI packages; `@source` (or v3 `content`) before marking public chrome done (LO-0110, LO-0113).
- `backend_playbook.md` — do not `RefreshDatabase` / `migrate:fresh` the operator Compose Postgres from feature tests (LO-0112, LO-0115).

### Closed

- LO-0110, LO-0113 infused (scan). LO-0112, LO-0115 infused (test DB). LO-0111, LO-0114 closed as product-backlog (color swatch on initialize status), not HQ.

## 2026-09-07 — Reuse harvest skips token kits; Laravel serve --no-reload (LO-0100, LO-0101)

### Changed

- `studio_harvest.harvest_reuse_items` — auto-LO only registry generic packages; skip `theme-tokens` / `design-tokens` / `kit-*` and project `ui/`.
- `library_registry.md` reuse enforcement — record first-brand kits `local`.
- `backend_playbook.md` — `artisan serve --no-reload` (or `php -S`) so Compose env reaches HTTP.
- SO-001 toolbox: reuse harvest + Laravel serve notes.

### Closed

- LO-0100, LO-0101 infused. LO-0102–LO-0109 closed as duplicates or product-backlog items (not HQ).

## 2026-09-07 — Close reuse-harvest LOs for first-brand kits (LO-0083–0099)

### Closed

- LO-0083–LO-0099 → `backlog/done/` without promoting into `studio-library/`. Reuse harvest auto-opened package LOs for a project's first-brand token/UI tree; record `./studio reuse --record <path> local` instead of copying client kits into HQ.

## 2026-09-07 — Mid-execute chat is inbox ACK, not a new assignment

### Fixed

- `./studio guard` is studio-core: while any project has work in flight, a user message is `INBOX_ACK` (auto-queued) and the current ACTION continues. Sprint-review `FEEDBACK_ONLY` no longer preempts an in-flight ticket.
- Execute CARD prints `MID-CHAT:` on looping steps. Notes work before a sprint exists (`docs/human-inbox.json`).

## 2026-09-07 — Anti-slop ignores published admin kit assets (LO-0082)

### Changed

- `studio-tools/validate_anti_slop.py` — skip Composer `vendor/` and published Filament-style `public/js|css|fonts/filament` (same class as `node_modules`).
- SO-001 toolbox: extend `IGNORE_PATTERNS` for generated admin-kit trees; do not rewrite vendor files.

### Closed

- LO-0082 → `backlog/done/`.


## 2026-09-07 — Close duplicate retro harvest LOs (LO-0076–0081)

### Closed

- LO-0076–LO-0081 → `backlog/done/` as duplicates of LO-0067–0075 / existing playbook rules (portability gate still lets principle-shaped retro lines through; prefer stronger dedupe next).

## 2026-09-07 — Portability gate for harvest / train / infusion

### Added

- `studio-tools/studio_portability.py` — rewrite + portability test; project-local log; HQ noun scan.
- Harvest drops non-portable titles to `projects/<p>/docs/studio-learnings-local.md` (no LO).
- LO frontmatter `train_skills`; execute train sidecar only for skill gaps.
- `./studio train` rejects non-portable topics; `./studio infusion` reports project-name hits in HQ docs.

### Changed

- `process/learning-loop.md` — portability gate as required harvest step.
- Train topics must be reusable principles (not product/surface incident lines).

## 2026-09-07 — Studio LO infusion gate clear (LO-0067–LO-0075)

### Added

- `knowledge-base/backend_playbook.md` — licence adapter contract (LO-0067 / LO-0072); stock imagery provider priority — primary aggregator first, fallbacks last (LO-0075).
- `knowledge-base/design_playbook.md` — per-cell pixel budgets and resolution-aware bento placement (LO-0068 / LO-0070 / LO-0073).
- `teams/09-studio-operations-evolution/skills/studio-tooling-maintenance.md` — SO-001 toolbox: licence slugs, bento budgets, degraded Suggested UX, sandbox smoke skip (LO-0071), provider priority (LO-0075).

### Changed

- `knowledge-base/contextual-ia-playbook.md` — anti-pattern: selection-order mosaic placement (LO-0070).
- `process/human-in-the-loop.md` — degraded Suggested copy must separate HTTP outage vs filter-empty (LO-0069 / LO-0074).
- `process/gates.md` — LO-0071: explicit `QUINSY_SKIP_SMOKE` rule for agent sandboxes where Chromium SIGSEGVs.

### Closed

- LO-0067, LO-0068, LO-0069, LO-0070, LO-0071, LO-0072, LO-0073, LO-0074, LO-0075 → `backlog/done/`.

## 2026-09-07 — Probe host ports before Docker publish (LO-0066)

### Changed

- New [host-port-allocation.md](knowledge-base/host-port-allocation.md): agents probe `docker ps` before pinning Compose host ports; no new CLI.
- PE-001, backend playbook, agent-context, HITL, docker template: host ports via env (`POSTGRES_HOST_PORT`, `REDIS_HOST_PORT`); textbook 5432/6379/3000 are not a reservation.

## 2026-09-07 — Playwright arm64 host override when os.cpus() is empty

### Fixed

- `studio-tools/run_qa_gate.py` — on Darwin arm64, set `PLAYWRIGHT_HOST_PLATFORM_OVERRIDE` from `platform.machine()` so smoke finds durable arm64 browsers when Cursor sandboxes return empty `os.cpus()` (Playwright otherwise picks mac-x64).

## 2026-09-07 — Imagery Suggested smoke + presentation layout DoD (LO-0062–0065)

### Changed

- `process/human-in-the-loop.md` — Suggested/found imagery must smoke signed-in provider path; empty-after-alive-copy is not done (LO-0062/0064). Imagery selection epics need presentation placement + composition quality DoD, not rail-only (LO-0063/0065).
- `knowledge-base/contextual-ia-playbook.md` — anti-pattern: picker without presentation layout DoD.

## 2026-09-07 — Execute loop hygiene: tests, worlds, lean status.json

### Fixed

- `test_studio_learning_gate.py` is unittest (discoverable), not pytest-only.
- `./studio verify-worlds` allows committed `intake/amendments/**/amendment_*.example.md` and ignores leftover dirs (`--help`, `LO-0042`, `testproj`). Non-example amendment binaries are gitignored.
- File-hash snapshots move to `docs/ticket-file-snapshots.json`; `gate_history` is capped so execute does not parse an 8MB `status.json`.

## 2026-09-07 — Studio settings: per-step token policy + host adapters

### Added

- [studio.settings.yaml](studio.settings.yaml) — medium-project defaults; per-step `context` / `budget` (intake, architecture, design, implement, …).
- `./studio settings` — merged policy + estimated usage. Local override: `studio.settings.local.yaml` (gitignored; **no API keys**).
- Execute CARD shows `COST`; at 100% of a knob → `INFORM cost-cap` naming the yaml key. `economy` / `standard` / `premium` profiles.
- [CLAUDE.md](../CLAUDE.md) and [GEMINI.md](../GEMINI.md) — same `./studio` loop; keys stay in the host.

### Changed

- Estimates are `chars/4` of CARD + listed files, not host billing. `./studio focus` resets session usage.


### Changed

- **Gate 1 (architecture)** is mandatory HITL after gate 0. Execute writes the blueprint, then stops for `./studio approve --gate 1`. Iterate with `./studio revise --gate 1`.
- **Gate 2 (design track)** is mandatory HITL after architecture: design direction, design system, stills/mocks or clickable prototype. Execute runs `./studio design`, then stops for `./studio approve --gate 2`. Per-ticket `approve-design` still applies in sprints.
- `./studio inform --gate 1` no longer marks architecture informed — it points at `./studio approve`.
- Root `README.md`, [GETTING_STARTED.md](GETTING_STARTED.md), and this ops [README.md](README.md) match that loop (train in parallel, stubs not pullable, scope/reuse inform).


## 2026-09-07 — Factory loop: HITL contraction, parallel train, human inbox (LO-0061)

### Changed

- **Mandatory HITL** was contracted (reuse/scope inform, parallel train). **Same-day correction:** architecture (gate 1) and design track (gate 2) remain standing HITL after PRD — see entry above.
- Sprint scope/groom are **agent-owned** (human may override). Reuse is an **inform brief** — `--approve` no longer blocks retro or the next sprint.
- Harvest stays immediate. Open LOs spawn `./studio train` **beside** product work. Execute returns `STUDIO_LO` only when idle (no ready IMPLEMENT).
- CARD lists `skills` + playbook paths. `./studio note` queues mid-execute input (ACK; drain after MOVE_DONE). Only “stop this ticket” preempts.
- `billing` and `feature-gating` are marked `stub: true` and **not pullable**. Pull → adapt in the project; promote only when the generic asset improved.

### Added

- `./studio note` / `inform --gate 1` / `veto` / `train`
- `studio_human_inbox.py`, `studio_train.py`


## 2026-09-07 — Execute respects cross-sprint done deps

### Fixed

- `studio_execute.py` — `project_done_ids()` reads `backlog/done/` so sprint tickets whose dependencies finished in prior sprints are no longer falsely blocked.
- Execute picks the next ticket in **scope-proposal.json order** (then priority, then id), so approved sprint goals lead.

## 2026-09-07 — Live home surface + mid-sprint rewrite + marketing canvas fidelity (LO-0054, LO-0057–0060)

### Changed

- `process/human-in-the-loop.md` — confirm live product home before scoping UI from amendment IA (LO-0057/0059); same-turn `plan.md` + defer when feedback rewrites sprint goal (LO-0060); mature AC before implement on mid-sprint pulls (LO-0058); marketing canvas stills must mount real product canvas / shared fixtures (LO-0054).
- `process/amendment-intake.md` — agent obligation: live home-surface check before grooming amendment-placed UI.
- `process/backlog-model.md` — mid-sprint goal rewrite + maturity for feedback pulls.
- `knowledge-base/contextual-ia-playbook.md` — anti-patterns for amendment-over-live and immature mid-sprint pulls; live-vs-draft checklist.
- `knowledge-base/visual-storytelling-playbook.md` — product fidelity rule for canvas/stylescape marketing stills.

## 2026-09-07 — Brownfield adopt (LO-0056)

### Added

- `./studio adopt <project> --from <git-url-or-path> [--intent intake/<p>.md]` — overlay studio docs on an existing codebase. Keeps the project’s `.git`. Never wipes `src/` / `app/`.
- Process [brownfield-adopt.md](process/brownfield-adopt.md) + as-built templates (`docs/as-built/00`–`07`) and `studio-templates/adopt_intent.md`.
- Execute: `mode: adopt` fills as-built (`IMPLEMENT`) then synthesizes PRD (`VERIFY`) before HITL gate 0. Gate 2 is design-of-what-exists — no empty Next.js prototype.

### Changed

- `init` / `bootstrap` / `start` / `design` refuse or skip empty-scaffold on a live tree.
- Docs: GETTING_STARTED, root README, AGENTS — existing-project path vs greenfield PRD.

## 2026-09-07 — Immediate harvest + mid-sprint infusion (LO-0055)

### Added

- `studio_harvest.py` — classify a learning when it is identified (package, ui-component, design/ux/ia/layout/usability, frontend/backend/database/security, process, tooling), append `knowledge-base/learnings/inbox.md`, open a compact LO with `infusion_kind` / `infusion_path`.
- `./studio learn`, `./studio retro --complete`, `./studio reuse`, and 3rd gate fail all harvest immediately — no human learn prompt, no wait until next sprint.

### Changed

- `./studio execute` returns `STUDIO_LO` **before the next project IMPLEMENT**, including mid-sprint. In-progress tickets still finish VERIFY/GATE/DEBUG/MOVE_DONE. HITL (gates 0–2, sprint-review) still wins.
- Does not copy project UI/tokens into `studio-library/`; inbox + LO is the capture; the agent generalizes on `STUDIO_LO`.

## 2026-09-07 — Agentic execute loop (LO-0053)


### Added

- `./studio execute <project> [--json]` — one next action (`IMPLEMENT` / `GATE` / `VERIFY` / `MOVE_DONE` / `DEBUG` / `STUDIO_LO` / `HITL`). Agent loops until HITL; does not ask to continue.
- Compact ticket cards (`./studio ticket-card`) and execution receipts (`./studio receipt`) — Plan, AC coverage, default flow (LO-0051) required before `move … done`.
- `./studio health <project>` — sprint state-graph check (open LOs, missing receipts, unmet deps).
- Bounded gate-fail debug files (`sprints/SPRINT-NN/debug/<ticket>.md`, max 3 retries) and auto-draft LO on exhaustion (`signal: gate-fail`).
- Retro `--complete` harvests `./studio learn` prompts from went badly / improve.

### Changed

- `ticket_helpers.py` renders compact tickets (no duplicated skills/deps, no filler BDD, no per-ticket boilerplate DoD).
- Session start: `./studio execute` is the driver; `resume` remains a checklist.
- Docs: root `README.md`, `.quinsy-studio/README.md`, `GETTING_STARTED.md` — execute loop, compact tickets, receipts, health, `STUDIO_LO`.

### Notes

- Markdown remains ticket source of truth (no SQL). Tokens are saved by layered load (card vs full ticket), not storage format.


## 2026-09-05 — Durable Playwright browsers for gate smoke (LO-0052)

### Fixed

- `studio-tools/run_qa_gate.py` — smoke sets `PLAYWRIGHT_BROWSERS_PATH` to `.quinsy-studio/.cache/playwright/<project>/` and clears `PLAYWRIGHT_HOST_PLATFORM_OVERRIDE`, so gate smoke does not reinstall into ephemeral Cursor sandbox caches or hit mac-x64/arm64 mismatches.
- `process/gates.md` — documents durable cache + `QUINSY_SKIP_SMOKE` opt-out.
- `.gitignore` — ignores `.quinsy-studio/.cache/`.
- Provenance: a product sprint review (process-gap).

## 2026-09-04 — Visible-outcome DoD: real end-to-end walkthrough required, not just green tests (LO-0051)

### Changed

- `process/iterative-delivery.md` — sprint plan Definition of Done requires that any ticket whose acceptance criteria is a **visible design/UX outcome** be verified by walking a real end-to-end scenario through the **default product flow**, with a before/after screenshot — not only green unit/QA tests.
- `process/human-in-the-loop.md` — Rule (LO-0051): a feature gated behind an unconfirmed or undiscoverable app state, or produced only by a code path the default flow never calls, counts as **not shipped** even with green gates. Sprint review means trying work through the same flow a real user reaches — not only reading `review.md`.
- Provenance: learning from a project sprint where gate-green tickets produced no visible change on the default path (`--source` on LO-0051).

## 2026-09-03 — Overlap check + mandatory scope-exclusions table in amendment intake (LO-0049, LO-0050)

### Changed

- `process/amendment-intake.md` — **Step 1.5 (overlap check)**: before drafting a new amendment, check `./studio amendments <project>` and existing `docs/amendments/*/01-vision-synthesis.md` for scope overlap; reconcile with a dormant approved amendment instead of drafting a parallel one.
- Mandatory **"Scope exclusions" table** in `02-requirements-addendum.md` (and surfaced in `10-approval-checklist.md`) for any requirement that freezes/excludes a system a reader would reasonably expect in scope.
- Provenance: LO-0049 / LO-0050 (`--source` on tickets).

## 2026-09-03 — Cross-surface acceptance + unread-field checks in amendment intake (LO-0048)

### Changed

- `process/amendment-intake.md` — agent obligations #8 and #9: before closing an amendment capability, re-check every promised **surface** (not only the last-tested one), and confirm newly authored frozen-type fields have at least one runtime reader before milestone review.
- Provenance: LO-0048.

## 2026-09-03 — Same-status ticket move must not unlink (LO-0047)

### Fixed

- `studio-tools/studio.py` `cmd_move` — when source and destination resolve to the same path (e.g. already `implement` → `implement`), update the ticket in place and **do not** `unlink()` after write (previously deleted the ticket)

## 2026-09-03 — Optional smoke skip for agent sandboxes (LO-0046)

### Changed

- `studio-tools/run_qa_gate.py` — `QUINSY_SKIP_SMOKE=1` skips Chromium smoke when the browser cannot launch (SIGSEGV / sandbox). Explicit opt-in only; local human runs leave unset.

## 2026-09-03 — Ticket ID allocation scans root backlog (LO-0045)

### Fixed

- `studio-tools/ticket_ids.py` — `scan_max_ticket_number` now includes root-level `backlog/{PREFIX}-*.md` (amendment-materialized / unscheduled tickets), not only `backlog/<status>/`
- Prevents `./studio ticket --from-feedback` from colliding with amendment-materialized IDs for any project prefix

### Added

- `studio-tools/test_ticket_ids.py` — root-level scan + allocate non-collision tests

## 2026-09-01 — Figma kit fidelity north-star DoD (LO-0044)

### Changed

- `knowledge-base/figma-plugin-host-networking.md` — kit fidelity DoD: north-star + screenshot; wireframe chrome fails
- `process/human-in-the-loop.md` — LO-0044 rule for professional / shadcn-class stickersheet tickets

## 2026-09-01 — Figma stickersheet inventory DoD (LO-0043)

### Changed

- `knowledge-base/figma-plugin-host-networking.md` — stickersheet DoD: section headlines alone are not done; assert inventory children on canvas
- `process/human-in-the-loop.md` — LO-0043 rule for kit / stickersheet placement tickets

## 2026-09-01 — Extension inbox sync port probe (LO-0042)

### Changed

- `knowledge-base/chrome-mv3-vite-content-scripts.md` — DoD: keep probing past plain-text wrong-app 404s until product JSON responds
- `process/human-in-the-loop.md` — LO-0042 rule for extension cloud-inbox multi-port sync

## 2026-09-01 — Figma localhost vs 127.0.0.1 prefs (LO-0041)

### Changed

- `knowledge-base/figma-plugin-host-networking.md` — localhost-only allowlist; `clientStorage` can override defaults with `127.0.0.1` and look like CSP failure
- `process/human-in-the-loop.md` — LO-0041 DoD: normalize API base to `localhost`; rebuild ≠ clear prefs

## 2026-09-01 — Component reuse ladder + right-rail dock pattern (LO-0040)

### Changed

- Rewrote LO-0040 as a **general** learning (was overfitted to one inspector surface)
- `process/learning-loop.md` — LO titles/proposals must state the general rule; `--source` is provenance only
- `knowledge-base/component-creation-playbook.md` — reuse ladder (reuse → project component → studio-library)
- `knowledge-base/frontend_playbook.md` — reuse ladder + right-rail dock organism
- `process/human-in-the-loop.md` — LO-0040 DoD generalized
- `process/project-archetypes.md` — saas-application UX option: right-rail nav + detail-rails
- `studio-library/ui/components/studio-rail/README.md` — pattern framing for cross-project reuse

## 2026-09-01 — Docked chrome DoD: edge + full height (LO-0039)

### Changed

- `process/human-in-the-loop.md` — LO-0039: reuse of `StudioPanel` / rails is not done on class-name reuse alone; require flush-edge + full-height live layout DoD
- `knowledge-base/frontend_playbook.md` — docked chrome reuse checklist (component + edge + height)

## 2026-08-31 — Design spec §2/§2c early + emoji mock scan (LO-0038, LO-0037)

### Changed

- `knowledge-base/design-spec-template.md` — LO-0038 callout: large mock packs still need §2 + §2c before approve-design
- `knowledge-base/design-system-compliance-checklist.md` — §2/§2c checklist item
- `studio-tools/design_ticket_helpers.py` — `design_mocks_emoji_icon_warning` (LO-0037)
- `studio-tools/studio.py` — `approve-design` warns on emoji-as-icon in mock HTML

## 2026-08-30 — No emoji-as-icons in mocks/UI (LO-0037)

### Changed

- `process/anti-slop.md` — Category 5b: emoji-as-icon banned in product UI and design-spec mocks; SVG / Icon components only
- `knowledge-base/design-system-compliance-checklist.md` — approve-design checklist item for no emoji + centered icons

## 2026-08-30 — Reuse: empty snapshot skip (LO-0036)

### Fixed

- `studio-tools/library_manager.py` — `check_reuse_before_done` returns clean when ticket has no implement snapshot (design-only done)
- `studio-tools/sprint_reuse_review.py` — skip empty snapshots so reuse review does not flag entire `packages/`

## 2026-08-29 — Canvas shell nested scroll (LO-0035)

### Changed

- `knowledge-base/frontend_playbook.md` — canvas `overflow-hidden` shells need nested scroll layouts for document routes; DialogShell tall-content pattern
- `process/human-in-the-loop.md` — LO-0035 rule

## 2026-08-29 — Review smoke surface match (LO-0034)

### Fixed

- `studio-tools/sprint_hitl.py` — Figma plugin smoke steps only for real plugin tickets; Brand kit / board tickets get webapp steps (not plugin OAuth defaults)
- `process/human-in-the-loop.md` — LO-0034 rule

## 2026-08-29 — Strategic feedback slicing (LO-0033)

### Changed

- `process/human-in-the-loop.md` — LO-0033: large review feedback → clarify + phase-aligned ticket slices (+ optional sprint roadmap) before next sprint; no mega-tickets

## 2026-08-29 — Brand-guide PDF WYSIWYG type DoD (LO-0032)

### Changed

- `knowledge-base/frontend_playbook.md` — PDF export DoD: screen and PDF must share the same type stack
- `process/human-in-the-loop.md` — LO-0032 rule for brand-guide / print WYSIWYG typography

## 2026-08-29 — Anti-slop dead-code regex (LO-0031)

### Fixed

- `studio-tools/validate_anti_slop.py` — “dead code after return” only matches same-indent statements (avoids nested JSX `return` false positives)

## 2026-08-29 — Feedback→ticket design brief infer (LO-0030)

### Changed

- `studio-tools/design_ticket_helpers.py` — `Design:` titles and Team 10 / in-context-mock scopes infer `ui-composition`
- `studio-tools/studio.py` — `--from-feedback` tickets infer type from title **plus** clarify scope/raw text

## 2026-08-29 — Sprint capacity 3–6

### Changed

- `process/human-in-the-loop.md` — sprints target **3–6** tickets; agents must not narrow proposals to 1–2 unless human asks for hotfix
- `studio-tools/sprint_backlog_validate.py` — `UNDER_CAPACITY` warning when sprint has fewer than 3 tickets

- 2026-09-14: LO-0232 infused — T0 edit-diff capture section added to knowledge-base/agentic-loop-playbook.md (edit distance as headline zero-traffic learning metric).
- 2026-09-14: LO-0233 infused — Quality ratchet section (error-analysis-first, judge discipline) added to knowledge-base/agentic-loop-playbook.md.
- 2026-09-14: LO-0234 infused — design lead-time rule + reject rubric added to knowledge-base/design_playbook.md; sprint-planning checklist updated in process/human-in-the-loop.md.
- 2026-09-14: LO-0238 infused — composer-executable contract made a sprint-entry requirement in process/ticket-workflow.md.
- 2026-09-14: LO-0239 infused — UI done requires commit+push to deploy-tracked branch (process/ticket-workflow.md).
- 2026-09-14: LO-0240 infused — push main on done when auto-deploy tracks it (same section).
- 2026-09-14: LO-0241 infused — manual pass in external render targets required before done (process/ticket-workflow.md).
- 2026-09-14: LO-0242 infused — shared model before parallel consumers (process/ticket-workflow.md).
- 2026-09-14: LO-0245 infused — batch IA design-track specs ahead of dependent feature work (knowledge-base/contextual-ia-playbook.md).
- 2026-09-14: LO-0246+LO-0248 infused — ticket state parity rule (process/gates.md); close receipt+gate+done in-session.
- 2026-09-14: LO-0249+LO-0250 infused — assertion sweep + literal verify rules (process/ticket-workflow.md).
- 2026-09-14: LO-0247 infused — symlinked layouts stay complete (knowledge-base/design_playbook.md).
- 2026-09-14: LO-0235 infused — sprint-planning-playbook.md authored (proof surface, truth before polish, disjoint file lists).
- 2026-09-14: LO-0251 infused — approve-scope reads scope-proposal.json; refresh after splitting an epic.
- 2026-09-14: LO-0252 infused — park parent epics with sprint_deferred before first scope proposal.
