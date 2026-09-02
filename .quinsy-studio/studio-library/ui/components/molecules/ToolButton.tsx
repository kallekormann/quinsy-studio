import type { ReactNode } from 'react';
import { Button } from '@ui/components/atoms/Button';
import { Tooltip } from '@ui/components/tooltip';
import {
  bloomToolButtonActiveClass,
  bloomToolButtonBaseClass,
  bloomToolButtonIdleClass,
} from '@ui/styles/chrome-styles';

export function ToolButton({
  children,
  active = false,
  label,
  placement = 'right',
  onClick,
}: {
  children: ReactNode;
  active?: boolean;
  label: string;
  placement?: 'top' | 'right' | 'bottom' | 'left';
  onClick?: () => void;
}) {
  return (
    <Tooltip label={label} placement={placement}>
      <Button
        type="button"
        variant="ghost"
        buttonSize="lg"
        iconOnly
        aria-label={label}
        aria-pressed={active}
        onClick={onClick}
        className={`${bloomToolButtonBaseClass} ${
          active ? bloomToolButtonActiveClass : bloomToolButtonIdleClass
        }`}
      >
        {children}
      </Button>
    </Tooltip>
  );
}
