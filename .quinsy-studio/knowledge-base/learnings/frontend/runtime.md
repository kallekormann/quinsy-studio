# frontend / runtime

Portable studio principles (not project incidents).
Matching playbook/skill: `knowledge-base/frontend_playbook.md`.

## Principles

- **LO-0384** 2026-10-12 :: Compose should run `next dev` for UI work once the image supports it
  - A production `build` + `start` cycle plus a named `.next` volume hides source bind-mounts until rebuild. Prefer `next dev` in Compose when the image can boot it, so composition tickets are visible without a full compile. See **PB-20261012-001**.
