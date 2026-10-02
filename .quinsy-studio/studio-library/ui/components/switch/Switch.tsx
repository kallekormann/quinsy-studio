/**
 * Studio Library — themable shadcn-style component.
 * Remap CSS variables in ui/tokens/design-tokens.css ( --primary, --background, … ).
 * Adapted from Command Center / shadcn; no product brand.
 */
"use client"

import * as React from "react"
import { cn } from '../../utils/cn'
import { Switch as SwitchPrimitive } from "radix-ui"

function Switch({
  className,
  size = "default",
  ...props
}: React.ComponentProps<typeof SwitchPrimitive.Root> & {
  size?: "sm" | "default"
}) {
  return (
    <SwitchPrimitive.Root
      data-slot="switch"
      data-size={size}
      className={cn(
        "peer relative inline-flex h-[18px] w-8 shrink-0 items-center rounded-full border border-transparent bg-muted outline-none transition-colors focus-visible:ring-2 focus-visible:ring-ring disabled:cursor-not-allowed disabled:opacity-50 data-[state=checked]:bg-accent data-[size=sm]:h-3.5 data-[size=sm]:w-6",
        className
      )}
      {...props}
    >
      <SwitchPrimitive.Thumb
        data-slot="switch-thumb"
        className="pointer-events-none block size-4 translate-x-0.5 rounded-full bg-surface shadow-sm transition-transform data-[state=checked]:translate-x-3.5 data-[size=sm]:size-3"
      />
    </SwitchPrimitive.Root>
  )
}

export { Switch }
