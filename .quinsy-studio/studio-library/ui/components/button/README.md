# Button Component

> Generischer, token-basierter Button mit mehreren Varianten.

## Varianten

| Variante | Beschreibung | Use Case |
|----------|-------------|----------|
| `primary` | Haupt-Aktion | Formular absenden, CTA |
| `secondary` | Sekundäre Aktion | Abbrechen, Zurück |
| `outline` | Begrenzte Aktion | Alternative Optionen |
| `ghost` | Inline-Aktion | Links, Navigation |
| `destructive` | Gefährliche Aktion | Löschen, Archivieren |

## Größen

| Größe | Padding | Font-Size |
|-------|---------|-----------|
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

## Beispiel

```tsx
import { Button } from '@studio/ui';

// Primärer Button
<Button variant="primary" size="md">
  Speichern
</Button>

// Loader-Button
<Button variant="primary" loading>
  Wird gespeichert...
</Button>

// Destructive Button
<Button variant="destructive">
  Löschen
</Button>
```

## Barrierefreiheit

- Keyboard-Navigierbar (Tab + Enter/Space)
- ARIA-Label bei Icon-Only-Buttons
- Focus-Indikator sichtbar
- Ausreichender Farbkontrast (WCAG AA)

## Dateien

- `Button.tsx` — Komponente
- `Button.stories.tsx` — Storybook
- `Button.test.tsx` — Tests
