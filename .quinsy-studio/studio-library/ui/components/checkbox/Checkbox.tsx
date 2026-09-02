/**
 * Moody Bloom — styled checkbox (Headless UI + tokens).
 */
'use client';

import type { ComponentProps, ReactNode } from 'react';
import { Checkbox as HeadlessCheckbox } from '@ui/primitives/headless/checkbox';

export interface CheckboxProps extends Omit<ComponentProps<typeof HeadlessCheckbox>, 'children'> {
  label?: ReactNode;
}

const boxClass =
  'group flex size-4 shrink-0 items-center justify-center rounded-[5px] border-[1.5px] border-[color:var(--line-strong)] bg-surface transition-[border-color,background-color,box-shadow] focus-visible:border-accent-500 focus-visible:outline-none data-[checked]:border-accent-500 data-[checked]:bg-accent-500 data-[checked]:shadow-[inset_0_0_0_3px_var(--surface)] data-[disabled]:opacity-45';

export function Checkbox({ label, className = '', disabled, ...props }: CheckboxProps) {
  return (
    <label
      className={`inline-flex cursor-pointer items-center gap-2 text-sm text-body ${disabled ? 'cursor-not-allowed opacity-45' : ''}`}
    >
      <HeadlessCheckbox className={`${boxClass} ${className}`} disabled={disabled} {...props}>
        <svg
          className="size-3 stroke-[color:var(--accent-ink)] opacity-0 group-data-[checked]:opacity-100"
          viewBox="0 0 14 14"
          fill="none"
          aria-hidden
        >
          <path d="M3 7l3 3 5-6" strokeWidth={2} strokeLinecap="round" strokeLinejoin="round" />
        </svg>
      </HeadlessCheckbox>
      {label ? <span>{label}</span> : null}
    </label>
  );
}
