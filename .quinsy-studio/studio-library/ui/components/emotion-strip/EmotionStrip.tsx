import type { CSSProperties } from 'react';

/** Moody Bloom brand ribbon — palette order as feeling (MOOD-0413 / MOOD-0416). */
export type EmotionStripSize = 'sm' | 'md' | 'lg' | 'block';

export type EmotionStripProps = {
  /** 3–5 CSS colors (hex, rgb, or var()) from board kit or palette extraction */
  colors: string[];
  size?: EmotionStripSize;
  /** Unequal segment widths for expressive palettes */
  weighted?: boolean;
  className?: string;
  'aria-label'?: string;
};

const SIZE_CLASS: Record<EmotionStripSize, string> = {
  sm: 'h-1.5 max-w-[120px]',
  md: 'h-2.5 max-w-[180px]',
  lg: 'h-3.5 max-w-[280px]',
  block: 'h-3.5 w-full max-w-none',
};

/** Weighted flex ratios from MOOD-0413 studio.css */
const WEIGHTED_FLEX = [2.2, 1.4, 1, 0.8, 0.6] as const;

function segmentFlex(index: number, weighted: boolean): CSSProperties {
  if (!weighted) return { flex: 1 };
  return { flex: WEIGHTED_FLEX[index] ?? 1 };
}

export function EmotionStrip({
  colors,
  size = 'md',
  weighted = false,
  className = '',
  'aria-label': ariaLabel = 'Color mood',
}: EmotionStripProps) {
  if (colors.length < 1) return null;

  return (
    <div
      role="img"
      aria-label={ariaLabel}
      className={`flex overflow-hidden rounded-full border border-[var(--line)] ${SIZE_CLASS[size]} ${className}`}
    >
      {colors.map((color, index) => (
        <span
          key={`${color}-${index}`}
          className="block min-w-0"
          style={{ ...segmentFlex(index, weighted), backgroundColor: color }}
        />
      ))}
    </div>
  );
}

/** Demo palette — Bloom warm stops for sticker sheet / docs */
export const EMOTION_STRIP_DEMO_COLORS = [
  'var(--color-accent-500)',
  'var(--color-accent-300)',
  'var(--color-neutral-200)',
  'var(--color-neutral-800)',
  'var(--color-success)',
] as const;
