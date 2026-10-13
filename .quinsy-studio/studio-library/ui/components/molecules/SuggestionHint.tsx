'use client';

import { Button } from '@ui/components/atoms/Button';

export type SuggestionHintProps = {
  label: string;
  actionLabel?: string;
  onAction: () => void;
  disabled?: boolean;
};

/** Non-blocking AI/heuristic suggestion row — uses the project accent tokens. */
export function SuggestionHint({
  label,
  actionLabel = 'Apply suggestion',
  onAction,
  disabled = false,
}: SuggestionHintProps) {
  return (
    <div className="mt-2 rounded-[12px] border border-accent-500/20 bg-accent-50/80 p-2.5 dark:border-accent-500/25 dark:bg-accent-500/10">
      <p className="text-xs text-neutral-600 dark:text-neutral-300">
        Suggested:{' '}
        <span className="font-medium text-neutral-800 dark:text-neutral-100">{label}</span>
      </p>
      <Button
        type="button"
        variant="ghost"
        buttonSize="sm"
        className="mt-1.5 h-auto min-h-0 px-0 py-0 text-xs font-medium text-accent-600 hover:bg-transparent hover:text-accent-500 dark:text-accent-400 dark:hover:text-accent-300"
        onClick={onAction}
        disabled={disabled}
      >
        {actionLabel}
      </Button>
    </div>
  );
}
