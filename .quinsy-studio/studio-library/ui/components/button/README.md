# Button Component

> Generic, token-based button with multiple variants.

## Variants

| Variant | Description | Use Case |
|---------|-------------|----------|
| `primary` | Primary action | Form submit, CTA |
| `secondary` | Secondary action | Cancel, Back |
| `outline` | Limited action | Alternative options |
| `ghost` | Inline action | Links, Navigation |
| `destructive` | Dangerous action | Delete, Archive |

## Sizes

| Size | Padding | Font Size |
|------|---------|-----------|
| `sm` | 0.5rem 1rem | 0.875rem |
| `md` | 0.625rem 1.25rem | 1rem |
| `lg` | 0.75rem 1.5rem | 1.125rem |

## API

```tsx
interface ButtonProps {
  variant?: 'primary' | 'secondary' | 'outline' | 'ghost' | 'destructive';
  size?: 'sm' | 'md' | 'lg';
  disabled?: boolean;
  loading?: boolean;
  children: React.ReactNode;
  onClick?: () => void;
}
```

## Example

```tsx
import { Button } from '@studio/ui';

// Primary button
<Button variant="primary" size="md">
  Save
</Button>

// Loading button
<Button variant="primary" loading>
  Saving...
</Button>

// Destructive button
<Button variant="destructive">
  Delete
</Button>
```

## Accessibility

- Keyboard navigable (Tab + Enter/Space)
- ARIA label for icon-only buttons
- Visible focus indicator
- Sufficient color contrast (WCAG AA)

## Files

- `Button.tsx` — Component
- `Button.stories.tsx` — Storybook
- `Button.test.tsx` — Tests
