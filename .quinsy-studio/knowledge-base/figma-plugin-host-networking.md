# Figma plugin host networking (CORS / origin null)

**Signal:** process-gap (LO-0022, LO-0041, LO-0043, LO-0044, source: moody)  
**Audience:** agents shipping Figma (or similar) plugins that call the project API

## Problem

Figma plugin **UI** runs in a sandboxed iframe (`origin: null`). Browser `fetch` from the UI to `http://127.0.0.1:…` fails CORS preflight unless the API explicitly allows it. Console noise like `Unrecognized feature: 'local-network-access'` is Figma chrome — not the root cause.

## Localhost vs 127.0.0.1 (LO-0041)

Figma `networkAccess` / CSP treat **`http://localhost:<port>`** and **`http://127.0.0.1:<port>`** as **different origins**.

| Rule | Detail |
|------|--------|
| Manifest | List **`http://localhost:<port>` only** in `devAllowedDomains` (or allowedDomains). Figma **rejects** `127.0.0.1` at manifest load. |
| Plugin API base | Default and persisted prefs must use **`localhost`**, never `127.0.0.1`. |
| Stale prefs | `figma.clientStorage` can restore an old `127.0.0.1:…` base after rebuild/reinstall. That overrides UI defaults and produces CSP errors that look like a “broken allowlist.” |
| Mitigate | On prefs load / `set-api-base`, normalize `127.0.0.1` → `localhost`. DoD: Login must hit an allowlisted `localhost` URL. |

CSP text such as *Connecting to 'http://127.0.0.1:…' violates … localhost:…* means the **request host is wrong**, not that localhost entries failed.

## Required pattern

1. **Network from plugin main thread** (`code.ts`) via `fetch` in the plugin sandbox (not subject to UI iframe CORS the same way), **or**
2. API routes used by the plugin (`/api/figma/*`) answer **OPTIONS** + `Access-Control-Allow-Origin` for plugin callers if UI must fetch.

Prefer (1): UI posts a message → main thread fetches → UI renders result.

## Definition of Done (plugin / OAuth / boards tickets)

Before `./studio move … done`:

1. Load the plugin in **Figma desktop** (or documented host).
2. Click the real primary CTA (e.g. Login with the product) — browser OAuth opens.
3. Confirm no CORS / CSP failure on `plugin-auth` / `boards` in the console (request host is `localhost`, not `127.0.0.1`).
4. Board list (or equivalent) loads after login.
5. Unit tests alone are insufficient.
6. Rebuild alone is not proof prefs are clean — assert the live API base or normalize storage.

## Definition of Done (stickersheet / kit placement — LO-0043)

Before marking stickersheet or “rich kit” tickets done:

1. After Import / place kit, open the stickersheet page in Figma.
2. **Fail** if Atoms / Molecules / Organisms (or equivalent) show **only** section titles + blurbs.
3. **Pass** only when inventory children are visible (e.g. Button / Input / Badge / Card frames — enough that a human can use them as a stickersheet).
4. Prefer an automated check (child count under each section frame, or named prefixes) in addition to human smoke.
5. Section scaffold without components is **not** done — even if gate 5 / unit tests are green.

## Definition of Done (kit fidelity — LO-0044)

When the ticket promises a **professional / shadcn-class** stickersheet:

1. A **written north-star** exists (ticket design spec or `docs/…`) covering: Figma Components vs frames, DNA type ramp, chrome quality (fills, borders, elevation), moodboard refs.
2. Human smoke compares live canvas to that north-star (screenshot or mock).
3. **Fail** if the sheet reads as wireframe chrome (empty white cards, thin unlabeled boxes, Inter-only when board DNA has faces).
4. Component count without fidelity is **not** done.

## Related

- HITL rules LO-0022 / LO-0041 in `process/human-in-the-loop.md`
- Chrome extension packaging: `chrome-mv3-vite-content-scripts.md`
