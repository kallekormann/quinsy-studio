# The path

Four doors. You only walk through the ones that match what you already have.

```
Direction  →  Ideation  →  you say yes  →  Intake
Intake     →  Bootstrap →  gates        →  Product
Existing code → Adopt   →  same gates   →  Product
A lesson in the product → separate chat →  Studio learning
```

## 1. Ideation

Open a chat. Say what you want to look into. Do not say "execute".

The desk researches and writes a case under `ideation/`. If several ideas remain, it asks which one. If one remains, it asks whether that case should become the product definition.

You say yes, or you reject or park it. Yes is the only step that writes the intake the next door can use.

Details: [The three loops](02-three-loops.md).

## 2. Intake and bootstrap

The product definition lives in `intake/` (a file or a folder of notes). That folder is local.

Say: *"Bootstrap `<project>` and walk me through gate 0."*

The agent creates `projects/<project>/` with its own git and fills the definition the gate checks. You read it. You sign gate 0 when it is the product you meant:

```bash
./studio approve <project> --gate 0
```

If the code already exists, skip bootstrap. Say: *"Adopt `<project>` from this folder and reconstruct as-built."* Then the same gates.

## 3. The product

Sign the gates in order. `approve --gate 2` is refused. Sign 2a, then 2b.

| Gate | You are signing | Command |
|------|-----------------|---------|
| 0 | The product definition | `./studio approve <project> --gate 0` |
| 1 | The architecture. A web app says Payload in, or an ADR that opts out | `./studio approve <project> --gate 1` |
| 2a | The design direction. No prototype yet | `./studio approve <project> --gate 2a` |
| 2b | The project kit: tokens and the base components | `./studio approve <project> --gate 2b` |

After gate 1, the next execute writes `apps/web` when Payload is in.

After gate 2b the agent plans milestones. You sign the roadmap (`./studio approve <project> --milestones`). Then the train repeats:

1. **Design.** The agent writes a spec and an interactive mock in the product app. You open the running route, not a folder of screenshots. `./studio mock <project> <ticket>` prints the address and the click-through script. You sign the phase with `./studio approve-design <project> --phase`. To push one ticket back: `./studio approve-design <project> <ticket> --reject --reason <code>`.
2. **Architecture.** The agent writes the note and signs it. You can veto.
3. **Implementation.** The agent builds from the mock code, not from the screenshots. You are not asked to approve each ticket. When a milestone is finished you review it before the next version starts.

Every few implementation phases the agent writes a cadence brief and keeps going. You reply later with `./studio feedback` if something should change. Design feedback waits for the next design phase. It is not patched in the middle of a build.

**Ship.** `./studio ship <project> --to dev` is the agent, before the cadence brief. Production is you: `./studio ship <project> --to main --approve`. That refuses if the production readiness check fails.

**Production access.** You fill names in `projects/<project>/.env.local`. `./studio env <project> prod --explain` tells you which names. The agent can deploy, read logs, and check status. A production migration waits for `--approve`.

Open a **new chat** for the product if the previous chat was ideation. In Cursor, bind that chat. See [Several products at once](03-several-products.md).

Say *"Execute `<project>`. Back on track."* when you return.

## 4. Learning and studio update

When a ticket teaches a rule another product would need, the product chat records it and tells you. It does not stop building to rewrite the studio.

In a **separate** chat, the agent infuses the lesson into a playbook or skill (`./studio train`). You commit that studio change. The learning ticket stays on your machine.

Do not do this in the product chat while a ticket is in progress. The product chat's job is the product.

## What you say, in one list

| Situation | What you say |
|-----------|----------------|
| New direction | "Look into …" |
| The case is the one | "Yes, write the PRD." |
| Start the product | "Bootstrap `<project>` and walk me through gate 0." |
| Code already exists | "Adopt `<project>` from this folder." |
| Return to a product | "Execute `<project>`. Back on track." |
| Cursor, this chat owns the product | "Bind this chat to `<project>`." |
| A small note mid-build | Say it. The agent queues it and continues. |
| Stop the current ticket | "Abort." |
| Change of direction after the gates | Put a brief in `intake/amendments/<project>/` and ask the agent to amend. |
