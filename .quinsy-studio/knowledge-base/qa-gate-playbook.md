# QA gate playbook (FE-006 + QA level 5)

> QA is a **gate**, not Team 12. Human HITL stays on gates 0–2, `approve-design`, UI sprint review, legal/security/destructive ops.

## Do

- **PB-20260915-002** helpful=15 harmful=0 :: npm_audit @vitest/mocker (moderate path-traversal advisory on the test mocker) is a documented gate-5 soft fail. Record it on the receipt; do not treat it as a done-blocker when RESULT is True.
- **PB-20260915-001** helpful=3 harmful=0 :: Before MOVE_DONE, run the same Prettier check the gate uses on the product tree. Named constants for 100/1000 must sit on an assignment after equals (anti-slop); do not stack two numeric const lines (redundant-variables).
- Run `./studio gate <project> --level 5` before `move … done` (build + tests + smoke). Level 2 lint-only is not done.
- Receipt records **Plan**, **AC coverage**, and **default-flow** (happy path the human will click). UI tickets: browser or documented substitute.
- Cover empty / loading / error when the ticket touches a surface that can be empty or fail.
- Smoke the RUNBOOK URL, not a guessed port.
- Playwright locators: **role / name**, not CSS soup (FE-006).
- Gate 5 **soft-warns** token `#hex` / `rgb()` and native `<select>` in product `app/`/`src/` (`studio_skill_checks.py`). Allowlist: `tokens`, tests, fixtures, studio-library primitives.

## Don’t

- Invent a QA department or extra ticket ACK.
- Treat green unit tests as proof the operator click works (LO-0155).
- Treat a hung loading surface as browser proof of list chrome (LO-0276, LO-0291). If the live list never left loading, record the hang and cite HTTP/API tests (curl, PHPUnit, Vitest) — do not claim a click-through.
- Skip migrate then call the API broken (LO-0227).

## Implement-fail

| Fail | Why |
|------|------|
| No execution receipt default-flow | `move … done` must refuse |
| UI changed, no browser/API proof | Appearance screenshot ≠ behavior |
| Pending schema, 500 treated as product bug | Migrate first |
| Design-track shipped without approved spec | Stay on Team 10 packet |

See [`process/gates.md`](../process/gates.md) and [`process/human-in-the-loop.md`](../process/human-in-the-loop.md).

## Deltas

- **PB-20261013-001** helpful=0 harmful=0 :: assumed: A source test that the copy or class name exists is enough for an acceptance criterion. signed: An AC on interactive UI passes only when a test asserts the handler or module the user actually hits. next: Independent QA must pass an AC only when a test asserts the handler the user triggers, never a copy string alone.
- **PB-20260916-003** helpful=0 harmful=0 :: When host-scoped live chrome never leaves loading, default-flow proof is HTTP/API tests (curl, PHPUnit, Vitest) plus a recorded hang — not a click-through screenshot.
- **PB-20260916-002** helpful=0 harmful=0 :: Default-flow proof for a host-scoped operator page is not a screenshot of Select a host. If host scope never left all, cite API or tests and record the hang — same class as a hung loading list.
- **PB-20260916-001** helpful=0 harmful=0 :: Gold-path coverage includes the operator-authorized approve or publish path when the autonomous exploration cap is already exhausted. A cap that pauses unattended jobs is not the only test of the operator go.
