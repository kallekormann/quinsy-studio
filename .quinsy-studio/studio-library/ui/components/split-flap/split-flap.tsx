/**
 * Studio Library — split-flap board.
 * Remap CSS variables in ui/tokens/design-tokens.css.
 * No product brand. Each character is a flap that rotates in place.
 */
"use client"

import * as React from "react"
import { cn } from "../../utils/cn"
import styles from "./split-flap.module.css"

const FLIP_MS = 140

function SplitFlap({
  value,
  cascade = false,
  plain = false,
  charset = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789 ",
  className,
  ...props
}: React.ComponentProps<"span"> & {
  value: string
  cascade?: boolean
  plain?: boolean
  charset?: string
}) {
  const [text, setText] = React.useState(value)

  React.useEffect(() => {
    if (!cascade) {
      setText(value)
      return
    }
    const reduce = window.matchMedia("(prefers-reduced-motion: reduce)").matches
    if (reduce) {
      setText(value)
      return
    }
    let cancelled = false
    const frames = Array.from({ length: value.length }, () => " ")
    setText(frames.join(""))
    const timers = value.split("").map((target, index) => {
      let cycles = 0
      return window.setInterval(() => {
        if (cancelled) return
        cycles += 1
        frames[index] = cycles > 8 + index * 3
          ? target
          : charset[Math.floor(Math.random() * charset.length)] || " "
        if (cycles > 8 + index * 3) window.clearInterval(timers[index])
        setText(frames.join(""))
      }, 50)
    })
    return () => {
      cancelled = true
      timers.forEach((id) => window.clearInterval(id))
    }
  }, [value, cascade, charset])

  return (
    <span
      data-slot="split-flap"
      role="status"
      aria-label={value}
      {...props}
      className={cn(styles.board, plain && styles.plain, className)}
    >
      {text.split("").map((char, index) => (
        <Flap key={`${index}-${text.length}`} char={char} />
      ))}
    </span>
  )
}

function Flap({ char }: { char: string }) {
  const [face, setFace] = React.useState(char)
  const [flipping, setFlipping] = React.useState(false)
  const shown = React.useRef(char)

  React.useEffect(() => {
    if (char === shown.current) return
    const reduce = window.matchMedia("(prefers-reduced-motion: reduce)").matches
    if (reduce) {
      shown.current = char
      setFace(char)
      return
    }
    setFlipping(true)
    const swap = window.setTimeout(() => {
      shown.current = char
      setFace(char)
    }, FLIP_MS / 2)
    const end = window.setTimeout(() => setFlipping(false), FLIP_MS)
    return () => {
      window.clearTimeout(swap)
      window.clearTimeout(end)
    }
  }, [char])

  return (
    <span className={cn(styles.cell, flipping && styles.flipping)} aria-hidden="true">
      <span className={styles.face}>{face === " " ? "" : face}</span>
    </span>
  )
}

export { SplitFlap }
