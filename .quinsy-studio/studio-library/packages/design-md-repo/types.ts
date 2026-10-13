/**
 * Design.md frontmatter types.
 * Rules & hooks only — board Style DNA supplies values at generate time.
 */

export type WhitespaceBias = 'generous' | 'compact' | 'dense';
export type BorderDefault = 'none' | 'hairline' | 'thick';
export type ShadowDefault = 'none' | 'soft' | 'hard-ink';
export type CornerBias = 'rounded' | 'sharp';

export type TypographyStyle = {
  size: number;
  lineHeight: number;
  weight: string;
};

export type DesignMdTokenHooks = {
  color_primitives: string[];
  color_semantic: string[];
  spacing: string[];
  radius: string[];
};

export type DesignMdLayout = {
  whitespace_bias?: WhitespaceBias;
  asymmetry?: {
    enabled?: boolean;
    recipes?: string[];
  };
  color_distribution: {
    tone: number;
    structure: number;
    accent: number;
  };
  borders: {
    default: BorderDefault;
    width_token?: string | null;
  };
  shadows: {
    default: ShadowDefault;
  };
  corners: {
    bias: CornerBias;
  };
};

export type DesignMdFrontmatter = {
  schema_version: '1.0';
  id: string;
  name: string;
  description?: string;
  style_dna_affinity?: string[];
  token_hooks: DesignMdTokenHooks;
  spacing_px: Record<string, number>;
  radius_px: Record<string, number>;
  typography: Record<string, TypographyStyle>;
  layout: DesignMdLayout;
  components?: Record<string, unknown>;
  modes: {
    light_dark: 'variable_modes';
  };
};

export type DesignMdDocument = {
  frontmatter: DesignMdFrontmatter;
  /** Optional narrative markdown after frontmatter — not executed by the engine. */
  narrative: string;
};

export type DesignMdValidationError = {
  path: string;
  message: string;
};

export type DesignMdValidationResult =
  { ok: true; document: DesignMdDocument } | { ok: false; errors: DesignMdValidationError[] };
