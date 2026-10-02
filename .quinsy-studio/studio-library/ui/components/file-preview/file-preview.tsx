/**
 * Studio Library — file preview.
 * Remap CSS variables in ui/tokens/design-tokens.css.
 * No product brand. Callers supply the pages, prose, plain text, or markdown.
 */
"use client"

import * as React from "react"
import { cn } from '../../utils/cn'

function PagedPreview({
  pages,
  kind = "page",
  fill = false,
}: {
  pages: React.ReactNode[]
  kind?: "page" | "slide"
  /** Pin the pager to the bottom of a stretched pane. */
  fill?: boolean
}) {
  const [index, setIndex] = React.useState(0)
  const count = pages.length
  const current = Math.min(index, Math.max(count - 1, 0))
  const label = kind === "slide" ? "Slide" : "Page"

  return (
    <div data-slot="paged-preview" className={cn(fill && "flex min-h-0 flex-1 flex-col")}>
      <div
        className={cn(
          fill && "preview-well min-h-0 flex-1",
          fill && kind === "slide" && "flex items-center justify-center p-8",
          fill && kind !== "slide" && "overflow-y-auto"
        )}
      >
      <div className={cn(fill && kind === "slide" && "w-full max-w-3xl", fill && kind !== "slide" && "p-4")}>
      <div
        className={cn(
          "overflow-hidden border border-border bg-card text-card-foreground shadow-md",
          kind === "slide" ? "aspect-video rounded-xl p-8" : "mx-auto aspect-[3/4] rounded-sm p-8",
          fill && kind === "slide" && "w-full"
        )}
      >
        {pages[current]}
      </div>
      </div>
      </div>
      <div className={cn("flex items-center justify-center gap-3", fill ? "shrink-0 border-t border-border bg-surface py-2" : "mt-3")}>
        <button
          type="button"
          className="inline-flex size-8 items-center justify-center rounded-full text-foreground hover:bg-muted disabled:opacity-40"
          aria-label={`Previous ${label.toLowerCase()}`}
          disabled={current === 0}
          onClick={() => setIndex((value) => Math.max(0, value - 1))}
        >
          <Caret direction="left" />
        </button>
        <p className="min-w-16 text-center text-xs text-muted-foreground">
          {label} {count === 0 ? 0 : current + 1} of {count}
        </p>
        <button
          type="button"
          className="inline-flex size-8 items-center justify-center rounded-full text-foreground hover:bg-muted disabled:opacity-40"
          aria-label={`Next ${label.toLowerCase()}`}
          disabled={current >= count - 1}
          onClick={() => setIndex((value) => Math.min(count - 1, value + 1))}
        >
          <Caret direction="right" />
        </button>
      </div>
    </div>
  )
}

function Caret({ direction }: { direction: "left" | "right" }) {
  return (
    <svg viewBox="0 0 16 16" className="size-4" aria-hidden>
      <path
        d={direction === "left" ? "M10 3 L5 8 L10 13" : "M6 3 L11 8 L6 13"}
        fill="none"
        stroke="currentColor"
        strokeWidth="1.5"
        strokeLinecap="round"
        strokeLinejoin="round"
      />
    </svg>
  )
}

function ProsePreview({ children, className }: { children: React.ReactNode; className?: string }) {
  return (
    <article
      data-slot="prose-preview"
      className={cn(
        "font-serif text-base leading-relaxed text-card-foreground [&_h1]:font-sans [&_h1]:text-2xl [&_h1]:font-semibold [&_h1]:tracking-tight [&_h2]:mt-6 [&_h2]:font-sans [&_h2]:text-lg [&_h2]:font-medium [&_p]:mt-4 [&_ul]:mt-4 [&_ul]:list-disc [&_ul]:pl-5 [&_li]:mt-1 [&_strong]:font-semibold",
        className
      )}
    >
      {children}
    </article>
  )
}

function PlainPreview({ text }: { text: string }) {
  return (
    <pre data-slot="plain-preview" className="whitespace-pre-wrap font-sans text-sm leading-relaxed text-card-foreground">
      {text}
    </pre>
  )
}

function MarkdownPreview({ source }: { source: string }) {
  return (
    <ProsePreview>
      {renderMarkdown(source)}
    </ProsePreview>
  )
}

function renderMarkdown(source: string) {
  const blocks: React.ReactNode[] = []
  const lines = source.replace(/\r\n/g, "\n").split("\n")
  let index = 0
  while (index < lines.length) {
    const line = lines[index]
    if (line.trim() === "") {
      index += 1
      continue
    }
    if (line.startsWith("### ")) {
      blocks.push(<h2 key={index}>{inline(line.slice(4))}</h2>)
      index += 1
      continue
    }
    if (line.startsWith("## ")) {
      blocks.push(<h2 key={index}>{inline(line.slice(3))}</h2>)
      index += 1
      continue
    }
    if (line.startsWith("# ")) {
      blocks.push(<h1 key={index}>{inline(line.slice(2))}</h1>)
      index += 1
      continue
    }
    if (line.startsWith("- ")) {
      const items: React.ReactNode[] = []
      while (index < lines.length && lines[index].startsWith("- ")) {
        items.push(<li key={index}>{inline(lines[index].slice(2))}</li>)
        index += 1
      }
      blocks.push(<ul key={`ul-${index}`}>{items}</ul>)
      continue
    }
    const paragraph: string[] = []
    while (index < lines.length && lines[index].trim() !== "" && !lines[index].startsWith("#") && !lines[index].startsWith("- ")) {
      paragraph.push(lines[index])
      index += 1
    }
    blocks.push(<p key={index}>{inline(paragraph.join(" "))}</p>)
  }
  return blocks
}

function inline(text: string) {
  const parts = text.split(/(\*\*[^*]+\*\*|\*[^*]+\*|`[^`]+`)/g)
  return parts.map((part, index) => {
    if (part.startsWith("**") && part.endsWith("**")) return <strong key={index}>{part.slice(2, -2)}</strong>
    if (part.startsWith("*") && part.endsWith("*")) return <em key={index}>{part.slice(1, -1)}</em>
    if (part.startsWith("`") && part.endsWith("`")) {
      return <code key={index} className="rounded bg-muted px-1 font-sans text-[0.85em]">{part.slice(1, -1)}</code>
    }
    return part
  })
}

export { PagedPreview, ProsePreview, PlainPreview, MarkdownPreview }
