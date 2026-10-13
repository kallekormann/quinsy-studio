# Studio HQ — autonomy program (PM, Engineering, Design, Growth)

> Studio-meta plan. Tickets `LO-0395` to `LO-0418` in `backlog/open/`. Nothing here writes into `projects/`.
> Companion to [hq-agency-agents-integration.md](hq-agency-agents-integration.md), which made the loop trustworthy. This program makes the loop **own the whole product** and stops the human only for product and design decisions.

## 1. Finding

Four read-only reviews of `.quinsy-studio/` agreed on one pattern: **the policy is written, the tooling does not drive it.**

| Area | Policy said | Tooling did |
|---|---|---|
| PM | Milestone roadmap for the whole product; milestone review when `Mn` is done; next milestone planned from that review | `approve --milestones` checked that `docs/phases/README.md` existed. Execute never looked at the roadmap and looped `retro → sprint` forever. Tickets existed for the active milestone only, and no checklist said what a finished product must contain |
| Engineering | Gate 5, receipt, fresh QA, finish gate before done | Checks ran only when `ticket.sprint == current_sprint`. QA PASS was self-signed. Native `<select>` and token literals were soft. No motion check. `ship --to main` pushed git and nothing else. No production access path; VPS posture was prose |
| Design | Learn ticket to ticket, milestone to milestone, project to project | Rejection reasons lived in product files only. No `approve-design --reject`. Feedback had severity, not a design taxonomy. HOLD and retro never harvested. Seven of nine UX skills had no Done evidence / Anti-patterns / Deltas, so infusion had nowhere to land |
| Growth | Drive usage inside the product; problem-first pages; one core message; organic discovery; fresh content | GD owned money pages, GM owned SEO/AEO/launch/email, PLG was an extension on GM-003. No in-app loop skill, no positioning artifact, no persona page program, no Posts model, GM-002 not a staffing companion |

## 2. Decisions

**Human stops (product and design decisions):** gate 0, gate 1, gate 2a, gate 2b, `approve-design --phase`, `milestone --approve`, `ship --to main --approve`, `ops migrate --prod --approve` and every destructive data step, abort, tech-veto.

**Agent-run with INFORM:** local `env up|migrate|dev`, `approve-arch --phase` (auto after the packet validator passes; one execute step of `TECH-VETO` window; `--reject` stays), cadence review (`ship --to dev` → `reality-check` → continue; the human reviews asynchronously with `feedback`).

**Production access:** SSH to the VPS and the Coolify API. The human sets the values in `projects/<p>/.env.local`. HQ names the variables (`./studio env <p> prod --explain`) and never reads a value.

**Three loops stay three:** ideation (`ideation/`, `intake/`), product (`projects/<p>/`), HQ learning (`.quinsy-studio/`). Positioning crosses from the desk to the product through the PRD only. Review files, ops logs and rejection reasons live under `projects/<p>/docs/`. `verify-worlds` and `verify-abstraction` stay green.

## 3. Waves

| Wave | LO | Scope |
|---|---|---|
| **W1 PM owns the whole product** | LO-0395–0398 | `knowledge-base/milestone-coverage-checklist.md`; `studio-templates/phases/milestone.md`; `approve --milestones` refuses missing coverage; `./studio milestone <p> plan\|review\|--approve\|plan --next` (`studio_milestones.py`); execute requires the roadmap after 2b and routes to `milestone review` when every `Mn` ticket is done; `cmd_sprint` refuses without an active milestone; PM CARD (PM-002, PM-004, PS-002, learnings READMEs); PM-002 rewritten to finish-the-project ownership |
| **W2a Done bar** | LO-0399–0401 | Receipt / QA / finish on every `move done`; native-select and token-literal hard at level 5 on UI tickets; QA verdict records the reviewer context and refuses the implementing session; reality `NEEDS WORK` files tickets; motion check from §2d; `## Skills read` with one applied rule per CARD file |
| **W2b Production path** | LO-0402–0404 | `compose.prod.yml` overlay; `./studio ops <p> readiness` writes `docs/ops/readiness.md` (PE-001 §6 as PASS/FAIL) and `ship --to main` refuses on FAIL; `env.schema.json` `prod` group; `env <p> prod --explain`; local `env` actions INFORM; `./studio ops <p> deploy\|logs\|status\|migrate --prod\|db\|cleanup` (`studio_ops.py`, HITL only on destructive); PE-001, PE-007, BE-002 point at the command |
| **W3 Design learns** | LO-0405–0408 | `approve-design --reject --reason <code>`; `revise` / `feedback` / `clarify` take `--design-reason`; HOLD, rejects and design feedback harvest as `design-gap/<code>`; retro `## Design`; UX-001–006, UX-008 on the skill template; `learnings/design/interaction.md`, `craft.md`; `SKILL_EXTRA_PLAYBOOKS` for UX-006/008/009; design specs carry `## Catalog applied` |
| **W4 Growth** | LO-0409–0414 | GD-004 in-product growth loops; GM-007 positioning and messaging; `12-positioning.md` and richer `02-personas.md` definitions, gate 0 refuses stubs; PRD positioning section; staffing rules (GD-004, GM-007, GM-002 with GM-001, GD-003 commercial); `growth-content-playbook.md`; in-app section in `growth-mechanics-playbook.md`; templates `growth-loop-map.md`, `persona-page-set.md`, `seo-foundation-pack.md`, `content-engine-pack.md`; Posts model in `payload-playbook.md`; coverage checklist lists them |
| **W5 Autonomy** | LO-0415–0418 | HITL matrix rewritten (`human-in-the-loop.md`, `AGENTS.md`, rules, `CLAUDE.md`, `studio-overview.md`); `approve-arch` auto with tech-veto; cadence INFORM; guard classifies HQ work as `STUDIO_META` even when it contains the word ideation; loop-separation checks; manuals and CHANGELOG |

## 4. How each team uses HQ knowledge

| Team | Where the knowledge is loaded | Where use is proven |
|---|---|---|
| PM | PM CARD on `milestone plan\|review`: skill files, team playbooks, `learnings/process/README.md`, domain READMEs | `Mn-review.md` cites PB ids; counted at `--approve` |
| Engineering | Execute CARD: skill files + playbooks | Receipt `## Skills read`: one applied rule per listed file; `trust_issues` fails blanks or files not on the CARD |
| Design | Design CARD: UX skills, `design-science-playbook.md`, `learnings/design/README.md` + topic files | Spec `## Catalog applied` with at least one PB id; `approve-design` refuses without it |
| Growth | GD/GM CARD: `growth-mechanics-playbook.md`, `growth-content-playbook.md`, PLG extension, marketing law | Receipt citations; persona page spec carries the positioning id |

## 5. Verification

Per wave: `python3 -m unittest discover -p 'test_*.py'` in `studio-tools`; `./studio verify-worlds`; `./studio verify-abstraction` (zero); `./studio lint-skills`; guard fixtures. A throwaway `projects/demo` tree (gitignored) from bootstrap to `milestone review`, deleted afterwards.
