# Item inspector panel

Context panel for selected canvas/asset metadata. Token-based; pair with `packages/item-tags`.

```tsx
import { ItemInspectorPanel } from '@/ui/components/item-inspector/ItemInspectorPanel';
import { parseItemTags, normalizeTags } from '@/packages/item-tags';

<ItemInspectorPanel
  title={summarizeItem(item)}
  itemType={item.type}
  tags={parseItemTags(item)}
  onTagsChange={(tags) => updateItemTags(item.id, normalizeTags(tags))}
  footer="More asset fields can slot in here."
/>
```
