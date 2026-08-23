# Atomic design in studio-library

Physical layout (flat folders + `kind` in manifest):

```
ui/
├── primitives/headless/<slug>/   # ui-primitive — Headless UI behavior
├── components/<slug>/            # ui-atom | ui-molecule | ui-organism
├── page-types/<name>/            # ui-page-type — templates
├── tokens/                       # ui-token
└── docs/                         # this reference
```

Projects mirror atoms/molecules/organisms under `ui/components/atoms|molecules|organisms/` after pull.

See [atomic-design-playbook.md](../../../../knowledge-base/atomic-design-playbook.md).
