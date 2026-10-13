# Skill: Frontend Testing (FE-006)

> Tests that prove the shipped behavior and do not flake. Unit tests where the logic lives, a few Playwright journeys where the integration is the risk, and evidence on the receipt that a reviewer can open. Trophy shape: many unit and API tests, fewer e2e. Receipt default-flow is the human proof. A UI change with no browser or API proof is not done.

## Metadata

```
skill_id: FE-006
name: Frontend Testing
team: 01-frontend-experience
lead_role: QA Specialist
support_roles: [Frontend Architect]
phases: [4, 5]
activation_triggers:
  - Ticket contains "Test", "Testing", "Coverage", "Unit-Test", "E2E", "Playwright"
  - Any UI ticket before MOVE_DONE (receipt evidence)
  - Gate 5 red on tests or smoke routes
pairs_with: [FE-004, FE-003, UX-009, SO-005]
```

## When to load

- Every UI or user-facing ticket in an implementation phase.
- When a test flakes, or gate 5 fails on tests or smoke.
- When adding `docs/smoke-routes.json` for a web app.

## Rules

### 1. Put the test where the logic lives

Pure functions, formatters, price math, access rules and hooks get Vitest unit tests. Payload access functions and hooks get tests against the Local API or a test database in Compose. Use a browser only when the integration itself is the risk: auth, the core job, checkout, a form that persists. If a unit or API test can prove it, it does not belong in Playwright.

### 2. Select like a user

Use `getByRole`, `getByLabel`, `getByText` and `getByPlaceholder` first. `getByTestId` is the escape hatch when semantics cannot reach the element. No CSS chains, no `nth-child`, no generated class names. A role selector that cannot find a control often means FE-004 is broken too.

### 3. No fixed sleeps

Never `page.waitForTimeout()` and never a `setTimeout` wait in a test. Wait on a condition: a web-first assertion (`await expect(locator).toBeVisible()`), a URL (`toHaveURL`), or a response (`page.waitForResponse`). Use `page.clock` for time-dependent flows.

### 4. Each test owns its data

Create what the test needs through Payload's REST API or a seed script in the Compose app container. Never through the admin UI, and never by relying on "the seed user" or another test's leftovers. Give records unique names per worker so parallel runs do not collide. Clean up, or use a throwaway database.

### 5. Set up through the API, assert through the UI

Log in once per worker with `POST /api/users/login` (or the project's auth collection) and save `storageState`. Test the login form once, in its own test. Every other test starts signed in.

### 6. Failures are debuggable from artifacts

`playwright.config.ts` sets `trace: 'retain-on-failure'`, `screenshot: 'only-on-failure'` and `forbidOnly: !!process.env.CI`. A failing run leaves a trace in `test-results/`. "Could not reproduce" without a trace is a tooling gap.

### 7. Retries measure flakiness; they do not fix it

Keep `retries: 0` on the blocking suite. A test that passes only on retry is flaky and not done. Run a new or changed test with `--repeat-each=10` before the receipt. Fix the root cause: a race, shared data, an animation, a third-party script. Block third-party routes with `page.route` when they slow or break loading.

### 8. Prove behavior, not appearance

A screenshot of a filled form does not prove it was saved. Assert the response status, then reload and assert the persisted value. Cover empty, loading and error when the surface can be empty or fail.

### 9. Smoke the real URL

`docs/smoke-routes.json` lists the routes gate 5 opens. Use the URL from the runbook, not a guessed port. A missing smoke file or `QUINSY_SKIP_SMOKE` is NOT TESTED, not a pass.

### 10. Planned gate check: `e2e_hygiene`

The gate will scan e2e files for `waitForTimeout`, `test.only`, CSS-chain and `nth-child` selectors, and a missing `trace` setting. Write tests that pass it now.

## Workflow

1. Map each AC to the lowest test level that proves it. Write the map in the receipt `## AC coverage`.
2. Write unit and API tests first. Run them.
3. Add or extend one Playwright test for the default flow when the ticket touches a journey.
4. Seed data through the API. Reuse the worker login fixture.
5. Run the new tests with `--repeat-each=10`. Fix any flake at the root.
6. Run `./studio gate <p> --level 5`.
7. Fill the receipt `## Default flow` and `## Evidence`.

Example:

```typescript
import { test, expect } from './fixtures';

test('owner renames a project', async ({ page, api }) => {
  const project = await api.create('projects', { name: `p-${test.info().workerIndex}` });
  await page.goto(`/projects/${project.id}/settings`);
  await page.getByLabel('Project name').fill('Renamed');
  const saved = page.waitForResponse((r) => r.url().includes(`/api/projects/${project.id}`) && r.ok());
  await page.getByRole('button', { name: 'Save' }).click();
  await saved;
  await page.reload();
  await expect(page.getByLabel('Project name')).toHaveValue('Renamed');
});
```

## Deliverables

- Unit and API tests next to the logic they cover.
- Playwright specs in the app's e2e folder, using the shared fixtures (`api`, worker `storageState`).
- `playwright.config.ts` with trace and screenshot on failure, `retries: 0`, `forbidOnly` in CI.
- `docs/smoke-routes.json` for every web app.

## Done evidence (receipt)

```markdown
## AC coverage
- AC1 rename persists → e2e `projects/rename.spec.ts` · PASS
- AC2 empty name refused → unit `validateName.test.ts` · PASS

## Default flow
- /projects/:id/settings → change name → Save → reload shows new name
- Screenshot: sprints/SPRINT-NN/evidence/<TICKET>/rename-1440.png

## Evidence
- `pnpm test` · PASS
- `npx playwright test projects/rename.spec.ts --repeat-each=10` · PASS (10/10)
- Smoke routes · PASS | NOT TESTED (reason)
- Trace on failure: none | test-results/<path>/trace.zip
```

Results are PASS, FAIL or NOT TESTED. Every path must exist.

## Anti-patterns

- `waitForTimeout` to "let it settle".
- Logging in through the form in every test.
- Tests that pass alone and fail in parallel because they share a record.
- Turning on retries to make the suite green.
- 40 browser tests for a validation matrix a unit test covers.
- Green unit tests offered as proof that the click works.
- Deleting a flaky test without finding the cause.

## Handoff

- **To QA_REVIEW:** the receipt `## AC coverage` and `## Evidence` with paths.
- **To UX-009:** the shipped route is stable enough to capture every state.
- **To SO-005:** the default-flow test runs against the dev URL with a base-URL switch.

## References

- [qa-gate-playbook.md](../../../knowledge-base/qa-gate-playbook.md)
- [frontend_playbook.md](../../../knowledge-base/frontend_playbook.md)
- [payload-playbook.md](../../../knowledge-base/payload-playbook.md) — auth collection, Local API
- [Playwright best practices](https://playwright.dev/docs/best-practices)
- Source: msitarzewski/agency-agents `testing/testing-test-automation-engineer.md`, `testing/testing-evidence-collector.md` (MIT)
