# Studio HQ — agency-agents integration plan

> Source: [msitarzewski/agency-agents](https://github.com/msitarzewski/agency-agents) (MIT), shallow clone of 2026-10-08.
> Read in full: Engineering (65), Design (10), Product (6), Marketing (37), Project Management (7), Testing (9), Security (12), plus `specialized/agents-orchestrator.md`, `specialized/specialized-workflow-architect.md`, `strategy/`, `examples/` and the repo's lint scripts.
> **Not a product milestone.** This plan stays `studio_meta`. Tickets become `LO-*` items once the human approves the plan.

**Policy**

1. **Embed, do not subscribe.** Copy rules, templates and checks into our skill files, playbooks and studio tools. Do not install agent files or add an external-skill source.
2. **No personas.** Drop identity, voice, emoji and "vibe" sections. Keep rules, deliverable templates and checks. An evaluator keeps one stance line (for example "default verdict FAIL without evidence").
3. **Rewrite for our stack and law.** Payload is the only auth and ORM. Postgres, Compose, Coolify. German and EU law replaces US frames (BFSG instead of Section 508, UWG §7 instead of CAN-SPAM, DSGVO Art. 33 for breaches).
4. **Drop invented numbers.** Most agents cite unsourced statistics and universal thresholds. Keep a number only if it is a published standard (Core Web Vitals, WCAG, mailbox-provider sender rules).
5. **A check beats a sentence.** When a rule can be checked by `run_qa_gate.py`, receipt validation or a gate validator, write the check.

---

## 1. How agency-agents works, and how it differs from our loop

The orchestrator and NEXUS pipeline are **markdown instructions only**. There is no state machine, no retry counter and no gate in code. The pipeline is: senior PM writes a task list, ArchitectUX writes a foundation, then a developer and an evidence QA agent loop per task (PASS or FAIL, at most 3 attempts), then a Reality Checker certifies the whole system and defaults to NEEDS WORK.

What the repo enforces in CI is the **format of agent files**: frontmatter fields, an originality check (no new agent may overlap an old one by 40% or more), and that the division and tool lists match the folders. Nothing checks that a run followed the pipeline.

Our studio is the reverse. `./studio execute` is a real driver in code with typed human stops, gate level 5 and a retry counter. Our weak point is that **the agent that writes the code also signs its own QA**: `receipt_issues` only checks that headings are not empty, so an untouched receipt stub passes.

| | agency-agents | Quinsy Studio |
|---|---|---|
| Driver | Prose orchestrator | `studio_execute.py` state machine |
| Roles | 230+ personas | One session, skill IDs on a card |
| QA | Separate evidence agent, PASS/FAIL per task | Gate level 5 plus a self-written receipt |
| Retries | "Max 3" in prose | `MAX_GATE_RETRIES = 3`, counted from the log |
| Evidence | Screenshots demanded, never checked | Screenshot path named, never checked |
| Handoffs | 7 rich templates | Compact card; no consumes/produces |
| Human stops | Few; AI gatekeepers | Typed HITL at gates, phases, cadence, ship |
| Consistency | CI lints agent files | Three hand-synced skill indexes, no lint |

**What we take from them:** an independent QA verdict that defaults to FAIL, evidence files that must exist, structured fail feedback, a workflow registry, handoff fields, and a lint for skill files.
**What we do not take:** personas, AI gatekeepers in place of human gates, universal thresholds, unsourced statistics, copy-paste handoffs, LLM-interpreted memory rollback.

---

## 2. Verdicts by division

Full per-agent notes live in the review transcripts. This table lists what is worth embedding. Everything not listed is a skip: off-stack platforms (WordPress, Drupal, WeChat, Feishu, GaussDB, ServiceNow, Solidity, embedded, network), China-platform marketing, enterprise-scale roles (studio producer, threat intel, SOC detection, compliance auditor, pentest), and persona-only files (senior developer, UI designer, content creator, whimsy injector).

### Engineering

| Agent | Verdict | Target |
|---|---|---|
| Payments & Billing Engineer | **New skill** | BE-008 Payments and billing |
| PDF Engine Architect (+ Universal Document Compiler print rules) | **New skill** | BE-009 Document generation (PDF, XRechnung/ZUGFeRD, GoBD) |
| i18n Engineer | **New skill** | FE-008 i18n and localization |
| Minimal Change Engineer | Loop | Receipt `## Scope` section |
| Code Reviewer | Loop | QA review severity taxonomy; AI-002 report format |
| Multi-Agent Systems Architect | Loop + enhance | QA loop exit rules; AI-003 |
| Database Reliability Engineer | Enhance | BE-002 expand/contract, PE-001 restore drills |
| Database Optimizer | Enhance | BE-002 |
| Privacy Engineer | Enhance | CL-004 data map and erase-everywhere |
| Identity & Access Engineer | Enhance | BE-003 |
| Section 508 Specialist (reframed to BFSG / EN 301 549) | Enhance | FE-004 |
| Prompt Engineer | Enhance | AI-001, AI-004 |
| Autonomous Optimization Architect, FinOps | Enhance | AI-001 LLM cost guardrails |
| RAG Pipeline Engineer | Enhance | AI-004 (pgvector, German full-text) |
| Backend Architect, API Platform Engineer | Enhance | BE-001 one error shape, compatibility table; BE-004 timeouts |
| Software Architect | Enhance | PS-002 trade-offs and reversibility |
| SRE, Incident Response Commander | Enhance | PE-007 |
| CMS Developer, Filament Optimization | Enhance | BE-007 admin form layout, cms-migration |
| AI Data Remediation Engineer | Enhance | cms-migration reconciliation and quarantine |
| Technical Writer, Codebase Onboarding Engineer | Enhance | SO-004, brownfield `adopt` as-built docs |
| Developer Tooling Engineer | Enhance | ✅ SO-001 rules for the `./studio` CLI; `test_cli_help.py` (done 2026-10-13) |
| WordPress/Drupal Performance, cart agents | Enhance (rules only) | FE-003 never cache private pages; BE-008 commerce rules |
| Data Visualization Engineer | Extension | `skill-extensions/data-visualization.md` |
| ATS Validator | Enhance (rules only) | PS-004 EU AI Act check; AI-002 no invented metrics |
| Mobile release, desktop app | Park | Only when a native archetype exists |

### Design and Product

| Agent | Verdict | Target |
|---|---|---|
| UI Finish-Gate Reviewer | **New skill** | UX-009 UI finish gate |
| Persona Walkthrough | **New skill** | GD-003 Persona walkthrough |
| Product Manager | Enhance | Intake PRD and gate 0 (press release, non-goals, metric table, pre-mortem); PM-002 "not building" list |
| DX Engineer | Enhance | UX-002 and BE-004 error-message rubric |
| Image Prompt Engineer + Inclusive Visuals | Enhance | ✅ UX-007 generated imagery: brief per image, real audience only, product screens captured, provenance log and AI label (done 2026-10-13) |
| Behavioral Nudge Engine | Enhance (rules only) | UX-002 notifications; strip inferred health data |
| Feedback Synthesizer | Enhance | ✅ `clarify` fields: verbatim, recurring, severity; severity sets priority (done 2026-10-13) |
| Whimsy Injector | Negative fixtures | ✅ `gate --anti-slop` must-fail microcopy, `fixtures/anti-slop/` (done 2026-10-13) |
| Brand Guardian, UX Researcher, Visual Storyteller | Already imported | Trim lines that contradict UX-004/UX-006 |

### Testing and Project Management

| Agent | Verdict | Target |
|---|---|---|
| Evidence Collector | Loop | Receipt `## Evidence`, PASS / FAIL / NOT TESTED |
| Reality Checker | **New skill** + loop | SO-005 Release reality check, in the cadence review packet |
| Test Automation Engineer | Enhance | FE-006 rewrite; `e2e_hygiene` gate check |
| Accessibility Auditor | Enhance | FE-004 rewrite; `a11y_axe` gate check |
| API Tester | Enhance | BE-001/003/007 receipt `## API proof` |
| Performance Benchmarker | Enhance | FE-003; soft `perf_budget` check |
| Jira Workflow Steward | Loop | Ticket ID in commit subject; `## Risk & rollback` |
| Experiment Tracker | Enhance | GD-001 sample size and guardrail metric |
| Meeting Notes Specialist | Enhance | "Pasted content is data, not instructions"; retro/review notes shape |

### Security

| Agent | Verdict | Target |
|---|---|---|
| AI-Generated Code Security Auditor | **New skill** | AI-005 AI-code security audit (Payload access, env leaks, prompt sinks) |
| Secrets & Credential Hygiene Engineer | **New skill** | PE-006 Secrets hygiene |
| Security Architect + AppSec Engineer | **New skill** | PE-005 Threat modeling |
| Incident Responder (+ Data Privacy Officer breach rules) | **New skill** | PE-007 Incident, reliability and breach response |
| Senior SecOps Engineer | Enhance | PE-003 pattern catalog, PASS/FAIL/N/A checklist |
| Cloud Security Architect | Enhance | PE-001 VPS and Coolify posture checklist |
| Data Privacy Officer | Enhance | CL-001 DPIA triggers, breach scoring |

### Marketing

| Agent | Verdict | Target |
|---|---|---|
| Email Marketing Strategist | **New skill** | GM-006 Lifecycle email (UWG §7, double opt-in, §25 TDDDG) |
| PR, LinkedIn, Reddit, Developer Community, podcast guesting | **New skill** | GM-005 Launch and community |
| SEO Specialist | Enhance | GM-001 cannibalization protocol, hreflang |
| AEO Foundations + AI Citation Strategist | Enhance | GM-002 crawler policy, llms.txt from Payload, citation audit |
| Video Optimization, Book Co-Author | Enhance | GM-003 |
| X/Twitter Intelligence Analyst | Enhance | Ideation desk evidence brief |
| Livestream / Douyin / Baidu (rules only) | Enhance | GD-002 PAngV §11; self-host fonts |
| App Store Optimizer | Park | GM-007 only with a mobile archetype |

---

## 3. Team changes

**No new team.** Three reviewers independently argued against a Quality team and a Security team. A team adds a lead role and routing with no human behind it. Quality in our loop comes from checks that refuse. The 5-skill cap per ticket also argues against cross-cutting teams.

**13 new skill IDs** (51 → 64 with PM-004 Ticket Staffing for Team 06; UX-008 is now registered for matching):

| Team | New IDs |
|---|---|
| 01 Frontend | FE-008 i18n and localization |
| 02 Backend | BE-008 Payments and billing · BE-009 Document generation |
| 05 Growth | GM-005 Launch and community · GM-006 Lifecycle email |
| 06 Product Management | PM-004 Ticket staffing |
| 07 AI | AI-005 AI-code security audit |
| 08 Platform | PE-005 Threat modeling · PE-006 Secrets hygiene · PE-007 Incident, reliability and breach response |
| 09 Studio Ops | SO-005 Release reality check |
| 10 Product Design | UX-009 UI finish gate |
| 11 Growth Design | GD-003 Persona walkthrough |

**One new extension:** `skill-extensions/marketing-law.md` under Team 03 (UWG §§5, 5a, 6, 7; fake reviews; §25 TDDDG; PAngV §11; tell-a-friend invites).

**Revisit a separate team** when security or QA passes six skills, needs its own sprint kind, or a second human joins as reviewer.

---

## 4. Loop changes

| # | Change | Where |
|---|---|---|
| L1 | ✅ **Receipt hardening.** Reject untouched stub text; screenshot paths must exist; results are PASS / FAIL / NOT TESTED; a missing `smoke-routes.json` or `QUINSY_SKIP_SMOKE` is NOT TESTED, not a pass | `receipt_checks.py` (`section_is_stub`, `trust_issues`), `studio_execute.write_receipt_stub`, `run_qa_gate` NOT TESTED (done 2026-10-12) |
| L2 | ✅ **Independent QA verdict.** New `QA_REVIEW` action after a green gate and before `MOVE_DONE`. A fresh-context subagent gets the card, diff, receipt and evidence only, judges against AC and Verify, defaults to FAIL without evidence, and writes `sprints/SPRINT-NN/qa/<TICKET>.md`. A FAIL counts toward the same 3 retries | `qa_review.py`, `./studio qa <p> <T> [--verdict PASS\|FAIL]`, execute `QA_REVIEW`; move done refuses without a QA PASS (done 2026-10-12) |
| L3 | ✅ **Structured fail feedback.** Debug file in Issue / Expected / Actual / Evidence / Fix / Files form; "fix only these". Escalate early when two attempts fail the same way. At 3 fails write an escalation packet, move the ticket to `blocked`, continue with independent siblings | `studio_execute.append_debug_attempt`, `write_escalation`, execute `BLOCK`; HITL `blocked-retries` only when nothing else can run (done 2026-10-12) |
| L4 | ✅ **Security gate checks.** `secret_scan`, `client_env_leak`, `insecure_env_fallback`, `docker_secret_leak` at level 2; `payload_access`, `local_api_override`, `webhook_signature`, `npm_audit_policy` at level 5; `llm_sink`, `sensitive_log`, `security_headers` as warnings | `security_checks.py` + `run_qa_gate.py`; waivers only in `docs/security/exceptions.md` with an expiry (done 2026-10-12) |
| L5 | ✅ **Quality gate checks.** `a11y_axe`, `e2e_hygiene`, `api_contract`; `perf_budget` as soft | `quality_checks.py` + `run_qa_gate.py` (done 2026-10-12) |
| L6 | ✅ **Receipt sections by skill.** `## Evidence` (UI), `## A11y` (UI), `## API proof` (BE-001/003/007), `## Security` (all), `## Threat delta` (triggered), `## Risk & rollback` (migrations, auth, infra), `## Scope` (all, with "follow-ups noted, not done") | `receipt_checks.required_sections`, `stub_sections` (done 2026-10-12) |
| L7 | ✅ **Threat delta per ticket** in the architecture phase, or `threat delta: none`. Project threat model and data map at gate 1 | `architecture_checks.py` (`gate_1_security_issues`, `threat_delta_issues`), `validate_gate_1`, `approve-arch` (done 2026-10-12) |
| L8 | ✅ **Workflow registry.** `docs/workflows/REGISTRY.md` at gate 1 (journeys and states); `WORKFLOW-*.md` per flow-shaped ticket in the architecture phase; branch test cases become `TC-nn` acceptance criteria | `architecture_checks.py` (`gate_1_workflow_issues`, `workflow_issues`) (done 2026-10-12) |
| L9 | ✅ **Design loop.** Five-second test on every design packet; persona walkthrough appendix on commercial packets; UX-009 finish gate (PASS / HOLD at 1440 and 390, with a Keep list) before `MOVE_DONE` on UI tickets, comparing the shipped screen with the signed real-UI mock screenshots. HOLD counts as a fail, not a new human stop | `design_ticket_helpers.design_spec_walkthrough_error` (approve-design), `qa_review` finish gate, `./studio qa <p> <T> --finish [PASS\|HOLD]`; move done refuses without it (done 2026-10-12) |
| L10 | ✅ **Gate 0 PRD.** Press-release paragraph, non-goals, metric table (baseline, target, window; unknown stays unknown), pre-mortem | `process_intake.prd_frame` / `prd_frame_issues` (`## Gate 0 frame`), `validate_gate_0` (done 2026-10-12) |
| L11 | ✅ **Reality check before cadence review.** After `ship --to dev`: one end-to-end journey, re-check of every done ticket's default-flow claim, automatic-fail triggers, verdict defaulting to NEEDS WORK. FAILED files debug tickets instead of asking for sign-off | `reality_check.py`, `./studio reality-check`, execute `REALITY_CHECK` before the cadence HITL; line at the top of `review.md` (done 2026-10-12) |
| L12 | ✅ **Pre-ship to main.** Git-history secret scan, secrets inventory complete, incident runbook present, no expired security exceptions, database ports not published | `ship_checks.py`, `ship --to main` (done 2026-10-12) |
| L13 | ✅ **Skill template and lint.** One template (frontmatter, Mission, Rules, Workflow, Deliverables, Done evidence, Anti-patterns, Handoff, Deltas). `lint_skills.py` keeps `skill_matcher`, `ticket_helpers` and `skill-registry.md` in sync | `lint_skills.py`, `./studio lint-skills [--strict]`, `knowledge-base/skill-template.md`; template gaps are warnings until the old skills are migrated (LO-0394) (done 2026-10-12) |
| L15 | ✅ **Ticket staffing (PM-004), done 2026-10-12.** Audit: skills came from title keywords only, substring matching (`ai` hit `email`, `main`, `detail`; `test` hit `latest`), no groom check, and the CARD never pointed at skill files. On one product's 11 tickets only 3 of 11 teams were ever staffed; no ticket had FE-004, FE-006, PE-003 or CL-001. Now: whole-word triggers; `staff_skills` adds companions from Target/Scope/AC with a reason (`## Staffing`); groom errors `SKILLS_MISSING` / `SKILL_UNKNOWN` / `STAFFING_GAP`; the CARD adds missing required companions and lists skill files; `test_staffing.py` keeps IDs, roles and files in sync | `skill_matcher.py`, `sprint_backlog_validate.py`, `studio_execute.staff_card`, Team 06 |
| L14 | ✅ **Retro metrics.** First-pass gate rate per check, average retries, QA fails, blocked tickets, from `execution-log.json` | `retro_metrics.py`, `sprint_hitl.prepare_retro` (`## Loop metrics`) (done 2026-10-12) |

---

## 5. Fixes found during the review (do first)

| Fix | File |
|---|---|
| ✅ **Real-UI mocks (human requirement).** A mock the human can sign looks exactly like the implemented app with the design solution woven in. One client `page.tsx` at `app/(design-mocks)/design-mocks/<TICKET>/` imports the real shell or view and real components and mounts `mock-scenario-panel` (`?state=`); nested `<state>/page.tsx` folders fail the packet. `(design-mocks)/layout.tsx` 404s in production; screenshots of every state, newer than the mock code, sit in `docs/design-specs/mocks/<TICKET>/`. `approve-design` refuses standalone HTML, folder-per-state packets, mocks without the panel, mocks without app or shell imports, inline styles, hex or arbitrary colours, and missing or stale screenshots. UX-009 (L9) later compares the shipped screen against these screenshots | `design_ticket_helpers.design_mocks_interactive_error`, `design_mocks_real_ui_error`, design-spec template §2c, Team 10 docs (done 2026-10-13) |
| ✅ Template `Users`/`Media` access was incomplete (any logged-in user could update or delete users); signup could not create users; secrets fell back to `''` | `studio-templates/payload/app/src/` (fixed 2026-10-12) |
| ✅ Billing package: Stripe webhook had no timestamp tolerance and read one `v1` only; checkout did not carry the Payload user ID | `studio-library/packages/billing/` (fixed 2026-10-12) |
| ✅ BE-002 still mentions `supabase start` and hosted-Auth `auth_user_id`; UUID rule vs Payload serial IDs | `02-backend-systems/skills/database-design.md` |
| ✅ Vendored Payload skill examples use `mongooseAdapter`; add a Postgres override note (do not edit the vendored file, refresh overwrites it) | `knowledge-base/payload-playbook.md` |
| ✅ PE-002 rollback says "run migration down"; replace with forward-fix and expand/contract | `08-platform-enterprise-engineering/skills/ci-cd-pipelines.md` |
| ✅ CL-003 cites § 55(2) RStV and the TMG; now § 18(2) MStV and § 5 DDG | `03-compliance-legal/skills/impressum-agb.md` |
| ✅ BE-001 and BE-004 use different error shapes; settle on `{code, message, details, request_id}` | BE-001, BE-004 |
| ✅ BE-003 password rules contradict NIST (composition rules, reuse history) | BE-003 |
| ✅ Prompt-injection points to PE-003, which has no prompt-injection content; point to AI-005 | AI-001, AI-003, AI-004, ai playbook |
| ✅ GM-001 "FAQPage for rich snippets" is outdated since 2023 | GM-001 |
| ✅ Imported agent copies contradict UX-004/UX-006 (invented demographics, made-up metrics, competing brand tokens) | `10-product-design-experience/agents/` |
| ✅ UX-008 missing from the registry trigger table and skill count | `skill-registry.md`, `skill_matcher.py` |
| ✅ Archetype stack rows still name Shopify/Medusa/WooCommerce and React Native; reconcile with Payload and PWA | `process/project-archetypes.md` |
---

## 6. Sprints

Each sprint is one HQ session: skill and playbook text, studio-tool checks with tests, CHANGELOG, then move the LO to `backlog/done/`.

| Sprint | Scope | Why this order |
|---|---|---|
| ✅ **S0 Fixes** | Section 5 | Wrong guidance is live today |
| ✅ **S1 Loop trust** | L1, L2, L3, L6 (`Evidence`, `Scope`) | Every later check depends on receipts that cannot be faked |
| ✅ **S2 Security** | PE-005, PE-006, PE-007, AI-005; L4, L7, L12; PE-003 and PE-001 enhancements; CL-004 data map | AI-written Payload code is the most likely real breach |
| ✅ **S3 Quality** | FE-006, FE-004, FE-003 rewrites; SO-005; L5, L11; BE `API proof` | Turns QA prose into gate checks |
| ✅ **S4 Design and product** | UX-009, GD-003; L9, L10; error-message rubric; imagery; anti-slop fixtures; clarify fields | Closes the gap between signed mock and shipped screen |
| ✅ **S5 Backend and commerce** | BE-008, BE-009, FE-008; BE-007 admin layout; private-page caching rule; BE-002 reliability; BE-003 identity; AI-001/AI-004 cost and prompt rules | Needed by the first SaaS or shop that bills |
| ✅ **S6 Growth** | GM-005, GM-006; GM-001/GM-002 rewrites; marketing-law extension; launch playbook and ticket templates; retire the bloomprotocol subscription | Launch work after the product loop is trustworthy |
| ✅ **S7 Consistency** | L8 workflow registry, L13 skill template and lint, L14 retro metrics; CLI rules for `./studio` | Structural; safe once the content has settled |
