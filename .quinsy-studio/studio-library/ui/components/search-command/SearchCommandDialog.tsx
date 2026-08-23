/**
 * Studio Library — CMD-K style search dialog (Headless UI Dialog + Combobox).
 */
'use client';

import {
  Combobox,
  ComboboxInput,
  ComboboxOption,
  ComboboxOptions,
} from '../../primitives/headless/combobox';
import {
  Dialog,
  DialogBackdrop,
  DialogPanel,
} from '../../primitives/headless/dialog';

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
  return (
    <Dialog open={open} onClose={onClose} className="relative z-[100]">
      <DialogBackdrop className="fixed inset-0 bg-neutral-900/40 backdrop-blur-sm" />
      <div className="fixed inset-0 flex items-center justify-center px-4">
        <DialogPanel className="w-full max-w-lg overflow-hidden rounded-[16px] border border-neutral-200 bg-white shadow-2xl dark:border-neutral-700 dark:bg-surface-dark">
          <Combobox
            value={null}
            onChange={(result: SearchCommandResult | null) => {
              if (result) {
                onSelect(result.id);
                onClose();
              }
            }}
          >
            <div className="border-b border-neutral-200 px-3 py-2 dark:border-neutral-700">
              <ComboboxInput
                autoFocus
                className="w-full border-0 bg-transparent px-1 text-neutral-900 outline-none placeholder:text-neutral-400 dark:text-neutral-100"
                placeholder={placeholder}
                displayValue={() => query}
                onChange={(event) => onQueryChange(event.target.value)}
              />
              <p className="px-1 pt-1 text-[11px] text-neutral-500">{hint}</p>
            </div>
            <ComboboxOptions
              static
              className="max-h-72 overflow-y-auto py-1 empty:hidden focus:outline-none"
            >
              {results.length === 0 ? (
                <div className="px-4 py-6 text-center text-sm text-neutral-500">{emptyLabel}</div>
              ) : (
                results.map((result) => (
                  <ComboboxOption
                    key={result.id}
                    value={result}
                    className="flex w-full cursor-default items-center justify-between px-4 py-2 text-left text-sm data-[focus]:bg-neutral-50 dark:data-[focus]:bg-neutral-800"
                  >
                    <span className="truncate text-neutral-800 dark:text-neutral-100">{result.label}</span>
                    <span className="ml-3 shrink-0 text-xs capitalize text-neutral-500">{result.type}</span>
                  </ComboboxOption>
                ))
              )}
            </ComboboxOptions>
          </Combobox>
        </DialogPanel>
      </div>
    </Dialog>
  );
}
