/**
 * Moody Bloom — position-aware Tooltip / label popover (MOOD-0425).
 * Hover + focus; portals to body; flips/shifts to stay in viewport.
 */
'use client';

import {
  useCallback,
  useEffect,
  useId,
  useLayoutEffect,
  useRef,
  useState,
  type ReactNode,
} from 'react';
import { createPortal } from 'react-dom';
import { POPOVER_Z_CLASS } from '@ui/styles/popover-styles';
import {
  computeTooltipPosition,
  type TooltipCoords,
  type TooltipPlacement,
} from './placement';

export type { TooltipPlacement };

export type TooltipVariant = 'tooltip' | 'popover';

export type TooltipProps = {
  /** Short label (icon buttons: Library, Inbox, …). */
  label?: ReactNode;
  /** Richer body — use with `variant="popover"`. */
  content?: ReactNode;
  /** Preferred side; flips when that side has no room. */
  placement?: TooltipPlacement;
  /**
   * `tooltip` — compact label chip.
   * `popover` — roomier panel for more text / structure.
   */
  variant?: TooltipVariant;
  delayShow?: number;
  delayHide?: number;
  disabled?: boolean;
  className?: string;
  children: ReactNode;
};

const tooltipPanelClass = [
  POPOVER_Z_CLASS,
  'pointer-events-none max-w-[14rem] rounded-md border border-[color:var(--line)]',
  'bg-[color:var(--color-surface)] px-2 py-1 text-[12px] font-medium leading-snug text-ink shadow-md',
].join(' ');

const richPanelClass = [
  POPOVER_Z_CLASS,
  'pointer-events-auto max-w-[18rem] rounded-[var(--radius-md)] border border-[color:var(--line)]',
  'bg-[color:var(--color-surface)] px-3 py-2 text-[13px] leading-snug text-body shadow-[var(--elevate-hover)]',
].join(' ');

export function Tooltip({
  label,
  content,
  placement = 'bottom',
  variant = 'tooltip',
  delayShow = 280,
  delayHide = 120,
  disabled = false,
  className = '',
  children,
}: TooltipProps) {
  const tipId = useId();
  const triggerRef = useRef<HTMLSpanElement>(null);
  const tipRef = useRef<HTMLDivElement>(null);
  const showTimer = useRef<ReturnType<typeof setTimeout> | null>(null);
  const hideTimer = useRef<ReturnType<typeof setTimeout> | null>(null);
  const [open, setOpen] = useState(false);
  const [mounted, setMounted] = useState(false);
  const [coords, setCoords] = useState<TooltipCoords | null>(null);

  const body = content ?? label;

  useEffect(() => {
    setMounted(true);
  }, []);

  const clearTimers = useCallback(() => {
    if (showTimer.current) clearTimeout(showTimer.current);
    if (hideTimer.current) clearTimeout(hideTimer.current);
    showTimer.current = null;
    hideTimer.current = null;
  }, []);

  const scheduleShow = useCallback(() => {
    if (disabled || body == null || body === '') return;
    clearTimers();
    showTimer.current = setTimeout(() => setOpen(true), delayShow);
  }, [body, clearTimers, delayShow, disabled]);

  const scheduleHide = useCallback(() => {
    clearTimers();
    hideTimer.current = setTimeout(() => setOpen(false), delayHide);
  }, [clearTimers, delayHide]);

  const updatePosition = useCallback(() => {
    const trigger = triggerRef.current;
    const tip = tipRef.current;
    if (!trigger || !tip) return;
    const next = computeTooltipPosition(
      trigger.getBoundingClientRect(),
      { width: tip.offsetWidth, height: tip.offsetHeight },
      placement,
    );
    setCoords(next);
  }, [placement]);

  useLayoutEffect(() => {
    if (!open) {
      setCoords(null);
      return;
    }
    updatePosition();
    window.addEventListener('resize', updatePosition);
    window.addEventListener('scroll', updatePosition, true);
    return () => {
      window.removeEventListener('resize', updatePosition);
      window.removeEventListener('scroll', updatePosition, true);
    };
  }, [open, updatePosition]);

  useEffect(() => () => clearTimers(), [clearTimers]);

  const panelClass = variant === 'popover' ? richPanelClass : tooltipPanelClass;

  const tipNode =
    open && mounted && body != null
      ? createPortal(
          <div
            ref={tipRef}
            id={tipId}
            role="tooltip"
            data-placement={coords?.placement ?? placement}
            className={`fixed ${panelClass} ${coords ? 'opacity-100' : 'opacity-0'} transition-opacity duration-100 ${className}`}
            style={
              coords
                ? { top: coords.top, left: coords.left }
                : { top: 0, left: 0, visibility: 'hidden' as const }
            }
            onMouseEnter={
              variant === 'popover'
                ? () => {
                    clearTimers();
                    setOpen(true);
                  }
                : undefined
            }
            onMouseLeave={variant === 'popover' ? scheduleHide : undefined}
          >
            {body}
          </div>,
          document.body,
        )
      : null;

  return (
    <>
      <span
        ref={triggerRef}
        className="inline-flex max-w-full"
        onMouseEnter={scheduleShow}
        onMouseLeave={scheduleHide}
        onFocusCapture={scheduleShow}
        onBlurCapture={scheduleHide}
        aria-describedby={open ? tipId : undefined}
      >
        {children}
      </span>
      {tipNode}
    </>
  );
}
