# Chrome MV3 + Vite — content script packaging

**Signal:** tooling-gap (LO-0011)  
**Audience:** agents shipping browser extensions from Vite multi-entry builds

## Problem

Vite multi-entry builds often emit content scripts as ES modules with shared chunks:

```js
import { … } from "./chunks/index.js";
```

Chrome **classic** `content_scripts` entries cannot load those imports. The script fails silently — `chrome.tabs.sendMessage` then errors and popups show vague copy like “Open a normal http(s) page…”.

## Required packaging (pick one)

### A — Prefer: single IIFE, no shared chunks (most compatible)

Build the **content** entry as `format: 'iife'` with `inlineDynamicImports: true` (or a dedicated Vite config) so `content.js` has **no** `import`/`export`. Keep `background` as `type: "module"` if needed.

### B — ES module content script

If you keep ESM output, set in `manifest.json`:

```json
"content_scripts": [
  {
    "matches": ["http://*/*", "https://*/*"],
    "js": ["content.js"],
    "run_at": "document_idle",
    "type": "module"
  }
]
```

Requires a Chromium version that supports module content scripts; still prefer inlining so `chunks/` path resolution is reliable under extension URLs.

## Definition of Done (extension tickets)

Before marking capture/toggle tickets done:

1. Load unpacked from **`dist/`** (not source).
2. Open a normal `https://` page and **hard-refresh** after install/reload.
3. Confirm console: content script loaded (project log prefix).
4. Toggle / hotkey arms overlay without the generic http(s) error.
5. Document any `VITE_*` env required for auth in the extension README (build-time inject).
6. **Inbox path (LO-0013):** “inbox saved” in the extension console is **not** enough. Either:
   - the capture appears in the **web app board Inbox** after sync (cloud `POST` / API), or
   - the ticket explicitly ships Sync UX + docs that local IDB ≠ board Inbox until sync.
7. **Cloud sync URL probe (LO-0042):** when the extension tries multiple localhost ports (stale `VITE_*` / `NEXT_PUBLIC_APP_URL`), **do not abort** on plain-text wrong-app responses such as `Server action not found.` (another Next app on `:3000`). Keep probing until the product API returns **product-shaped JSON** (`{ error }` / `{ ok, item }`) or a real auth/validation rejection. Stop only on product JSON auth/config errors — not on sibling apps’ 404 text. Align baked app URL with the live `npm run dev` port after rebuild + Load unpacked.
8. **Inbox delete bidirectional (LO-0160):** do not call companion ↔ cloud inbox “ready” while delete is one-way (local IDB only or cloud only). Same product surface → same delete semantics, or an explicit local-only label. Pair with design_playbook dual-surface delete (LO-0158).
9. **Global mode arm order (LO-0157, LO-0159):** for any “armed / capture on for all tabs” pattern:
   - Fan out apply messages (and **inject the content script on miss**) **before** writing durable/session storage that other surfaces treat as “already on.”
   - Writing storage first lets a closing popup abort mid-fan-out: UI shows armed while pages never got the overlay.
   - Prefer **storage-last**: confirm apply (or schedule inject+retry) → then persist the armed flag. On open tabs without a listener, `scripting.executeScript` / equivalent inject-on-miss, then re-send apply.

## Related

- Sprint review brief must point reviewers at live app + extension `dist/` — see `sprint_hitl.py` review template (LO-0012).
- Capture → board Inbox sync is a product ticket when missing (pattern: companion capture → authenticated inbox).
