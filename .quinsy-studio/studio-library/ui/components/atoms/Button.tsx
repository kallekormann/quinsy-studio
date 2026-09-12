import type { ComponentProps, ReactNode } from 'react';
import { Button as KitButton } from '../button/button';

/** Legacy variant names used by older library molecules. Prefer kit `variant="default"`. */
export type ButtonVariant =
  | 'primary'
  | 'secondary'
  | 'outline'
  | 'soft'
  | 'ghost'
  | 'link'
  | 'danger';
export type ButtonSize = 'sm' | 'md' | 'lg';

export interface ButtonProps extends Omit<ComponentProps<'button'>, 'size'> {
  variant?: ButtonVariant;
  buttonSize?: ButtonSize;
  iconOnly?: boolean;
  children: ReactNode;
}

const variantMap = {
  primary: 'default',
  secondary: 'secondary',
  outline: 'outline',
  soft: 'secondary',
  ghost: 'ghost',
  link: 'link',
  danger: 'destructive',
} as const;

const sizeMap = { sm: 'sm', md: 'default', lg: 'lg' } as const;

/**
 * Compatibility wrapper around the themable shadcn Button.
 * New UI should import from `ui/components/button`.
 */
export function Button({
  variant = 'primary',
  buttonSize = 'md',
  iconOnly = false,
  className = '',
  children,
  type = 'button',
  ...props
}: ButtonProps) {
  return (
    <KitButton
      type={type}
      variant={variantMap[variant]}
      size={iconOnly ? 'icon' : sizeMap[buttonSize]}
      className={className}
      {...props}
    >
      {children}
    </KitButton>
  );
}
