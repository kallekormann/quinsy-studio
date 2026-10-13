/**
 * Write systems/<id>/Design.md + catalog.json + SOURCE.md.
 * node packages/design-md-repo/scripts/write-cores.mjs
 */
import { mkdirSync, writeFileSync, readFileSync } from 'node:fs';
import { dirname, join } from 'node:path';
import { fileURLToPath } from 'node:url';
import { createRequire } from 'node:module';

const require = createRequire(import.meta.url);
const { dump } = require('js-yaml');

const root = join(dirname(fileURLToPath(import.meta.url)), '..');

// Profiles mirrored from compile-cores.ts — keep in sync when editing.
const SHARED_HOOKS = {
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

const SHARED_SPACING = {
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

const SHARED_RADIUS = {
  xs: 2,
  sm: 4,
  md: 8,
  lg: 12,
  xl: 16,
  '2xl': 24,
  full: 9999,
};

const SHARED_TYPO = {
  'Display/Hero-Large': { size: 56, lineHeight: 1.1, weight: 'Bold' },
  'Display/Hero-Medium': { size: 44, lineHeight: 1.2, weight: 'Bold' },
  'Heading/H1': { size: 32, lineHeight: 1.3, weight: 'Bold' },
  'Heading/H2': { size: 24, lineHeight: 1.35, weight: 'SemiBold' },
  'Heading/H3': { size: 20, lineHeight: 1.4, weight: 'SemiBold' },
  'Body/Regular': { size: 16, lineHeight: 1.5, weight: 'Regular' },
  'Utility/Caption': { size: 12, lineHeight: 1.4, weight: 'Regular' },
  'Utility/Code': { size: 13, lineHeight: 1.45, weight: 'Regular' },
};

const CORE_PROFILES = [
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

function toFrontmatter(p) {
  return {
    schema_version: '1.0',
    id: p.id,
    name: p.name,
    description: p.description,
    style_dna_affinity: p.style_dna_affinity,
    token_hooks: SHARED_HOOKS,
    spacing_px: SHARED_SPACING,
    radius_px: SHARED_RADIUS,
    typography: SHARED_TYPO,
    layout: {
      whitespace_bias: p.whitespace_bias,
      asymmetry: {
        enabled: p.asymmetry,
        recipes: p.asymmetry
          ? ['split_60_40_alternate', 'negative_margin_overlap', 'offset_media']
          : [],
      },
      color_distribution: { tone: 0.6, structure: 0.3, accent: 0.1 },
      borders: { default: p.borders, width_token: p.borders === 'none' ? null : 'sm' },
      shadows: { default: p.shadows },
      corners: { bias: p.corners },
    },
    components: {
      button_radius_token: p.corners === 'sharp' ? 'xs' : 'md',
      card_padding_token: p.whitespace_bias === 'dense' ? 'sm' : 'md',
      card_border: p.borders !== 'none',
    },
    modes: { light_dark: 'variable_modes' },
  };
}

function render(p) {
  const yamlDumpLineWidth = 100;
  const yaml = dump(toFrontmatter(p), { lineWidth: yamlDumpLineWidth, noRefs: true });
  return `---\n${yaml.trim()}\n---\n\n# ${p.name}\n\n${p.description}\n\n_Source: ${p.source}_\n\n_Grammar only — Style DNA / board supplies values at generate time. Does not restyle the product's own chrome._\n`;
}

const catalog = {
  schema_version: '1.0',
  default_system_id: 'soft-ui',
  systems: CORE_PROFILES.map((p) => ({
    id: p.id,
    name: p.name,
    description: p.description,
    source: p.source,
    default: !!p.default,
  })),
};

writeFileSync(join(root, 'catalog.json'), `${JSON.stringify(catalog, null, 2)}\n`);

const sourceLines = [
  '# Design.md SOURCE map',
  '',
  'Maps curated **Design.md** cores → editorial sources.',
  '',
  '| System id | Source | Notes |',
  '|-----------|--------|--------|',
];
for (const p of CORE_PROFILES) {
  sourceLines.push(
    `| \`${p.id}\` | ${p.source} | ${p.default ? '**Default** generate grammar' : 'Catalog choice'} |`,
  );
}
sourceLines.push(
  '',
  'Do not edit studio SKILL.md files in place — compile into `systems/<id>/Design.md`.',
  '',
);
writeFileSync(join(root, 'SOURCE.md'), sourceLines.join('\n'));

for (const p of CORE_PROFILES) {
  const dir = join(root, 'systems', p.id);
  mkdirSync(dir, { recursive: true });
  writeFileSync(join(dir, 'Design.md'), render(p));
}

// Sanity: ensure studio presets on disk are covered (except README-only missing folders)
const presetsRoot = join(root, '../../../../.quinsy-studio/knowledge-base/aesthetic-presets');
try {
  const { readdirSync, statSync } = await import('node:fs');
  const onDisk = readdirSync(presetsRoot).filter((name) => {
    try {
      return statSync(join(presetsRoot, name)).isDirectory();
    } catch {
      return false;
    }
  });
  const ids = new Set(CORE_PROFILES.map((p) => p.id));
  const missing = onDisk.filter((slug) => slug !== 'README' && !ids.has(slug));
  if (missing.length) {
    console.warn('Presets on disk not in CORE_PROFILES:', missing.join(', '));
  }
} catch {
  /* studio path optional in some checkouts */
}

console.log(`Wrote ${CORE_PROFILES.length} Design.md cores + catalog.json`);
void readFileSync; // keep import used if tree-shaken
