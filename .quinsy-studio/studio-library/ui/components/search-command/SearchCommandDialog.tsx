/**
 * Studio Library — CMD-K style search dialog for filterable item lists.
 * Pass precomputed results or wire to packages/item-search in the project.
 */
'use client';

import { useEffect } from 'react';
import { Input } from '../input/Input';

export type SearchCommandResult = {
  id: string;
  label: string;
  type: string;
};

export type SearchCommandDialogProps = {
  open: boolean;
  query: string;
  results: SearchCommandResult[];
  placeholder?: string;
  hint?: string;
  emptyLabel?: string;
  onQueryChange: (value: string) => void;
  onClose: () => void;
  onSelect: (id: string) => void;
};

export function SearchCommandDialog({
  open,
  query,
  results,
  placeholder = 'Search tags, filenames, notes, colors…',
  hint = '⌘K · matches filter the canvas · Esc to close',
  emptyLabel = 'No matches',
  onQueryChange,
  onClose,
  onSelect,
}: SearchCommandDialogProps) {
  useEffect(() => {
    if (!open) return;
    const onKeyDown = (event: KeyboardEvent) => {
      if (event.key === 'Escape') {
        event.preventDefault();
        onClose();
      }
    };
    window.addEventListener('keydown', onKeyDown);
    return () => window.removeEventListener('keydown', onKeyDown);
  }, [open, onClose]);

  if (!open) {
    return null;
  }

  return (
    <div
      className="fixed inset-0 z-50 flex items-start justify-center bg-neutral-900/40 px-4 pt-[12vh] backdrop-blur-sm"
      onMouseDown={onClose}
    >
      <div
        className="w-full max-w-lg overflow-hidden rounded-[16px] border border-neutral-200 bg-white shadow-2xl dark:border-neutral-700 dark:bg-surface-dark"
        onMouseDown={(event) => event.stopPropagation()}
        role="dialog"
        aria-label="Search items"
      >
        <div className="border-b border-neutral-200 px-3 py-2 dark:border-neutral-700">
          <Input
            autoFocus
            placeholder={placeholder}
            value={query}
            onChange={(e) => onQueryChange(e.target.value)}
            className="border-0 bg-transparent px-1 shadow-none focus:ring-0"
          />
          <p className="px-1 pt-1 text-[11px] text-neutral-500">{hint}</p>
        </div>
        <ul className="max-h-72 overflow-y-auto py-1">
          {results.length === 0 ? (
            <li className="px-4 py-6 text-center text-sm text-neutral-500">{emptyLabel}</li>
          ) : (
            results.map((result) => (
              <li key={result.id}>
                <button
                  type="button"
                  className="flex w-full items-center justify-between px-4 py-2 text-left text-sm hover:bg-neutral-50 dark:hover:bg-neutral-800"
                  onClick={() => {
                    onSelect(result.id);
                    onClose();
                  }}
                >
                  <span className="truncate text-neutral-800 dark:text-neutral-100">
                    {result.label}
                  </span>
                  <span className="ml-3 shrink-0 text-xs capitalize text-neutral-500">
                    {result.type}
                  </span>
                </button>
              </li>
            ))
          )}
        </ul>
      </div>
    </div>
  );
}
