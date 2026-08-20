# QA smoke routes

Playwright-based post-build smoke tests driven by a JSON route list. Used by Quinsy Studio QA gate level 5 (`docs/smoke-routes.json`).

## Pull

```bash
./studio library pull <project> qa-smoke
```

## Setup in project

1. Copy `smoke-routes.example.json` → `docs/smoke-routes.json` and edit routes.
2. Add npm script (adjust path if you pull to `scripts/qa/`):

```json
{
  "scripts": {
    "smoke": "node scripts/qa/run-smoke-routes.mjs",
    "smoke:config": "node scripts/qa/run-smoke-routes.mjs --config docs/smoke-routes.json"
  }
}
```

3. Dev dependency: `playwright` (and `npx playwright install chromium` in CI).

## Config

| Field | Default | Description |
|-------|---------|-------------|
| `port` | 3456 | Local server port |
| `host` | 127.0.0.1 | Bind host |
| `startCommand` | `next start` | Spawn command; `{port}` `{host}` placeholders |
| `startCwd` | `.` | Working directory for server |
| `routes[].path` | — | Path to hit |
| `routes[].expectText` | — | Substring in `body` |
| `routes[].expectSelector` | — | CSS selector must appear |
| `routes[].waitForUrl` | — | RegExp string for `page.waitForURL` |

## Studio QA gate

`run_qa_gate.py` runs `npm run smoke` when `docs/smoke-routes.json` exists and gate level ≥ 5.
