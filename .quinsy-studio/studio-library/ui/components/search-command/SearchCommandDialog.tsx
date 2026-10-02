/**
 * Studio Library — CMD-K style search dialog for filterable item lists.
 * Pass precomputed results. Group them with `type`. Optional `detail` is a second line.
 */
'use client';

import { useEffect, useState } from 'react';
import { createPortal } from 'react-dom';
import { Search } from 'lucide-react';
import { Input } from '../input/Input';
import { Kbd } from '../kbd';

export type SearchCommandResult = {
  id: string;
  label: string;
  type: string;
  detail?: string;
};

export type SearchCommandDialogProps = {
  open: boolean;
  query: string;
  results: SearchCommandResult[];
  placeholder?: string;
  hint?: string;
  emptyLabel?: string;
  /** Render in place, for a sticker. The app uses the overlay. */
  inline?: boolean;
  onQueryChange: (value: string) => void;
  onClose: () => void;
  onSelect: (id: string) => void;
};

export function SearchCommandDialog({
  open,
  query,
  results,
  placeholder = 'Search',
  hint = 'to close',
  emptyLabel = 'No matches',
  inline = false,
  onQueryChange,
  onClose,
  onSelect,
}: SearchCommandDialogProps) {
  const [active, setActive] = useState(0);

  useEffect(() => {
    setActive(0);
  }, [query, results.length]);

  useEffect(() => {
    if (!open || inline) return;
    const onKeyDown = (event: KeyboardEvent) => {
      if (event.key === 'Escape') {
        event.preventDefault();
        onClose();
      }
      if (event.key === 'ArrowDown') {
        event.preventDefault();
        setActive((index) => Math.min(index + 1, Math.max(results.length - 1, 0)));
      }
      if (event.key === 'ArrowUp') {
        event.preventDefault();
        setActive((index) => Math.max(index - 1, 0));
      }
      if (event.key === 'Enter' && results[active]) {
        event.preventDefault();
        onSelect(results[active].id);
        onClose();
      }
    };
    window.addEventListener('keydown', onKeyDown);
    return () => window.removeEventListener('keydown', onKeyDown);
  }, [open, inline, onClose, onSelect, results, active]);

  if (!open) return null;

  const panel = (
    <div
      className="w-full max-w-lg overflow-hidden rounded-2xl border border-border bg-popover text-popover-foreground shadow-md"
      onMouseDown={(event) => event.stopPropagation()}
      role="dialog"
      aria-label="Search"
    >
      <div className="flex items-center gap-2 border-b border-border px-3">
        <Search className="size-4 shrink-0 text-muted-foreground" aria-hidden />
        <Input
          autoFocus
          placeholder={placeholder}
          value={query}
          onChange={(event) => onQueryChange(event.target.value)}
          className="h-10 border-0 bg-transparent px-0 shadow-none focus-visible:border-transparent focus-visible:ring-0"
        />
        <span className="flex shrink-0 items-center gap-1.5 text-xs text-muted-foreground">
          <Kbd>Esc</Kbd>
          {hint}
        </span>
      </div>
      <ul className="max-h-80 overflow-y-auto px-1 py-1">
        {results.length === 0 ? (
          <li className="px-3 py-6 text-center text-sm text-muted-foreground">{emptyLabel}</li>
        ) : (
          results.map((result, index) => (
            <li key={result.id}>
              {index === 0 || results[index - 1].type !== result.type ? (
                <p className="px-2 pb-1 pt-2 text-[11px] font-semibold uppercase tracking-wide text-muted-foreground">
                  {result.type}
                </p>
              ) : null}
              <button
                type="button"
                className={`w-full rounded-lg px-2 py-1.5 text-left ${index === active ? 'bg-muted' : 'hover:bg-muted'}`}
                onMouseEnter={() => setActive(index)}
                onClick={() => {
                  onSelect(result.id);
                  onClose();
                }}
              >
                <span className="block truncate text-sm">{result.label}</span>
                {result.detail ? (
                  <span className="block truncate text-xs text-muted-foreground">{result.detail}</span>
                ) : null}
              </button>
            </li>
          ))
        )}
      </ul>
    </div>
  );

  if (inline) return panel;

  return createPortal(
    <div
      className="fixed inset-0 z-[100] flex items-start justify-center bg-[var(--scrim)] px-4 pt-[15vh]"
      onMouseDown={onClose}
    >
      {panel}
    </div>,
    document.body,
  );
}
