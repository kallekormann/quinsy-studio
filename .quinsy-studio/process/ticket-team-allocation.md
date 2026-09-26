# Ticket team allocation

Every backlog ticket must declare **who owns the work** before implementation. Auto-matching from `./studio ticket` is a starting point only — the agent must verify allocation at groom time.

## Principle

| Ticket kind | Design phase (Team 10) | Implement phase (Team 01) |
|-------------|------------------------|---------------------------|
| **UI new component** | UX-001/002/005 + UX-006 | FE-001, FE-002, FE-004, FE-007 after `approve-design` |
| **UI composition** | UX-002, UX-003, UX-006 | FE-001, FE-002, FE-007 |
| **UI styling** (tokens, dark mode) | UX-006 review optional | FE-001, FE-002, UX-006, AI-002 |
| **Marketing page** | UX-007, UX-006, UX-005, **GD-001, GD-002**, GM-003 if public URL | FE-001, FE-002 after `approve-design` |
| **Pricing / checkout / PLP / PDP** | Same as marketing or `ui-composition` + **GD-001, GD-002** | FE after `approve-design` |
| **Workflow explainer** | UX-007, UX-002, UX-001 | FE-001 after `approve-design` |
| **IA / navigation** | UX-003 only; `./studio ia-audit` | — (spec for gate 2 / milestone) |
| **IA / feature placement** | UX-003, UX-002 | FE-001 after `approve-design` (if UI moves) |
| **Canvas / interaction** | UX-002 as needed | FE-001, FE-002 |
| **API / data / auth** | — | `02-backend-systems` BE-001–BE-003 |
| **Jobs / queues / outbox** | — | BE-006 |
| **Email / integrations** | — | BE-005 |
| **AI adapter / eval / RAG** | — | AI-001, AI-004 (`## Eval` on receipt) |
| **Durable agent jobs** | — | AI-003 (not PE-002) |
| **Legal / privacy** | — | CL-001, CL-003 |
| **Architecture / ADR** | — | PS-002 |
| **Growth / copy** | UX-007 optional; **GD-001** if experiment | GM-003 (SEO/AEO copy); Team 11 for hypothesis |
| **Process / studio** | — | SO-002 |

## Design-track HITL (major UX / UI / IA)

Tickets with `ticket_type` in `ui-new-component`, `ui-composition`, `marketing-page`, `workflow-explainer`, `ia-navigation`, `ia-feature-placement`:

