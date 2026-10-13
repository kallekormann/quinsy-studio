# Library

Before anyone writes a new component or package, the agent looks in the studio library.

```bash
./studio library list
./studio library suggest <project> "auth button"
./studio library pull <project> tokens button auth-login
```

A pull is boilerplate. The product adapts tokens, copy, and business rules. The look stays in the project. Gate 2b does not merge a product's visual design back into the library.

## What is pullable

| Asset | Pull? |
|-------|--------|
| Headless primitives (button, dialog, tokens scaffold) | Yes. Adapt them. |
| `billing` (Stripe and Lemon Squeezy) | Yes. |
| `feature-gating` | No. It is a stub. Build it in the product, then promote a working generic. |
| `packages/auth` | No. Login is the Payload Users collection. |

Promote only when the **generic** piece got better, and only after the ticket is done:

```bash
./studio library promote <project> packages/billing --ticket <ticket>
```

Do not promote a client's colors, a one-off layout, or a half-finished stub.

New behavior for a primitive is written in the studio library first, then pulled. The playbook is [component-creation-playbook.md](../knowledge-base/component-creation-playbook.md). The index is [library_registry.md](../studio-library/library_registry.md).

## UI kit

Every product app that uses the library has these from the day it is created, not after the first failed import: `radix-ui`, `class-variance-authority`, `clsx`, `tailwind-merge`, `lucide-react`, and `@headlessui/react` for Headless primitives. Bootstrap, design, and adopt write `docs/setup/ui-kit.md` and merge the peers into `package.json`.

## Motion

Motion is on unless the spec says `motion: off`. Transitions are part of the spec, not a polish pass. The extension is [motion-transitions.md](../knowledge-base/skill-extensions/motion-transitions.md).
