import { dump } from 'js-yaml';
import type {
  DesignMdFrontmatter,
  WhitespaceBias,
  BorderDefault,
  ShadowDefault,
  CornerBias,
} from './types';

export type CoreProfile = {
  id: string;
  name: string;
  description: string;
  source: string;
  style_dna_affinity?: string[];
  whitespace_bias: WhitespaceBias;
  borders: BorderDefault;
  shadows: ShadowDefault;
  corners: CornerBias;
  asymmetry: boolean;
  default?: boolean;
};

const SHARED_HOOKS: DesignMdFrontmatter['token_hooks'] = {
  color_primitives: ['brand', 'gray'],
  color_semantic: [
    'bg.canvas',
    'bg.surface-primary',
    'bg.surface-secondary',
    'text.primary',
    'text.secondary',
    'text.tertiary',
    'brand.primary',
    'brand.secondary',
    'status.success-bg',
    'status.success-text',
    'status.warning-bg',
    'status.warning-text',
    'status.danger-bg',
    'status.danger-text',
    'status.info-bg',
    'status.info-text',
  ],
  spacing: ['3xs', '2xs', 'xs', 'sm', 'md', 'lg', 'xl', '2xl', '3xl'],
  radius: ['xs', 'sm', 'md', 'lg', 'xl', '2xl', 'full'],
};

const SHARED_SPACING: Record<string, number> = {
  '3xs': 2,
  '2xs': 4,
  xs: 8,
  sm: 12,
  md: 16,
  lg: 24,
  xl: 32,
  '2xl': 48,
  '3xl': 64,
};

const SHARED_RADIUS: Record<string, number> = {
  xs: 2,
  sm: 4,
  md: 8,
  lg: 12,
  xl: 16,
  '2xl': 24,
  full: 9999,
};

const SHARED_TYPO: DesignMdFrontmatter['typography'] = {
  'Display/Hero-Large': { size: 56, lineHeight: 1.1, weight: 'Bold' },
  'Display/Hero-Medium': { size: 44, lineHeight: 1.2, weight: 'Bold' },
  'Heading/H1': { size: 32, lineHeight: 1.3, weight: 'Bold' },
  'Heading/H2': { size: 24, lineHeight: 1.35, weight: 'SemiBold' },
  'Heading/H3': { size: 20, lineHeight: 1.4, weight: 'SemiBold' },
  'Body/Regular': { size: 16, lineHeight: 1.5, weight: 'Regular' },
  'Utility/Caption': { size: 12, lineHeight: 1.4, weight: 'Regular' },
  'Utility/Code': { size: 13, lineHeight: 1.45, weight: 'Regular' },
};

