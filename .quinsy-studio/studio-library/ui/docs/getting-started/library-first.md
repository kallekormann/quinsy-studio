# Library-first UI

Before writing markup in a project:

```bash
./studio library suggest <project> "<feature description>"
./studio library pull <project> <names...>
```

Rules:

1. **Prefer styled atoms/molecules** (`button`, `card`, `dropdown-menu`) over raw primitives.
2. **Gate 2b pulls the base kit** (`button`, `input`, `popover`, `tooltip`, `dropdown-menu`, `dialog`, `sidebar`, `auth-login`). Style those files. Do not draw a second copy.
3. **Use primitives** when no styled component exists — then promote to studio-library.
4. **Never** hand-roll focus traps, Escape handlers, or portal modals.
5. **Install kit peers** in the project app (`docs/setup/ui-kit.md`) — `radix-ui`, `class-variance-authority`, `clsx`, `tailwind-merge`, `lucide-react`.
6. **Keep the kit motion.** Dialog, menu, tooltip, sheet, button, and the rest already use `--motion-*`. Do not add a second duration. Specs name the motion in §2d. HITL `motion: off` sets project durations to `0ms`.

See [component-creation-playbook.md](../../../../knowledge-base/component-creation-playbook.md) and [motion-transitions.md](../../../../knowledge-base/skill-extensions/motion-transitions.md).
