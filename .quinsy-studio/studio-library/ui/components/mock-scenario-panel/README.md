# mock-scenario-panel

Dev-only scenario harness for design mocks. Every design-track mock route in
`app/(design-mocks)/design-mocks/<TICKET>/` must make its scenario states
(empty / loading / error, open / closed, long-content) reachable in the running
prototype — this panel is the standard way.

- Floating panel of state buttons; active state lives in `?state=` so the human
  clicks through **and** Playwright captures each state by URL
  (`…/design-mocks/<TICKET>/?state=empty`).
- `useMockScenario()` hook keeps component state and the URL in sync without a
  framework-specific router import.
- Styled with project tokens (`bg-background`, `text-muted-foreground`, …).

```tsx
'use client'
import { MockScenarioPanel, useMockScenario } from '@/components/mock-scenario-panel'

export default function MockPage() {
  const [state, setState] = useMockScenario()
  return (
    <>
      <RealView data-state={state} loading={state === 'loading'} items={state === 'empty' ? [] : demoItems} />
      <MockScenarioPanel ticketId="T-0042" scenarios={['rest', 'empty', 'loading', 'error']} value={state} onValueChange={setState} />
    </>
  )
}
```

Never ship outside the `(design-mocks)` route group — the group layout already
404s in production.
