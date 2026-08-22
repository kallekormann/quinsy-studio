import { describe, expect, it } from 'vitest';
import { itemsInMarquee, normalizeRect } from './rect-selection';

describe('normalizeRect', () => {
  it('handles negative drag dimensions', () => {
    expect(normalizeRect({ x: 10, y: 10, width: -20, height: -30 })).toEqual({
      x: -10,
      y: -20,
      width: 20,
      height: 30,
    });
  });
});

describe('itemsInMarquee', () => {
  it('returns intersecting item ids', () => {
    const hits = itemsInMarquee(
      [{ id: 'a', x: 0, y: 0, width: 10, height: 10, type: 'note' }],
      { x: 5, y: 5, width: 10, height: 10 },
    );
    expect(hits).toEqual(['a']);
  });
});
