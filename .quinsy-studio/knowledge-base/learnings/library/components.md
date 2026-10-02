# library / components

Portable studio principles (not project incidents).
Matching playbook/skill: `studio-library/library_registry.md`.

## Principles

- **LO-0368** 2026-10-01 :: Do not re-emit existing arbitrary Tailwind size classes as new diff lines
  - See **PB-20261001-001**. The UI receipt scans added `tsx`/`css` lines. Copying an old `text-[12px]` onto a rewritten `className` fails even when the control already used it.
- **PB-20260929-001** helpful=0 harmful=0 :: When reuse review flags files under a product ui/components kit, record them as project-local. Do not open a studio LO to copy token-bound molecules into studio-library.
- **LO-0364** 2026-09-29 :: Keep the project UI kit in the product repo. Do not open a studio LO to copy token-bound molecules into studio-library.
  - See **PB-20260929-001**.
- **LO-0363** 2026-09-29 :: When reuse review flags product ui/components kit files, record them as project-local.
  - See **PB-20260929-001**.
