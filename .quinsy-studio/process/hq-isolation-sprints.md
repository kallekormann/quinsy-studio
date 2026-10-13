# Studio HQ isolation epic — sprint plan

> Pause **product** `./studio execute` until these four HQ sprints are `done`.
> Then resume `./studio focus <p> && ./studio execute <p>` with secrets, Docker, and parallel-safe HQ.

**Not a product milestone.** Tickets are `LO-*` in `.quinsy-studio/backlog/open/`.
**HITL:** env/Docker architecture is this document + per-ticket AC (no UX mocks). UX sign-off stays on **product** design-track packets.

**How to run**

1. This chat stays `studio_meta` (do not queue on a product sprint inbox).
2. Implement one LO at a time: code + tests + `.quinsy-studio/CHANGELOG.md` → move LO to `backlog/done/`.
3. Do not open a product IMPLEMENT until **HQ-ISO-04** is complete (or you explicitly abort the epic).
4. Product agents must **INFORM** open LO counts; they must not steal the session for `STUDIO_LO` (that behavior is HQ-ISO-03).

**Capacity target:** ≥5 concurrent client chats. **Docker:** required (tell the human to install if missing).

---

## Sprint HQ-ISO-01 — Secrets and Docker inject

Ship first. Product agents must not Read env **values**; migrate/dev only after `--approve`, inside Compose.

| ID | Estimate | Title |
|----|----------|--------|
| LO-0314 | M | Secret values must live outside agent-readable trees; schema files list names only | **done** |
| LO-0315 | L | `./studio env` must inject named variables into Docker only after HITL `--approve` | **done** |
| LO-0316 | M | Gate, migrate, and product boot must require Docker and must not print secret values | **done** |

## Sprint HQ-ISO-02 — HQ write integrity

Safe for five harvest/train/promote writers.

| ID | Estimate | Title |
|----|----------|--------|
| LO-0317 | S | Studio HQ pre-commit must refuse `projects/` in the studio index | **done** |
| LO-0318 | M | Infusion and learn commits must abort on product nouns and serialize HQ JSON with a lock | **done** |
| LO-0319 | S | Abstraction verify must scan every real project folder name, not one hardcoded product | **done** |

## Sprint HQ-ISO-03 — Execute loop (product vs HQ)

| ID | Estimate | Title |
|----|----------|--------|
| LO-0320 | S | Every execute CARD must re-inject a short constitution (worlds, secrets, HITL packets) | **done** |
| LO-0321 | S | Product execute must INFORM open HQ learning counts and must not switch to STUDIO_LO mid-project | **done** |
| LO-0322 | S | `approve --gate N` must refuse unless gate N-1 is already approved | **done** |
| LO-0323 | S | HITL copy must point at design/arch/env packets; must not invent a morning-brief UX | **done** |

## Sprint HQ-ISO-04 — Five concurrent products

| ID | Estimate | Title |
|----|----------|--------|
| LO-0324 | M | Studio settings must cap concurrent executes and queue the rest | **done** |
| LO-0325 | M | Focus must not clobber another live chat’s isolation; one product tree per session | **done** |
| LO-0326 | S | GETTING_STARTED / AGENTS must state Docker-required, one-chat-per-product, HQ train in a separate session | **done** |

**After HQ-ISO-04:** product work resumes in a **product** chat (`./studio focus <p> && ./studio execute <p>`). Open a **separate** HQ chat only when INFORM reports learning tickets.

---

## Out of scope (later)

- Same-window parallel agents (one chat per product inside one Cursor root). Specified in [hq-session-binding.md](hq-session-binding.md) (`LO-0419`–`LO-0424`). Until that epic is done, this document's rule stands: one isolation surface per workspace.
- Full compose lifecycle (spin down on idle).
- Moving the Cursor IDE itself into Docker.
- Morning-brief dashboards.
- Reading `.env` values “just for migrate” without `--approve`.
