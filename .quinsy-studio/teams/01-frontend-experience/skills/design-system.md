# Skill: Design System (FE-002)

```
skill_id: FE-002
team: 01-frontend-experience
lead_role: Frontend Engineer
```

Apply **already approved** project tokens to the **pulled** studio-library kit. Visual language is Team 10 / gate 2. The product app starts from the materialized prototype; do not rebuild button, popover, tooltip, dropdown, or dialog beside `ui/components/<slug>/`.

**Playbook:** [frontend_playbook.md](../../../knowledge-base/frontend_playbook.md)

**Don’t:** a second palette. **shadcn is not the kit.** **Implement-fail:** dark mode that ignores tokens; raw hex in product UI when tokens exist (gate 5 warn); a second motion scale beside `--motion-*`.

**Extension:** [motion-transitions.md](../../../knowledge-base/skill-extensions/motion-transitions.md).

Zone-sourced kit rails reassemble from current children; do not rematch a stale stored palette after add/delete (LO-0290).

## Deltas

- **PB-20260926-001** helpful=0 harmful=0 :: Keep layout and composition work on the live layout-picker cards. Do not invent a second block-list editor, a second intake inbox, or a one-off product-detail workbench.
- **PB-20260916-001** helpful=0 harmful=0 :: When a chrome ticket removes or rewires a control, update the gold-path source test in the same change.
