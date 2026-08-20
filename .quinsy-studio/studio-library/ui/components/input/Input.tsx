/**
 * Studio Library — generic text input.
 */
import type { ComponentProps } from 'react';

export interface InputProps extends ComponentProps<'input'> {
  label?: string;
}

export function Input({ label, className = '', id, ...props }: InputProps) {
  const inputId = id || 'input';
  return (
    <div className="w-full">
      {label && (
        <label htmlFor={inputId} className="mb-1 block text-sm font-medium text-neutral-600">
          {label}
        </label>
      )}
      <input
        id={inputId}
        className={`w-full rounded-lg border border-neutral-300 bg-surface px-4 py-2 text-neutral-900 shadow-sm placeholder:text-neutral-400 focus:border-primary-500 focus:outline-none focus:ring-2 focus:ring-primary-200 ${className}`}
        {...props}
      />
    </div>
  );
}
