# Item tags

Parse and normalize tags stored in item `contentJson.tags`. Zero dependencies.

## Pull

```bash
./studio library pull <project> item-tags
```

## Usage

```typescript
import { parseItemTags, normalizeTags, collectTags } from '@/packages/item-tags';

const tags = parseItemTags({ contentJson: item.contentJson });
await saveTags(item.id, normalizeTags(['Warm', 'hero']));
```

Pair with `item-search` and `item-inspector` UI components.
