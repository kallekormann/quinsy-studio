# Upgrade soft-path pattern (LO-0142)

When a marketing or paywall **soft-path** sends a free user to Settings (or Account) because checkout is unavailable:

**Do:** Land on the real Account (or plan) surface — not a dead hash (`#billing`).  
**Do:** Make Free + **Upgrade** obvious without hunting (badge + primary CTA in the first Account viewport).  
**Do:** Prefer auto-opening the upgrade dialog when intent is explicit — e.g. `?upgrade=1` / `?tab=account&upgrade=1` — so soft-path equals “see upgrade,” not “find Settings.”  
**Don't:** Mark soft-path done because the URL parses if Free users still see Pro-only chrome or no Upgrade control.  
**Don't:** Rely on a modal that only opens after an unmarked click when the journey was “upgrade now.”

Compose with Headless UI dialog + library Button/Badge; keep plan copy in the project.
