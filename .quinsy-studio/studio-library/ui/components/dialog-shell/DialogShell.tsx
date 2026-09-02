/**
 * Moody Bloom — DialogShell molecule
 * Header (title) + body + footer (actions). Primary action should be rightmost.
 */
'use client';

import type { ReactNode } from 'react';
import {
  Dialog,
  DialogBackdrop,
  DialogDescription,
  DialogPanel,
  DialogTitle,
} from '@headlessui/react';

export type DialogShellProps = {
  open: boolean;
  onClose: () => void;
  title: ReactNode;
  description?: ReactNode;
  children: ReactNode;
  /** Footer actions — place primary button last (rightmost in LTR). Omit when no actions. */
  footer?: ReactNode;
  className?: string;
  panelClassName?: string;
  initialFocus?: boolean;
};

export function DialogShell({
  open,
  onClose,
  title,
  description,
  children,
  footer,
  className = '',
  panelClassName = '',
}: DialogShellProps) {
  return (
    <Dialog open={open} onClose={onClose} className={`relative z-50 ${className}`}>
      <DialogBackdrop
        transition
        className="fixed inset-0 bg-black/40 transition duration-150 data-closed:opacity-0"
      />
      <div className="fixed inset-0 flex items-center justify-center p-4">
        <DialogPanel
          transition
          className={`flex max-h-[min(90dvh,40rem)] w-full max-w-md flex-col rounded-xl border border-[color:var(--line)] bg-surface p-0 shadow-float outline-none transition duration-150 data-closed:scale-95 data-closed:opacity-0 dark:bg-surface ${panelClassName}`}
        >
          <header className="shrink-0 border-b border-[color:var(--line)] px-6 py-4">
            <DialogTitle className="text-lg font-semibold text-ink">{title}</DialogTitle>
            {description ? (
              <DialogDescription className="mt-1 text-sm text-body">
                {description}
              </DialogDescription>
            ) : null}
          </header>
          <div className="min-h-0 flex-1 overflow-y-auto overscroll-contain px-6 py-4">
            {children}
          </div>
          {footer ? (
            <footer className="flex shrink-0 flex-row-reverse flex-wrap items-center justify-start gap-2 border-t border-[color:var(--line)] px-6 py-4">
              {footer}
            </footer>
          ) : null}
        </DialogPanel>
      </div>
    </Dialog>
  );
}
