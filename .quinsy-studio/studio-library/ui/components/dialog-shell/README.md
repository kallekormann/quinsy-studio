# DialogShell

Reusable modal chrome: **header** (title + optional description), **body**, **footer** (actions).

## Pull

```bash
./studio library pull <project> dialog-shell
```

Also needs Headless UI Dialog primitive:

```bash
./studio library pull <project> dialog
```

## Usage

```tsx
<DialogShell
  open={open}
  onClose={onClose}
  title="Export board"
  description="Download as PNG, PDF, or tokens."
  footer={
    <>
      <Button variant="primary">Export</Button>
      <Button variant="ghost">Cancel</Button>
    </>
  }
>
  …body…
</DialogShell>
```

Footer uses `flex-row-reverse` so the **first** child is the primary (rightmost in LTR). Pass primary first in the fragment.

## Surfaces

- Light: `bg-white`
- Dark: `dark:bg-surface-dark` — same elevated panel token as Card / ItemInspector. Do not override with `neutral-900`.

## A11y

- Focus trapped by Headless UI Dialog
- Esc / backdrop click → `onClose`
- Title via `DialogTitle`; description via `DialogDescription` when provided
