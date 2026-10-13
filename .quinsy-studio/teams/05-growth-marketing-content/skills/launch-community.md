# Skill: Launch and Community

> Plans and runs a product launch and the community work around it: one launch plan, channel-specific posts that follow each channel's own rules, honest disclosure of who is posting, and measurement that needs no tracking consent. The agent drafts and prepares. The human posts from their own accounts. Nothing is faked: no sock puppets, no bought votes, no reviews we wrote ourselves.

## Metadata

```
skill_id: GM-005
name: Launch and Community
team: 05-growth-marketing-content
lead_role: Growth Manager
support_roles: [Content Strategist, SEO Specialist, Legal & Privacy Officer]
phases: [5, 6, 7]
activation_triggers:
  - Ticket words: launch plan, product hunt launch, show hn, press release, reddit post, community launch, podcast guest, press kit
  - Milestone that ends in a public release (first `ship --to main` of a product)
  - Ticket that creates a Discord server, GitHub Discussions, forum or changelog channel
pairs_with: [GM-001, GM-002, GM-003, GM-006, CL-001, GD-002]
```

## When to load

- When a milestone's last ticket is a public release. Write the launch plan in the milestone's design or architecture phase, not on launch day.
- For any post, pitch or press text that goes to a channel we do not own.
- When the product opens a community space (Discord, GitHub Discussions, forum).
- Also load `knowledge-base/skill-extensions/marketing-law.md` for every public claim, review request or partner post.

## Rules

### 1. One launch plan per release

`docs/growth/launch-plan.md` holds: goal (one number with a window, or "unknown" with how we will learn it), audience, three key messages at most, proof for each message, channels in scope and out of scope, asset list, timeline from T-14 to T+7, who does each step (agent drafts, human posts), measurement, risks, and the disclosure line used on every channel.

### 2. The human posts; the agent never creates accounts

The agent writes drafts into `docs/growth/launch/<channel>.md`. The human posts from their own named account. The agent does not register accounts, log in to social platforms, or post on anyone's behalf. One person, one account per platform.

### 3. Disclose affiliation every time

Every post, comment or reply about our product by the founder, staff, a contractor or a paid partner says so in the first lines: "I built this", "I work on X", "Werbung" or "Anzeige" for paid partner content. Hiding the commercial purpose breaks § 5a(4) UWG. Posing as a neutral user breaks UWG Annex no. 23. Platforms ban it too.

### 4. No fake voices

No sock-puppet accounts, no bought upvotes, likes or followers, no vote rings or engagement pods, no asking friends to upvote, no reviews written by us or paid for without disclosure. Fake or commissioned reviews are always unfair (UWG Annex no. 23c). Product Hunt and Hacker News detect and penalise vote solicitation.

### 5. Follow each channel's own rules

Read the current rules page before drafting. Record the URL and the date read in the launch plan.

| Channel | Checkable rules |
|---|---|
| Reddit | Read the subreddit sidebar and rules. Post only where self-promotion is allowed or the post answers the subreddit's topic. Say "I built this". No cross-posting the same text to many subreddits. Answer comments in the thread. |
| Product Hunt | The maker is listed and answers comments. Do not ask for upvotes; ask people to look and give feedback. The day resets at 00:00 Pacific Time. Gallery, tagline and first comment ready the day before. |
| Hacker News (Show HN) | Title starts `Show HN:`. Only for something people can try now; not a landing page, waitlist, signup wall or fundraiser. Do not solicit votes or comments. The maker posts a first comment with context and stays to answer. |
| LinkedIn | Post from the founder's personal profile. No engagement pods. Disclose paid partnerships. |
| Developer communities (Discord, GitHub Discussions, forums) | Member value first. Channel rules and moderation policy written before the first member joins. Public praise, private correction. |
| Podcasts | Pitch one angle per show, personalised to recent episodes. Paid placements are labelled "Werbung". Guests consent to publishing before recording. |
| Press | One story per pitch, personalised to the journalist's beat. Honour embargoes. No superlatives ("first", "leading", "best") without proof. |

### 6. Claims must survive § 5 UWG

Every claim in a post, press release or launch page is true and provable. Sole-position claims ("the only", "first in Germany") need evidence filed next to the draft. Numbers in a pitch come from our own measured data, with the source named. No invented user counts or "trusted by" logos without permission.

### 7. Measure with UTM and cookieless analytics

Every link we place carries `utm_source`, `utm_medium` and `utm_campaign` (lowercase, hyphenated, listed in `docs/growth/utm-register.md`). No email addresses, user IDs or other personal data in UTM parameters. Count with a privacy-friendly analytics tool that stores nothing on the device (for example self-hosted Umami or Plausible on Coolify). If a tool sets cookies or reads device storage, § 25 TDDDG consent applies and the CL-002 banner gates it.

