import { readdirSync, readFileSync, statSync } from 'node:fs';
import { dirname, join } from 'node:path';
import { fileURLToPath } from 'node:url';
import { describe, expect, it } from 'vitest';
import { loadDesignMdCatalog } from './catalog';
import { CORE_PROFILES } from './compile-cores';
import { validateDesignMd } from './validate';

const here = dirname(fileURLToPath(import.meta.url));

describe('compiled Design.md cores (MOOD-0256)', () => {
  it('catalog lists every profile with Bloom default', () => {
    const catalog = loadDesignMdCatalog();
    expect(catalog.default_system_id).toBe('moody-bloom');
    expect(catalog.systems).toHaveLength(CORE_PROFILES.length);
    const bloom = catalog.systems.find((s) => s.id === 'moody-bloom');
    expect(bloom?.default).toBe(true);
    expect(catalog.systems.filter((s) => s.default).length).toBe(1);
  });

  it('every systems/*/Design.md validates', () => {
    const systemsDir = join(here, 'systems');
    const ids = readdirSync(systemsDir).filter((name) => {
      try {
        return statSync(join(systemsDir, name)).isDirectory();
      } catch {
        return false;
      }
    });
    expect(ids.length).toBeGreaterThanOrEqual(17);
    for (const id of ids) {
      const raw = readFileSync(join(systemsDir, id, 'Design.md'), 'utf8');
      const result = validateDesignMd(raw);
      expect(result.ok, `${id}: ${!result.ok ? JSON.stringify(result.errors) : ''}`).toBe(true);
    }
  });

  it('Bloom and Brutalist contrast pair both validate', () => {
    for (const id of ['moody-bloom', 'brutalist-ui']) {
      const raw = readFileSync(join(here, 'systems', id, 'Design.md'), 'utf8');
      const result = validateDesignMd(raw);
      expect(result.ok).toBe(true);
    }
  });
});
