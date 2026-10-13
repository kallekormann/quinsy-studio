'use client';

import type { ReactNode } from 'react';
import { Button } from '@ui/components/atoms/Button';
import { CloseIcon } from '@ui/components/atoms/Icon';
import { Tooltip } from '@ui/components/tooltip';
import {
  studioRailButtonActiveClass,
  studioRailButtonBaseClass,
  studioRailClass,
  studioPanelBodyClass,
  studioPanelClass,
  studioPanelHeaderClass,
  studioPanelTitleClass,
} from './studio-rail-styles';

export type StudioPeerId = 'inspector' | 'inbox' | 'library' | 'export' | 'brand-kit';

export type StudioRailItem = {
  id: StudioPeerId;
  label: string;
  icon: ReactNode;
  badge?: ReactNode;
};

export type StudioRailProps = {
  items: StudioRailItem[];
  activePeer: StudioPeerId | null;
  onPeerChange: (peer: StudioPeerId | null) => void;
  className?: string;
};

export type StudioPanelProps = {
  title: string;
  children: ReactNode;
  headerTrailing?: ReactNode;
  onClose?: () => void;
  className?: string;
  /** Full-bleed scroll body for docked drawer content (inbox, library). */
  flushBody?: boolean;
  'data-testid'?: string;
};

export type StudioDockProps = {
  items: StudioRailItem[];
  activePeer: StudioPeerId | null;
  onPeerChange: (peer: StudioPeerId | null) => void;
  panelTitle?: string;
  panelTrailing?: ReactNode;
  /** Close the active panel (on title chrome, not item row). */
  onPanelClose?: () => void;
  children?: ReactNode;
  className?: string;
  panelFlush?: boolean;
};

/** Icon rail — docked 52px column on the board stage right edge. */
export function StudioRail({ items, activePeer, onPeerChange, className = '' }: StudioRailProps) {
  return (
    <nav className={`${studioRailClass} ${className}`} aria-label="Studio panels">
      {items.map((item) => {
        const active = activePeer === item.id;
        return (
          <Tooltip key={item.id} label={item.label} placement="left">
            <Button
              type="button"
              variant="ghost"
              buttonSize="lg"
              iconOnly
              aria-label={item.label}
              aria-current={active ? 'true' : undefined}
              className={`${studioRailButtonBaseClass} ${active ? studioRailButtonActiveClass : ''}`}
              onClick={() => onPeerChange(active ? null : item.id)}
            >
              {item.icon}
              {item.badge ? (
                <span className="pointer-events-none absolute -right-0.5 -top-0.5">
                  {item.badge}
                </span>
              ) : null}
            </Button>
          </Tooltip>
        );
      })}
    </nav>
  );
}

/** Docked panel shell — 300px chrome column beside the rail. */
export function StudioPanel({
  title,
  children,
  headerTrailing,
  onClose,
  className = '',
  flushBody = false,
  'data-testid': dataTestId,
}: StudioPanelProps) {
  return (
    <aside
      className={`${studioPanelClass} ${className}`}
      aria-label={title}
      data-testid={dataTestId}
    >
      <div className={studioPanelHeaderClass}>
        <h3 className={studioPanelTitleClass}>{title}</h3>
        <div className="flex shrink-0 items-center gap-1">
          {headerTrailing ? <div>{headerTrailing}</div> : null}
          {onClose ? (
            <Tooltip label="Close panel" placement="left">
              <Button
                type="button"
                variant="ghost"
                buttonSize="sm"
                className="h-8 w-8 px-0"
                aria-label={`Close ${title}`}
                onClick={onClose}
              >
                <CloseIcon size={20} />
              </Button>
            </Tooltip>
          ) : null}
        </div>
      </div>
      <div
        className={
          flushBody
            ? 'flex min-h-0 flex-1 flex-col overflow-hidden px-3.5 pt-3.5 pb-3.5'
            : studioPanelBodyClass
        }
      >
        {children}
      </div>
    </aside>
  );
}

/** Rail + optional panel — panel renders when `activePeer` is set and `children` provided. */
export function StudioDock({
  items,
  activePeer,
  onPeerChange,
  panelTitle,
  panelTrailing,
  onPanelClose,
  children,
  className = '',
  panelFlush = false,
}: StudioDockProps) {
  const showPanel = activePeer !== null && children !== undefined;

  return (
    <div className={`flex h-full min-h-0 shrink-0 ${className}`}>
      {showPanel && panelTitle ? (
        <StudioPanel
          title={panelTitle}
          headerTrailing={panelTrailing}
          onClose={onPanelClose}
          flushBody={panelFlush}
        >
          {children}
        </StudioPanel>
      ) : null}
      <StudioRail items={items} activePeer={activePeer} onPeerChange={onPeerChange} />
    </div>
  );
}
