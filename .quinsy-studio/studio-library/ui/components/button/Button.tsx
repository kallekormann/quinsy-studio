/**
 * Studio Library — generic button (token-based primary/neutral).
 * Projects remap --color-primary-* in local ui/tokens/design-tokens.css.
 */
import type { ComponentProps, ReactNode } from 'react';

export type ButtonVariant = 'primary' | 'secondary' | 'outline' | 'ghost' | 'destructive';
export type ButtonSize = 'sm' | 'md' | 'lg';

export interface ButtonProps extends Omit<ComponentProps<'button'>, 'size'> {
  variant?: ButtonVariant;
  size?: ButtonSize;
  loading?: boolean;
  children: ReactNode;
}

const variantClass: Record<ButtonVariant, string> = {
  primary:
    'bg-primary-600 text-white hover:bg-primary-700 focus-visible:ring-2 focus-visible:ring-primary-500 focus-visible:ring-offset-2',
  secondary: 'bg-neutral-100 text-neutral-900 hover:bg-neutral-200',
  outline: 'border border-neutral-300 bg-surface text-neutral-900 hover:bg-neutral-50',
  ghost: 'text-neutral-700 hover:bg-neutral-100',
  destructive:
    'bg-error-500 text-white hover:bg-error-700 focus-visible:ring-2 focus-visible:ring-error-500',
};

const sizeClass: Record<ButtonSize, string> = {
  sm: 'px-3 py-1.5 text-sm',
  md: 'px-4 py-2 text-sm',
  lg: 'px-5 py-2.5 text-base',
};

export function Button({
  variant = 'primary',
  size = 'md',
  loading = false,
  className = '',
  children,
  type = 'button',
  disabled,
  ...props
}: ButtonProps) {
  return (
    <button
      type={type}
      className={`inline-flex items-center justify-center rounded-lg font-medium transition-colors focus-visible:outline-none disabled:opacity-50 ${variantClass[variant]} ${sizeClass[size]} ${className}`}
      disabled={disabled || loading}
      {...props}
    >
      {loading ? '…' : children}
    </button>
  );
}
