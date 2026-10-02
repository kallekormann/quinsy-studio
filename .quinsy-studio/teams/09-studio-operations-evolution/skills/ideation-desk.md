# Ideation desk

Human map of where this desk sits: [studio-overview.md](../../../process/studio-overview.md). This file is the method. The desk ends at a PRD in `intake/`. Bootstrap starts the product.

A trigger with no topic is a valid start. Ask once what to look into. A market is optional. Do not search in that turn.

After the human answers, run signals, cluster, ideas, compete, shape, score, and present in that same turn. Research wherever the sources are. Do not ask the human to continue, and do not stop between sections.

Ask a question only when a fact only the human knows would change the problem.

When more than one idea remains, stop and ask which problem or idea to focus on. Give each one a short paragraph. When one idea remains, do not ask. Write the build for that idea, run `./studio ideate case`, and explain that case in the chat.

The case states the problem and the evidence, the idea, the solution vision, the full feature set, and the scope. The last line asks whether this should become the intake PRD. On yes, run approve and promote. On no, run reject or park. The human does not name those commands. Do not write the PRD before they say yes. Bootstrap stays a separate command.

Search the web and fetch the pages. The CLI does not search. Record every search with `./studio ideate search` and every fetch with `./studio ideate fetch` before a paraphrase. A session with no recorded search cannot finish. Do not search from memory. Record every file change through `./studio ideate`.

Do not write the intake PRD until the human says yes. On yes, run `approve` and `promote`. On no, run `reject` or `park`. Do not edit `rubric.md`. Propose changes with `./studio ideate propose`. Do not write into `projects/`. Do not copy outside skill files into this desk.

A medium run uses `--budget normal`.

The order inside the turn is design thinking. Empathize is signals. Define is cluster. Ideate is one idea per sourced problem, plus at most four Blue Ocean lines. Competition is the solution space. Shape is the architecture and the experience for that audience. Score comes after shape. Prototype and test stay in the product loop after a PRD. Shape is not a PRD and it does not implement anything.

Official APIs first. Respect site terms. An unofficial endpoint is fragile in `sources.md` and is never the only source. Never invent a URL. No URL and date means unverified and does not count. Evidence is from the last 24 months unless `--in-force` marks a legal duty. Independent means a different domain, a different author, and a different thread.

Four filters, applied in this run. They are not questions for the human.

- Diverge, then converge. Broad search first, then narrow to the problems the sources repeat. Store several candidate problems from sources before choosing. A discarded candidate keeps a one-line reason. Do not build a list of unsourced ideas.
- Problem-first. A product shape is not an idea until a person is on a sourced line. A solution looking for a use needs two sourced problems, or it is dropped.
- Two sentences on the idea, in plain language: who struggles, and what the idea does.
- Feasible, then positioned. Keep an idea when a sourced person has the pain and the job can be software. Builder time is not a ceiling. One solo builder, with AI agents for coding and design, ships in chunks of about two months. Each chunk is a full web app: big enough to use that builder and those agents, and small enough to finish in about two months. The first chunk is the MVP. Later chunks stay in the idea. An incumbent does not by itself discard it. Do not discard an idea, and do not score time-to-MVP at 0, because the full solution takes longer than two months, has a backend, or needs a later chunk.
  - Open, or no product category yet: keep it only when sources show a workaround, a payment, or a new duty. An empty search is not a market.
  - Me-too: keep it and write the positioning. Who it is for, what is dropped, and what is raised against the incumbent. A crowded or saturated idea still needs that positioning before competitor weakness can score above 2.
  - Not feasible: discard it when a fetched statute or regulator page forbids the activity, when the sources show the job cannot be done in software, or when the job is medicine or clinical care. Medicine and clinical care are out of reach. Other trades are in reach when the activity is allowed and the job is software. Name the page, or name this reach limit, in the discard reason.

## brief

`./studio ideate` with no topic opens this section. Ask what to look into. Do not suggest a country. Do not search. When they answer, pass their words as the focus: `./studio ideate "their words"`. Add `--market "..."` only if they named a market. That stores `hitl_market` and does not limit where you search.

## signals

Empathize. Use the brief: a life situation, a product category, a platform, or a legal duty. Search in whatever market the sources live in. Record the place a source comes from on the evidence line. Do not require one country.

Use web search and page fetch, then record `./studio ideate search --source <row> --outcome new|empty` and `./studio ideate fetch` before a paraphrase. Store `./studio ideate deepen <id> --source --url --date --count --paraphrase --author --thread`. A paraphrase is at most 200 characters. Do not store the raw page. Two empty searches close that source row. The CLI enforces the budget. At wrap-up, stop collecting and present from what is stored.

Scout habits to keep from the incubator method, without its database: Reddit public JSON, the Hacker News Algolia API, store-review pages, and web search for the rest. Add niche forums, YouTube comments, Etsy, Gumroad, Upwork, Fiverr, and host stores. A local legal duty is useful when the brief names one. It is not a requirement.

