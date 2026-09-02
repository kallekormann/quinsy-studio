/**
 * Moody Dropdown — Listbox select (not native OS chrome).
 * Panel language aligned with UserMenu popover.
 */
'use client';

import type { ReactNode } from 'react';
import {
  Listbox,
  ListboxButton,
  ListboxOption,
  ListboxOptions,
} from '@ui/primitives/headless/listbox';
import { ChevronDownIcon } from '@ui/components/atoms/Icon';
import { fieldLabelClassName } from '@ui/components/atoms/field-styles';
import { popoverPanelClass } from '@ui/styles/popover-styles';

export type DropdownOption<T extends string | number = string> = {
  value: T;
  label: ReactNode;
  disabled?: boolean;
};

export type DropdownProps<T extends string | number = string> = {
  value: T;
  onChange: (value: T) => void;
  options: DropdownOption<T>[];
  label?: ReactNode;
  disabled?: boolean;
  className?: string;
  buttonClassName?: string;
  'aria-label'?: string;
};

const panelClass = `${popoverPanelClass} mt-1 max-h-60 w-[var(--button-width)] overflow-auto`;

const buttonClass =
  'relative flex h-[34px] w-full items-center justify-between gap-2 rounded-md border border-[color:var(--line)] bg-[color:var(--color-surface)] px-3 text-left text-sm text-ink transition-[border-color,background-color] hover:bg-surface-2 focus-visible:border-accent-500 focus-visible:outline-none data-[open]:border-accent-500 disabled:cursor-not-allowed disabled:opacity-45';

function optionClass(focus: boolean, selected: boolean, disabled?: boolean) {
  return [
    'flex w-full cursor-default rounded-lg px-2.5 py-2 text-left text-sm',
    disabled ? 'opacity-40' : '',
    focus || selected
      ? 'bg-accent-100 text-accent-600 dark:bg-accent-100/20 dark:text-accent-500'
      : 'text-body',
    selected ? 'font-medium' : '',
  ]
    .filter(Boolean)
    .join(' ');
}

export function Dropdown<T extends string | number = string>({
  value,
  onChange,
  options,
  label,
  disabled = false,
  className = '',
  buttonClassName = '',
  'aria-label': ariaLabel,
}: DropdownProps<T>) {
  const selected = options.find((opt) => opt.value === value) ?? options[0];

  return (
    <div className={`w-full ${className}`}>
      {label ? <span className={fieldLabelClassName}>{label}</span> : null}
      <Listbox value={value} onChange={onChange} disabled={disabled}>
        <ListboxButton className={`${buttonClass} ${buttonClassName}`} aria-label={ariaLabel}>
          <span className="truncate">{selected?.label ?? 'Select…'}</span>
          <ChevronDownIcon size={16} className="shrink-0 text-muted" aria-hidden />
        </ListboxButton>
        <ListboxOptions portal anchor="bottom start" className={panelClass}>
          {options.map((opt) => (
            <ListboxOption
              key={String(opt.value)}
              value={opt.value}
              disabled={opt.disabled}
              className={({ focus, selected: isSelected }) =>
                optionClass(focus, isSelected, opt.disabled)
              }
            >
              {opt.label}
            </ListboxOption>
          ))}
        </ListboxOptions>
      </Listbox>
    </div>
  );
}
