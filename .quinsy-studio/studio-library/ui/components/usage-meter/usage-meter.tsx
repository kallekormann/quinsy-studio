/**
 * Studio Library — themable usage meter.
 * Remap CSS variables in ui/tokens/design-tokens.css ( --primary, --background, … ).
 * No product brand. Filled segments are used. The remainder is a hollow bar.
 */
"use client"

import * as React from "react"
import { cn } from '../../utils/cn'

export type UsageMeterSegment = {
  id: string
  value: number
  kind: string
  label: string
}

function UsageMeter({
  segments,
  capacity,
  activeId,
  openId,
  formatAmount = (value) => String(value),
  className,
}: {
  segments: UsageMeterSegment[]
  capacity: number
  activeId?: string
  openId?: string
  formatAmount?: (value: number) => string
  className?: string
}) {
  const used = segments.reduce((sum, segment) => sum + segment.value, 0)
  const free = Math.max(0, capacity - used)
  const parts = [
    ...segments.map((segment) => ({
      ...segment,
      amount: formatAmount(segment.value),
      hollow: false,
    })),
    {
      id: '__free',
      value: free,
      kind: 'Free space',
      label: 'Not used',
      amount: formatAmount(free),
      hollow: true,
    },
  ]

  return (
    <div
      data-slot="usage-meter"
      className={cn('flex h-3 min-w-0 flex-1 items-stretch rounded-full border border-border bg-transparent p-0.5', className)}
      role="group"
      aria-label={`${formatAmount(used)} used, ${formatAmount(free)} free`}
    >
      {parts.map((part, index) => (
        <span
          key={part.id}
          className="group/segment relative h-full min-w-0"
          style={{ flexGrow: part.value, flexBasis: 0, minWidth: part.value > 0 ? 6 : 0 }}
        >
          <button
            type="button"
            className={cn(
              'h-full w-full rounded-full outline-none focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-ring',
              part.hollow ? 'bg-transparent hover:bg-muted' : part.id === activeId ? 'bg-primary' : 'bg-foreground group-hover/segment:bg-primary'
            )}
            aria-label={`${part.kind}, ${part.label}, ${part.amount}`}
          />
          <span
            role="tooltip"
            className={cn(
              'pointer-events-none absolute top-full z-30 mt-2 w-max rounded-2xl border border-border bg-popover px-3 py-2 text-left text-xs text-popover-foreground shadow-md',
              index === 0 ? 'left-0' : index === parts.length - 1 ? 'right-0' : 'left-1/2 -translate-x-1/2',
              openId === part.id ? 'block' : 'hidden group-hover/segment:block group-focus-within/segment:block'
            )}
          >
            <span className="block font-medium">{part.kind}</span>
            <span className="mt-0.5 block text-muted-foreground">{part.label}</span>
            <span className="mt-0.5 block text-muted-foreground">{part.amount}</span>
          </span>
        </span>
      ))}
    </div>
  )
}

export { UsageMeter }
