/**
 * Studio Library — styled radio group (Headless UI + tokens).
 */
'use client';

import type { ReactNode } from 'react';
import { Radio, RadioGroup } from '../../primitives/headless/radio-group';

export type RadioOption = { value: string; label: ReactNode };

export type RadioGroupProps = {
  name: string;
  label?: ReactNode;
  value: string;
  onChange: (value: string) => void;
  options: RadioOption[];
  className?: string;
};

export function StyledRadioGroup({
  name,
  label,
  value,
  onChange,
  options,
  className = '',
}: RadioGroupProps) {
  return (
    <fieldset className={className}>
      {label ? (
        <legend className="mb-2 text-sm font-medium text-neutral-700 dark:text-neutral-200">{label}</legend>
      ) : null}
      <RadioGroup value={value} onChange={onChange} name={name} className="space-y-2">
        {options.map((option) => (
          <Radio
            key={option.value}
            value={option.value}
            className="group flex cursor-pointer items-center gap-2 text-sm text-neutral-800 data-[focus]:outline data-[focus]:outline-2 data-[focus]:outline-offset-2 data-[focus]:outline-primary-500 dark:text-neutral-100"
          >
            <span className="flex size-4 items-center justify-center rounded-full border border-neutral-400 group-data-[checked]:border-primary-600 dark:border-neutral-500">
              <span className="size-2 rounded-full bg-primary-600 opacity-0 group-data-[checked]:opacity-100" />
            </span>
            <span>{option.label}</span>
          </Radio>
        ))}
      </RadioGroup>
    </fieldset>
  );
}
