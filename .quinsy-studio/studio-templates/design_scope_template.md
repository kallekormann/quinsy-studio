# Design scope — {{PROJECT}}

> **Date:** {{DATE}}
> **Status:** pending user confirmation

## Mock scope

**Selected scope:** `{{SCOPE}}`

| Option | Meaning |
|--------|---------|
| `journey` | Mock the **full core user journey** end-to-end (all steps clickable in prototype) |
| `core-views` | Mock only **key screens/pages** (faster; journey described in docs) |

## Core user journey (agreed)

_Document the journey from `docs/definitions/03-user-journeys.md` that drives mocks._

1. _Step 1_
2. _Step 2_
3. _Step 3_

## Screens to mock

### If scope = `journey`

| # | Screen | Route | Journey step |
|---|--------|-------|--------------|
| 1 | | `/mocks/...` | |

### If scope = `core-views`

| # | Screen | Route | Why core |
|---|--------|-------|----------|
| 1 | Home | `/mocks/home` | Primary entry |

## Required shell

Archetype: `{{ARCHETYPE}}`

The PRD journey is not the whole prototype. These routes are required (`internal-tool` omits marketing and legal; `api-service` has no UI prototype). `core-views` may stub the journey. `journey` links the shell and the core path.

{{SHELL_ROUTES}}

## Sticker sheet

- Route: `/sticker-sheet`
- Includes: **design tokens** (color, type, spacing) **and** component states (atoms → organisms)

## Approval checklist (gate 2)

- [ ] Visual direction matches PRD
- [ ] Tokens defined in `ui/tokens/design-tokens.json`
- [ ] Atoms/molecules/organisms scaffolded under `ui/components/`
- [ ] Shell routes from Required shell exist and use the pulled kit (`auth-login`, sidebar or `studio-rail`)
- [ ] Prototype runs: `cd design/prototype && npm run dev`
- [ ] After gate 2b, product `app/` is a copy of this baseline and `design/prototype/` is still there
