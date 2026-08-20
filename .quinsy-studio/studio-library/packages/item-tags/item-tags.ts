import type { TagContentCarrier } from './types';

export function parseContentRecord(contentJson: string): Record<string, unknown> {
  try {
    return JSON.parse(contentJson) as Record<string, unknown>;
  } catch {
    return {};
  }
}

export function parseItemTags(item: TagContentCarrier): string[] {
  const parsed = parseContentRecord(item.contentJson);
  const raw = parsed.tags;
  if (!Array.isArray(raw)) {
    return [];
  }
  return raw
    .filter((tag): tag is string => typeof tag === 'string')
    .map((tag) => tag.trim().toLowerCase())
    .filter(Boolean);
}

export function normalizeTags(tags: string[]): string[] {
  const seen = new Set<string>();
  const normalized: string[] = [];
  for (const tag of tags) {
    const value = tag.trim().toLowerCase();
    if (!value || seen.has(value)) continue;
    seen.add(value);
    normalized.push(value);
  }
  return normalized;
}

export function itemMatchesTagFilter(item: TagContentCarrier, query: string): boolean {
  const needle = query.trim().toLowerCase();
  if (!needle) {
    return true;
  }
  return parseItemTags(item).some((tag) => tag.includes(needle));
}

export function collectTags(items: TagContentCarrier[]): string[] {
  const tags = new Set<string>();
  for (const item of items) {
    for (const tag of parseItemTags(item)) {
      tags.add(tag);
    }
  }
  return [...tags].sort();
}
