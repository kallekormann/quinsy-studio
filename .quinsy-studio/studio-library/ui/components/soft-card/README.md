# SoftCard

Neutral Bloom elevation for cards and panels — `var(--line)` border + `shadow-sm` / `shadow-md` on hover. **No coral glow. No translate/scale hover motion.**

## Class helpers

```tsx
import { softCardClass, softCardInteractiveClass } from '@ui/components/soft-card';

<article className={softCardInteractiveClass}>…</article>
<div className={`${softCardClass} p-4`}>…</div>
```

## Component

```tsx
import { SoftCard } from '@ui/components/soft-card';

<SoftCard interactive padding="md">Board preview</SoftCard>
<SoftCard selected>Active card</SoftCard>
```

| Prop | Default | Notes |
|------|---------|-------|
| `interactive` | `false` | Hover shadow + stronger border (no transform) |
| `selected` | `false` | Accent wash, no glow shadow |
| `padding` | `md` | `none \| sm \| md` |