1. Team 10 **writes** `docs/design-specs/<TICKET>.md` (template: `knowledge-base/design-spec-template.md`). Ticket create may drop a **stub**; a stub is not approvable. Never tell the human to review a path that is not filled.
2. Spec includes **§2 Context & placement** + **§2c in-context mocks** (HTML under `docs/design-specs/mocks/<TICKET>/`, **this project's CSS tokens**, **all states**) + **Atomic Inventory** + **Design Rationale**
3. Multi-surface: workflow map per `workflow-definition-playbook.md`
4. Human: `./studio approve-design <project> <ticket-id>` — CLI **fails** if spec/mocks/tokens/states are incomplete. `ia-navigation` also requires `./studio ia-audit` pass (≤7 top-level, depth ≤3).
5. `./studio move … implement` is **blocked** until `design_status: approved`

Execute: if the spec or mocks are missing, ACTION is **IMPLEMENT (write deliverables)** — not HITL. HITL `approve-design` only when the files would pass the CLI gate.

Prefer a **design sprint** (or a design slice of scope) for these tickets. Do not mix “invent a new atom” into a feature sprint.

**Stay on the system:** `feature`, `bug`, `ui-styling` tickets only compose **already approved** library components and gate-2 tokens. If a component/token/pattern is missing, **split a design-track ticket** — do not one-off CSS.

**Rule (LO-0213 / LO-0218 / LO-0220 / LO-0222):** At ticket create/clarify, create `docs/design-specs/<TICKET>.md` (do not share one spec across tickets). Lock **§2 + §2c** before `./studio sprint --approve-scope` for design-track types.

`ui-styling` tickets skip design HITL but still require FE-001 + FE-002 + UX-006 + AI-002 on implement.

**Rule (LO-0184 — do not over-classify polish as design-track):** Copy cleanup, icon-size parity, removing leftover helper cards, and checkbox chrome on existing atoms are usually `ui-styling` or `bug` with `design_status: n/a`. Mis-tagging them as `ui-composition` / `ui-new-component` still forces a Team 10 spec for work that already has a shipped component. At groom: set explicit `ticket_type` + `design_status: n/a` when no new composition or atom is introduced.

**Rule (LO-0197 — split visitor-tool vs editorial “go to comparison” labels first):** When a shop/catalog **shortlist** control uses the same verb as **open an editorial comparison article**, rename the shortlist (add / already-in-set) **before** adding catalog checkboxes or other bulk-select chrome. Keep the editorial cue on article links only. Copy-only label splits stay `ui-styling` / `design_status: n/a` unless layout changes.

## Skill loads by phase

| Phase | Command | Load |
|-------|---------|------|
| Design | `./studio move … design` (or groom assigns Team 10) | UX skills per `ticket_type`; CARD playbooks: product-ux, interaction-ux, contextual-ia, design-science, **design-direction** at 2a; `workflow-definition-playbook.md` when multi-surface; aesthetic preset **optional**; `brand-guardian-checklist.md`; **commercial surfaces:** `growth-mechanics-playbook.md` + GD-001/GD-002 |
| Approve | `./studio approve-design` | **HITL** for design-track only |
| Implement | `./studio move … implement` | FE-001, FE-002; FE-004 if color/a11y; `./studio library pull` — stay on tokens |

## Library-first rule

Before custom markup:

```bash
./studio library list
./studio library suggest <project> "<feature>"
./studio library pull <project> dialog button card dropdown-menu
```

**Tailwind + Headless UI + kit peers required** for all UI implement tickets. Product app: `radix-ui`, `class-variance-authority`, `clsx`, `tailwind-merge`, `lucide-react`. Read [ui/docs/README.md](../studio-library/ui/docs/README.md) and `docs/setup/ui-kit.md`.


New atoms/molecules → `component-creation-playbook.md` → studio-library first.

## Ticket frontmatter (UI example)

```yaml
team: 10-product-design-experience
ticket_type: ui-new-component
design_status: pending
design_spec: docs/design-specs/TICKET-0100.md
skills: [UX-002, UX-005, UX-006, AI-002]
executable_by: composer   # composer | opus | human — see ticket-authoring-playbook.md
```

After approval:

```yaml
design_status: approved
design_approved_at: 2026-08-23 12:00
team: 01-frontend-experience
skills: [FE-001, FE-002, FE-004, UX-006, AI-002]
```

## Grooming checklist

- [ ] `ticket_type` set (auto on `./studio ticket` or manual)
- [ ] Design-track tickets have `design_spec` path
- [ ] Team 10 skills for design; Team 01 for implement
- [ ] Atomic inventory lists library pulls vs new studio-library work
- [ ] §2 Context & placement filled for UI tickets (not layout-only placeholders)
- [ ] No **XL** tickets in sprint — split (≤8 files, ≤400 lines)
- [ ] Verify commands are **literal** with expected output (not “tests pass”)
- [ ] Shared names are **verbatim artifacts**; later tickets quote earlier ones
- [ ] `executable_by: composer|opus|human` set when a small/fast model will implement
- [ ] `./studio groom --approve` only after skills are explicit

## Related

- [contextual-ia-playbook.md](../knowledge-base/contextual-ia-playbook.md)
- [workflow-definition-playbook.md](../knowledge-base/workflow-definition-playbook.md)
- [design-system-compliance-checklist.md](../knowledge-base/design-system-compliance-checklist.md)
- [studio-abstraction.md](studio-abstraction.md)

- [skill-registry.md](../teams/skill-registry.md) — Team 10 UX-001–UX-007; Team 11 GD-001–GD-002
- [human-in-the-loop.md](human-in-the-loop.md) — design-track `approve-design`; other tickets stay on the design system
- [component-creation-playbook.md](../knowledge-base/component-creation-playbook.md)
- [ticket-authoring-playbook.md](../knowledge-base/ticket-authoring-playbook.md) — small-model contract (F1–F6)
