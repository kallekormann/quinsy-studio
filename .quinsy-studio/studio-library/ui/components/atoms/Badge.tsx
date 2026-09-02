import type { ReactNode } from 'react';

export type BadgeVariant = 'default' | 'pro' | 'view' | 'accent';

const styles: Record<BadgeVariant, string> = {
  default: 'bg-neutral-100 text-neutral-600 dark:bg-neutral-800 dark:text-neutral-300',
  pro: 'bg-accent-100 text-accent-600 dark:bg-accent-500/20 dark:text-accent-400',
  view: 'bg-coral-500/10 text-coral-500',
  accent: 'bg-accent-500 text-white',
};

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
    <span
      className={`inline-flex items-center rounded-full px-2.5 py-0.5 text-xs font-semibold ${styles[variant]} ${className}`}
    >
      {children}
    </span>
  );
}
