/**
 * Studio Library — dropdown menu molecule (Headless UI Menu + tokens).
 */
'use client';

import type { ReactNode } from 'react';
import {
  Menu,
  MenuButton,
  MenuItem,
  MenuItems,
} from '../../primitives/headless/menu';

export type DropdownMenuItem = {
  id: string;
  label: ReactNode;
  onSelect?: () => void;
  destructive?: boolean;
  disabled?: boolean;
};

export type DropdownMenuProps = {
  trigger: ReactNode;
  items: DropdownMenuItem[];
  align?: 'left' | 'right';
  className?: string;
};

export function DropdownMenu({ trigger, items, align = 'left', className = '' }: DropdownMenuProps) {
  return (
    <Menu as="div" className={`relative inline-block text-left ${className}`}>
      <MenuButton className="inline-flex items-center rounded-lg focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-primary-500">
        {trigger}
      </MenuButton>
      <MenuItems
        anchor={align === 'right' ? 'bottom end' : 'bottom start'}
        className="z-50 mt-1 min-w-[10rem] rounded-lg border border-neutral-200 bg-surface py-1 shadow-lg focus:outline-none dark:border-neutral-700 dark:bg-surface-dark"
      >
        {items.map((item) => (
          <MenuItem key={item.id} disabled={item.disabled}>
            {({ focus }) => (
              <button
                type="button"
                className={`block w-full px-4 py-2 text-left text-sm ${
                  item.destructive ? 'text-error-600' : 'text-neutral-800 dark:text-neutral-100'
                } ${focus ? 'bg-neutral-100 dark:bg-neutral-800' : ''} ${item.disabled ? 'opacity-50' : ''}`}
                onClick={item.onSelect}
              >
                {item.label}
              </button>
            )}
          </MenuItem>
        ))}
      </MenuItems>
    </Menu>
  );
}
