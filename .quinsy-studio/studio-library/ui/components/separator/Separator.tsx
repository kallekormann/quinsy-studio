/**
 * Studio Library — themable shadcn-style component.
 * Remap CSS variables in ui/tokens/design-tokens.css ( --primary, --background, … ).
 * Adapted from shadcn; no product brand.
 */
"use client"

import * as React from "react"
import { cn } from '../../utils/cn'
import { Separator as SeparatorPrimitive } from "radix-ui"

function Separator({
  className,
  orientation = "horizontal",
  decorative = true,
  ...props
}: React.ComponentProps<typeof SeparatorPrimitive.Root>) {
  return (
    <SeparatorPrimitive.Root
      data-slot="separator"
      decorative={decorative}
      orientation={orientation}
      className={cn(
        "shrink-0 bg-border data-horizontal:h-px data-horizontal:w-full data-vertical:w-px data-vertical:self-stretch",
        className
      )}
      {...props}
    />
  )
}

export { Separator }
