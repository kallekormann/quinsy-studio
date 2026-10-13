# Skill: Visual Storyteller (UX-007)

> Marketing pages, workflow explainers, storyboards and the imagery on them. The page tells one story in the order the PRD persona asks their questions, and every picture shows something true about the product or its users. Generated images follow a written brief, never show invented customers or fake product screens, and carry provenance, alt text and the AI-content disclosure the law requires.

## Metadata

```
skill_id: UX-007
name: Visual Storyteller
team: 10-product-design-experience
lead_role: Visual Storyteller (Director)
support_roles: [Growth Designer, Brand Guardian, Copywriter]
phases: [3, 4]
activation_triggers:
  - ticket_type marketing-page or workflow-explainer
  - Any ticket that adds a hero, illustration, OG image or other generated or stock imagery
  - Phrases: "landing page", "hero section", "storyboard", "explainer", "illustration", "imagery", "generated image", "og image"
pairs_with: [GD-001, GD-002, GD-003, GM-001, GM-003, UX-004, UX-006, FE-004, CL-001]
```

Default verdict: no image ships until its brief, its provenance line and its alt text exist.

## When to load

- Design phase of a marketing page, workflow explainer, pricing page or storyboard. On commercial surfaces Team 11 (GD-001/GD-002) loads too.
- Any ticket that adds or replaces imagery, including OG and social cards and email headers.
- Not for icons (SVG from the library, LO-0037) or product screenshots (capture the real app; see Rule 4).

## Rules

### 1. One story, in the persona's order

The page answers the persona's questions in order: what is this, is it for me, does it work, what does it cost, what do I do next. Each fold has one job, and its picture serves that job. Scroll is the narrative (`visual-storytelling-playbook.md`); never hijack scroll or hide content behind motion.

### 2. Every image has a job and a brief

Before generating or buying an image, write its brief in the spec under §5 `### Imagery`: the fold, the job (show the outcome, show the setting, explain a step), the subject, setting, light, framing and aspect ratio, what must not appear, and the alt text. An image without a job is cut, not prettified.

### 3. Show the real audience, never an invented one

People in images match the personas in `docs/definitions/02-personas.md` and the research files: their trade, workplace, tools and region. Do not invent age, gender, ethnicity or disability mixes to look diverse, and do not default to one look either. When the sources say nothing, show the work (hands, tools, the job site, the screen in use) rather than a face. Never give people in images names, quotes or job titles: a generated person presented as a customer is a fake testimonial (UWG §5, `skill-extensions/marketing-law.md`).

### 4. Product screens are captures, not drawings

Any image that shows the product is a screenshot of the running app with seeded, realistic data, in the gate-2b tokens. Never generate or paint a UI. Never show a feature that does not exist yet without a visible "coming soon" label.

### 5. Prompt like a photographer, check like an editor

Write prompts as subject, action, setting, light, lens or medium, composition, and palette from the project tokens. Name what to exclude (text, logos, watermarks, extra fingers, brand marks of others). Generate several, then reject any image with garbled text, wrong anatomy, impossible tools, stereotyped staging or a look that contradicts DESIGN.md. Never put words inside a generated image; set text in HTML.

### 6. Provenance and disclosure

Record every image in `docs/design-specs/imagery.md`: file path, source (generated with model and date, stock with licence and URL, or own photo), the brief it answers, and alt text. Realistic generated images of people, places or events are labelled as AI-generated where a viewer could take them for real (EU AI Act Art. 50(4), applicable since 2 August 2026). Stock needs a licence that covers web and ads. Never use an image of a real, identifiable person without a release.

### 7. Weight, format and accessibility

Ship AVIF or WebP through `next/image` with `sizes`, width and height set, and the hero under 200 KB at 1440. Alt text says what the image shows for the page's purpose; a purely decorative image gets `alt=""`. Text over images keeps 4.5:1 contrast at every breakpoint (FE-004).

## Workflow

1. Read the PRD personas, DESIGN.md and spec §5 Story and §6 Growth intent.
2. Write the fold-by-fold story and mark which folds need an image and why.
3. Write each image brief in the spec §5 `### Imagery` table.
4. Capture product screens from the running app; generate or license the rest.
5. Edit: reject and regenerate per Rule 5. Compress and export.
6. Fill `docs/design-specs/imagery.md` and place the images in the real-UI mock.
7. Hand the packet to GD-003 for the five-second test and walkthrough.

## Deliverables

Spec §5 `### Imagery`:

```markdown
| Fold | Job | Brief (subject · setting · light · framing · ratio) | Exclude | Alt |
|------|-----|-----------------------------------------------------|---------|-----|
| 1 | Show the outcome | Tiler's hands on a tablet showing the paid-invoice list · van interior · morning daylight · close, 3:2 | faces, text, logos | Tablet showing three invoices marked paid |
```

`docs/design-specs/imagery.md`:

```markdown
| File | Source | Licence / model + date | Brief | Alt | AI label |
|------|--------|------------------------|-------|-----|----------|
| public/img/hero-1440.avif | generated | <model>, 2026-10-13 | TICKET fold 1 | Tablet showing three invoices marked paid | not needed (no realistic person) |
```

## Done evidence

```markdown
## Evidence
- Imagery log: docs/design-specs/imagery.md (n images, every row has source, alt, AI label)
- Hero weight: public/img/hero-1440.avif 148 KB — PASS
- Product shots: captured from /app/invoices with seed data — PASS
```

## Anti-patterns

- Generated people presented as customers, team members or reviewers.
- A painted dashboard instead of a screenshot of the app.
- Words baked into a generated image.
- Diversity staged from a quota instead of the real audience; or one default look everywhere.
- Purple-gradient abstract blobs as a hero because nothing else had a job.
- Alt text that says "image" or repeats the headline.
- A 2 MB PNG hero.

## Handoff

- **To GD-003:** the packet with images in place for the five-second test.
- **To GM-001/GM-003:** OG image, alt text and captions for search and answer engines.
- **To FE-001:** final assets, sizes and the imagery log.
- **To CL-001 / marketing-law:** any image of a real person or a customer claim.

## Deltas

Imagery rules come from the agency-agents Image Prompt Engineer and Inclusive Visuals agents, rewritten to the studio's evidence rules: no invented demographics (UX-004/UX-006), no fake testimonials (marketing-law), product screens captured from the real app (real-UI mocks).

## References

- **Agent:** `agents/design-visual-storyteller.md`
- **Playbooks:** `knowledge-base/visual-storytelling-playbook.md` (scroll as narrative), `knowledge-base/growth-mechanics-playbook.md` (landing and pricing), `knowledge-base/delight-playbook.md`
- **Email:** [email-design.md](../../../knowledge-base/skill-extensions/email-design.md) — transactional and newsletter HTML, preheader, CTA copy
- **Slides/PDF:** optional `anthropic_docs` pdf/pptx; theme-factory packs for artifacts only — map product UI to presets and tokens
- [marketing-law.md](../../../knowledge-base/skill-extensions/marketing-law.md) — UWG, fake reviews
- [hq-agency-agents-integration.md](../../../process/hq-agency-agents-integration.md) — Design and Product table
