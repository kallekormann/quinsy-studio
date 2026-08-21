import { parseContentRecord, parseItemTags } from '../item-tags/item-tags';
import type { SearchableItem } from './types';

function parseNoteText(item: SearchableItem): string {
  const parsed = parseContentRecord(item.contentJson);
  return typeof parsed.text === 'string' ? parsed.text : '';
}

function parseFileName(item: SearchableItem): string {
  const parsed = parseContentRecord(item.contentJson);
  return typeof parsed.fileName === 'string' ? parsed.fileName : '';
}

function parseFrameTitle(item: SearchableItem): string {
  const parsed = parseContentRecord(item.contentJson);
  return typeof parsed.title === 'string' ? parsed.title : 'Section';
}

function parsePalette(item: SearchableItem): string[] {
  const parsed = parseContentRecord(item.contentJson);
  const raw = parsed.palette;
  return Array.isArray(raw) ? raw.filter((c): c is string => typeof c === 'string') : [];
}

/** Concatenate searchable metadata (tags, text, filename, palette, type). */
export function buildItemSearchText(item: SearchableItem): string {
  const parts: string[] = [item.type, ...parseItemTags(item)];

  if (item.type === 'frame') {
    parts.push(parseFrameTitle(item));
  }
  if (item.type === 'note') {
    parts.push(parseNoteText(item));
  }
  if (item.type === 'image') {
    parts.push(parseFileName(item), ...parsePalette(item));
  }

  return parts.join(' ').toLowerCase();
}

export function itemMatchesSearch(item: SearchableItem, query: string): boolean {
  const needle = query.trim().toLowerCase();
  if (!needle) {
    return true;
  }
  return buildItemSearchText(item).includes(needle);
}

export function searchItems(items: SearchableItem[], query: string): SearchableItem[] {
  const needle = query.trim().toLowerCase();
  if (!needle) {
    return items;
  }
  return items.filter((item) => itemMatchesSearch(item, needle));
}

export function summarizeItem(item: SearchableItem): string {
  if (item.type === 'note') {
    const text = parseNoteText(item);
    return text ? `Note · ${text.slice(0, 48)}` : 'Note';
  }
  if (item.type === 'frame') {
    return `Frame · ${parseFrameTitle(item)}`;
  }
  const fileName = parseFileName(item);
  const tags = parseItemTags(item);
  if (fileName) {
    return `Image · ${fileName}`;
  }
  if (tags.length > 0) {
    return `Image · ${tags.join(', ')}`;
  }
  return 'Image';
}
