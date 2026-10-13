'use client';

import { createContext, useCallback, useContext, useMemo, useState, type ReactNode } from 'react';
import { motion, useReducedMotion } from 'framer-motion';
import { Button } from '../atoms/Button';
import { CloseIcon } from '../atoms/Icon';
import {
  bloomPanelBodyClass,
  bloomPanelEyebrowClass,
  bloomPanelHeaderClass,
  bloomPanelTitleClass,
  FLOATING_RIGHT_RAIL_CLASS,
} from '@ui/styles/chrome-styles';
import { FLOATING_RIGHT_RAIL_WIDTH_PX, floatingRightRailMotion } from '@/lib/motion/app-motion';

export type InspectorPanelShellProps = {
  eyebrow: string;
  title: string;
  subtitle?: string;
  children: ReactNode;
  className?: string;
  /** Exclusive accordion: which section id is open. */
  defaultOpenSection?: string;
  /** Dismiss control — clears selection / closes panel. */
  onClose?: () => void;
};

type AccordionCtx = {
  openId: string | null;
  setOpenId: (id: string) => void;
};

const InspectorAccordionContext = createContext<AccordionCtx | null>(null);

export function useInspectorAccordion(): AccordionCtx {
  const ctx = useContext(InspectorAccordionContext);
  if (!ctx) {
    return {
      openId: null,
      setOpenId: () => undefined,
    };
  }
  return ctx;
}

/** Floating metadata panel chrome for item inspectors (studio rail family). */
export function InspectorPanelShell({
  eyebrow,
  title,
  subtitle,
  children,
  className = '',
  defaultOpenSection = 'tags',
  onClose,
}: InspectorPanelShellProps) {
  const reduceMotion = useReducedMotion();
  const [openId, setOpenIdState] = useState<string | null>(defaultOpenSection);
  const setOpenId = useCallback((id: string) => {
    setOpenIdState((prev) => (prev === id ? id : id));
  }, []);
  const value = useMemo(() => ({ openId, setOpenId }), [openId, setOpenId]);

  return (
    <InspectorAccordionContext.Provider value={value}>
      <motion.aside
        initial={reduceMotion ? false : floatingRightRailMotion.initial}
        animate={floatingRightRailMotion.animate}
        exit={reduceMotion ? { opacity: 0 } : floatingRightRailMotion.exit}
        transition={reduceMotion ? { duration: 0 } : floatingRightRailMotion.transition}
        className={`${FLOATING_RIGHT_RAIL_CLASS} ${className}`}
        style={{ right: 12, width: FLOATING_RIGHT_RAIL_WIDTH_PX }}
        aria-label="Inspector"
      >
        <div className={bloomPanelHeaderClass}>
          <div className="min-w-0 flex-1">
            <p className={bloomPanelEyebrowClass}>{eyebrow}</p>
            <p className={`truncate ${bloomPanelTitleClass}`}>{title}</p>
            {subtitle ? (
              <p className="mt-0.5 text-xs text-[color:var(--body)]">{subtitle}</p>
            ) : null}
          </div>
          {onClose ? (
            <Button
              type="button"
              variant="ghost"
              buttonSize="sm"
              className="h-10 w-10 shrink-0 px-0"
              aria-label="Close inspector"
              onClick={onClose}
            >
              <CloseIcon size={24} />
            </Button>
          ) : null}
        </div>
        <div className={bloomPanelBodyClass}>{children}</div>
      </motion.aside>
    </InspectorAccordionContext.Provider>
  );
}

export function InspectorPanelSection({
  children,
  className = '',
}: {
  children: ReactNode;
  className?: string;
}) {
  return (
    <div className={`mt-3 border-t border-[color:var(--line)] pt-3 ${className}`}>{children}</div>
  );
}

/** Exclusive accordion row — only one open at a time within the shell. */
export function InspectorAccordionSection({
  id,
  title,
  children,
  trailing,
}: {
  id: string;
  title: string;
  children: ReactNode;
  trailing?: ReactNode;
}) {
  const { openId, setOpenId } = useInspectorAccordion();
  const open = openId === id;

  return (
    <div className="border-t border-[color:var(--line)] first:border-t-0">
      <button
        type="button"
        className="flex w-full items-center gap-2 py-2.5 text-left"
        aria-expanded={open}
        onClick={() => setOpenId(id)}
      >
        <span className="text-[10px] text-neutral-400" aria-hidden>
          {open ? '▾' : '▸'}
        </span>
        <span className="flex-1 text-xs font-medium text-neutral-700 dark:text-neutral-200">
          {title}
        </span>
        {trailing ? <span onClick={(e) => e.stopPropagation()}>{trailing}</span> : null}
      </button>
      {open ? <div className="pb-3 pl-4">{children}</div> : null}
    </div>
  );
}
