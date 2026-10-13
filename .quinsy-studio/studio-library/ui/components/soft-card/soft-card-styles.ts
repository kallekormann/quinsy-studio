/**
 * Bloom soft card elevation — neutral border + shadow only (no coral glow, no translate/scale).
 * Soft surface for board and control cards.
 */

/** Static surface card (settings panels, motif demos) */
export const softCardClass =
  'rounded-[var(--radius-xl)] border border-[color:var(--line)] bg-surface dark:bg-surface-dark';

/** Hub / library cards: elevate via shadow + border — no transform motion */
export const softCardInteractiveClass =
  'rounded-[var(--radius-xl)] border border-[color:var(--line)] bg-surface shadow-sm transition-[box-shadow,border-color] hover:border-[color:var(--line-strong)] hover:shadow-md dark:bg-surface-dark';

/** Selected hub card — accent wash, still no glow shadow */
export const softCardSelectedClass =
  'border-[color:color-mix(in_srgb,var(--color-accent-500)_50%,var(--line))] bg-[color:var(--color-accent-100)] shadow-none dark:bg-accent-500/10';
