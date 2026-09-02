/**
 * Moody Bloom — dropdown menu molecule (Headless UI Menu + tokens).
 * Panel uses shared popover styles (high z-index + opaque surface).
 */
'use client';

import type { ReactNode } from 'react';
import { Menu, MenuButton, MenuItem, MenuItems } from '../../primitives/headless/menu';
import { popoverPanelClass } from '@ui/styles/popover-styles';

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

export function DropdownMenu({
  trigger,
  items,
  align = 'left',
  className = '',
}: DropdownMenuProps) {
  return (
    <Menu as="div" className={`relative inline-block text-left ${className}`}>
      <MenuButton className="inline-flex items-center rounded-md focus-visible:border-accent-500 focus-visible:outline-none">
        {trigger}
      </MenuButton>
      <MenuItems
        portal
        anchor={align === 'right' ? 'bottom end' : 'bottom start'}
        className={`${popoverPanelClass} mt-1 min-w-[10rem]`}
      >
        {items.map((item) => (
          <MenuItem key={item.id} disabled={item.disabled}>
            {({ focus }) => (
              <button
                type="button"
                className={`block w-full px-4 py-2 text-left text-sm ${
                  item.destructive ? 'text-danger' : 'text-ink'
                } ${focus ? 'bg-[color:var(--accent-wash)] text-[color:var(--accent-strong)]' : ''} ${item.disabled ? 'opacity-40' : ''}`}
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
