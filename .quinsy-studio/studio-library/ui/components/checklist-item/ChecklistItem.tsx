/**
 * Studio Library — selectable checklist row (generic list item with toggle).
 */
'use client';

import { CheckIcon } from '../icon/Icon';

export interface ChecklistItemProps {
  label: string;
  meta?: string;
  checked?: boolean;
  onToggle?: () => void;
}

export function ChecklistItem({ label, meta, checked, onToggle }: ChecklistItemProps) {
  return (
    <div
      className={`flex items-center gap-3 rounded-lg border border-neutral-200 bg-surface p-4 shadow-sm ${
        checked ? 'opacity-60' : ''
      }`}
    >
      <button
        type="button"
        onClick={onToggle}
        aria-label={checked ? 'Checked' : 'Mark checked'}
        className={`flex h-6 w-6 shrink-0 items-center justify-center rounded-full border-2 transition-colors ${
          checked
            ? 'border-primary-600 bg-primary-600 text-white'
            : 'border-neutral-300 hover:border-primary-400'
        }`}
      >
        {checked && <CheckIcon size={14} />}
      </button>
      <div className="min-w-0 flex-1">
        <p className={`font-medium text-neutral-800 ${checked ? 'line-through' : ''}`}>{label}</p>
        {meta && <p className="text-sm text-neutral-500">{meta}</p>}
      </div>
    </div>
  );
}
