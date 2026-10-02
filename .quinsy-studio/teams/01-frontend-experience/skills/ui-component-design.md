# Skill: UI Component Design (FE-001)

```
skill_id: FE-001
team: 01-frontend-experience
lead_role: Frontend Engineer
```

Compose studio-library + project tokens. **Playbook:** [frontend_playbook.md](../../../knowledge-base/frontend_playbook.md) · [frontend-team-canon-ledger.md](../../../knowledge-base/frontend-team-canon-ledger.md)

**Do:** `library suggest` → `pull`; kit peers in `docs/setup/ui-kit.md`; Tailwind + Headless/Radix. Motion ships on the pulled kit (`--motion-duration-*`). **Don’t:** new atoms in a feature ticket; a second fade on a kit dialog. **Implement-fail:** native `<select>` on product chrome; duplicate organism; hand-rolled overlay timing.

**Extension:** [motion-transitions.md](../../../knowledge-base/skill-extensions/motion-transitions.md). `motion: off` is a human command, then project tokens at `0ms`.

**Deliverables:** inventory of pulled components vs spec; no one-off CSS control.
