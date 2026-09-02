import type { ReactNode } from 'react';

export type SeparatorProps = {
  /** Labeled divider — text centered between hairlines (Bloom 07). */
  label?: ReactNode;
  className?: string;
};

export function Separator({ label, className = '' }: SeparatorProps) {
  if (label) {
    return (
      <div
        className={`my-4 flex items-center gap-3 text-[11px] font-semibold uppercase tracking-wide text-muted ${className}`}
        role="separator"
      >
        <span className="h-px flex-1 bg-[color:var(--line)]" aria-hidden />
        <span>{label}</span>
        <span className="h-px flex-1 bg-[color:var(--line)]" aria-hidden />
      </div>
    );
  }

  return (
    <hr role="separator" className={`my-4 h-px border-0 bg-[color:var(--line)] ${className}`} />
  );
}
