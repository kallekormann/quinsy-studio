/**
 * Studio Library — styled native select (Headless UI + tokens).
 */
'use client';

import type { ComponentProps, ReactNode } from 'react';
import { Select as HeadlessSelect } from '../../primitives/headless/select';

export interface SelectProps extends ComponentProps<typeof HeadlessSelect> {
  label?: ReactNode;
}

const fieldClass =
  'w-full rounded-lg border border-neutral-300 bg-surface px-4 py-2 text-neutral-900 shadow-sm focus:border-primary-500 focus:outline-none focus:ring-2 focus:ring-primary-200 dark:border-neutral-600 dark:bg-surface-dark dark:text-neutral-100';

export function Select({ label, className = '', id, children, ...props }: SelectProps) {
  const selectId = id || 'select';
  return (
    <div className="w-full">
      {label && (
        <label htmlFor={selectId} className="mb-1 block text-sm font-medium text-neutral-600 dark:text-neutral-300">
          {label}
        </label>
      )}
      <HeadlessSelect id={selectId} className={`${fieldClass} ${className}`} {...props}>
        {children}
      </HeadlessSelect>
    </div>
  );
}
