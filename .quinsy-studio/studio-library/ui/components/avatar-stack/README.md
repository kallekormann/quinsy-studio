# AvatarStack

Overlapping circular avatars for collaboration presence (mock `13-collaboration.html`). Profile initials or photos — not name chips.

## Usage

```tsx
import { AvatarStack } from '@ui/components/avatar-stack';

<AvatarStack
  aria-label="Collaborators online"
  people={[
    { id: '1', initials: 'KA', title: 'You', isYou: true, background: '…' },
    { id: '2', initials: 'AR', title: 'Alex · editing', ringColor: '#3b82f6', background: '…' },
  ]}
/>
```

## Props

| Prop | Default | Notes |
|------|---------|-------|
| `people` | — | `id`, `initials`, `title`; optional `imageUrl`, `background`, `ringColor`, `isYou`, `onClick` |
| `maxVisible` | `4` | Remaining count shown as `+N` pill |
| `size` | `md` | `sm` (24px) or `md` (28px) |
| `aria-label` | `Collaborators` | List accessible name |

## Behavior

- First avatar flush left; each subsequent overlaps by 8px (`-ml-2` at `md`).
- `+N` uses neutral `surface-2` fill (not a photo).
- Optional presence ring via `ringColor` (matches cursor color in collab mock).
