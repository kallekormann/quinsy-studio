# M<n> — <version name>

> One milestone is one version a person can use. Written by PM-002 after gate 2b, approved with `./studio approve <project> --milestones`. Coverage rows come from `knowledge-base/milestone-coverage-checklist.md`.

**Status:** planned | active | review | done
**Depends on:** M<n-1>

## Goal

One paragraph: what a person can do after this milestone that they could not do before. Name the persona from `docs/definitions/02-personas.md`.

## In scope

- Capability (PRD section reference)
- Capability (PRD section reference)

## Out of scope

- Capability, and the milestone that carries it

## Coverage

| Area | Depth in this milestone | PRD reference |
|------|-------------------------|---------------|
| Scaffolding and repo shape | foundation / hardening / complete | PRD §x |
| Data model and database | | |
| API and services | | |
| Authentication and access | | |
| Security hardening | | |
| Privacy and legal | | |
| Frontend boilerplate and app shell | | |
| UX flows and interaction | | |
| Motion and delight | | |
| Performance | | |
| Operations and production | | |
| Testing and quality | | |

Delete rows this milestone does not carry; add the growth, billing, i18n, content and launch rows when the checklist marks them required.

## Success criteria

- Measurable statement with the command, route or metric that proves it
- Measurable statement

## Risks and decisions for the human

- Decision the human must take at `./studio milestone <project> --approve`

## Tickets

Written by `./studio milestone <project> plan` when this milestone becomes active. One line per ticket: `- <title> :: <one-sentence scope>`. The CLI creates and staffs the ticket (PM-004), stamps `milestone: M<n>`, and replaces the line with the ticket id.

- <title> :: <scope>
