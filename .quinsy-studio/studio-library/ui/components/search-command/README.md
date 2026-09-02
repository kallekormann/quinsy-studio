# Search command dialog

CMD-K / palette-style modal. Token-based styling; pair with `packages/item-search`.

```tsx
import { SearchCommandDialog } from '@/ui/components/search-command/SearchCommandDialog';
import { searchItems, summarizeItem } from '@/packages/item-search';

const results = searchItems(items, query).map((item) => ({
  id: item.id,
  label: summarizeItem(item),
  type: item.type,
}));
```

Wire `⌘K` in your board page to toggle `open`.
