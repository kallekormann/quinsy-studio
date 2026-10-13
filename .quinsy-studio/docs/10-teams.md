# Teams

The studio staffs work the way a product manager would. Every ticket names an owner skill first, then companions from other teams, with the reason written under Staffing. `./studio groom` refuses a sprint when a ticket has no skills, an unknown skill, or a missing companion.

You do not pick the team in chat. The ticket content does. Trigger words find the owner. The staffing rules add the companions: security and an AI security check on auth, privacy on personal data, accessibility and tests on UI, secrets when keys are involved, payments when money moves, marketing law when email or commercial claims go out. Waive a companion only with a written reason.

Skills are the team members. Each one is a file the agent reads before it codes. The full list is [Skills](11-skills.md). The index the tools use is [skill-registry.md](../teams/skill-registry.md).

## Why these eleven

| Team | Why it is on the ticket |
|------|-------------------------|
| [01 Frontend](../teams/01-frontend-experience/README.md) | The screens people use: components, tokens, performance, accessibility, tests. |
| [02 Backend](../teams/02-backend-systems/README.md) | Data, APIs, auth, Payload, payments, jobs, documents. |
| [03 Compliance](../teams/03-compliance-legal/README.md) | Privacy, cookies, terms, and data minimization, so a product can ship where those rules apply. |
| [04 Strategy](../teams/04-product-strategy-architecture/README.md) | What to build, which stack, and whether it is feasible. Gates 0 and 1 live here. |
| [05 Growth](../teams/05-growth-marketing-content/README.md) | How people find the product and what the words say: search, content, launch, email, positioning. |
| [06 Product management](../teams/06-product-management-operating-model/README.md) | Staffs every ticket. Also research, roadmap, and how the team is shaped. |
| [07 AI](../teams/07-ai-autonomous-systems/README.md) | When the product calls a model, and the check that generated code is not slop. |
| [08 Platform](../teams/08-platform-enterprise-engineering/README.md) | Docker, deploy, security, secrets, monitoring, incidents. |
| [09 Studio operations](../teams/09-studio-operations-evolution/README.md) | The studio itself: tools, process, learning, docs, and the release reality check. |
| [10 Product design](../teams/10-product-design-experience/README.md) | The experience before code: flows, IA, visual design, brand, and the finish gate against the mock. |
| [11 Growth design](../teams/11-growth-design/README.md) | Commercial surfaces and experiments. Paired with Team 10. The ticket stays on team 10. |

Team 10 writes design. Team 01 builds it. Team 11 is added when the surface is commercial (landing, pricing, checkout, catalog, product page). Team 06 is on every ticket because staffing is the job, not an optional review.

## What a skill file is

A skill has an id (`FE-001`, `BE-007`, `UX-002`), the situations that load it, the rules, and the anti-patterns. The execute card lists the files. The agent reads those files, not a summary from memory.

External skill packages can be installed with `./studio install --with-skills`. They are reference. Internal skills and the anti-slop rules stay in charge. Extensions in `knowledge-base/skill-extensions/` deepen a skill. They do not add a new id.

New behavior for a component goes into the studio library first, then a product pulls it. See [Library](12-library.md).
