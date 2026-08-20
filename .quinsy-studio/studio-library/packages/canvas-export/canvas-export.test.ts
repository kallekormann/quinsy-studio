import { describe, expect, it } from 'vitest';
import { boundsForItems, itemExportBounds, unionBounds } from './canvas-export';

const PIXELS = { item: 80, paletteExtra: 20 } as const;

function makeItem(overrides: Partial<Parameters<typeof itemExportBounds>[0]>) {
  return {
    id: 'item-1',
    type: 'note',
    x: 0,
    y: 0,
    width: PIXELS.item,
    height: PIXELS.item,
    contentJson: '{}',
    ...overrides,
  };
}

describe('canvas-export bounds', () => {
  it('adds palette height for images', () => {
    const item = makeItem({
      type: 'image',
      contentJson: JSON.stringify({ palette: ['#111111'] }),
    });
    expect(itemExportBounds(item).height).toBeGreaterThan(PIXELS.item);
  });

  it('unions item bounds', () => {
    const bounds = boundsForItems([
      makeItem({ x: 0, y: 0, width: PIXELS.item, height: PIXELS.item }),
      makeItem({ id: '2', x: 200, y: 50, width: PIXELS.item, height: 60 }),
    ]);
    expect(bounds?.width).toBe(280);
  });

  it('returns null for empty union', () => {
    expect(unionBounds([])).toBeNull();
  });
});
