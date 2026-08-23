# Design science playbook

Theory-backed, measurable design decisions for Team 10.

## Gestalt (perception)

| Principle | Application |
|-----------|-------------|
| Proximity | Related controls share spacing group (8pt multiples) |
| Similarity | Same action = same button variant |
| Closure | Cards/containers imply boundaries |
| Continuity | Eye path follows F/Z pattern on marketing pages |
| Figure-ground | Canvas vs chrome contrast |

## Calculable rules

| Domain | Rule | Tool |
|--------|------|------|
| Contrast | Text ≥4.5:1, large UI ≥3:1 | `design_math.contrast_ratio` |
| Type scale | base × φ^n | `design_math.golden_scale` |
| Palette | 60-30-10 split | `design_math.palette_60_30_10` |
| IA | ≤7 top-level nav, depth ≤3 | `design_math.ia_nav_audit` |
| Touch | ≥44×44px targets | spec checklist |
| Measure | 45–75 characters line length | typography spec |

## Usability

Nielsen heuristics (see `design_playbook.md`): visibility, match, control, consistency, error prevention, recognition, flexibility, minimalism, error recovery, help.

## Accessibility

WCAG 2.1 AA — load FE-004 + `ux-accessibility` external skill at implement.

Run `./studio approve-design` only after contrast table is filled with calculated ratios.
