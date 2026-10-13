/**
 * Write systems/<id>/Design.md + catalog.json + SOURCE.md.
 * Run: npx tsx packages/design-md-repo/scripts/write-cores.ts
 * or: node --import tsx ...
 */
import { mkdirSync, writeFileSync } from 'node:fs';
import { dirname, join } from 'node:path';
import { fileURLToPath } from 'node:url';
import { dump } from 'js-yaml';
import { CORE_PROFILES, profileToFrontmatter, type CoreProfile } from '../compile-cores';

const root = join(dirname(fileURLToPath(import.meta.url)), '..');
const YAML_DUMP_LINE_WIDTH = 100;

function renderDesignMdFile(profile: CoreProfile): string {
  const fm = profileToFrontmatter(profile);
  const yaml = dump(fm, { lineWidth: YAML_DUMP_LINE_WIDTH, noRefs: true });
  return `---\n${yaml.trim()}\n---\n\n# ${profile.name}\n\n${profile.description}\n\n_Source: ${profile.source}_\n\n_Grammar only — Style DNA / board supplies values at generate time. Does not restyle the product's own chrome._\n`;
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
  const note = p.default ? '**Default** generate grammar' : 'Catalog choice';
  sourceLines.push(`| \`${p.id}\` | ${p.source} | ${note} |`);
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
  writeFileSync(join(dir, 'Design.md'), renderDesignMdFile(p));
}

console.log(`Wrote ${CORE_PROFILES.length} Design.md cores + catalog.json`);
