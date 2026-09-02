/**
 * Moody Bloom — segmented A|B (or A|B|C) toggle.
 * Pixel-aligned to MOOD-0413 mock `.seg` (07-components.html).
 */
'use client';

import type { ReactNode } from 'react';
import { Radio, RadioGroup } from '@ui/primitives/headless/radio-group';

export type SegmentedToggleOption = {
  value: string;
  label: ReactNode;
  disabled?: boolean;
};

export type SegmentedToggleProps = {
  name: string;
  value: string;
  onChange: (value: string) => void;
  options: SegmentedToggleOption[];
  label?: ReactNode;
  className?: string;
  size?: 'sm' | 'md';
};

export function SegmentedToggle({
  name,
  value,
  onChange,
  options,
  label,
  className = '',
  size = 'sm',
}: SegmentedToggleProps) {
  const pad = size === 'sm' ? 'h-[26px] px-3 text-[12px]' : 'h-8 px-3.5 text-[13px]';

  return (
    <fieldset className={`m-0 border-0 p-0 ${label ? 'block min-w-0' : 'contents'} ${className}`}>
      {label ? (
        <legend className="mb-2 text-[11px] font-medium uppercase tracking-wide text-muted">
          {label}
        </legend>
      ) : null}
      <RadioGroup
        value={value}
        onChange={onChange}
        name={name}
        className="inline-flex shrink-0 items-center gap-0 rounded-full border border-[color:var(--line)] bg-surface-2 p-[3px]"
      >
        {options.map((option) => (
          <Radio
            key={option.value}
            value={option.value}
            disabled={option.disabled}
            className={`inline-flex cursor-pointer items-center justify-center rounded-full border-0 bg-transparent font-medium leading-none text-muted transition-[background-color,color,box-shadow] duration-[var(--dur-fast)] data-[checked]:bg-[color:var(--color-surface)] data-[checked]:text-ink data-[checked]:shadow-seg data-[disabled]:cursor-not-allowed data-[disabled]:opacity-40 focus:outline-none data-[focus]:outline data-[focus]:outline-2 data-[focus]:outline-offset-2 data-[focus]:outline-accent-500 ${pad}`}
          >
            {option.label}
          </Radio>
        ))}
      </RadioGroup>
    </fieldset>
  );
}
