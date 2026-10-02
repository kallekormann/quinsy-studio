# skeleton

**Atomic level:** Atom (`ui-atom`)

Themable shadcn-style control. Classes use semantic tokens (`bg-primary`, `text-muted-foreground`, `border-input`, …) mapped in `ui/tokens/design-tokens.css`.

**Peers:** none beyond React + Tailwind tokens

Pull: `./studio library pull <project> skeleton`

Motion: uses the studio `--motion-*` tokens (duration, easing, and scale). Do not add a second duration or fade. `motion: off` is a project token override, not a fork of this file.
