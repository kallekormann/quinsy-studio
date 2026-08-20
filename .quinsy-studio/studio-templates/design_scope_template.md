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

## Sticker sheet

- Route: `/sticker-sheet`
- Includes: **design tokens** (color, type, spacing) **and** component states (atoms → organisms)

## Approval checklist (gate 2)

- [ ] Visual direction matches PRD
- [ ] Tokens defined in `ui/tokens/design-tokens.json`
- [ ] Atoms/molecules/organisms scaffolded under `ui/components/`
- [ ] Prototype runs: `cd design/prototype && npm run dev`
