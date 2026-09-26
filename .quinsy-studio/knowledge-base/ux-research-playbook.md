# UX research playbook (UX-004)

Research that changes the spec — not a persona poster. Distilled from Indi Young *Mental Models*, paired with PM-001. Usability inspection still uses Nielsen (see [interaction-ux-playbook.md](interaction-ux-playbook.md)).

Gate **2a** is a **human** interview (`docs/design/discovery.md`), not invented personas. Do not fill `A:` lines yourself. See [design-direction-playbook.md](design-direction-playbook.md).

## Always

**Do**

- Describe **tasks people are trying to finish** (mental-model spaces), then map product capabilities onto those tasks.
- Separate **what we heard / saw** from **what we infer**.
- If there is no research access this sprint: say **assumption** in the spec and list what would falsify it. Do not invent quotes.
- Interview prompts: task, last time they did it, tools they used, where it broke (Young). Do not duplicate PM-001 personas.

**Don’t**

- Invent a named persona with hobbies and a stock photo as a substitute for tasks.
- Use demographics (“busy millennial”) as a design requirement.
- Use “users want delight / it should feel premium” as evidence — name the **task** and the **moment** (empty, wait, peak–end) if emotion matters ([delight-playbook.md](delight-playbook.md)).
- Run a survey to justify a layout you already drew.

**Spec / mock fail**

- “Users want it to feel premium” with no task or evidence.
- Usability claims (“intuitive”) with no heuristic or observed fail.
- Research section that only restates the PRD.

## Mental models (Young)

**Do:** Group tasks into towers (e.g. “choose a plan,” “pay,” “fix a failed pay”). For each, list current tools and **gaps**. Design fills a gap; it does not add a tower the audience does not have.

**Don’t:** Force a marketing funnel onto a task that is actually “stay compliant” or “export the file.”

**Fail:** Feature placed on a surface that does not match the task’s context (hand to UX-003).

## Light usability (no lab)

**Do:** Heuristic pass with [interaction-ux-playbook.md](interaction-ux-playbook.md) fail table. Five-second scan: can a new person name the job and the next click (Krug)?

**Don’t:** Call a hallway opinion a study. Don’t block the sprint on a full interview series unless the ticket is UX-004-led.

**Fail:** Shipping a new IA with zero scan test and no surface map.
