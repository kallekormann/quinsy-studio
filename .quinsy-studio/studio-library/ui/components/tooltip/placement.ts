/** Preferred side of the trigger; flips when that side has no room. */
export type TooltipPlacement = 'top' | 'right' | 'bottom' | 'left';

export type TooltipCoords = {
  top: number;
  left: number;
  placement: TooltipPlacement;
};

/** Gap from trigger + minimum inset from viewport edges (px). */
const EDGE_PAD = 8;

const FLIP_ORDER: Record<TooltipPlacement, TooltipPlacement[]> = {
  top: ['top', 'bottom', 'right', 'left'],
  bottom: ['bottom', 'top', 'right', 'left'],
  left: ['left', 'right', 'top', 'bottom'],
  right: ['right', 'left', 'top', 'bottom'],
};

function rawPosition(
  placement: TooltipPlacement,
  trigger: DOMRect,
  tip: { width: number; height: number },
  gap: number,
): { top: number; left: number } {
  switch (placement) {
    case 'top':
      return {
        top: trigger.top - tip.height - gap,
        left: trigger.left + trigger.width / 2 - tip.width / 2,
      };
    case 'bottom':
      return {
        top: trigger.bottom + gap,
        left: trigger.left + trigger.width / 2 - tip.width / 2,
      };
    case 'left':
      return {
        top: trigger.top + trigger.height / 2 - tip.height / 2,
        left: trigger.left - tip.width - gap,
      };
    case 'right':
      return {
        top: trigger.top + trigger.height / 2 - tip.height / 2,
        left: trigger.right + gap,
      };
  }
}

function fits(
  top: number,
  left: number,
  tip: { width: number; height: number },
  vw: number,
  vh: number,
): boolean {
  return (
    top >= EDGE_PAD &&
    left >= EDGE_PAD &&
    top + tip.height <= vh - EDGE_PAD &&
    left + tip.width <= vw - EDGE_PAD
  );
}

function shiftIntoView(
  top: number,
  left: number,
  tip: { width: number; height: number },
  vw: number,
  vh: number,
): { top: number; left: number } {
  return {
    top: Math.min(Math.max(top, EDGE_PAD), Math.max(EDGE_PAD, vh - tip.height - EDGE_PAD)),
    left: Math.min(Math.max(left, EDGE_PAD), Math.max(EDGE_PAD, vw - tip.width - EDGE_PAD)),
  };
}

/**
 * Place a floating tip relative to a trigger rect.
 * Tries preferred side, then flips; finally shifts into the viewport.
 */
export function computeTooltipPosition(
  trigger: DOMRect,
  tip: { width: number; height: number },
  preferred: TooltipPlacement,
  gap: number = EDGE_PAD,
): TooltipCoords {
  const vw = window.innerWidth;
  const vh = window.innerHeight;

  for (const placement of FLIP_ORDER[preferred]) {
    const raw = rawPosition(placement, trigger, tip, gap);
    if (fits(raw.top, raw.left, tip, vw, vh)) {
      return { ...raw, placement };
    }
  }

  const fallback = rawPosition(preferred, trigger, tip, gap);
  const shifted = shiftIntoView(fallback.top, fallback.left, tip, vw, vh);
  return { ...shifted, placement: preferred };
}
