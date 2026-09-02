# EmotionStrip

Moody’s brand visual: a rounded palette ribbon. Same shape everywhere; colors follow the board kit or moment.

**Design:** `docs/design-specs/mocks/MOOD-0413/24-moody-motifs.html`

## Usage

```tsx
import { EmotionStrip } from '@ui/components/emotion-strip';

<EmotionStrip
  size="sm"
  colors={['#e56b4e', '#f0a890', '#e8d8cc', '#5a4034']}
/>

<EmotionStrip size="block" weighted colors={palette} className="mt-1.5" />
```

## Props

| Prop | Type | Default | Notes |
|------|------|---------|-------|
| `colors` | `string[]` | — | 3–5 CSS colors; returns `null` when empty |
| `size` | `sm \| md \| lg \| block` | `md` | `block` = full width at `lg` height |
| `weighted` | `boolean` | `false` | Unequal segment flex (expressive moods) |
| `className` | `string` | — | Layout/spacing on the outer shell |
| `aria-label` | `string` | `Color mood` | Accessible name |

## Rules

- No glow or caption text — one strip per surface is enough.
- Prefer token vars (`var(--color-accent-500)`) over raw hex in app code.
- **Rejected motifs (do not build):** Mood Caption, Wash Bloom, Artifact Deck.
