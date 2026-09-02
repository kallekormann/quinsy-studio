/**
 * Studio Library — Card atom (surface container).
 * Bloom soft-card family (MOOD-0413) — neutral elevate, no coral glow.
 */
import type { ComponentProps, ReactNode } from 'react';
import { softCardClass, softCardInteractiveClass } from '@ui/components/soft-card';

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
  const surface = interactive ? softCardInteractiveClass : softCardClass;

  return (
    <div className={`${surface} ${paddingClass[padding]} ${className}`} {...props}>
      {children}
    </div>
  );
}
