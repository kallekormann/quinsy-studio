import type { ComponentProps, ReactNode } from 'react';

export type ButtonVariant =
  'primary' | 'secondary' | 'outline' | 'soft' | 'ghost' | 'link' | 'danger';
export type ButtonSize = 'sm' | 'md' | 'lg';

export interface ButtonProps extends Omit<ComponentProps<'button'>, 'size'> {
  variant?: ButtonVariant;
  buttonSize?: ButtonSize;
  /** Icon-only square button (Bloom 07). */
  iconOnly?: boolean;
  children: ReactNode;
}

/**
 * Base matches MOOD-0413 `.btn`:
 * height 32px · 12px type · leading-none so labels sit optically centered.
 */
const baseClass =
  'inline-flex items-center justify-center gap-1.5 font-medium leading-none transition-[background-color,border-color,color,filter,box-shadow] duration-[var(--dur-fast)] focus-visible:outline-none focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-accent-500 disabled:pointer-events-none disabled:opacity-45';

const variantClass: Record<ButtonVariant, string> = {
  primary:
    'rounded-full border border-transparent bg-[linear-gradient(180deg,#ef7d62_0%,var(--accent)_100%)] text-[color:var(--accent-ink)] shadow-[0_1px_0_rgba(255,255,255,0.25)_inset,var(--elevate-hover)] hover:brightness-[1.03] focus-visible:border-accent-500',
  secondary:
    'rounded-full border border-transparent bg-surface-2 text-ink hover:bg-[color:var(--accent-soft)]',
  /** Mock `.btn.outline` — md radius, surface fill, accent-soft hover */
  outline:
    'rounded-md border border-[color:var(--line)] bg-[color:var(--color-surface)] text-ink hover:bg-[color:var(--accent-soft)]',
  soft: 'rounded-full border border-transparent bg-[color:var(--accent-wash)] text-[color:var(--accent-strong)] hover:bg-accent-200',
  ghost:
    'rounded-md border border-transparent bg-transparent text-body hover:bg-[color:var(--accent-soft)] hover:text-[color:var(--accent-strong)]',
  link: 'h-auto rounded-none border-0 bg-transparent p-0 text-[color:var(--accent-strong)] underline underline-offset-[3px] hover:text-accent-500',
  danger: 'rounded-md border border-danger/30 bg-danger/10 text-danger hover:bg-danger/15',
};

/** sm = compact hub “+ Board” (28px); md = default mock `.btn` (32px) */
const sizeClass: Record<ButtonSize, string> = {
  sm: 'h-7 px-3 text-[12px]',
  md: 'h-8 px-3 text-[12px]',
  lg: 'h-10 px-4 text-[13px]',
};

const iconOnlySizeClass: Record<ButtonSize, string> = {
  sm: 'size-8 p-0',
  md: 'size-8 p-0',
  lg: 'size-9 p-0',
};

export function Button({
  variant = 'primary',
  buttonSize = 'md',
  iconOnly = false,
  className = '',
  children,
  type = 'button',
  ...props
}: ButtonProps) {
  const shapeClass = iconOnly ? 'rounded-md' : '';
  const size = iconOnly ? iconOnlySizeClass[buttonSize] : sizeClass[buttonSize];

  return (
    <button
      type={type}
      className={`${baseClass} ${variantClass[variant]} ${size} ${shapeClass} ${className}`}
      {...props}
    >
      {children}
    </button>
  );
}
