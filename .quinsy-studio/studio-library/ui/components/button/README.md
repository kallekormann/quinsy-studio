# Button

Generic token-based button. Uses `primary-*` and `neutral-*` Tailwind classes mapped to studio CSS variables.

Variants: `primary` | `secondary` | `outline` | `ghost` | `link` | `destructive`  
Sizes: `sm` | `md` | `lg`

Projects remap brand by overriding `--color-primary-*` in local `ui/tokens/design-tokens.css`.

## Icon-only chrome (LO-0187 / LO-0190)

Icon-only toolbar controls should use **outline / ghost / secondary (dimmed)** variants that follow light/dark tokens — not a bright soft wash or solid white disc. Reserve `primary` for the main call-to-action on the surface.
