import type { ReactNode } from 'react';
import { Badge as KitBadge } from '../badge/badge';

export type BadgeVariant = 'default' | 'pro' | 'view' | 'accent';

const variantMap = {
  default: 'secondary',
  pro: 'default',
  view: 'outline',
  accent: 'default',
} as const;

export function Badge({
  children,
  variant = 'default',
  className = '',
}: {
  children: ReactNode;
  variant?: BadgeVariant;
  className?: string;
}) {
  return (
    <KitBadge variant={variantMap[variant]} className={className}>
      {children}
    </KitBadge>
  );
}
