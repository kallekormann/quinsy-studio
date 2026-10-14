# The product loop

This is the loop that builds one product. Its reason is simple: a definition you signed should become software, and the agent should not stop to ask whether to continue.

| | |
|--|--|
| **Input** | A product definition in `intake/`, or a repository you already have. |
| **Output** | `projects/<name>/` with its own git: specs, code, tickets, and a ship you approved. |
| **You** | Sign the packets below. Say abort only to stop the ticket in flight. |
| **The agent** | Runs `./studio execute <project>`, does that one step, and runs it again until a packet needs you. |

Open a new chat for the product. Do not keep building in the ideation chat. In Cursor, bind that chat. See [Several products at once](03-several-products.md).

## Two ways in

**New product.** You say *"Bootstrap `<project>` and walk me through gate 0."* Bootstrap creates the product folder and the definition the gate checks. It also installs the UI kit peers (`radix-ui`, `class-variance-authority`, `clsx`, `tailwind-merge`, `lucide-react`, `@headlessui/react`) so the first screen does not fail on a missing import.

**Existing code.** You say *"Adopt `<project>` from this folder and reconstruct as-built."* Do not bootstrap a live tree. Adopt lays studio docs over the code. The agent fills `docs/as-built/` with real paths, then the same gates. Gate 2b maps the UI that exists. It does not invent a fake prototype. The long spec is [brownfield-adopt.md](../process/brownfield-adopt.md).

## The four gates

Sign them in order. `./studio approve <project> --gate 2` is refused. Sign 2a, then 2b.

| Gate | You are deciding | What you read |
|------|------------------|---------------|
| **0** | Is this the product? Problem, audience, scope. On an adopt, this is the as-built truth plus a synthesized definition. | The definition packet |
| **1** | Is this the architecture? Stack, data, vendors. A web app says `Payload: in`, or `Payload: out` with an ADR that opts out. | The architecture packet |
| **2a** | Is this the design direction? Identity, before any prototype. | Discovery plus `DESIGN.md` |
| **2b** | Is this the kit every later screen inherits? Tokens, base components, sticker of states. | The project kit |

To send one back: *"Revise gate N: …"* The agent runs `./studio revise`.

These are **human gates**. `./studio gate <project> --level 5` is a different system: automated checks (lint, types, tests, build, security) before a ticket can close. Level 5 is not gate 5 of the human sequence. There is no human gate 5.

After gate 1, the next execute writes `apps/web` when Payload is in. See [Foundation](13-foundation.md).

## After the gates

You sign the milestone roadmap (`./studio approve <project> --milestones`). The agent writes tickets for the active version only. When that version's tickets are done, you review the milestone before the next version starts. You can re-plan, re-order, or open a design sprint. The spec is [milestone-planning.md](../process/milestone-planning.md).

Then the train repeats. An empty phase is skipped. One unsigned ticket does not freeze a sibling that is ready.

1. **Design.** Team 10 writes a spec and an interactive mock: a route in the product app, with the real components, working handlers, and the motion the spec names. `./studio mock <project> <ticket>` prints the URL and the click-through. You open the running route. You sign the phase with `./studio approve-design <project> --phase`. To push one ticket back, reject it with a reason: `hierarchy`, `density`, `motion`, `copy`, `flow`, `uniqueness`, `a11y`, or `brand`. Commercial surfaces also load Team 11.
2. **Architecture.** The agent writes the note and signs the phase. You can veto if it cannot be built, or if you will not accept the approach. An infeasible design goes back to the next design cycle and stays out of implementation.
3. **Implementation.** The agent builds from the mock code. It does not wait for you to approve each ticket. Library first, then the project's tokens. Local migrations run as sprint work. You are told they ran.

Every few implementation phases the agent writes a cadence brief and keeps going. You reply later with `./studio feedback` or a note. Execute turns that into a backlog ticket (and asks one question per item if the note is too thin). Design tickets wait for the next design phase. They are not patched in the middle of a build.

Hygiene (lint, debt) is a sprint that sits outside this train. It does not count toward the cadence.

## What you stop for

| You stop | The agent runs and tells you |
|----------|------------------------------|
| Gates 0, 1, 2a, 2b | Local Docker, migrate, dev |
| Milestone roadmap and each milestone review | Architecture phase sign-off |
| Each design phase | Cadence briefs |
| Ship to production (`--to main --approve`) | Deploy, logs, status |
| A production migration or a destructive data step | A push to `dev` before the cadence brief |
| A tech veto, or abort | Reality check of the dev build |
| Every remaining ticket blocked after three failures | Closing a ticket that already has proof |

A blocked ticket alone is not a stop. Siblings continue.

## When a ticket is done

`./studio move <project> <ticket> done` commits the **product** repo only if all of these exist:

- A receipt whose result lines are PASS, FAIL, or NOT TESTED, with real paths.
- Automated gate level 5 green.
- A QA PASS from a context that did not write the code (`./studio qa`).
- On a ticket with signed mock shots, the finish gate (`./studio qa <project> <ticket> --finish`) at desktop and phone width.

Three red gates, QA fails, or finish holds, and the ticket goes `blocked` with an escalation packet.

## Two kinds of change after the gates

**A small note.** *"Feedback: …"* Execute clarifies and tickets it. It waits for the right phase. If a fact is missing, you answer one question per item.

**A change of direction.** Drop a brief in `intake/amendments/<project>/` and ask the agent to run amendment intake. You get an analysis (vision, requirements, architecture, a roadmap, ticket drafts). Nothing is built until you approve the amendment. If the roadmap changed, you sign milestones again. The spec is [amendment-intake.md](../process/amendment-intake.md).

## Words, if you want them in one list

[What you say](15-what-you-say.md).