A line is a real pain when someone states a frustration, a workaround they pay for, or a missing piece. Drop long quotes.

## cluster

Define. Read `INDEX.md` only. Match the sentence, the segment, and the trigger keywords. A discarded row has a one-line reason and is not reopened. The CLI refuses a duplicate. `./studio ideate problem --sentence "..." --segment "..." --keywords "a, b, c" --region ... --language ... --category ...` creates the next `P-xxx` only when the index has no match. Region is the place the sources describe, and it may be blank. Keep the candidate problems the sources support. Use `./studio ideate recluster` when a later signal should move, and stop when the CLI says the re-cluster cap is reached. Do not open an idea in this section.

## ideas

One idea for each strong problem the funnel kept. Do not invent extra ideas to reach a count. The desk sources the problems. A product the human names is a hypothesis to test, including as a me-too, and it is not dropped only because a similar product exists. Shapes: marketplace listing, extension, mini web app, SaaS, or other. Every idea traces to a `P-id`. The pitch is two sentences. On a me-too, the Blue Ocean lines are the positioning.

`./studio ideate idea --title "..." --problems P-001 --shape "marketplace listing" --domain trade --host Notion --pitch "Who struggles. What the idea does." --blue "factors incumbents compete on" --blue "eliminate or reduce" --blue "raise or create" --blue "non-customer"`

`--domain` is `trade`, `life`, or `clinical`. `clinical` is medicine or clinical care and is a knock-out (`medicine-out-of-reach`). It cannot validate or promote. A non-clinical trade uses `trade`. A life situation that is not clinical uses `life`. Fit 0 is also a knock-out (`out-of-reach`) for hardware or a license this builder does not hold. Time to MVP 0 is not a knock-out. Use it only when the first chunk cannot be a web app in about two months. Score 3 when later chunks remain and the first chunk is a full web app in that window. Score 5 when the whole solution fits in one such chunk.

Blue Ocean is at most four lines. Name the factors, what is eliminated, reduced, raised, or created, and the non-customer. No filler.

## compete

Competitors are stored once. Check the index before `./studio ideate competitor --name "..." --url ... --category ...`. Fill a field with `./studio ideate field C-001 --field pricing --tag verified --value "..." --url ... --date YYYY-MM-DD`. Tags are `verified`, `inferred`, or `unknown`. Unknown stays unknown. Anything the company did not state is `inferred`.

Penetration is a proxy: store counts, stars, downloads, funding, or a verified sale price. Set the tier with `--tier dominant|established|growing|niche|dormant|unknown` on the penetration field. A traffic estimate is fragile. A verified sale price outweighs the other proxies.

`./studio ideate matrix --idea I-001 --feature "..." --competitor C-001 --mark "table stakes"`
Marks: `table stakes`, `differentiator`, `gap nobody covers`.

For each product, record how a user's existing tool is wired in, the steps, and what stops the sequence. Wiring is one of three kinds: the book they already use sends the truth, a file is uploaded, or the payment tool is the book. Steps can be a message, a physical letter, a phone call, or a hand-off to a collection firm. A letter and a collection hand-off are steps to fetch and record when the audience needs them. Do not invent the legal procedure. A collection firm takes a file. The app does not become the collector. If a fetched statute says that hand-off needs a license this builder does not hold, score fit at 0.

## shape

The problem space, the solution space, and the architecture and experience for the audience this idea is for. Do this before present. A session idea with no shape makes the shortlist incomplete.

`./studio ideate shape I-001 --problem "..." --solution "..." --architecture "..." --experience "..." --steps "..." --mvp "..." --later "..."`

- Problem: who struggles, what they already do, and what they already use.
- Solution: what the stored competitors offer, which wiring each one uses, and which steps each one runs. Name what is table stakes and what is still open.
- Architecture: the systems the product needs. Stay attached to the tool the person already uses, so the sequence stops when that tool says the job is done. A letter is a document handed to a print-and-post service. A collection firm is a case file handed to a partner. Do not design a new ledger. Do not write a PRD.
- Experience: what that person does, in order, from the thing they already did to the last step they decide.
- Steps: every step the finished product runs, including the ones that come after the first chunk.
- First chunk: the MVP. One chunk of about two months. A full web app for one solo builder and the AI agents that code and design. Name what the person can do at the end of that chunk.
- Later chunks: the remaining steps, one chunk at a time. Each chunk is the same size. Do not leave them as a vague "later."

A price on a competitor page is a neighboring price. A testimonial is not a survey. A success rate the vendor states is not a counted source.

`./studio ideate pricing --idea I-001 --unit "per seat" --competitor C-001 --price "12 EUR"`

