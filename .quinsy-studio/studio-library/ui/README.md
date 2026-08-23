# Studio Library UI — Atomic structure

```
ui/
├── docs/                    ← UI reference (Tailwind + Headless UI index)
├── tokens/                  ← ui-token
├── primitives/headless/     ← ui-primitive (@headlessui/react re-exports)
├── components/              ← ui-atom | ui-molecule | ui-organism (kind in manifest.json)
├── page-types/              ← ui-page-type
└── sticker-sheet/           ← visual catalog
```

| Atomic level | Library path | Pull example |
|--------------|--------------|--------------|
| Primitives | `primitives/headless/dialog/` | `dialog` |
| Atoms | `components/button/` | `button` |
| Molecules | `components/dropdown-menu/` | `dropdown-menu` |
| Organisms | `components/pageshell/` | `pageshell` |
| Templates | `page-types/comparison/` | `comparison` |

**Start here:** [ui/docs/README.md](./docs/README.md)

**After git clone:** run `./studio install` at repo root (see [installation](./docs/getting-started/installation.md)).
