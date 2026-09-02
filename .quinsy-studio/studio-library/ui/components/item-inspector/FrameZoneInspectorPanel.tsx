'use client';

import type { ReactNode } from 'react';
import { Badge } from '@ui/components/badge/Badge';
import { Input } from '@ui/components/input/Input';
import { Dropdown } from '@ui/components/dropdown';
import {
  InspectorPanelSection,
  InspectorPanelShell,
} from '@ui/components/molecules/InspectorPanelShell';
import { SuggestionHint } from '@ui/components/molecules/SuggestionHint';
import { PresentationDeckIcon } from '@ui/components/atoms/Icon';
import type { PresentationSectionRole } from '@/lib/presentation/presentation-roles';
import {
  PRESENTATION_ROLE_OPTIONS,
  isUniquePresentationRole,
  presentationRoleLabel,
} from '@/lib/presentation/presentation-roles';

export type FrameZoneInspectorPanelProps = {
  title: string;
  tags: string[];
  presentationRole: PresentationSectionRole | null;
  usedRoles: Set<PresentationSectionRole>;
  suggestedRole: PresentationSectionRole | null;
  onTagsChange: (tags: string[]) => void;
  onPresentationRoleChange: (role: PresentationSectionRole | null) => void;
  footer?: ReactNode;
  className?: string;
  onClose?: () => void;
};

export function FrameZoneInspectorPanel({
  title,
  tags,
  presentationRole,
  usedRoles,
  suggestedRole,
  onTagsChange,
  onPresentationRoleChange,
  footer,
  className = '',
  onClose,
}: FrameZoneInspectorPanelProps) {
  const handleTagInput = (raw: string) => {
    const nextTags = raw
      .split(',')
      .map((tag) => tag.trim())
      .filter(Boolean);
    onTagsChange(nextTags);
  };

  const isRoleDisabled = (role: PresentationSectionRole): boolean => {
    if (!isUniquePresentationRole(role)) {
      return false;
    }
    if (presentationRole === role) {
      return false;
    }
    return usedRoles.has(role);
  };

  return (
    <InspectorPanelShell
      eyebrow="Selection"
      title={title}
      subtitle="Idea zone · double-click title on canvas to rename"
      className={className}
      onClose={onClose}
    >
      <InspectorPanelSection>
        <Dropdown
          label="Use in presentation as"
          value={presentationRole ?? ''}
          onChange={(value) => {
            onPresentationRoleChange(value ? (value as PresentationSectionRole) : null);
          }}
          options={[
            { value: '', label: 'Not included in presentation' },
            ...PRESENTATION_ROLE_OPTIONS.map((option) => ({
              value: option.id,
              label: `${option.label}${isRoleDisabled(option.id) ? ' (in use)' : ''}`,
              disabled: isRoleDisabled(option.id),
            })),
          ]}
        />

        {presentationRole ? (
          <div className="mt-2 flex items-center gap-1.5 text-[11px] text-accent-600 dark:text-accent-400">
            <PresentationDeckIcon size={14} aria-hidden />
            <span>In presentation · {presentationRoleLabel(presentationRole)}</span>
          </div>
        ) : null}

        {!presentationRole && suggestedRole ? (
          <SuggestionHint
            label={presentationRoleLabel(suggestedRole)}
            onAction={() => onPresentationRoleChange(suggestedRole)}
            disabled={isRoleDisabled(suggestedRole)}
          />
        ) : null}
      </InspectorPanelSection>

      <InspectorPanelSection>
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
        {footer ? <div className="mt-2 text-[11px] text-neutral-500">{footer}</div> : null}
      </InspectorPanelSection>
    </InspectorPanelShell>
  );
}
