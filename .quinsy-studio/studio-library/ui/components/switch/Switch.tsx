/**
 * Studio Library — styled toggle switch (Headless UI + tokens).
 */
'use client';

import type { ComponentProps, ReactNode } from 'react';
import { Switch as HeadlessSwitch } from '../../primitives/headless/switch';

export interface SwitchProps extends Omit<ComponentProps<typeof HeadlessSwitch>, 'children'> {
  label?: ReactNode;
}

export function Switch({ label, className = '', ...props }: SwitchProps) {
  return (
    <label className="inline-flex cursor-pointer items-center gap-3 text-sm text-neutral-800 dark:text-neutral-100">
      <HeadlessSwitch
        className={`group relative inline-flex h-6 w-11 shrink-0 rounded-full bg-neutral-300 transition data-[checked]:bg-primary-600 data-[focus]:outline data-[focus]:outline-2 data-[focus]:outline-offset-2 data-[focus]:outline-primary-500 dark:bg-neutral-600 ${className}`}
        {...props}
      >
        <span className="pointer-events-none inline-block size-5 translate-x-0.5 rounded-full bg-white shadow transition group-data-[checked]:translate-x-5" />
      </HeadlessSwitch>
      {label ? <span>{label}</span> : null}
    </label>
  );
}
