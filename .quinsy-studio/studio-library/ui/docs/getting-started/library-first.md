# Library-first UI

Before writing markup in a project:

```bash
./studio library suggest <project> "<feature description>"
./studio library pull <project> <names...>
```

Rules:

1. **Prefer styled atoms/molecules** (`button`, `card`, `dropdown-menu`) over raw primitives.
2. **Use primitives** when no styled component exists — then promote to studio-library.
3. **Never** hand-roll focus traps, Escape handlers, or portal modals.
4. **Install kit peers** in the project app (`docs/setup/ui-kit.md`) — `radix-ui`, `class-variance-authority`, `clsx`, `tailwind-merge`, `lucide-react`.

See [component-creation-playbook.md](../../../../knowledge-base/component-creation-playbook.md).
