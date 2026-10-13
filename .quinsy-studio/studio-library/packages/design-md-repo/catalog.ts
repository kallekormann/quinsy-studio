/**
 * Catalog index for curated Design.md systems.
 */
import { readFileSync } from 'node:fs';
import { dirname, join } from 'node:path';
import { fileURLToPath } from 'node:url';

export type DesignMdCatalogEntry = {
  id: string;
  name: string;
  description?: string;
  source?: string;
  default?: boolean;
};

export type DesignMdCatalog = {
  schema_version: string;
  default_system_id: string;
  systems: DesignMdCatalogEntry[];
};

const CATALOG_PATH = join(dirname(fileURLToPath(import.meta.url)), 'catalog.json');

export function loadDesignMdCatalog(): DesignMdCatalog {
  return JSON.parse(readFileSync(CATALOG_PATH, 'utf8')) as DesignMdCatalog;
}

export function getDefaultSystemId(catalog: DesignMdCatalog = loadDesignMdCatalog()): string {
  return catalog.default_system_id;
}
