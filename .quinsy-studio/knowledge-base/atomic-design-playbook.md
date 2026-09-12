# Atomic Design playbook

Brad Frost hierarchy mapped to Quinsy studio-library.

## Always

**Do:** Inventory every control in the spec (primitive → page). Pull before inventing. New generic atoms go in studio-library first.

**Don’t:** Skip levels (organism made of raw HTML with no atoms). One-off project components that duplicate a library slug.

**Fail:** Atomic inventory empty on a `ui-new-component` / `ui-composition` spec. “New? yes” with no library ticket/path.

## Levels

| Level | Library path | Project path | Owner |
|-------|--------------|--------------|-------|
| Primitives (a11y) | `ui/primitives/headless/<slug>/` | — | Studio HQ |
| Atoms | `ui/components/<slug>/` (`ui-atom`) | `ui/components/atoms/` | Spec → library → pull |
| Molecules | `ui/components/<slug>/` (`ui-molecule`) | `ui/components/molecules/` | Compose atoms |
| Organisms | `ui/components/<slug>/` (`ui-organism`) | `ui/components/organisms/` | Chrome sections |
| Templates | `ui/page-types/<name>/` | reference in prototype | Layout zones |
| Pages | — | `app/` routes | Instantiate template |

## Rules

1. **No skipping levels** — molecules list atom children; organisms list molecules/atoms.
2. **Library-first** — `./studio library list` / `suggest` before new markup.
3. **New generics in studio-library** — never one-off components in project only.
4. **Headless primitives** — Dialog, Menu, etc. for behavior; style with project tokens.

## When to create what

- **New atom** — single control (Button variant, Badge) not composable from existing.
- **New molecule** — 2+ atoms, one job (SearchField = Input + Button).
- **New organism** — app chrome (TopBar, SettingsPanel).
- **New page-type** — marketing or app shell layout reused across routes.

Gate 2 sticker sheet groups components by atomic level.
