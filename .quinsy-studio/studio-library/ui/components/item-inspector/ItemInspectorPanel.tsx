/**
 * Studio Library — contextual metadata panel for a selected canvas item.
 * Tags today; extend with notes, EXIF, etc. via `children` or extra fields.
 */
'use client';

import type { ReactNode } from 'react';
import { Badge } from '../badge/Badge';
import { Input } from '../input/Input';

export type ItemInspectorPanelProps = {
  title: string;
  subtitle?: string;
  itemType: string;
  tags: string[];
  onTagsChange: (tags: string[]) => void;
  footer?: ReactNode;
  className?: string;
};

export function ItemInspectorPanel({
  title,
  subtitle,
  itemType,
  tags,
  onTagsChange,
  footer,
  className = '',
}: ItemInspectorPanelProps) {
  const handleTagInput = (raw: string) => {
    const nextTags = raw
      .split(',')
      .map((tag) => tag.trim())
      .filter(Boolean);
    onTagsChange(nextTags);
  };

  return (
    <aside
      className={`absolute right-4 top-20 z-10 w-72 rounded-[16px] border border-neutral-200/80 bg-white/95 p-3 shadow-lg backdrop-blur dark:border-neutral-700 dark:bg-surface-dark/95 ${className}`}
    >
      <p className="text-xs font-semibold uppercase tracking-wide text-neutral-500">Item</p>
      <p className="mt-1 truncate text-sm font-medium text-neutral-800 dark:text-neutral-100">
        {title}
      </p>
      {subtitle ? (
        <p className="mt-0.5 truncate text-xs text-neutral-500">{subtitle}</p>
      ) : (
        <p className="mt-0.5 text-xs capitalize text-neutral-500">{itemType}</p>
      )}

      <div className="mt-3 border-t border-neutral-200 pt-3 dark:border-neutral-700">
        <label className="mb-1 block text-xs font-medium text-neutral-600 dark:text-neutral-300">
          Tags
        </label>
        <Input
          placeholder="comma-separated tags"
          defaultValue={tags.join(', ')}
          key={`${title}-${tags.join('|')}`}
          onBlur={(e) => handleTagInput(e.target.value)}
          onKeyDown={(e) => {
            if (e.key === 'Enter') {
              e.currentTarget.blur();
            }
          }}
        />
        {tags.length > 0 && (
          <div className="mt-2 flex flex-wrap gap-1">
            {tags.map((tag) => (
              <Badge key={tag}>{tag}</Badge>
            ))}
          </div>
        )}
        {footer ? (
          <div className="mt-2 text-[11px] text-neutral-500">{footer}</div>
        ) : null}
      </div>
    </aside>
  );
}
