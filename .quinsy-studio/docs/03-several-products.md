# Several products at once

You can have many products under `projects/`. Each one has its own git. The studio repo does not contain them.

The hard part is the editor, not git. One Cursor window has one ignore list. If two chats both run "focus this product", the second chat hides the first product from every chat. Session binding fixes that **in Cursor only**.

## The rule

**One chat, one product.** Do not ask one chat to build two products.

| How you work | What to do |
|--------------|------------|
| Cursor, and HQ `runtime` is `cursor` | In each chat, bind that chat to its product. See below. |
| Claude Code, Gemini, or a terminal agent | Leave `runtime` as something other than `cursor`, or accept one focused product at a time. `./studio focus <project>` picks the product and hides the others. A second product is a second window, or you wait until the first chat has stopped. |
| You, in your own terminal | You can `git -C projects/<name>` any product. Binding is only for agent chats. |

Up to five products can be in `./studio execute` at once. A sixth waits until one reaches a human stop or you release it: `./studio execute <project> --release`.

## Bind a Cursor chat

You do **not** look up an id. Cursor does not show it in the sidebar. The chat already has it. The studio's hook copies it onto the command when the **agent** runs the command.

In the chat that should own the product, say:

> Bind this chat to `<project>`.

The agent runs:

```bash
./studio bind <project>
```

It does not type `--session`. The hook adds `--session <this-chat>` before the command runs. Later `./studio execute`, `guard`, and `focus` in that same chat get the same id the same way.

Confirm, still in that chat:

> Show what this chat is bound to.

The agent runs `./studio bind --show`. You should see the project name. `(unbound)` means the hook did not add the id, or this chat has not bound yet.

Then say:

> Execute `<project>`.

A bound execute does not rewrite the ignore list, so the other chat keeps its product.

## What you should not do

- Do not paste `./studio bind <project>` into a terminal you opened yourself. Your terminal is not the chat, so it has no chat id, and bind refuses.
- Do not copy an id from another chat. Each chat has its own.
- Do not `./studio focus <other-product>` inside a chat that is already bound. That chat stays on its product. Open another chat and bind that one.
- Do not set `runtime: cursor` and then expect Claude Code to bind. Claude Code never runs the Cursor hooks. It keeps workspace focus.

## What the first bind changes

The first successful bind stops hiding every other product in the ignore list. Hiding was one list for the whole window, which is what made chats fight. After that, the hooks refuse a bound chat that tries to read or `git` a different product. Studio files (`.quinsy-studio/`, this manual) stay readable.

Until a chat is bound, it still follows the last `./studio focus`. Bind it before you run a second product in the same window.

## If bind says it refused

| Message | Meaning |
|---------|---------|
| runtime is not `cursor` | HQ `.quinsy-studio/studio.settings.yaml` has another `runtime`. Cursor multi-chat is off. Use `./studio focus`, or set `runtime: cursor` and bind again. |
| pass `--session` | The command ran outside the agent hook (your own terminal, or the hook did not fire). Run it from the agent in that chat, with no `--session` flag. |
| project not found | There is no `projects/<name>/` folder yet. Bootstrap or adopt first. |
