import type { ReactNode } from 'react';
import { PaletteStrip } from '@ui/components/molecules/PaletteStrip';

const GRADIENTS = [
  'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
  'linear-gradient(135deg, #f093fb 0%, #f5576c 100%)',
  'linear-gradient(135deg, #4facfe 0%, #00f2fe 100%)',
  'linear-gradient(160deg, #ffecd2 0%, #fcb69f 100%)',
];

export function MockImageCard({
  index,
  className = '',
  selected = false,
}: {
  index: number;
  className?: string;
  selected?: boolean;
}) {
  return (
    <div
      className={`group relative w-48 overflow-hidden rounded-[16px] bg-white shadow-card transition-shadow dark:bg-surface-dark ${
        selected ? 'ring-2 ring-accent-500 ring-offset-2 ring-offset-transparent' : ''
      } ${className}`}
    >
      <div className="aspect-[4/5]" style={{ background: GRADIENTS[index % GRADIENTS.length] }} />
      <div className="border-t border-neutral-100 p-2 dark:border-neutral-700">
        <PaletteStrip />
      </div>
    </div>
  );
}

export function MockStickyNote({ className = '' }: { className?: string }) {
  return (
    <div
      className={`w-40 rounded-[12px] border border-amber-200/80 bg-amber-50 p-3 shadow-md dark:border-amber-900/50 dark:bg-amber-950/40 ${className}`}
    >
      <p className="text-sm font-medium text-amber-900 dark:text-amber-100">Mood direction</p>
      <p className="mt-1 text-xs text-amber-800/80 dark:text-amber-200/80">
        Soft brutalism · warm neutrals
      </p>
    </div>
  );
}

export function MockFrame({ children, label }: { children: ReactNode; label: string }) {
  return (
    <div className="rounded-[20px] border-2 border-dashed border-accent-400/50 bg-accent-500/5 p-4">
      <span className="mb-2 block text-xs font-semibold uppercase tracking-wide text-accent-600 dark:text-accent-400">
        {label}
      </span>
      <div className="flex flex-wrap gap-4">{children}</div>
    </div>
  );
}
