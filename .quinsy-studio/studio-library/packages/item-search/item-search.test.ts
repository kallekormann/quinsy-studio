import { describe, expect, it } from 'vitest';
import { itemMatchesSearch, searchItems, summarizeItem } from './item-search';

describe('item-search', () => {
  it('matches across tags and note text', () => {
    const item = {
      id: '1',
      type: 'note',
      contentJson: JSON.stringify({ text: 'hero board', tags: ['warm'] }),
    };
    expect(itemMatchesSearch(item, 'hero')).toBe(true);
    expect(itemMatchesSearch(item, 'cold')).toBe(false);
  });

  it('summarizes for command palette', () => {
    expect(
      summarizeItem({
        id: '1',
        type: 'image',
        contentJson: JSON.stringify({ fileName: 'logo.png' }),
      }),
    ).toContain('logo.png');
  });

  it('filters items', () => {
    const items = [
      { id: 'a', type: 'note', contentJson: JSON.stringify({ text: 'alpha' }) },
      { id: 'b', type: 'note', contentJson: JSON.stringify({ text: 'beta' }) },
    ];
    expect(searchItems(items, 'beta')).toHaveLength(1);
  });
});
