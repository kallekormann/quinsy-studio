# Differential demo — contrast core pair

## Pair

| Role         | System id      | Path                             |
| ------------ | -------------- | -------------------------------- |
| Default / A  | `soft-ui`      | `systems/soft-ui/Design.md`      |
| Contrast / B | `brutalist-ui` | `systems/brutalist-ui/Design.md` |

Same moodboard Style DNA × two grammars proves the interpreter.

## Non-goal

Neither core restyles the product's own chrome or tokens. The pair is generation-only.

## Operator check

```bash
cd projects/<project>
npx vitest run packages/design-md-repo/parse.test.ts packages/design-md-repo/compile-cores.test.ts
```

Both cores must `validateDesignMd` + `parseDesignMdToLayoutParams` green.
