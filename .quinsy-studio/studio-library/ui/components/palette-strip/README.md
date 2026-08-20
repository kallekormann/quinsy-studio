# Palette strip

Renders a row of color swatches using studio neutral/primary tokens. Use with `packages/color-extraction`.

```tsx
import { PaletteStrip } from '@/ui/components/palette-strip/PaletteStrip';
import { extractPaletteFromFile } from '@/packages/color-extraction';

const colors = await extractPaletteFromFile(file);
<PaletteStrip colors={colors} showLabels onSwatchClick={(hex) => navigator.clipboard.writeText(hex)} />
```

Props: `colors`, `label`, `showLabels`, `onSwatchClick`, `trailing`, `className`.
