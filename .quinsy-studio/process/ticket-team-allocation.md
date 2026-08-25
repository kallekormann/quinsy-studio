# Ticket team allocation

Every backlog ticket must declare **who owns the work** before implementation. Auto-matching from `./studio ticket` is a starting point only — the agent must verify allocation at groom time.

## Principle

| Ticket kind | Design phase (Team 10) | Implement phase (Team 01) |
|-------------|------------------------|---------------------------|
| **UI new component** | UX-001/002/005 + UX-006 | FE-001, FE-002, FE-004 after `approve-design` |
| **UI composition** | UX-002, UX-003, UX-006 | FE-001, FE-002 |
| **UI styling** (tokens, dark mode) | UX-006 review optional | FE-001, FE-002, UX-006, AI-002 |
| **Marketing page** | UX-007, UX-006, UX-005, GM-003 | FE-001, FE-002 after HITL |
| **Workflow explainer** | UX-007, UX-002, UX-001 | FE-001 after HITL |
| **IA / navigation** | UX-003 only | — (spec for gate 2 / milestone) |
| **IA / feature placement** | UX-003, UX-002 | FE-001 after `approve-design` (if UI moves) |
| **Canvas / interaction** | UX-002 as needed | FE-001, FE-002 |
| **API / data / auth** | — | `02-backend-systems` BE-001–BE-003 |
| **Email / integrations** | — | BE-005 |
| **Legal / privacy** | — | CL-001, CL-003 |
| **Architecture / ADR** | — | PS-002 |
| **Growth / copy** | UX-007 optional | GM-003 |
| **Process / studio** | — | SO-002 |

## Design HITL gate (mandatory)

Tickets with `ticket_type` in `ui-new-component`, `ui-composition`, `marketing-page`, `workflow-explainer`, `ia-navigation`, `ia-feature-placement`:

1. Team 10 writes `docs/design-specs/<TICKET>.md` (template: `knowledge-base/design-spec-template.md`)
2. Spec includes **§2 Context & placement** + **Atomic Inventory** + **Design Rationale**
3. Multi-surface: workflow map per `workflow-definition-playbook.md`
4. Human: `./studio approve-design <project> <ticket-id>` (warns if §2 missing)
5. `./studio move … implement` is **blocked** until `design_status: approved`

`ui-styling` tickets skip design HITL but still require FE-001 + FE-002 + UX-006 + AI-002 on implement.

## Skill loads by phase

| Phase | Command | Load |
|-------|---------|------|
| Design | `./studio move … design` (or groom assigns Team 10) | UX skills per `ticket_type`; `contextual-ia-playbook.md`; `workflow-definition-playbook.md` when multi-surface; aesthetic preset + `brand-guardian-checklist.md` |
| Approve | `./studio approve-design` | Human only |
| Implement | `./studio move … implement` | FE-001, FE-002; FE-004 if color/a11y; `./studio library pull` |

## Library-first rule

Before custom markup:

```bash
./studio library list
./studio library suggest <project> "<feature>"
./studio library pull <project> dialog button card dropdown-menu
```

**Tailwind + Headless UI required** for all UI implement tickets. Read [ui/docs/README.md](../studio-library/ui/docs/README.md).


New atoms/molecules → `component-creation-playbook.md` → studio-library first.

## Ticket frontmatter (UI example)

```yaml
team: 10-product-design-experience
ticket_type: ui-new-component
design_status: pending
design_spec: docs/design-specs/TICKET-0100.md
skills: [UX-002, UX-005, UX-006, AI-002]
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
- [ ] Team 10 skills for design; Team 01 for implement (after approval)
- [ ] Atomic inventory lists library pulls vs new studio-library work
- [ ] §2 Context & placement filled for UI tickets (not layout-only placeholders)
- [ ] `./studio groom --approve` only after skills are explicit

## Related

- [contextual-ia-playbook.md](../knowledge-base/contextual-ia-playbook.md)
- [workflow-definition-playbook.md](../knowledge-base/workflow-definition-playbook.md)
- [design-system-compliance-checklist.md](../knowledge-base/design-system-compliance-checklist.md)
- [studio-abstraction.md](studio-abstraction.md)

- [skill-registry.md](../teams/skill-registry.md) — Team 10 UX-001–UX-007
- [human-in-the-loop.md](human-in-the-loop.md) — `approve-design`
- [component-creation-playbook.md](../knowledge-base/component-creation-playbook.md)
