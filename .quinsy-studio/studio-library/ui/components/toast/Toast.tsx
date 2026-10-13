import type { ReactNode } from 'react';

export type ToastTone = 'ok' | 'info' | 'err';

export type ToastProps = {
  tone?: ToastTone;
  children: ReactNode;
  actions?: ReactNode;
  className?: string;
};

const TONE_CLASS: Record<ToastTone, string> = {
  ok: 'border-[color-mix(in_srgb,var(--ok)_35%,var(--line))] text-ink',
  info: 'border-[color:var(--line)] text-ink',
  err: 'border-[color-mix(in_srgb,var(--danger)_35%,var(--line))] text-ink',
};

const ICON_TONE_CLASS: Record<ToastTone, string> = {
  ok: 'text-[color:var(--ok)]',
  info: 'text-accent-600 dark:text-accent-400',
  err: 'text-[color:var(--danger)]',
};

function ToastIcon({ tone }: { tone: ToastTone }) {
  if (tone === 'ok') {
    return (
      <svg
        className={`size-[18px] shrink-0 ${ICON_TONE_CLASS[tone]}`}
        viewBox="0 0 24 24"
        fill="none"
        stroke="currentColor"
        strokeWidth="2"
        aria-hidden
      >
        <path d="M5 13l4 4L19 7" />
      </svg>
    );
  }
  if (tone === 'err') {
    return (
      <svg
        className={`size-[18px] shrink-0 ${ICON_TONE_CLASS[tone]}`}
        viewBox="0 0 24 24"
        fill="none"
        stroke="currentColor"
        strokeWidth="2"
        aria-hidden
      >
        <circle cx="12" cy="12" r="9" />
        <path d="M12 8v5M12 16h.01" />
      </svg>
    );
  }
  return (
    <svg
      className={`size-[18px] shrink-0 ${ICON_TONE_CLASS[tone]}`}
      viewBox="0 0 24 24"
      fill="none"
      stroke="currentColor"
      strokeWidth="2"
      aria-hidden
    >
      <circle cx="12" cy="12" r="9" />
      <path d="M12 8h.01M11 12h1v4h1" />
    </svg>
  );
}

/**
 * Toast surface — Bloom mock 20.
 * One toast at a time; place inside ToastViewport (viewport bottom).
 */
export function Toast({ tone = 'info', children, actions, className = '' }: ToastProps) {
  return (
    <div
      role={tone === 'err' ? 'alert' : 'status'}
      className={`inline-flex max-w-[min(420px,92vw)] items-center gap-2.5 rounded-[var(--radius-lg)] border bg-surface px-3.5 py-2.5 text-xs text-body shadow-[var(--elevate-hover,0_8px_24px_rgba(18,32,43,0.12))] ${TONE_CLASS[tone]} ${className}`}
    >
      <ToastIcon tone={tone} />
      <span className="min-w-0 flex-1">{children}</span>
      {actions ? <span className="ml-auto inline-flex shrink-0 gap-1.5">{actions}</span> : null}
    </div>
  );
}

/**
 * Fixed viewport host — bottom-center, generous bottom inset.
 * pointer-events none on the host; toast surface re-enables interaction.
 */
export function ToastViewport({
  children,
  className = '',
}: {
  children: ReactNode;
  className?: string;
}) {
  return (
    <div
      className={`pointer-events-none fixed inset-x-0 bottom-0 z-50 flex justify-center px-4 pb-8 pt-3 sm:pb-10 ${className}`}
      aria-live="polite"
    >
      <div className="pointer-events-auto">{children}</div>
    </div>
  );
}
