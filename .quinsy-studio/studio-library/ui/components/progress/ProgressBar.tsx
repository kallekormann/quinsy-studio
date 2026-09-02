export type ProgressBarProps = {
  value: number;
  label?: string;
  hint?: string;
  className?: string;
};

/** Bloom accent fill — MOOD-0413 mock `20-stylescape-toasts-export.html`. */
export function ProgressBar({ value, label, hint, className = '' }: ProgressBarProps) {
  const clamped = Math.min(100, Math.max(0, value));

  return (
    <div className={className}>
      {label ? (
        <div className="mb-1.5 flex items-center justify-between gap-2 text-[11px] text-neutral-500 dark:text-neutral-400">
          <span>{label}</span>
          <span className="tabular-nums">{Math.round(clamped)}%</span>
        </div>
      ) : null}
      <div
        className="h-1.5 overflow-hidden rounded-full border border-neutral-200 bg-neutral-100 dark:border-neutral-700 dark:bg-neutral-800"
        role="progressbar"
        aria-valuemin={0}
        aria-valuemax={100}
        aria-valuenow={clamped}
      >
        <div
          className="h-full rounded-full bg-accent-500 transition-[width] duration-300 ease-out dark:bg-accent-400"
          style={{ width: `${clamped}%` }}
        />
      </div>
      {hint ? (
        <p className="mt-2 text-[11px] text-neutral-500 dark:text-neutral-400">{hint}</p>
      ) : null}
    </div>
  );
}
