# design-md-repo

Moody-owned **Design.md** systems for the Figma companion (AM-008 / M19).

## Layout

```
packages/design-md-repo/
  schema/design-md.schema.json   # contract docs (MOOD-0254)
  validate.ts                    # YAML frontmatter + field errors
  catalog.json / catalog.ts      # curated index; default = moody-bloom
  SOURCE.md                      # system ← aesthetic-preset | Bloom tokens
  systems/<id>/Design.md         # cores (MOOD-0256)
  fixtures/                      # validator goldens
```

**Product chrome is separate:** catalog cores do not restyle the Moody webapp. Selector default is **Moody Bloom**; Brutalist (and other presets) are generate grammars only.

## Usage

```ts
import {
  validateDesignMd,
  loadDesignMdCatalog,
  getDefaultSystemId,
} from '@packages/design-md-repo';

const catalog = loadDesignMdCatalog();
getDefaultSystemId(catalog); // 'moody-bloom'

const result = validateDesignMd(rawMarkdown);
```
