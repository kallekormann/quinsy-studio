# Ticket team allocation

Every backlog ticket must declare **who owns the work** before implementation. Auto-matching from `./studio ticket` is a starting point only — the agent must verify allocation at groom time.

## Principle

| Ticket kind | Primary team | Required skills (load before coding) |
|-------------|--------------|-------------------------------------|
| **UI / visual** (components, layout, dark mode, polish) | `01-frontend-experience` | FE-001 UI Component Design, FE-002 Design System; read `design/prototype` + project tokens |
| **Canvas / interaction** | `01-frontend-experience` | FE-001, FE-002; read `docs/definitions/10-canvas-interactions.md` |
| **API / data / auth** | `02-backend-systems` | BE-001–BE-003 as applicable |
| **Email / integrations** | `02-backend-systems` | BE-005 Third-Party Integrations |
| **Legal / privacy** | `03-compliance-legal` | CL-001, CL-003 |
| **Architecture / ADR** | `04-product-strategy-architecture` | PS-002 Architecture Decisions |
| **Growth / copy** | `05-growth-marketing-content` | GM-003 Content Strategy |
| **Process / studio** | `09-studio-operations-evolution` | SO-002 Process Optimization |

## UI tickets — design gate (mandatory)

Tickets that touch **visible UI** (new components, styling, layout, themes) must:

1. Set `team: 01-frontend-experience` in frontmatter
2. List skills: `FE-001`, `FE-002` (and `FE-004` if contrast/a11y)
3. Agent loads before implement:
   - `teams/01-frontend-experience/skills/ui-component-design.md`
   - `teams/01-frontend-experience/skills/design-system.md`
   - Project `design/prototype` sticker sheet or `ui/tokens/design-tokens.css`
4. Acceptance criteria include **light + dark mode** when the surface appears on the canvas or in chrome

**Gap this addresses:** UI tickets were auto-assigned to frontend by keyword but implemented without loading design-system skills — causing regressions like unreadable dark-mode hint bars.

## How allocation works in tooling

| Step | Command / file |
|------|----------------|
| Auto-match skills | `skill_matcher.py` → `match_skills(title + body)` |
| Auto-match team | `team_for_skills()` → first skill prefix (FE → 01-frontend…) |
| Override at groom | Human edits ticket `team` + `skills` in frontmatter |
| Verify at implement | `./studio move … implement` prints library hint; agent reads `skills` |

## Ticket frontmatter template (UI example)

```yaml
team: 01-frontend-experience
skills: [FE-001, FE-002, FE-004]
```

## Grooming checklist (human + agent)

- [ ] Ticket `team` matches the mapping table above
- [ ] UI tickets include FE-001 + FE-002 in `skills`
- [ ] API tickets include BE-* skills, not default frontend
- [ ] `./studio groom --approve` only after skills are explicit

## Related

- [skill-registry.md](../teams/skill-registry.md)
- [human-in-the-loop.md](human-in-the-loop.md) — sprint review feedback flow
- [agent-context.md](agent-context.md)
