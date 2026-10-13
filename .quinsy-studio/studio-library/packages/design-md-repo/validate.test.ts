import { readFileSync } from 'node:fs';
import { dirname, join } from 'node:path';
import { fileURLToPath } from 'node:url';
import { load as loadYaml } from 'js-yaml';
import { describe, expect, it } from 'vitest';
import { splitDesignMd, validateDesignMd, validateDesignMdFrontmatter } from './validate';

const here = dirname(fileURLToPath(import.meta.url));

function fixture(name: string): string {
  return readFileSync(join(here, 'fixtures', name), 'utf8');
}

describe('validateDesignMd', () => {
  it('accepts a minimal valid Design.md', () => {
    const result = validateDesignMd(fixture('valid-minimal.Design.md'));
    expect(result.ok).toBe(true);
    if (result.ok) {
      expect(result.document.frontmatter.id).toBe('minimal-fixture');
      expect(result.document.frontmatter.modes.light_dark).toBe('variable_modes');
      expect(result.document.narrative).toContain('Fixture only');
    }
  });

  it('rejects missing typography floor with field paths', () => {
    const result = validateDesignMd(fixture('invalid-missing-typography.Design.md'));
    expect(result.ok).toBe(false);
    if (!result.ok) {
      expect(result.errors.some((e) => e.path === '/typography')).toBe(true);
      expect(result.errors.length).toBeGreaterThan(0);
    }
  });

  it('rejects non-kebab id', () => {
    const result = validateDesignMd(fixture('invalid-bad-id.Design.md'));
    expect(result.ok).toBe(false);
    if (!result.ok) {
      expect(result.errors.some((e) => e.path === '/id')).toBe(true);
    }
  });

  it('rejects missing frontmatter fence', () => {
    const result = validateDesignMd('# just markdown\n');
    expect(result.ok).toBe(false);
    if (!result.ok) {
      expect(result.errors[0]?.message).toMatch(/frontmatter/i);
    }
  });

  it('validateDesignMdFrontmatter validates objects', () => {
    const split = splitDesignMd(fixture('valid-minimal.Design.md'));
    expect('yaml' in split).toBe(true);
    if (!('yaml' in split)) return;
    const data = loadYaml(split.yaml);
    const result = validateDesignMdFrontmatter(data);
    expect(result.ok).toBe(true);
  });
});