/** On-disk aesthetic presets; soft-ui is the default. */
export const CORE_PROFILES: CoreProfile[] = [
  {
    id: 'soft-ui',
    name: 'Soft UI',
    description: 'Warm consumer premium, glass, bounce.',
    source: 'aesthetic-presets/soft-ui/SKILL.md',
    default: true,
    whitespace_bias: 'generous',
    borders: 'none',
    shadows: 'soft',
    corners: 'rounded',
    asymmetry: false,
  },
  {
    id: 'minimalist-ui',
    name: 'Minimalist UI',
    description: 'Restrained whitespace, monochrome productivity.',
    source: 'aesthetic-presets/minimalist-ui/SKILL.md',
    whitespace_bias: 'generous',
    borders: 'hairline',
    shadows: 'none',
    corners: 'rounded',
    asymmetry: false,
  },
  {
    id: 'brutalist-ui',
    name: 'Brutalist UI',
    description: 'Raw high-contrast editorial — the contrast core.',
    source: 'aesthetic-presets/brutalist-ui/SKILL.md',
    style_dna_affinity: ['Bold', 'Editorial'],
    whitespace_bias: 'dense',
    borders: 'thick',
    shadows: 'hard-ink',
    corners: 'sharp',
    asymmetry: true,
  },
  {
    id: 'apple-like-ui',
    name: 'Apple-like UI',
    description: 'Cupertino glass, system hierarchy.',
    source: 'aesthetic-presets/apple-like-ui/SKILL.md',
    whitespace_bias: 'generous',
    borders: 'none',
    shadows: 'soft',
    corners: 'rounded',
    asymmetry: false,
  },
  {
    id: 'stripe-like-ui',
    name: 'Stripe-like UI',
    description: 'FinTech precision, soft structural elevation.',
    source: 'aesthetic-presets/stripe-like-ui/SKILL.md',
    whitespace_bias: 'compact',
    borders: 'hairline',
    shadows: 'soft',
    corners: 'rounded',
    asymmetry: false,
  },
  {
    id: 'linear-like-ui',
    name: 'Linear-like UI',
    description: 'Dark productivity, keyboard-first density.',
    source: 'aesthetic-presets/linear-like-ui/SKILL.md',
    whitespace_bias: 'compact',
    borders: 'hairline',
    shadows: 'none',
    corners: 'rounded',
    asymmetry: false,
  },
  {
    id: 'notion-like-ui',
    name: 'Notion-like UI',
    description: 'Calm workspace, blocky surfaces.',
    source: 'aesthetic-presets/notion-like-ui/SKILL.md',
    whitespace_bias: 'generous',
    borders: 'hairline',
    shadows: 'none',
    corners: 'rounded',
    asymmetry: false,
  },
  {
    id: 'adobe-like-ui',
    name: 'Adobe-like UI',
    description: 'Pro creative chrome, dense panels.',
    source: 'aesthetic-presets/adobe-like-ui/SKILL.md',
    whitespace_bias: 'dense',
    borders: 'hairline',
    shadows: 'none',
    corners: 'sharp',
    asymmetry: false,
  },
  {
    id: 'paypal-like-ui',
    name: 'PayPal-like UI',
    description: 'Trust and commerce clarity.',
    source: 'aesthetic-presets/paypal-like-ui/SKILL.md',
    whitespace_bias: 'compact',
    borders: 'hairline',
    shadows: 'soft',
    corners: 'rounded',
    asymmetry: false,
  },
  {
    id: 'amazon-like-ui',
    name: 'Amazon-like UI',
    description: 'Commerce density and scanability.',
    source: 'aesthetic-presets/amazon-like-ui/SKILL.md',
    whitespace_bias: 'dense',
    borders: 'hairline',
    shadows: 'none',
    corners: 'sharp',
    asymmetry: false,
  },
  {
    id: 'nike-like-ui',
    name: 'Nike-like UI',
    description: 'Bold athletic, hero imagery bias.',
    source: 'aesthetic-presets/nike-like-ui/SKILL.md',
    whitespace_bias: 'compact',
    borders: 'none',
    shadows: 'soft',
    corners: 'rounded',
    asymmetry: true,
  },
  {
    id: 'space-x-like-ui',
    name: 'SpaceX-like UI',
    description: 'Industrial sci-fi mission control.',
    source: 'aesthetic-presets/space-x-like-ui/SKILL.md',
    whitespace_bias: 'dense',
    borders: 'hairline',
    shadows: 'none',
    corners: 'sharp',
    asymmetry: false,
  },
  {
    id: 'nordic-design-ui',
    name: 'Nordic Design UI',
    description: 'Light calm Scandinavian productivity.',
    source: 'aesthetic-presets/nordic-design-ui/SKILL.md',
    whitespace_bias: 'generous',
    borders: 'none',
    shadows: 'soft',
    corners: 'rounded',
    asymmetry: false,
  },
  {
    id: 'cosmic-void-ui',
    name: 'Cosmic Void UI',
    description: 'Deep space, luminous accents.',
    source: 'aesthetic-presets/cosmic-void-ui/SKILL.md',
    whitespace_bias: 'generous',
    borders: 'none',
    shadows: 'soft',
    corners: 'rounded',
    asymmetry: true,
  },
  {
    id: 'technical-blueprint-ui',
    name: 'Technical Blueprint UI',
    description: 'CAD / terminal blueprint grammar.',
    source: 'aesthetic-presets/technical-blueprint-ui/SKILL.md',
    whitespace_bias: 'dense',
    borders: 'hairline',
    shadows: 'none',
    corners: 'sharp',
    asymmetry: false,
  },
  {
    id: 'academic-editorial-ui',
    name: 'Academic Editorial UI',
    description: 'Scholarly structure for long-form.',
    source: 'aesthetic-presets/academic-editorial-ui/SKILL.md',
    whitespace_bias: 'generous',
    borders: 'hairline',
    shadows: 'none',
    corners: 'sharp',
    asymmetry: true,
  },
];

export function profileToFrontmatter(profile: CoreProfile): DesignMdFrontmatter {
  return {
    schema_version: '1.0',
    id: profile.id,
    name: profile.name,
    description: profile.description,
    style_dna_affinity: profile.style_dna_affinity,
    token_hooks: SHARED_HOOKS,
    spacing_px: SHARED_SPACING,
    radius_px: SHARED_RADIUS,
    typography: SHARED_TYPO,
    layout: {
      whitespace_bias: profile.whitespace_bias,
      asymmetry: {
        enabled: profile.asymmetry,
        recipes: profile.asymmetry
          ? ['split_60_40_alternate', 'negative_margin_overlap', 'offset_media']
          : [],
      },
      color_distribution: { tone: 0.6, structure: 0.3, accent: 0.1 },
      borders: {
        default: profile.borders,
        width_token: profile.borders === 'none' ? null : 'sm',
      },
      shadows: { default: profile.shadows },
      corners: { bias: profile.corners },
    },
    components: {
      button_radius_token: profile.corners === 'sharp' ? 'xs' : 'md',
      card_padding_token: profile.whitespace_bias === 'dense' ? 'sm' : 'md',
      card_border: profile.borders !== 'none',
    },
    modes: { light_dark: 'variable_modes' },
  };
}

const YAML_DUMP_LINE_WIDTH = 100;

export function renderDesignMdFile(profile: CoreProfile): string {
  const fm = profileToFrontmatter(profile);
  const yaml = dump(fm, { lineWidth: YAML_DUMP_LINE_WIDTH, noRefs: true });
  return `---\n${yaml.trim()}\n---\n\n# ${profile.name}\n\n${profile.description}\n\n_Source: ${profile.source}_\n\n_Grammar only — Style DNA / board supplies values at generate time. Does not restyle the product's own chrome._\n`;
}
