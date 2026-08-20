# Comparison Page Type

> Page type for comparisons, alternatives, and "best of" lists.

## Use Cases

- Product comparisons
- Feature matrix
- Price comparison
- Alternatives to known tools
- "X vs. Y" articles

## Structure

```
┌─────────────────────────────────────────────────────────┐
│                     HEADER                              │
│  Title, Subtitle, CTA                                  │
├─────────────────────────────────────────────────────────┤
│                  INTRO                                  │
│  Context, Problem Statement, Target Audience            │
├─────────────────────────────────────────────────────────┤
│              COMPARISON TABLE                           │
│  Features, Prices, Ratings                              │
├─────────────────────────────────────────────────────────┤
│              DETAILED SECTIONS                          │
│  Pros/Cons for each option                              │
├─────────────────────────────────────────────────────────┤
│              RECOMMENDATION                             │
│  Recommendation per use case                            │
├─────────────────────────────────────────────────────────┤
│              FAQ                                        │
│  Frequently asked questions                             │
├─────────────────────────────────────────────────────────┤
│              CTA                                        │
│  Next steps                                             │
└─────────────────────────────────────────────────────────┘
```

## Components

- `ComparisonTable` — Feature matrix
- `OptionCard` — Individual option with pros/cons
- `RatingBadge` — Rating display
- `RecommendationBox` — Recommendation box

## Data Model

```typescript
interface Comparison {
  title: string;
  subtitle: string;
  options: Option[];
  features: Feature[];
  recommendation: Recommendation;
}

interface Option {
  name: string;
  logo?: string;
  price?: string;
  rating: number;
  pros: string[];
  cons: string[];
  bestFor: string;
}

interface Feature {
  name: string;
  description?: string;
  values: Record<string, boolean | string>;
}
```

## SEO

- Schema.org: `Product`, `Review`, `AggregateRating`
- Comparison keywords in H1/H2
- Structured data for rich snippets
