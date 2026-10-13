# Skill: Hypothesis & experiment design (GD-001)

```
skill_id: GD-001
team: 11-growth-design
lead_role: Growth Designer
```

When conversion is the job: write a falsifiable claim, one change, a metric or stand-in count, and stop rules. Load on landing, pricing, checkout, PLP, PDP, and any ticket that asks for an A/B or “let’s test.”

**Playbook:** [growth-mechanics-playbook.md](../../../knowledge-base/growth-mechanics-playbook.md)  
**Canon:** [design-team-canon-ledger.md](../../../knowledge-base/design-team-canon-ledger.md)

**Deliverables:** spec §8 Growth intent; no variant mock unless the one change is named.

**Don’t:** A/B a broken flow; dark patterns; Team 05 copy tests that restyle the page.

## Sample size and minimum detectable effect (before any A/B)

An A/B test that cannot reach its sample size is a guess with extra code. Plan it before building the variant.

1. **Baseline:** the primary metric's current rate, measured from our own analytics over a stated window. If there is no baseline, write `baseline: unknown` and measure first. Never borrow a conversion rate from a blog or benchmark.
2. **Minimum detectable effect (MDE):** the smallest change the human would act on, as an absolute or relative change, chosen in the spec by the human. Not a default.
3. **Error rates:** significance level α = 0.05 (two-sided) and power 80 % are the conventional defaults. State them; change only with a reason.
4. **Sample size per variant:** compute from baseline, MDE, α and power with a standard calculator or library (for example `statsmodels` power functions for two proportions). Paste the inputs and the result in the spec.
5. **Duration:** sample size ÷ eligible traffic per variant per day, rounded up to full weeks so weekday patterns even out. Fix the end date before launch.
6. **Feasibility:** if the duration exceeds the window the milestone allows, do not run the A/B. Ship the best-reasoned version, watch the stand-in count, and use qualitative checks instead (five-second test, GD-003 persona walkthrough).
7. **No peeking:** decide only at the planned sample size. Stopping early on a "significant" result needs a sequential method declared up front.
8. **One primary metric.** More than one variant against control → correct for multiple comparisons (e.g. Bonferroni) or reduce variants.
9. **Sample ratio check:** at the end, compare assignment counts with the planned split (chi-square test). A mismatch means broken assignment; discard the result.

## Guardrail metric

Every experiment names at least one guardrail: a metric that must not get worse while the primary metric moves. Pick it from what the change could break:

- Checkout or pricing: payment errors, refunds or cancellations within the trial, support contacts.
- Signup or onboarding: activation (core action done), unsubscribes, spam complaints.
- Any surface: page performance (LCP, INP against Core Web Vitals thresholds), error rate, accessibility regressions.

The spec states the guardrail, its baseline, and the stop rule ("stop and roll back if the guardrail worsens by more than X"), with X set by the human. A primary-metric win with a guardrail loss is not a win.

## Consent and ethics

- Assignment that stores an ID on the device (cookie, localStorage) needs § 25 TDDDG consent. Without consent, those users see control and are not counted; note the resulting bias in the spec.
- No variant may hide prices, add pre-ticked options or fake urgency ([marketing-law.md](../../../knowledge-base/skill-extensions/marketing-law.md)).

**Spec §8 Growth intent, experiment block:** hypothesis · one change · primary metric + baseline · MDE · α / power · sample size per variant · duration and end date · guardrail + stop rule · consent note · decision rule.

**Source:** agency-agents `project-management/project-management-experiment-tracker.md` (MIT), invented success rates and revenue claims removed.
