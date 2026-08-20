import { describe, expect, it } from 'vitest';
import { collectTags, normalizeTags, parseItemTags } from './item-tags';

describe('item-tags', () => {
  it('parses tags from contentJson', () => {
    expect(
      parseItemTags({ contentJson: JSON.stringify({ tags: ['Warm', 'hero'] }) }),
    ).toEqual(['warm', 'hero']);
  });

  it('normalizes tags', () => {
    expect(normalizeTags([' Warm ', 'warm'])).toEqual(['warm']);
  });

  it('collects unique board tags', () => {
    expect(
      collectTags([
        { contentJson: JSON.stringify({ tags: ['a'] }) },
        { contentJson: JSON.stringify({ tags: ['b', 'a'] }) },
      ]),
    ).toEqual(['a', 'b']);
  });
});
