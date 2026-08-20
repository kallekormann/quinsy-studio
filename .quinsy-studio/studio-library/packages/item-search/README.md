# Item search

CMD-K style metadata search over canvas items (`contentJson` tags, text, filenames, palette). Depends on `item-tags` (bundled in same pull folder).

## Pull

```bash
./studio library pull <project> item-search item-tags
```

## Usage

```typescript
import { searchItems, summarizeItem, itemMatchesSearch } from '@/packages/item-search';

const matches = searchItems(boardItems, query);
const muted = items.filter((i) => !itemMatchesSearch(i, query));
```

Pair with `search-command` UI component.
