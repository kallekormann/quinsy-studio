import { describe, expect, it } from 'vitest';
import { getDefaultSystemId, loadDesignMdCatalog } from './catalog';

describe('design-md-repo catalog (MOOD-0255)', () => {
  it('loads catalog with Bloom as default id', () => {
    const catalog = loadDesignMdCatalog();
    expect(catalog.schema_version).toBe('1.0');
    expect(catalog.default_system_id).toBe('moody-bloom');
    expect(getDefaultSystemId(catalog)).toBe('moody-bloom');
  });
});