`./studio ideate crowd I-001 --class crowded --wedge "Dutch GDPR listing" --bundling-risk "host could ship this free" --competitors C-001`

Classes: `open`, `contested`, `crowded`, `saturated`. In a crowded or saturated space the CLI refuses a competitor-weakness score above 2 without a wedge. A price-only wedge needs `--wedge-price-only yes --wedge-cost-evidence yes` and a source. A marketplace shape scans the top neighboring listings only (price, reviews, missing piece), up to the budget's listing cap. A SaaS idea in a crowded space gets full profiles up to the profile cap. This pass may use at most one third of the search and fetch budget.

## score

Print each idea with `./studio ideate show I-001` and name that path. Then score every dimension for every idea in this same turn. Each CLI call still carries only that dimension's sources. Do not wait for the human to name the next dimension.

Leave a dimension empty when the source is missing. Do not write 0 or 3 as a stand-in. An empty write does not use the pass. A number does, and it needs `--sources`.

`./studio ideate score I-001 --dimension willingness_to_pay --value 3 --sources "url and date"`

Dimension names: willingness_to_pay, demand_volume, frequency_urgency, reachability, time_to_mvp, monetization, platform_risk, trend, competitor_weakness, fit.

Competitor weakness stays empty until the idea links to competitor files. Trend 0 is a knock-out unless the idea was created with `--legal-duty`. The pass cap is in the session budget.

Time to MVP uses chunks, not a ceiling. One solo builder, with AI agents for coding and design, ships in chunks of about two months. Each chunk is a full web app: big enough for that builder and those agents. Score 0 only when the first chunk cannot be a web app in about two months, or the compliance is medicine or another clinical license. Score 3 when the full solution needs later chunks and the first chunk is a full web app inside about two months. Score 5 when the whole solution fits in one such chunk. A days-long slice is too small to be a chunk.

Fit does not drop because one person is building it. Score 0 for medicine, clinical care, or hardware or a license this builder does not hold. Score 3 for a non-clinical trade or life situation that needs domain learning. Score 5 for an ordinary web app for a non-clinical trade.

## present

`./studio ideate qualify I-001 --fit applies|outside|global --note "what the sources show"`

If the brief named a market, each idea is `applies` or `outside`. `applies` means the sourced lines show the problem in that market. `outside` means they do not, and that idea is not a shortlist winner. If no market was named, every idea is `global`. Do not stamp a country onto it.

`./studio ideate present` writes `ideation/shortlist/YYYY-MM-DD.md` and closes the session. A finished shortlist has recorded searches. When a market was stated, every idea in the session has a market check. The shortlist is the record. It is not the human stop, and it does not write a PRD.

If several ideas remain, ask which one to focus on. If one remains, continue to the case in this same turn.

## case

Write the build before the case. The case is the document the human reads. It is not the intake file.

`./studio ideate build I-001 --user "..." --system "..." --backend "..." --infrastructure "..." --modules "..."`

- User tasks: every task the person does in the finished product.
- System tasks: every task the system does in the finished product.
- Backend: the records and the rules. Name them.
- Infrastructure: the running pieces. Name them.
- Modules: the full solution cut into scope modules. The first line of the first module says `Bootstrap focuses on` that module. Every module says `Not in this module` for the work that waits. The final module is the finished product. Later modules are part of the product.

`./studio ideate case I-001` prints the problem and the evidence, the idea, the solution vision, every step, and the scope. It refuses a thin idea. It does not write `intake/`. Explain that case in the chat. The last line asks whether this should become the intake PRD.

## prd

On yes, write the PRD. Promote refuses a thin brief and refuses an idea that is not approved. Saying yes is the approval. The human does not have to say the word approve.

`./studio ideate prd I-001` writes `intake/<slug>.md` in the Rhodes shape: problem, audience, the full steps, user tasks, system tasks, backend, infrastructure, and scope modules. The first module is the focus. The later modules stay in the PRD. `./studio ideate promote` writes that same PRD and refuses when any of those parts is missing. Bootstrap is still a separate command.

`./studio ideate stop --reason "..."` closes the session and does not write a shortlist.

## learn

Append source notes to `ideation/sources.md` and duplicate notes to `ideation/learnings.md` by saying what changed in the chat and recording a proposal when the rubric should move. The 2026-10-02 builder-time calibration is in `rubric.md`: time is not a ceiling. One solo builder, with AI agents for coding and design, ships in chunks of about two months. The first chunk is the MVP. Later chunks stay in the idea. Medicine and clinical care are not in reach. Shape records the full steps, the first chunk, and the later chunks before present.

`./studio ideate propose --text "..."` appends `ideation/rubric-proposals.md` and does not edit `rubric.md`.

`./studio ideate apply-rubric --note "..."` is only for a proposal the human already approved.

A portable method rule can later go through `./studio learn` in a studio session. It does not enter a product sprint and it does not call `execute`.
