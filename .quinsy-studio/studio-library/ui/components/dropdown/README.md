# Dropdown

Single-value **Listbox** dropdown for product surfaces. Popover panel matches menu language (border, shadow, soft hover) — **not** native OS `<select>` chrome.

## Pull

```bash
./studio library pull <project> dropdown listbox
```

## Usage

```tsx
<Dropdown
  label="Resolution"
  value={pixelRatio}
  onChange={setPixelRatio}
  options={[
    { value: 1, label: '1× (screen)' },
    { value: 2, label: '2× (default)' },
  ]}
/>
```

## A11y

- Headless UI Listbox: keyboard nav, Esc, focus management
- Provide `label` or `aria-label`
