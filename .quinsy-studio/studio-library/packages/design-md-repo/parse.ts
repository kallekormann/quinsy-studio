/**
 * Parse validated Design.md → layout-engine params (MOOD-0260).
 * No per-preset hardcoded branches — behavior comes from frontmatter.
 */
import type { DesignMdDocument, DesignMdFrontmatter } from './types';
import { validateDesignMd, validateDesignMdFrontmatter } from './validate';
import type { DesignMdValidationError } from './types';

export type LayoutEngineParams = {
  systemId: string;
  systemName: string;
  schemaVersion: string;
  tokenHooks: DesignMdFrontmatter['token_hooks'];
  spacingPx: Record<string, number>;
  radiusPx: Record<string, number>;
  typography: DesignMdFrontmatter['typography'];
  layout: {
    whitespaceBias: DesignMdFrontmatter['layout']['whitespace_bias'];
    asymmetryEnabled: boolean;
    asymmetryRecipes: string[];
    colorDistribution: DesignMdFrontmatter['layout']['color_distribution'];
    borders: DesignMdFrontmatter['layout']['borders'];
    shadows: DesignMdFrontmatter['layout']['shadows'];
    corners: DesignMdFrontmatter['layout']['corners'];
  };
  components: Record<string, unknown>;
  modes: DesignMdFrontmatter['modes'];
  styleDnaAffinity: string[];
};

export type ParseDesignMdResult =
  { ok: true; params: LayoutEngineParams } | { ok: false; errors: DesignMdValidationError[] };

export function frontmatterToLayoutEngineParams(fm: DesignMdFrontmatter): LayoutEngineParams {
  return {
    systemId: fm.id,
    systemName: fm.name,
    schemaVersion: fm.schema_version,
    tokenHooks: fm.token_hooks,
    spacingPx: fm.spacing_px,
    radiusPx: fm.radius_px,
    typography: fm.typography,
    layout: {
      whitespaceBias: fm.layout.whitespace_bias,
      asymmetryEnabled: Boolean(fm.layout.asymmetry?.enabled),
      asymmetryRecipes: fm.layout.asymmetry?.recipes ?? [],
      colorDistribution: fm.layout.color_distribution,
      borders: fm.layout.borders,
      shadows: fm.layout.shadows,
      corners: fm.layout.corners,
    },
    components: fm.components ?? {},
    modes: fm.modes,
    styleDnaAffinity: fm.style_dna_affinity ?? [],
  };
}

export function documentToLayoutEngineParams(doc: DesignMdDocument): LayoutEngineParams {
  return frontmatterToLayoutEngineParams(doc.frontmatter);
}

/** Validate + parse Design.md text into engine params. */
export function parseDesignMdToLayoutParams(raw: string): ParseDesignMdResult {
  const validated = validateDesignMd(raw);
  if (!validated.ok) {
    return validated;
  }
  return { ok: true, params: documentToLayoutEngineParams(validated.document) };
}

/** Validate + parse an already-loaded frontmatter object. */
export function parseFrontmatterToLayoutParams(data: unknown): ParseDesignMdResult {
  const validated = validateDesignMdFrontmatter(data);
  if (!validated.ok) {
    return validated;
  }
  return { ok: true, params: documentToLayoutEngineParams(validated.document) };
}
