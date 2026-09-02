/**
 * Moody Bloom — styled toggle switch (Headless UI + tokens).
 */
'use client';

import type { ComponentProps, ReactNode } from 'react';
import { Switch as HeadlessSwitch } from '@ui/primitives/headless/switch';

export interface SwitchProps extends Omit<ComponentProps<typeof HeadlessSwitch>, 'children'> {
  label?: ReactNode;
}

const trackClass =
  'group relative inline-flex h-6 w-10 shrink-0 rounded-full border border-[color:var(--line)] bg-surface-2 transition-[background-color,border-color] focus-visible:border-accent-500 focus-visible:outline-none data-[checked]:border-transparent data-[checked]:bg-accent-500 data-[disabled]:opacity-45';

const thumbClass =
  'pointer-events-none absolute left-0.5 top-0.5 size-[18px] rounded-full bg-surface shadow-sm transition-transform group-data-[checked]:translate-x-4';

export function Switch({ label, className = '', disabled, ...props }: SwitchProps) {
  return (
    <label
      className={`inline-flex cursor-pointer items-center gap-2.5 text-sm text-body ${disabled ? 'cursor-not-allowed opacity-45' : ''}`}
    >
      <HeadlessSwitch className={`${trackClass} ${className}`} disabled={disabled} {...props}>
        <span aria-hidden className={thumbClass} />
      </HeadlessSwitch>
      {label ? <span>{label}</span> : null}
    </label>
  );
}
