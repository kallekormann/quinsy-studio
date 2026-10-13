/**
 * Docked Studio rail + panel.
 * Solid `--color-chrome`; 52px rail · 300px panel.
 */

export const STUDIO_RAIL_WIDTH_PX = 52;
export const STUDIO_PANEL_WIDTH_PX = 300;

export const studioRailClass =
  'flex w-[52px] shrink-0 flex-col items-center gap-1 border-l border-[color:var(--line)] bg-chrome py-2';

export const studioRailButtonBaseClass =
  'relative flex h-10 w-10 items-center justify-center rounded-[12px] border-0 bg-transparent p-0 text-muted transition-colors duration-[var(--dur-fast)] ease-[var(--ease-out)] hover:bg-surface-2 hover:text-ink';

export const studioRailButtonActiveClass =
  'bg-[color:var(--accent-wash)] text-accent-600 before:absolute before:right-[-1px] before:top-2 before:bottom-2 before:w-0.5 before:rounded-l before:bg-accent-600 dark:text-accent-500 before:dark:bg-accent-500';

export const studioPanelClass =
  'flex w-[300px] shrink-0 flex-col min-h-0 border-l border-[color:var(--line)] bg-chrome';

export const studioPanelHeaderClass =
  'flex shrink-0 items-start justify-between gap-2 border-b border-[color:var(--line)] px-3.5 py-3';

export const studioPanelTitleClass =
  'm-0 text-[11px] font-semibold uppercase tracking-[0.05em] text-muted';

export const studioPanelBodyClass =
  'min-h-0 flex-1 overflow-y-auto overscroll-contain px-3.5 pb-3.5';
