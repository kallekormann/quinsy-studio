# Skill: Visual UI Design (UX-005)

```
skill_id: UX-005
team: 10-product-design-experience
lead_role: UI/Visual Designer
```

Typography, color, layout, Gestalt, golden ratio. All values calculable in design spec.

**Aesthetic preset:** load [aesthetic-presets.md](aesthetic-presets.md) + one preset from `knowledge-base/aesthetic-presets/<slug>/SKILL.md`.

**External:** `ux-visual-design`, `ux-typography`, `ux-color-theory`, `taste-skill`

**Playbook:** `knowledge-base/design-science-playbook.md`

---

## Toolbox (trained — TR-0012)

### Upgrade soft-path composition (LO-0142)

- When checkout is deferred, the soft-path must land on a **real** plan/Account surface (not a dead hash) with Free + Upgrade in the first viewport, **or** auto-open the upgrade dialog (`?upgrade=1`).
- A modal that only opens after an unmarked click fails “upgrade now” intent.
- Compose with Headless UI dialog + library Button/Badge; keep plan copy in the project.
- Pattern: [upgrade-soft-path.md](../../../studio-library/ui/docs/patterns/upgrade-soft-path.md). FE cross-link: [frontend_playbook.md](../../../knowledge-base/frontend_playbook.md).
