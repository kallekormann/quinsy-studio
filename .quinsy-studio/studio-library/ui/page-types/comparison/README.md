# Comparison Page Type

> Seitentyp für Vergleiche, Alternativen und "Best of"-Listen.

## Use Cases

- Produktvergleiche
- Feature-Matrix
- Preisvergleich
- Alternativen zu bekannten Tools
- "X vs. Y" Artikel

## Struktur

```
┌─────────────────────────────────────────────────────────┐
│                     HEADER                              │
│  Titel, Untertitel, CTA                                │
├─────────────────────────────────────────────────────────┤
│                  INTRO                                  │
│  Kontext, Problemstellung, Zielgruppe                  │
├─────────────────────────────────────────────────────────┤
│              COMPARISON TABLE                           │
│  Features, Preise, Bewertungen                         │
├─────────────────────────────────────────────────────────┤
│              DETAILED SECTIONS                          │
│  Pro/Contra für jede Option                            │
├─────────────────────────────────────────────────────────┤
│              RECOMMENDATION                             │
│  Empfehlung je nach Use Case                           │
├─────────────────────────────────────────────────────────┤
│              FAQ                                        │
│  Häufige Fragen                                        │
├─────────────────────────────────────────────────────────┤
│              CTA                                        │
│  Nächste Schritte                                       │
└─────────────────────────────────────────────────────────┘
```

## Komponenten

- `ComparisonTable` — Feature-Matrix
- `OptionCard` — Einzelne Option mit Pro/Contra
- `RatingBadge` — Bewertungsanzeige
- `RecommendationBox` — Empfehlungsbox

## Datenmodell

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
- Vergleichs-Keywords in H1/H2
- Strukturierte Daten für Rich Snippets
