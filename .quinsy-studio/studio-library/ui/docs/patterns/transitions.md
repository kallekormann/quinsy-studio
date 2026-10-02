# Transitions

Product UI moves by default. Durations and scales live on `--motion-*` in `ui/tokens/design-tokens.css`. `prefers-reduced-motion` sets those durations to `0ms`. HITL opt-out is the spec line `motion: off`, which does the same override in the **project** token file.

Kit overlays already use the scale:

| Surface | Open | Close | Enter scale | Exit scale |
|---------|------|-------|-------------|------------|
| Dialog, alert dialog | `--motion-duration-fast` | `--motion-duration-quick` | `--motion-scale-large` | `--motion-scale-large` |
| Menu, popover, select | `--motion-duration-fast` | `--motion-duration-quick` | `--motion-scale-medium` | `--motion-scale-tiny` |
| Tooltip | `--motion-duration-quick` after `--motion-duration-micro` | `--motion-duration-quick`, no delay | `--motion-scale-small` | `--motion-scale-small` |
| Sheet | `--motion-duration-slow` | `--motion-duration-medium` | travel, no scale | quieter travel |

Easing is `--motion-ease-smooth-out`, except tooltips (`--motion-ease-out`). The enter/exit animation reads `--tw-enter-scale` and `--tw-exit-scale`, so the centering translate stays.

Headless UI `Transition` is the primitive when a surface is not a kit component:

```tsx
import { Transition } from '@/ui/primitives/headless/transition';

<Transition
  show={open}
  enter="transition ease-[var(--motion-ease-smooth-out)] duration-[var(--motion-duration-fast)]"
  enterFrom="opacity-0 scale-[var(--motion-scale-large)]"
  enterTo="opacity-100 scale-100"
  leave="transition ease-[var(--motion-ease-smooth-out)] duration-[var(--motion-duration-quick)]"
  leaveFrom="opacity-100 scale-100"
  leaveTo="opacity-0 scale-[var(--motion-scale-large)]"
>
  {children}
</Transition>
```

Doctrine: [skill-extensions/motion-transitions.md](../../../../knowledge-base/skill-extensions/motion-transitions.md).

Reference: [Headless UI transitions](https://headlessui.com/react/transition).
