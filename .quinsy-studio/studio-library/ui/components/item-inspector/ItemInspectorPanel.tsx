/**
 * Studio Library — contextual metadata panel for a selected canvas item.
 * Tags + exclusive accordion sections via children.
 */
'use client';

import type { ReactNode } from 'react';
import { Badge } from '../badge/Badge';
import { Input } from '../input/Input';
import { InspectorAccordionSection, InspectorPanelShell } from '../molecules/InspectorPanelShell';

export type ItemInspectorPanelProps = {
  title: string;
  subtitle?: string;
  itemType: string;
  tags: string[];
  onTagsChange: (tags: string[]) => void;
  footer?: ReactNode;
  children?: ReactNode;
  className?: string;
  onClose?: () => void;
};

export function ItemInspectorPanel({
  title,
  subtitle,
  itemType,
  tags,
  onTagsChange,
  footer,
  children,
  className = '',
  onClose,
}: ItemInspectorPanelProps) {
  const handleTagInput = (raw: string) => {
    const nextTags = raw
      .split(',')
      .map((tag) => tag.trim())
      .filter(Boolean);
    onTagsChange(nextTags);
  };

  return (
    <InspectorPanelShell
      eyebrow="Item"
      title={title}
      subtitle={subtitle ?? itemType}
      className={className}
      defaultOpenSection="tags"
      onClose={onClose}
    >
      <InspectorAccordionSection id="tags" title="Tags">
        <Input
          placeholder="Tags, comma-separated"
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
        {footer ? <div className="mt-2 text-[11px] text-neutral-500">{footer}</div> : null}
      </InspectorAccordionSection>
      {children}
    </InspectorPanelShell>
  );
}
