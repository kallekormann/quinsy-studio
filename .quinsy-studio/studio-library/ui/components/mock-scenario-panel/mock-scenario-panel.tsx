/**
 * Studio Library — design-mock scenario harness (dev-only).
 *
 * Floating panel for `(design-mocks)` routes: lists the scenario states a mock
 * must make reachable (empty / loading / error, open / closed, long-content, …),
 * keeps the active state in `?state=` so the human can click through the running
 * prototype AND Playwright can capture each state by URL:
 *
 *   http://localhost:3000/design-mocks/<TICKET>/?state=empty
 *
 * Framework-agnostic: reads/writes `window.location.search` directly, so it
 * works in any React app router without importing next/navigation.
 * Never ship this outside the (design-mocks) route group.
 */
'use client'

import { useEffect, useState } from 'react'
import { cn } from '../../utils/cn'

export interface MockScenario {
  /** URL value, e.g. "empty", "loading", "error", "open" */
  id: string
  /** Button label; defaults to id */
  label?: string
}

const QUERY_KEY = 'state'

function readStateFromUrl(fallback: string): string {
  if (typeof window === 'undefined') return fallback
  return new URLSearchParams(window.location.search).get(QUERY_KEY) ?? fallback
}

function writeStateToUrl(id: string) {
  if (typeof window === 'undefined') return
  const url = new URL(window.location.href)
  url.searchParams.set(QUERY_KEY, id)
  window.history.replaceState(null, '', url.toString())
}

export function useMockScenario(defaultState = 'rest'): [string, (id: string) => void] {
  const [state, setState] = useState(defaultState)
  useEffect(() => {
    setState(readStateFromUrl(defaultState))
  }, [defaultState])
  const set = (id: string) => {
    setState(id)
    writeStateToUrl(id)
  }
  return [state, set]
}

export interface MockScenarioPanelProps {
  scenarios: Array<MockScenario | string>
  /** Current state; pair with useMockScenario */
  value: string
  onValueChange: (id: string) => void
  /** Ticket id shown as the panel title, e.g. "T-0042" */
  ticketId?: string
  className?: string
}

/**
 * Usage inside a mock page:
 *
 *   const [state, setState] = useMockScenario()
 *   <MockScenarioPanel scenarios={['rest','empty','loading','error']} value={state} onValueChange={setState} />
 *   {state === 'empty' ? <EmptyView /> : <RealView data-state={state} … />}
 */
export function MockScenarioPanel({
  scenarios,
  value,
  onValueChange,
  ticketId,
  className,
}: MockScenarioPanelProps) {
  const items = scenarios.map((s) => (typeof s === 'string' ? { id: s } : s))
  return (
    <aside
      data-slot="mock-scenario-panel"
      data-state={value}
      className={cn(
        'fixed bottom-4 right-4 z-50 flex max-w-xs flex-wrap items-center gap-1 rounded-md border border-border bg-background/95 p-2 shadow-md backdrop-blur',
        className,
      )}
      aria-label="Mock scenario switcher"
    >
      {ticketId ? (
        <span className="w-full px-1 font-mono text-[10px] uppercase tracking-wide text-muted-foreground">
          {ticketId} · mock states
        </span>
      ) : null}
      {items.map((s) => (
        <button
          key={s.id}
          type="button"
          onClick={() => onValueChange(s.id)}
          aria-pressed={value === s.id}
          className={cn(
            'rounded-sm px-2 py-1 font-mono text-xs transition-colors duration-150',
            value === s.id
              ? 'bg-primary text-primary-foreground'
              : 'bg-muted text-muted-foreground hover:bg-accent hover:text-accent-foreground',
          )}
        >
          {s.label ?? s.id}
        </button>
      ))}
    </aside>
  )
}
