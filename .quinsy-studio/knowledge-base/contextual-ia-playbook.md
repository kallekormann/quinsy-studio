# Contextual IA Playbook

> **Skill:** UX-003 (Information Architecture)  
> **When:** Before any UI spec that adds or moves a capability across surfaces.  
> **Not for:** Navigation chrome only — see nav audit below.

## Core question

**Given the user's intent and context, which surface is the natural home for this capability?**

Layout polish (width, spacing, tokens) comes **after** placement is decided.

---

## Context-of-use matrix

For each capability, answer:

| Dimension | Questions |
|-----------|-----------|
| **User intent** | What is the user trying to accomplish? (collaborate, present to client, configure, export, …) |
| **Mental model** | Which domain does this belong to? (board editing, sharing, presentation narrative, settings, …) |
| **Frequency** | Primary workflow vs occasional admin |
| **Audience** | Internal collaborator vs external guest vs owner |
| **Entry point** | Where does the user already be when they need this? |

### Example (generic)

| Capability | Wrong home | Right home | Why |
|------------|------------|------------|-----|
| Canvas read-only link | — | Share dialog | User is on board, wants to send canvas view |
| Client presentation link + guest access | Share dialog | Presentation builder | User is authoring narrative; guest settings are presentation context |
| Board delete | Share dialog | Board overflow / settings | Destructive board admin, not sharing |
| Collaborator invite | Share dialog | Share dialog (invite tab) | Collaboration intent matches share |

---

## Surface map (required deliverable)

For milestones with 3+ primary surfaces, maintain:

`projects/<project>/docs/ia/surface-map.md`

```markdown
# Surface map — <project>

| Surface | Primary intent | Capabilities (home) | Must NOT host |
|---------|----------------|---------------------|---------------|
| Board canvas | Edit content | tools, export trigger | guest link settings |
| Share dialog | Collaborate | canvas link, invite | presentation builder settings |
| Presentation builder | Author + ship client view | presentation link, guest access | canvas invite |
```

Update when amendments or new surfaces land.

---

## Anti-patterns

| Pattern | Symptom | Fix |
|---------|---------|-----|
| **Capability dumping ground** | One dialog/menu accumulates unrelated controls | Split by context-of-use; one primary intent per surface |
| **Duplicate entry points** | Same action in header + menu + dialog | Pick one primary; secondary only if workflow demands |
| **Layout-first tickets** | "Widen dialog" without placement review | Reframe as `ia-feature-placement` or add placement section to spec |
| **Nav-only IA** | UX-003 only audits top nav | Run contextual placement for feature tickets |
| **Spec inherits wrong placement** | Remediation copies old wireframes | Placement section must justify surface, not inherit |
| **Amendment IA over live product** (LO-0057 / LO-0059) | Sprint scopes UI to kit / guide slots while users already edit the capability on another surface | Confirm live home with HITL; update surface map; defer wrong-home tickets |
| **Mid-sprint pull without maturity** (LO-0058) | Feedback ticket enters current sprint and flags `IMMATURE_TICKET` | Fill ≥2 BDD AC + Scope (and design-approve if design-track) before `implement` — pull is OK; immature body is not |
| **Picker without presentation DoD** (LO-0063 / LO-0065) | Rail selection ships; presentation keeps a flat mid-page image list | Same epic (or paired ticket) must place imagery on the presentation surface with editorial layout quality before review |

## Live home vs amendment draft

Amendment `04-ui-ux-concept.md` / surface maps are **proposals**. Before a sprint commits UI to that placement:

1. Open the live product (or as-built notes) and ask: where does the user already expect this capability?
2. If live home ≠ amendment home, prefer the live home unless the amendment is explicitly superseding it (and HITL approved).
3. Record the decision in the ticket Scope / design spec §2 — not only in chat.

---

## Nav audit (traditional IA)

When **navigation** changes:

- Top-level items ≤ 7
- Max depth ≤ 3
- Run `design_math.ia_nav_audit` when available
- Document in design spec §3 IA

---

## Ticket types

| Type | UX-003 required | Deliverable |
|------|-----------------|-------------|
| `ia-navigation` | Yes | Nav map + metrics |
| `ia-feature-placement` | Yes | Surface map delta + placement rationale |
| `ui-composition` (multi-surface) | Yes | Context & placement section in design spec |
| `ui-composition` (single surface) | Recommended | Brief placement note |

---

## Design spec gate

Every design spec **must** include **§2 Context & placement** (see `design-spec-template.md`).

`./studio approve-design` warns if the section is missing or empty.

---

## Related

- [workflow-definition-playbook.md](workflow-definition-playbook.md)
- [design-spec-template.md](design-spec-template.md)
- [ticket-team-allocation.md](../process/ticket-team-allocation.md)
