# Forms

Compose with Field primitive + styled atoms:

```tsx
import { Field, Fieldset, Label, Description, Legend } from '@/ui/primitives/headless/field';
import { Input } from '@/ui/components/input';
import { Select } from '@/ui/components/select';
import { Checkbox } from '@/ui/components/checkbox';
import { Switch } from '@/ui/components/switch';
```

Rules:

- Wrap each control in `Field` + `Label`
- Use `Fieldset` + `Legend` for groups
- Prefer `RadioGroup` molecule or `Listbox` for custom single-select
- Run contrast check via `design_math.py` on token pairs

Reference: [Headless UI Field](https://headlessui.com/react/fieldset), [Luke Wroblewski form design](https://www.lukew.com/).
