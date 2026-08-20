# Color extraction

Client-side dominant-color palette extraction. Zero dependencies — copy into `packages/color-extraction/` or pull via studio library.

## Pull

```bash
./studio library pull <project> color-extraction
```

## Usage

```typescript
import {
  extractPaletteFromFile,
  extractPaletteFromPixels,
  type ExtractPaletteOptions,
} from '@/packages/color-extraction';

const options: ExtractPaletteOptions = {
  count: 5,
  size: 64,
  fallback: ['#111827', '#6B7280', '#F3F4F6'],
};

// Browser: image upload
const palette = await extractPaletteFromFile(file, options);

// Tests / workers: raw RGBA buffer
const fromPixels = extractPaletteFromPixels(imageData.data, options);
```

## UI pairing

Use with studio-library `palette-strip` component to render swatches under image cards.

## Options

| Option | Default | Description |
|--------|---------|-------------|
| `count` | 5 | Swatch count |
| `size` | 64 | Raster edge when decoding blobs |
| `sampleStride` | 1 | Skip pixels when counting |
| `quantizeStep` | 32 | RGB bucket size |
| `minAlpha` | 128 | Ignore transparent pixels |
| `fallback` | neutral palette | Pad short results |
