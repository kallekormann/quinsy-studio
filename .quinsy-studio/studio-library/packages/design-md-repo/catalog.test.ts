import { describe, expect, it } from 'vitest';
import { getDefaultSystemId, loadDesignMdCatalog } from './catalog';

describe('design-md-repo catalog', () => {
  it('loads catalog with soft-ui as default id', () => {
    const catalog = loadDesignMdCatalog();
    expect(catalog.schema_version).toBe('1.0');
    expect(catalog.default_system_id).toBe('soft-ui');
    expect(getDefaultSystemId(catalog)).toBe('soft-ui');
  });
});
