#!/usr/bin/env node
/**
 * Merge Supabase local keys from `supabase status -o env` into .env.local
 * Maps CLI output → NEXT_PUBLIC_* names Next.js expects.
 */
import { execSync } from 'node:child_process';
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const root = process.argv[2] ? path.resolve(process.argv[2]) : path.resolve(__dirname, '..', '..', '..');

const envPath = path.join(root, '.env.local');

const mapping = {
  API_URL: 'NEXT_PUBLIC_SUPABASE_URL',
  ANON_KEY: 'NEXT_PUBLIC_SUPABASE_ANON_KEY',
  PUBLISHABLE_KEY: 'NEXT_PUBLIC_SUPABASE_ANON_KEY',
  SERVICE_ROLE_KEY: 'SUPABASE_SERVICE_ROLE_KEY',
  SECRET_KEY: 'SUPABASE_SERVICE_ROLE_KEY',
};

function parseEnvOutput(output) {
  const values = {};
  for (const line of output.split('\n')) {
    const match = line.match(/^([A-Z_]+)="(.*)"$/);
    if (match) {
      values[match[1]] = match[2];
    }
  }
  return values;
}

function upsertEnvLines(existing, updates) {
  const lines = existing ? existing.split('\n') : [];
  const keys = new Set(Object.values(updates));
  const managedPrefixes = ['NEXT_PUBLIC_SUPABASE_', 'SUPABASE_SERVICE_ROLE_KEY'];

  const filtered = lines.filter((line) => {
    const trimmed = line.trim();
    if (!trimmed || trimmed.startsWith('#')) {
      return true;
    }
    const key = trimmed.split('=')[0]?.trim();
    if (keys.has(key)) {
      return false;
    }
    if (managedPrefixes.some((prefix) => key?.startsWith(prefix) || key === prefix)) {
      return false;
    }
    return true;
  });

  while (filtered.length > 0) {
    const last = filtered[filtered.length - 1]?.trim() ?? '';
    if (last === '' || last.startsWith('# Supabase')) {
      filtered.pop();
      continue;
    }
    break;
  }

  const block = ['', '# Supabase (from npm run supabase:env)'];
  for (const [key, value] of Object.entries(updates)) {
    block.push(`${key}=${value}`);
  }

  return [...filtered, ...block].join('\n').replace(/\n+$/, '\n');
}

function main() {
  let output;
  try {
    output = execSync('npx supabase status -o env', { cwd: root, encoding: 'utf8' });
  } catch {
    console.error('Run `npx supabase start` first.');
    process.exit(1);
  }

  const status = parseEnvOutput(output);
  const updates = {};
  for (const [from, to] of Object.entries(mapping)) {
    if (status[from] && !updates[to]) {
      updates[to] = status[from];
    }
  }

  if (!updates.NEXT_PUBLIC_SUPABASE_URL || !updates.NEXT_PUBLIC_SUPABASE_ANON_KEY) {
    console.error('Supabase status missing API_URL or ANON_KEY.');
    process.exit(1);
  }

  const existing = fs.existsSync(envPath) ? fs.readFileSync(envPath, 'utf8') : '';
  fs.writeFileSync(envPath, upsertEnvLines(existing, updates));
  console.log(`Updated ${path.relative(root, envPath)} with Supabase keys.`);
}

main();
