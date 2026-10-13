/**
 * Studio Library — themable shadcn-style component.
 * Remap CSS variables in ui/tokens/design-tokens.css ( --primary, --background, … ).
 * Adapted from shadcn; no product brand.
 */
"use client"

import * as React from "react"
import { cn } from '../../utils/cn'
import { Progress as ProgressPrimitive } from "radix-ui"

function Progress({
  className,
  value,
  ...props
}: React.ComponentProps<typeof ProgressPrimitive.Root>) {
  return (
    <ProgressPrimitive.Root
      data-slot="progress"
      className={cn(
        "relative flex h-1 w-full items-center overflow-x-hidden rounded-full bg-muted",
        className
      )}
      {...props}
    >
      <ProgressPrimitive.Indicator
        data-slot="progress-indicator"
        className="size-full flex-1 bg-primary transition-[transform,width] duration-[var(--motion-duration-medium)] ease-[var(--motion-ease-smooth-out)] motion-reduce:transition-none"
        style={{ transform: `translateX(-${100 - (value || 0)}%)` }}
      />
    </ProgressPrimitive.Root>
  )
}

export { Progress }
