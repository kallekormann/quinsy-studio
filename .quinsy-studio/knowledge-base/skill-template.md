# Skill: <Name>

> Mission in two to four sentences: what the skill decides or produces, for which tickets, and the bar it holds. Write it for the implementer who reads only this line.

## Metadata

```
skill_id: XX-NNN
name: <Name>
team: <NN-team-folder>
lead_role: <role from ticket_helpers.SKILL_ROLE_MAP>
support_roles: [<role>, <role>]
phases: [<n>]
activation_triggers:
  - <ticket signal>
  - Phrases: "<trigger>", "<trigger>"
pairs_with: [<skill IDs>]
```

Default verdict: <what holds until proof exists>. Omit for skills that do not judge.

## When to load

- <ticket situations>
- Not for <the near-miss case>.

## Rules

### 1. <Rule as an imperative>

<One paragraph. A rule the gate, the receipt or a reviewer can check.>

## Workflow

1. <step>
2. <step>

## Deliverables

<Files with their paths and a short example of the shape.>

## Done evidence

What the receipt shows on a ticket that carried this skill. Every path must exist on disk.

```markdown
## <Receipt section>
- <line with a path or command>
```

## Anti-patterns

- <the mistake agents make with this skill>

## Handoff

- **To <team or skill>:** <what they receive>

## Deltas

Optional. What this studio changed from the source the skill came from, and why.

## References

- <playbooks, sibling skills, source with licence>

---

Register a new skill in four places, in one change, then run `python3 studio-tools/lint_skills.py`:

1. `skill_matcher.INTERNAL_SKILLS` (name and triggers).
2. `ticket_helpers.SKILL_ROLE_MAP` (lead role).
3. The `skill_id:` line in this file, inside the team folder that owns the prefix (`SKILL_PREFIX_TEAM`).
4. A row in `teams/skill-registry.md`.

Drift between them is an error. A missing template section is a warning; `--strict` makes it an error.
