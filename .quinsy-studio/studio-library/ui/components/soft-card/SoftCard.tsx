import type { ComponentProps, ReactNode } from 'react';
import {
  softCardClass,
  softCardInteractiveClass,
  softCardSelectedClass,
} from './soft-card-styles';

export type SoftCardPadding = 'none' | 'sm' | 'md';

export type SoftCardProps = ComponentProps<'div'> & {
  children: ReactNode;
  padding?: SoftCardPadding;
  interactive?: boolean;
  selected?: boolean;
};

const paddingClass: Record<SoftCardPadding, string> = {
  none: '',
  sm: 'p-3',
  md: 'p-3.5',
};

export function SoftCard({
  children,
  padding = 'md',
  interactive = false,
  selected = false,
  className = '',
  ...props
}: SoftCardProps) {
  const surface = interactive ? softCardInteractiveClass : softCardClass;
  const state = selected ? softCardSelectedClass : '';

  return (
    <div
      className={`${surface} ${state} ${paddingClass[padding]} ${className}`}
      {...props}
    >
      {children}
    </div>
  );
}
