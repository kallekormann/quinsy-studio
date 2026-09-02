/**
 * Moody Bloom — styled radio group (Headless UI + tokens).
 */
'use client';

import type { ReactNode } from 'react';
import { Radio, RadioGroup } from '../../primitives/headless/radio-group';

export type RadioOption = { value: string; label: ReactNode; disabled?: boolean };

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
        <legend className="mb-2 text-sm font-medium text-ink dark:text-ink">{label}</legend>
      ) : null}
      <RadioGroup value={value} onChange={onChange} name={name} className="space-y-2">
        {options.map((option) => (
          <Radio
            key={option.value}
            value={option.value}
            disabled={option.disabled}
            className="group flex cursor-pointer items-center gap-2 text-sm text-body data-[disabled]:cursor-not-allowed data-[disabled]:opacity-45 data-[focus]:outline-none"
          >
            <span
              aria-hidden
              className="size-4 shrink-0 rounded-full border-[1.5px] border-[color:var(--line-strong)] bg-surface group-focus-visible:border-accent-500 group-data-[checked]:border-accent-500 group-data-[checked]:bg-accent-500 group-data-[checked]:shadow-[inset_0_0_0_3px_var(--surface)]"
            />
            <span>{option.label}</span>
          </Radio>
        ))}
      </RadioGroup>
    </fieldset>
  );
}
