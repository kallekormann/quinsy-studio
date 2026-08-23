/**
 * Studio Library — styled textarea (Headless UI + tokens).
 */
'use client';

import type { ComponentProps } from 'react';
import { Textarea as HeadlessTextarea } from '../../primitives/headless/textarea';

export interface TextareaProps extends ComponentProps<typeof HeadlessTextarea> {
  label?: string;
}

const fieldClass =
  'w-full rounded-lg border border-neutral-300 bg-surface px-4 py-2 text-neutral-900 shadow-sm placeholder:text-neutral-400 focus:border-primary-500 focus:outline-none focus:ring-2 focus:ring-primary-200 dark:border-neutral-600 dark:bg-surface-dark dark:text-neutral-100';

export function Textarea({ label, className = '', id, ...props }: TextareaProps) {
  const inputId = id || 'textarea';
  return (
    <div className="w-full">
      {label && (
        <label htmlFor={inputId} className="mb-1 block text-sm font-medium text-neutral-600 dark:text-neutral-300">
          {label}
        </label>
      )}
      <HeadlessTextarea id={inputId} className={`${fieldClass} min-h-[96px] ${className}`} {...props} />
    </div>
  );
}
