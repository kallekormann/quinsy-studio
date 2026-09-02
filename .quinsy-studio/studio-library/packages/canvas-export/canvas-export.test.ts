import { describe, expect, it } from 'vitest';
import {
  assertExportDataUrl,
  boundsForItems,
  dataUrlToUint8Array,
  downloadBlob,
  itemExportBounds,
  unionBounds,
} from './canvas-export';

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

describe('dataUrlToUint8Array (MOOD-0356)', () => {
  it('decodes base64 PNG data URLs without fetch', () => {
    const dataUrl = `data:image/png;base64,${btoa('png-bytes')}`;
    const { bytes, mime } = dataUrlToUint8Array(dataUrl);
    expect(mime).toBe('image/png');
    expect(String.fromCharCode(...bytes)).toBe('png-bytes');
  });
});

describe('export download guards (MOOD-0357)', () => {
  it('rejects empty data URLs', () => {
    expect(() => assertExportDataUrl('data:image/png;base64,')).toThrow(/empty/i);
  });

  it('rejects undersized blobs', () => {
    expect(() => downloadBlob(new Blob([new Uint8Array([1, 2])]), 'x.png')).toThrow(/empty/i);
  });

  it('accepts a non-empty PNG data URL decode', () => {
    const payload = 'x'.repeat(64);
    const dataUrl = `data:image/png;base64,${btoa(payload)}`;
    expect(() => assertExportDataUrl(dataUrl)).not.toThrow();
  });
});
