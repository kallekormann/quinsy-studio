/**
 * Studio Library — neutral app page shell (header + content).
 */
import type { ReactNode } from 'react';

export interface PageShellProps {
  children: ReactNode;
  title?: string;
  headerRight?: ReactNode;
}

export function PageShell({ children, title = 'App', headerRight }: PageShellProps) {
  return (
    <div className="min-h-screen bg-bg">
      <header className="border-b border-neutral-200 bg-surface px-6 py-4">
        <div className="mx-auto flex max-w-3xl items-center justify-between">
          <h1 className="text-xl font-semibold text-neutral-900">{title}</h1>
          {headerRight}
        </div>
      </header>
      <main className="mx-auto max-w-3xl px-4 py-8">{children}</main>
    </div>
  );
}
