# The three loops

The studio runs three loops. They do not share a backlog, and a chat should stay in one of them.

```
Ideation desk          Product                 Studio learning
ideation/              projects/<name>/        .quinsy-studio/
"Is this worth it?"    "Build this product."   "Teach the studio."
```

A sentence can move from one loop to the next only at a named door: you say yes and that writes the product definition, or a finished ticket produces a lesson that is generic enough to keep.

## 1. Ideation — decide whether to build

**Use it when** you have a direction and no product yet. A trade, a job, a frustration. Not a ticket list.

**What it does.** The desk looks at real complaints and existing products, then writes a case: who hurts, what they do today, what a first version would be. Medicine and clinical care are out of reach. Other trades stay in reach. One person, with agents for code and design, ships the first version in about two months. Later ideas stay in the case. They are not built yet.

**What it does not do.** It does not open a sprint. It does not run `./studio execute`. It does not write the product definition until you say yes.

**Where the files go.** `ideation/`. That folder is local. It is not in studio git.

**When you are done.** You say yes. That writes the intake the product loop can bootstrap. Or you reject or park the case.

Stay in the ideation chat for the research. Open a **new** chat when the product exists.

## 2. The product — build one product

**Use it when** a product definition exists (`intake/`) or the code already exists and you adopt it.

**What it does.** Gates, then a repeating train: design, architecture, implementation. The agent runs `./studio execute <project>` and does the one next step until it must stop for you.

**You stop for:** the product definition (gate 0), the architecture (gate 1), the design direction (gate 2a), the project kit (gate 2b), each milestone roadmap and milestone review, each design phase, shipping to production, a production database migration or a destructive data step, and a tech veto. You do not approve every ticket.

**The agent runs and tells you:** local Docker, architecture sign-off inside a phase, cadence briefs, deploys and logs.

**Where the files go.** `projects/<name>/`, in that product's own git. Design specs, code, tickets, and ops logs live there.

**One chat, one product.** A second product gets its own chat. See [Several products at once](03-several-products.md).

## 3. Studio learning — make the next product easier

**Use it when** a ticket taught something that would help a different product. A rule, a trap, a better default.

**What it does.** The lesson is written in generic language (no client name, no one-off ticket id) and infused into a playbook, a skill, or the learnings catalog. That infusion is committed in the studio repo. The learning ticket itself stays local.

**What it does not do.** It does not pause the product. The product chat keeps building. Learning runs in a **separate** chat, or the product chat only records the lesson and tells you the count.

**Where the files go.** The durable text is under `.quinsy-studio/knowledge-base/`. The open learning tickets are under `.quinsy-studio/backlog/` and are not pushed as the lesson itself.

## Which chat am I in?

| You said | Loop |
|----------|------|
| "Look into …" / "ideate" | Ideation |
| "Execute <project>" / "back on track" | Product |
| "LO-…" / "quinsy-studio process" / this manual | Studio learning or studio docs |

If a product chat is mid-ticket and you type a side note, the agent queues it and keeps the current step. It does not drop the ticket to start your note. Say abort only when you mean stop that ticket.
