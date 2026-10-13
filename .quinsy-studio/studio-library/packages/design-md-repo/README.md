# design-md-repo

Curated **Design.md** systems: a validator, a parser to layout parameters, and a catalog of cores compiled from the studio aesthetic presets.

## Layout

```
packages/design-md-repo/
  schema/design-md.schema.json   # contract docs
  validate.ts                    # YAML frontmatter + field errors
  catalog.json / catalog.ts      # curated index; default = soft-ui
  SOURCE.md                      # system ← aesthetic preset
  systems/<id>/Design.md         # cores
  fixtures/                      # validator goldens
```

**Product chrome is separate:** catalog cores are generate grammars. They do not restyle the product that uses them; the product's look stays in its own tokens. A product that wants its own brand as a core adds it in its repo, not here.

## Usage

```ts
import {
  validateDesignMd,
  loadDesignMdCatalog,
  getDefaultSystemId,
} from '@packages/design-md-repo';

const catalog = loadDesignMdCatalog();
getDefaultSystemId(catalog); // 'soft-ui'

const result = validateDesignMd(rawMarkdown);
```
