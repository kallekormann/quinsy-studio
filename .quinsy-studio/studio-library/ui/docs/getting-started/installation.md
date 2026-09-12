# Installation

## 0. Studio HQ (after git clone)

From the **quinsy-studio** repo root:

```bash
./studio install
```

Installs into `node_modules/` (gitignored):

- `tailwindcss` + `@tailwindcss/vite` — [Tailwind CSS v4](https://tailwindcss.com/docs/)
- `@headlessui/react` — [Headless UI](https://headlessui.com)

Optional external skill packages (large download):

```bash
./studio install --with-skills
```

Requires **Node.js 20+**. Lockfile: `package-lock.json` (committed).

## 1. Tailwind CSS v4 (projects)

Follow [Tailwind installation](https://tailwindcss.com/docs/installation) for your framework (Vite, Next.js, etc.).

Minimum for Quinsy projects:

```bash
npm install tailwindcss @tailwindcss/vite
```

Import in your CSS:

```css
@import "tailwindcss";
```

Pull studio tokens:

```bash
./studio library pull <project> tokens
```

Wire `ui/tokens/tailwind.preset.ts` into your Tailwind config so `primary-*`, `surface`, `neutral-*` resolve to project brand CSS variables.

## 2. Headless UI (projects)

Required when pulling **primitives** or Headless molecules (`dialog-shell`, `search-command`, `dropdown` Listbox, `segmented-toggle`):

```bash
npm install @headlessui/react
```

Peer dependency documented on every primitive README.

## 2b. shadcn-style kit (mandatory on project setup)

Every new project (`./studio init` / `bootstrap` / `design`) and every **adopt** overlay gets `docs/setup/ui-kit.md`. The design-prototype `package.json` already lists these. On `./studio library pull` of UI, they are merged into the live app `package.json` if missing.

**Do not wait until a component import fails.** Install in the React app:

```bash
npm install radix-ui class-variance-authority clsx tailwind-merge lucide-react
npm install @headlessui/react
```

Optional, per component README: `cmdk`, `vaul`, `@base-ui/react`, `input-otp`, `react-day-picker`, `recharts`, `embla-carousel-react`, `react-resizable-panels`, `sonner`.

Theme: import pulled `ui/tokens/design-tokens.css` (includes `--primary` / `--background` aliases). See [shadcn-coverage.md](../shadcn-coverage.md).

## 3. Pull components

```bash
./studio library list
./studio library suggest <project> "settings modal form"
./studio library pull <project> button input dialog card dropdown-menu
```

## 4. Sticker sheet

After gate 2, validate components in `design/prototype/app/sticker-sheet/`.

## Reference

- Studio UI catalog: [ui/docs/README.md](../README.md)
- Tailwind utilities: [tailwindcss.com/docs](https://tailwindcss.com/docs/)
