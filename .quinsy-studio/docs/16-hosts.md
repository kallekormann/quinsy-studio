# Cursor, Claude Code, and the CLI

Open the studio repo at its root, the folder that contains `./studio`. Do not open only `projects/<name>/`.

| Host | How a product is selected |
|------|---------------------------|
| Cursor, when `runtime` is `cursor` | Each chat binds its own product. You do not look up an id. See [Several products at once](03-several-products.md). |
| Claude Code, Gemini CLI, or `runtime` set to anything else | `./studio focus <project>` hides the other products in that workspace. One product at a time in that window. |

The same `./studio` loop runs in all of them. Keys stay in the host. They are never written into studio settings.

## Cursor asking "Allow"

If Cursor shows Allow when the agent runs `./studio move … done`, that is Cursor's own approval, not a studio gate. The command already requires a receipt and a green automated gate. You do not also approve the ticket in chat.

Studio commands are listed so they can start without that card. Shipping to `main` and pushing `main` stay blocked until you ask. Studio stops are unchanged: gates, the design phase, production ship, a production migration, a tech veto.

Reload the window after you change allowlists.

## Session start

```bash
./studio install
./studio verify-worlds
./studio verify-abstraction
./studio settings
./studio execute <project>
```

In Cursor, bind the chat before execute if this window holds more than one product. Elsewhere, focus, then execute. The agent does the next step and runs execute again until it must stop for you.
