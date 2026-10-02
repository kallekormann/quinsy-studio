# file-preview

**Atomic level:** Molecule (`ui-molecule`)

Viewers for a file the caller already has:

- `PagedPreview` — a page or a slide, with previous and next
- `ProsePreview` — a styled document (headings, paragraphs, lists)
- `PlainPreview` — plain text, line breaks kept
- `MarkdownPreview` — headings, lists, bold, italic, and code from a markdown string

Styled only with semantic tokens. The caller supplies the content.

Pull: `./studio library pull <project> file-preview`
