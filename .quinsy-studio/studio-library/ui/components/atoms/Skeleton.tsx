import type { ComponentProps } from 'react';

export type SkeletonVariant = 'line' | 'line-sm' | 'block' | 'circle' | 'card';

export interface SkeletonProps extends ComponentProps<'div'> {
  variant?: SkeletonVariant;
}

const variantClass: Record<SkeletonVariant, string> = {
  line: 'h-3 w-full',
  'line-sm': 'h-2.5 w-3/4',
  block: 'h-10 w-full rounded-lg',
  circle: 'h-8 w-8 shrink-0 rounded-full',
  card: 'h-16 w-full rounded-lg',
};

export function Skeleton({
  variant = 'line',
  className = '',
  'aria-hidden': ariaHidden = true,
  ...props
}: SkeletonProps) {
  return (
    <div
      aria-hidden={ariaHidden}
      className={`rounded-md bg-neutral-200/80 motion-reduce:animate-none dark:bg-neutral-700/60 motion-safe:animate-pulse ${variantClass[variant]} ${className}`}
      {...props}
    />
  );
}
