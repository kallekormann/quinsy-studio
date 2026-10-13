# SegmentedToggle

Horizontal labeled A|B (or A|B|C) control for **product choices where each option has a name**.

Pull: `./studio library pull <project> segmented-toggle`

## When to use

| Need                                                | Component             |
| --------------------------------------------------- | --------------------- |
| Boolean on/off                                      | `Switch`              |
| Labeled exclusive options (Selected \| Whole board) | **SegmentedToggle**   |
| Long list / many options                            | `Dropdown` / `Select` |
| Vertical list with descriptions                     | `RadioGroup` (styled) |

## A11y

Built on Headless UI `RadioGroup` — arrow keys move selection; focus ring on `data-focus`.

Visual: `p-[3px]` track, 26×12px segments, selected `shadow-seg` on `bg-surface`.

## Example

```tsx
<SegmentedToggle
  name="export-scope"
  label="Export area"
  value={scope}
  onChange={setScope}
  options={[
    { value: 'selection', label: 'Selected', disabled: !hasSelection },
    { value: 'board', label: 'Whole board' },
  ]}
/>
```
