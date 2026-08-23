/**
 * Studio Library — styled checkbox (Headless UI + tokens).
 */
'use client';

import type { ComponentProps, ReactNode } from 'react';
import { Checkbox as HeadlessCheckbox } from '../../primitives/headless/checkbox';

export interface CheckboxProps extends Omit<ComponentProps<typeof HeadlessCheckbox>, 'children'> {
  label?: ReactNode;
}

export function Checkbox({ label, className = '', ...props }: CheckboxProps) {
  return (
    <label className="inline-flex cursor-pointer items-center gap-2 text-sm text-neutral-800 dark:text-neutral-100">
      <HeadlessCheckbox
        className={`group flex size-4 items-center justify-center rounded border border-neutral-400 bg-surface data-[checked]:border-primary-600 data-[checked]:bg-primary-600 data-[focus]:outline data-[focus]:outline-2 data-[focus]:outline-offset-2 data-[focus]:outline-primary-500 dark:border-neutral-500 ${className}`}
        {...props}
      >
        <svg
          className="size-3 stroke-white opacity-0 group-data-[checked]:opacity-100"
          viewBox="0 0 14 14"
          fill="none"
        >
          <path d="M3 7l3 3 5-6" strokeWidth={2} strokeLinecap="round" strokeLinejoin="round" />
        </svg>
      </HeadlessCheckbox>
      {label ? <span>{label}</span> : null}
    </label>
  );
}
