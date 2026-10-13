# backend / queues

Portable studio principles (not project incidents).
Matching playbook/skill: `knowledge-base/backend_playbook.md`.

## Principles

- **LO-0376** 2026-10-04 :: A test that re-queues ready files must restore them when a check fails
  - A test that marks ready work as queued must put that work back when an assertion throws. Restore in a finally, not after the assertion.
- **LO-0371** 2026-10-03 :: Requeue tests stay on the rows they created
  - A job that requeues existing work is tested on the rows that test created. Restore any other rows the test marked queued before the test reads them.
- **PB-20260925-001** helpful=0 harmful=0 :: Do not enqueue HQ skill-catalog work on the product sprint inbox. Route it to the studio LO and train queue. Product execute INFORM the open HQ LO count. Infuse those jobs in a HQ session; STUDIO_LO only when the product loop is idle.
- **LO-0341** 2026-09-25 :: HQ skill-catalog work stays on the studio LO/train queue
  - See **PB-20260925-001**. Do not enqueue HQ notes on the product sprint inbox. Product execute INFORM the open HQ LO count; infuse in HQ when idle.
- **LO-0303** 2026-09-16 :: Dead image URLs should queue public-photo research in the same gold path as pers
  - Dead image URLs should queue public-photo research in the same gold path as pers
