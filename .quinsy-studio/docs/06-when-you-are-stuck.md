# When you are stuck

The agent is supposed to stop only for the rows below. If it asks "should I continue?" mid-build, tell it to run `./studio execute <project>` again.

## It is waiting for you

| It says | You do |
|---------|--------|
| Gate 0, 1, 2a, or 2b | Read the packet. `./studio approve <project> --gate N`, or say what is wrong. |
| Milestone roadmap or milestone review | Read `docs/phases/` in the product. Approve, or say what to re-plan. |
| Design phase | Open the mock URL from `./studio mock`. Sign `./studio approve-design <project> --phase`, or reject one ticket with a reason code. |
| Ship to main | `./studio ship <project> --to main --approve` when you want production. |
| Production migrate, or delete data | Add `--approve` only if you mean it. |
| Tech veto | You decide. The agent does not ship that approach until you say so. |

## It is not waiting

| It says | Meaning |
|---------|---------|
| INFORM | It did the step and is going on. Local Docker, an architecture sign-off, a cadence brief, a deploy. |
| EXECUTE QUEUED | Five products are already running. Release one, or wait. |
| SESSION_BOUND | This chat is bound to a different product. Open another chat. |
| CROSS_PROJECT | The sentence named another product. Stay here, or bind a new chat. |
| cost-cap | The chat is full. Raise the named key. Do not paste the repo in. |

## The usual fixes

**Wrong product in this chat.** In Cursor: "Bind this chat to `<project>`." Then "Show what this chat is bound to." In Claude Code or a CLI: `./studio focus <project>` in that session only, and do not focus a second product in the same window.

**Two chats keep hiding each other's files.** They are both using focus. Bind each Cursor chat instead. Read [Several products at once](03-several-products.md).

**Design looks like pictures only.** The mock has to be a route you can click. `./studio mock <project> <ticket>` fails until the handlers, the states, and the click-through script exist. You review the running page.

**A lesson mentions a client name.** It stays in the product. Only a generic rule is infused into the studio.

**You want the long version.** [Getting Started](../GETTING_STARTED.md) is the script. [Operations manual](../README.md) is every flag. This folder is the map.
