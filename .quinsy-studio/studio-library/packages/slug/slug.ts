export function slugifyName(name: string, fallback = 'item'): string {
  const base = name
    .trim()
    .toLowerCase()
    .replace(/[^a-z0-9]+/g, '-')
    .replace(/^-+|-+$/g, '')
    .slice(0, 48);
  return base || fallback;
}

export function withSlugSuffix(slug: string, suffix: string): string {
  const trimmed = slug.slice(0, 40);
  return `${trimmed}-${suffix}`;
}
