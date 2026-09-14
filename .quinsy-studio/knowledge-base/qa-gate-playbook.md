# QA gate playbook (FE-006 + QA level 5)

> QA is a **gate**, not Team 12. Human HITL stays on gates 0–2, `approve-design`, UI sprint review, legal/security/destructive ops.

## Do

- Run `./studio gate <project> --level 5` before `move … done` (build + tests + smoke). Level 2 lint-only is not done.
- Receipt records **Plan**, **AC coverage**, and **default-flow** (happy path the human will click). UI tickets: browser or documented substitute.
- Cover empty / loading / error when the ticket touches a surface that can be empty or fail.
- Smoke the RUNBOOK URL, not a guessed port.

## Don’t

- Invent a QA department or extra ticket ACK.
- Treat green unit tests as proof the operator click works (LO-0155).
- Skip migrate then call the API broken (LO-0227).

## Implement-fail

| Fail | Why |
|------|------|
| No execution receipt default-flow | `move … done` must refuse |
| UI changed, no browser/API proof | Appearance screenshot ≠ behavior |
| Pending schema, 500 treated as product bug | Migrate first |
| Design-track shipped without approved spec | Stay on Team 10 packet |

See [`process/gates.md`](../process/gates.md) and [`process/human-in-the-loop.md`](../process/human-in-the-loop.md).