### 8. Launch content lives in Payload

The launch post, changelog entry, press kit page and FAQ are Payload documents in the product app, published through the normal flow. No hand-edited HTML pages outside the CMS. The press kit page holds the boilerplate, logo files, screenshots, founder photo and a contact address.

### 9. Community spaces need a health owner

Before opening a space: channel structure, rules, onboarding message, moderation policy, response time the human can actually keep. Measure health, not size: share of questions with a reply, time to first reply, share of answers from the top few members. Do not mobilise members against critics or the press.

## Workflow

1. Read the PRD, milestone plan, `marketing-law.md` and `knowledge-base/launch-playbook.md`. When the milestone is planned, add the launch tickets from `studio-templates/growth/launch-ticket-pack.md`.
2. Write `docs/growth/launch-plan.md` from `studio-templates/growth/launch-plan.md` (rule 1). List channels in and out of scope with a reason.
3. Read each channel's rules page; note URL and date (rule 5).
4. Draft per-channel posts in `docs/growth/launch/<channel>.md`, each with its disclosure line and UTM link.
5. Draft the press release and press kit page as Payload content (rule 8).
6. Fill `docs/growth/utm-register.md` and check analytics records a test visit per UTM.
7. Run the launch-day checklist below. Mark each line PASS, FAIL or NOT TESTED.
8. Hand drafts to the human. The human posts. The agent watches replies and drafts answers.
9. At T+7 write `## Results` in the launch plan: visits and signups per UTM source, what we learned, follow-ups.

### Launch-day checklist

- [ ] Production release done through `./studio ship <p> --to main --approve` (human HITL).
- [ ] Smoke routes green on production; signup, login and first core action work.
- [ ] Impressum (§ 5 DDG), privacy policy and terms reachable from every page footer.
- [ ] Prices follow PAngV (total price incl. VAT; GD-002).
- [ ] Confirmation and welcome mails arrive (GM-006); double opt-in works.
- [ ] Error monitoring and uptime alert active; someone is on watch for the first hours.
- [ ] Support inbox answered; reply drafts ready for common questions.
- [ ] Each UTM link opens the right page and shows in analytics.
- [ ] Rollback plan written: which commit to redeploy in Coolify.
- [ ] Every channel draft has its disclosure line and has been checked against that channel's rules.

## Deliverables

- `docs/growth/launch-plan.md` with sections `## Goal`, `## Audience`, `## Messages`, `## Channels`, `## Timeline`, `## Measurement`, `## Risks`, `## Disclosure`, `## Results`.
- `docs/growth/launch/<channel>.md` per channel in scope.
- `docs/growth/utm-register.md`.
- Payload content: launch post, changelog entry, press kit page.
- If a community space opens: `docs/growth/community.md` (structure, rules, onboarding, moderation, health metrics).

## Done evidence (receipt)

- Launch plan exists with all headings; every channel row names its rules URL and date read.
- Every draft contains a disclosure line and a UTM link listed in the register.
- Launch-day checklist copied into the receipt with PASS / FAIL / NOT TESTED per line.
- One test visit per UTM source visible in analytics (screenshot path).
- Claims list with evidence path for every sole-position or numeric claim.

## Anti-patterns

- Launch plan written on launch day.
- "Please upvote us" on Product Hunt, Hacker News or in a mailing.
- Staff posting as "a happy user". Reviews from friends without disclosure.
- One identical post blasted to ten subreddits.
- Show HN for a waitlist page.
- Personal data in UTM parameters. Google Analytics loaded before consent.
- Success metrics copied from a blog ("aim for 85% upvote ratio") instead of our own baseline.
- A Discord with twelve empty channels and no one answering.

## Handoff

- To GM-003: messages and proof feed the blog post and changelog copy.
- To GM-006: launch signups enter the welcome flow; launch mailing goes only to confirmed subscribers.
- To GM-001 / GM-002: press kit and launch post get metadata, schema and llms.txt entries.
- To GD-002: launch landing page and pricing follow commercial-surface rules.
- To CL-001 / CL-002: any new analytics tool, community platform or podcast host is a processor to list.

## References

- Hacker News guidelines and Show HN rules (news.ycombinator.com/newsguidelines.html, /showhn.html).
- Product Hunt posting guidelines (help.producthunt.com).
- Reddit Content Policy and each subreddit's rules.
- UWG §§ 5, 5a, Annex nos. 11, 23, 23c. `knowledge-base/skill-extensions/marketing-law.md`.
- Source: agency-agents `marketing/marketing-pr-communications-manager.md`, `marketing-linkedin-content-creator.md`, `marketing-reddit-community-builder.md`, `marketing-developer-community-builder.md`, `marketing-global-podcast-strategist.md` (MIT), rewritten without personas or invented targets.
