# Differential demo — contrast core pair (MOOD-0263)

## Pair

| Role         | System id      | Path                             |
| ------------ | -------------- | -------------------------------- |
| Default / A  | `moody-bloom`  | `systems/moody-bloom/Design.md`  |
| Contrast / B | `brutalist-ui` | `systems/brutalist-ui/Design.md` |

Same moodboard Style DNA × two grammars proves the interpreter (AM-008).

## Non-goal

Brutalist does **not** restyle Moody product chrome or tokens. Pair is generation-only.

## Operator check

```bash
cd projects/moody
npx vitest run packages/design-md-repo/parse.test.ts packages/design-md-repo/compile-cores.test.ts
```

Both cores must `validateDesignMd` + `parseDesignMdToLayoutParams` green.
