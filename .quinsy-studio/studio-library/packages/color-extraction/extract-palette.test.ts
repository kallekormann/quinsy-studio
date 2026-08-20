import { describe, expect, it } from 'vitest';
import { extractPaletteFromPixels } from './extract-palette';

describe('extractPaletteFromPixels', () => {
  it('returns N hex colors from dominant pixels', () => {
    const data = new Uint8ClampedArray(4 * 4 * 4);
    for (let i = 0; i < data.length; i += 4) {
      data[i] = 255;
      data[i + 1] = 0;
      data[i + 2] = 0;
      data[i + 3] = 255;
    }

    const palette = extractPaletteFromPixels(data, { count: 5, sampleStride: 1 });
    expect(palette).toHaveLength(5);
    expect(palette[0]).toMatch(/^#[0-9A-F]{6}$/);
  });
});
