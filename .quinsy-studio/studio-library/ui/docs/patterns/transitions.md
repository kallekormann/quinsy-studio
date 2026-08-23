# Transitions

Use Headless UI `Transition` primitive with Tailwind utilities.

```tsx
import { Transition } from '@/ui/primitives/headless/transition';

<Transition
  show={open}
  enter="transition ease-out duration-200"
  enterFrom="opacity-0 scale-95"
  enterTo="opacity-100 scale-100"
  leave="transition ease-in duration-150"
  leaveFrom="opacity-100 scale-100"
  leaveTo="opacity-0 scale-95"
>
  {children}
</Transition>
```

Reference: [Headless UI transitions](https://headlessui.com/react/transition), [Tailwind transition](https://tailwindcss.com/docs/transition-property).
