/**
 * Studio Library — Card atom (surface container).
 */
import type { ComponentProps, ReactNode } from 'react';

export type CardPadding = 'none' | 'sm' | 'md' | 'lg';

export interface CardProps extends ComponentProps<'div'> {
  children: ReactNode;
  padding?: CardPadding;
  interactive?: boolean;
}

const paddingClass: Record<CardPadding, string> = {
  none: '',
  sm: 'p-3',
  md: 'p-4',
  lg: 'p-6',
};

export function Card({
  children,
  padding = 'md',
  interactive = false,
  className = '',
  ...props
}: CardProps) {
  return (
    <div
      className={`rounded-xl border border-neutral-200 bg-surface shadow-sm dark:border-neutral-700 dark:bg-surface-dark ${
        interactive ? 'transition-shadow hover:shadow-md' : ''
      } ${paddingClass[padding]} ${className}`}
      {...props}
    >
      {children}
    </div>
  );
}
