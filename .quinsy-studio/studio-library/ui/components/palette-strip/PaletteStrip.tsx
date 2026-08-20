/**
 * Studio Library — horizontal palette swatch strip (token-based borders/surface).
 * Pair with packages/color-extraction for image-derived palettes.
 */
import type { CSSProperties, ReactNode } from 'react';

export type PaletteStripProps = {
  /** HEX colors, e.g. from extractPaletteFromFile */
  colors: string[];
  /** Accessible label for the strip */
  label?: string;
  /** Show hex under each swatch */
  showLabels?: boolean;
  /** Called when user clicks a swatch */
  onSwatchClick?: (hex: string, index: number) => void;
  className?: string;
  /** Optional slot after swatches (copy button, etc.) */
  trailing?: ReactNode;
};

export function PaletteStrip({
  colors,
  label = 'Color palette',
  showLabels = false,
  onSwatchClick,
  className = '',
  trailing,
}: PaletteStripProps) {
  if (colors.length === 0) return null;

  return (
    <div
      className={`flex flex-wrap items-end gap-2 ${className}`}
      role="group"
      aria-label={label}
    >
      {colors.map((hex, index) => {
        const clickable = Boolean(onSwatchClick);
        const swatchStyle: CSSProperties = { backgroundColor: hex };
        const inner = (
          <>
            <span
              className="block h-8 w-8 rounded-md border border-neutral-200 shadow-sm ring-1 ring-black/5"
              style={swatchStyle}
              title={hex}
            />
            {showLabels ? (
              <span className="mt-1 block text-center font-mono text-[10px] text-neutral-500">
                {hex}
              </span>
            ) : null}
          </>
        );

        if (clickable) {
          return (
            <button
              key={`${hex}-${index}`}
              type="button"
              className="rounded-lg p-0.5 transition hover:bg-neutral-100 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-primary-500"
              onClick={() => onSwatchClick?.(hex, index)}
              aria-label={`Color ${hex}`}
            >
              {inner}
            </button>
          );
        }

        return (
          <div key={`${hex}-${index}`} className="flex flex-col items-center">
            {inner}
          </div>
        );
      })}
      {trailing}
    </div>
  );
}
