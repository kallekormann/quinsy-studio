# Load caps

`./studio settings` is a load limit, not a bill. The numbers are not a Cursor, Claude, or Gemini invoice. They estimate how much text one execute step asked the agent to read, roughly characters divided by four. When the studio prints `INFORM cost-cap`, raise the key it names, then continue. Do not paste the repo into the chat to get around it.

Higher numbers do not make the work better. They only delay the stop.

## Two ledgers

| Ledger | Command | Committed file | Your override (gitignored) | What it limits |
|--------|---------|----------------|----------------------------|----------------|
| Studio | `./studio settings` | `.quinsy-studio/studio.settings.yaml` | `.quinsy-studio/studio.settings.local.yaml` | Training and infusion |
| Product | `./studio settings <project>` | `projects/<project>/docs/studio.settings.yaml` | `docs/studio.settings.local.yaml` in that product | That product's execute loop |

No API keys in either file. Keys stay in the app you use to talk to the agent.

`./studio focus <project>` resets that product's session counter. The studio counter stays until `./studio settings --reset-usage`. When the line says `ledger=project` or `ledger=hq`, raise the key in that ledger's local file.

An older product that has no settings file yet: `./studio settings <project> --init`. That does not overwrite a file you already edited.

## What each number limits

| Knob | Limits | When it fires |
|------|--------|----------------|
| `steps.<step>.context` | This one turn (the card plus the files it listed) | The ticket's files are too large for one load. Raise `context`, or list fewer files. |
| `steps.<step>.budget` | Every turn of that kind since the last reset | Many execute loops. Raise that step's `budget`, or focus again to reset. |
| `session_token_budget` | All steps added together | The session ceiling. Set it at least as high as the step budgets you expect in one focus. |

`cost.profile` multiplies the table: `economy` about half, `standard` the baseline, `premium` about double. Day-to-day tweaks belong in the local file so a clone keeps the baseline.

The committed baseline is medium: session 400k, implement context 28k and budget 400k, design context 40k and budget 400k. That covers a medium sprint if you re-focus between phases. A large existing codebase wants a higher product session in the local file. Leave the studio ledger at medium unless training itself is hitting the cap.

After `INFORM cost-cap`, raise only the named key, about one and a half times, and run execute again. If the session fires while the step budgets still have room, raise `session_token_budget` first.
