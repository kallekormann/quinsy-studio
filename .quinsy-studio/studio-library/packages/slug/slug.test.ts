import { describe, expect, it } from 'vitest';
import { slugifyName, withSlugSuffix } from './slug';

describe('slugifyName', () => {
  it('normalizes names', () => {
    expect(slugifyName('Studio North', 'team')).toBe('studio-north');
    expect(slugifyName('  ', 'team')).toBe('team');
  });
});

describe('withSlugSuffix', () => {
  it('appends a unique suffix', () => {
    expect(withSlugSuffix('studio-north', 'a1b2')).toBe('studio-north-a1b2');
  });
});
