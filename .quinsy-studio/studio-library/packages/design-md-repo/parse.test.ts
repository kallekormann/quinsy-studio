import { readFileSync } from 'node:fs';
import { dirname, join } from 'node:path';
import { fileURLToPath } from 'node:url';
import { describe, expect, it } from 'vitest';
import { parseDesignMdToLayoutParams } from './parse';

const here = dirname(fileURLToPath(import.meta.url));

function systemDesignMd(id: string): string {
  return readFileSync(join(here, 'systems', id, 'Design.md'), 'utf8');
}

describe('parseDesignMdToLayoutParams', () => {
  it('parses soft-ui and Brutalist into params without preset id branches', () => {
    for (const id of ['soft-ui', 'brutalist-ui', 'stripe-like-ui'] as const) {
      const result = parseDesignMdToLayoutParams(systemDesignMd(id));
      expect(result.ok).toBe(true);
      if (!result.ok) continue;
      expect(result.params.systemId).toBe(id);
      expect(result.params.tokenHooks.spacing.length).toBeGreaterThan(0);
      expect(result.params.spacingPx.md).toBeTypeOf('number');
      expect(result.params.modes.light_dark).toBe('variable_modes');
      expect(result.params.layout.colorDistribution).toMatchObject({
        tone: expect.any(Number),
        structure: expect.any(Number),
        accent: expect.any(Number),
      });
    }
  });

  it('surfaces Brutalist sharp / hard-ink from params (not hardcoded id switch)', () => {
    const result = parseDesignMdToLayoutParams(systemDesignMd('brutalist-ui'));
    expect(result.ok).toBe(true);
    if (!result.ok) return;
    expect(result.params.layout.corners.bias).toBe('sharp');
    expect(result.params.layout.shadows.default).toBe('hard-ink');
    expect(result.params.layout.asymmetryEnabled).toBe(true);
  });

  it('rejects invalid Design.md with field errors', () => {
    const result = parseDesignMdToLayoutParams('# no frontmatter\n');
    expect(result.ok).toBe(false);
    if (!result.ok) {
      expect(result.errors.length).toBeGreaterThan(0);
    }
  });
});
