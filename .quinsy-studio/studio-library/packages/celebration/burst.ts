/** Shared spark burst — extension overlay + web Analyze (MOOD-0332 / MOOD-0337). */

export const CELEBRATION_SPARK_COLORS = [
  '#8b5cf6',
  '#3DDC97',
  '#FFD166',
  '#FFFFFF',
  '#A78BFA',
  '#F472B6',
] as const;

export type BurstSparksOptions = {
  /** Parent for spark nodes (document body, or a shadow root). */
  host: ParentNode & { appendChild: (node: Node) => Node };
  cx: number;
  cy: number;
  count?: number;
  /** Inject keyframes once into this document (web path). Shadow hosts pass CSS separately. */
  injectStyles?: boolean;
  className?: string;
  sizePx?: number;
  durationMs?: number;
  distMin?: number;
  distSpan?: number;
  liftPx?: number;
};

const STYLE_ATTR = 'data-moody-celebration-style';

function ensureDocumentStyles(doc: Document, durationMs: number): void {
  let style = doc.querySelector(`style[${STYLE_ATTR}]`) as HTMLStyleElement | null;
  if (!style) {
    style = doc.createElement('style');
    style.setAttribute(STYLE_ATTR, 'true');
    doc.head.appendChild(style);
  }
  style.textContent = `
    @keyframes moody-spark {
      0% { opacity: 1; transform: translate(0, 0) scale(1); }
      100% { opacity: 0; transform: translate(var(--dx), var(--dy)) scale(0.2); }
    }
    @keyframes moody-celebrate-ring {
      0% { opacity: 0.55; transform: translate(-50%, -50%) scale(0.4); }
      100% { opacity: 0; transform: translate(-50%, -50%) scale(1.6); }
    }
    .moody-spark {
      position: fixed;
      width: 5px;
      height: 5px;
      border-radius: 50%;
      pointer-events: none;
      z-index: 99999;
      opacity: 0;
      will-change: transform, opacity;
      box-shadow: 0 0 6px rgba(139, 92, 246, 0.45);
    }
    .moody-spark.go {
      animation: moody-spark ${durationMs}ms cubic-bezier(0.2, 0.7, 0.2, 1) forwards;
    }
    .moody-celebrate-ring {
      position: fixed;
      width: 96px;
      height: 96px;
      margin: 0;
      border-radius: 9999px;
      border: 2px solid rgba(139, 92, 246, 0.7);
      pointer-events: none;
      z-index: 99998;
      left: 0;
      top: 0;
      animation: moody-celebrate-ring 1100ms cubic-bezier(0.22, 1, 0.36, 1) forwards;
    }
  `;
}

/** Radial spark burst at (cx, cy). Matches extension capture celebration feel. */
export function burstSparks(options: BurstSparksOptions): void {
  const {
    host,
    cx,
    cy,
    count = 8,
    injectStyles = false,
    className = 'moody-spark',
    sizePx = 5,
    durationMs = 640,
    distMin = 18,
    distSpan = 22,
    liftPx = 8,
  } = options;

  if (injectStyles && typeof document !== 'undefined') {
    ensureDocumentStyles(document, durationMs);
  }

  for (let i = 0; i < count; i++) {
    const spark = document.createElement('div');
    spark.className = className;
    spark.setAttribute('aria-hidden', 'true');
    const angle = (Math.PI * 2 * i) / count + (Math.random() * 0.35 - 0.17);
    const dist = distMin + Math.random() * distSpan;
    spark.style.left = `${cx}px`;
    spark.style.top = `${cy}px`;
    spark.style.width = `${sizePx}px`;
    spark.style.height = `${sizePx}px`;
    spark.style.background = CELEBRATION_SPARK_COLORS[i % CELEBRATION_SPARK_COLORS.length]!;
    spark.style.setProperty('--dx', `${Math.cos(angle) * dist}px`);
    spark.style.setProperty('--dy', `${Math.sin(angle) * dist - liftPx}px`);
    host.appendChild(spark);
    requestAnimationFrame(() => spark.classList.add('go'));
    window.setTimeout(() => spark.remove(), durationMs + 60);
  }
}

export type CelebrationBurstOptions = {
  /** Louder Analyze success (MOOD-0337). */
  intensity?: 'default' | 'loud';
  /** Draw a expanding ring behind sparks. */
  ring?: boolean;
};

/** Web helper: burst around an anchor element (or viewport center). */
export function celebrationBurst(
  anchor?: HTMLElement | null,
  options: CelebrationBurstOptions = {},
): void {
  if (typeof document === 'undefined') {
    return;
  }
  const loud = options.intensity === 'loud';
  const rect = anchor?.getBoundingClientRect();
  const cx = rect ? rect.left + rect.width / 2 : window.innerWidth / 2;
  const cy = rect ? rect.top + rect.height / 2 : window.innerHeight / 3;

  ensureDocumentStyles(document, loud ? 1400 : 640);

  // MOOD-0351: sparks only — no expanding ring (reads as a broken border).
  burstSparks({
    host: document.body,
    cx,
    cy,
    count: loud ? 22 : 10,
    injectStyles: false,
    sizePx: loud ? 9 : 5,
    durationMs: loud ? 1400 : 640,
    distMin: loud ? 42 : 22,
    distSpan: loud ? 70 : 28,
    liftPx: loud ? 18 : 10,
  });
}
