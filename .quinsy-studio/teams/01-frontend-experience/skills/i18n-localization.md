# Skill: i18n and Localization

> Makes the product correct in every locale it ships. UI strings come from message catalogs. Content is translated only through Payload localization. Plurals, dates, numbers and money go through ICU and `Intl`. Locale is in the URL, and every public route tells GM-001 its language alternates. A pseudo-locale run proves nothing is hard-coded.

## Metadata

```
skill_id: FE-008
name: i18n and Localization
team: 01-frontend-experience
lead_role: Frontend Architect
support_roles: [Frontend Engineer, Backend Engineer, Content Strategist]
phases: [2, 3, 4, 5]
activation_triggers:
  - Blueprint `Locales:` lists more than one locale
  - Ticket adds a locale, a language switcher, localized content or localized email/PDF
  - Any UI ticket in a project whose `docs/i18n.md` lists more than one locale
  - Ticket words: i18n, localization, translation, locale, hreflang, multilingual
pairs_with: [BE-007, GM-001, BE-009, FE-004, CL-003]
```

## When to load

- Gate 1: when the blueprint has `Locales:`. Write `docs/i18n.md` in the architecture packet.
- Every UI ticket in a multi-locale project: rules 2, 4 and 5 apply to each new string.
- Single-locale projects: still use catalogs for UI strings, so adding a locale later is data work, not a rewrite.

## Rules

### 1. `docs/i18n.md` is the contract

It lists: locales (same list as Payload `localization.locales` and the blueprint), default locale, fallback chain (`de-AT → de → en`), URL strategy (rule 6), catalog path, the formatter helper, the time-zone rule, and who translates. A locale that is not in this file does not ship.

### 2. Two kinds of text, two paths

| Text | Where it lives | How it is translated |
|---|---|---|
| UI chrome: buttons, labels, errors, empty states, emails' fixed text | `apps/web/src/messages/<locale>.json` | Catalog per locale |
| Content: pages, posts, products, legal pages, anything an editor writes | Payload fields with `localized: true` | Payload localization |

Do not add `next-intl`, `i18next` or another content-translation package for content fields. Do not put content in catalogs or chrome in Payload. Payload's admin UI language is a separate setting (`i18n.supportedLanguages` in the Payload config) and is not product UI.

### 3. One formatter helper

`src/i18n/` exports `t(locale, key, values)` built on `intl-messageformat` (ICU), plus `formatMoney`, `formatDate`, `formatNumber` on `Intl`. Server components call it directly; client components get the locale and messages from a provider set in the locale layout. A framework instead of the helper needs an ADR and must not touch content fields.

### 4. Complete ICU messages, no concatenation

- One key is one full sentence with named placeholders: `"cart.count": "{count, plural, =0 {Dein Warenkorb ist leer} one {# Artikel im Warenkorb} other {# Artikel im Warenkorb}}"`.
- Every `plural` and `select` has an `other` branch. Never `count === 1 ? … : …`.
- No `"Hallo " + name` and no JSX that glues fragments into a sentence. Rich text uses ICU tags (`<link>…</link>`) mapped to components.
- Each key carries a translator note in `messages/_context.json` (noun or verb, where it shows, max length if any).

### 5. Format nothing by hand

- Money: `Intl.NumberFormat(locale, { style: 'currency', currency })` with the integer minor units from BE-008 divided once in the helper.
- Dates and times: `Intl.DateTimeFormat` with an explicit `timeZone`. Event times use the user's time zone (stored on the user, default from `docs/i18n.md`). Civil dates (birthdays, due dates) are formatted with `timeZone: 'UTC'`.
- Lists and relative times: `Intl.ListFormat`, `Intl.RelativeTimeFormat`.
- Format on the server with the same locale and time zone the client uses, or pass both down. A different default on the client causes hydration mismatches.
- Sorting and search of names use `Intl.Collator(locale)`. Truncate with `Intl.Segmenter`, not `slice`.

### 6. Locale routing

- Locale is a path segment inside each route group: `src/app/(marketing)/[locale]/…` and `src/app/(app)/[locale]/…`. `/admin` and `/api` have no locale segment.
- Middleware picks the locale for a bare URL: saved user choice (cookie or user field), then `Accept-Language`, then the default. Never IP location alone. It redirects; it does not rewrite silently.
- `<html lang>` is the resolved locale. Unknown locale segments return 404.
- Payload reads pass `locale` and `fallbackLocale` from the segment. Only admin code uses `locale: 'all'`.
- The language switcher links to the same page in the other locale (the localized slug), not to the home page.

### 7. hreflang hand-off to GM-001

Each public page's `generateMetadata` sets `alternates.languages` for every published locale plus `x-default`, from the localized slugs Payload returns. Only locales with a published translation are listed. GM-001 owns sitemap, canonical and indexing rules; FE-008 supplies the locale map. The receipt shows one rendered example.

### 8. Layout survives other languages

- Use logical properties: Tailwind `ms-`, `me-`, `ps-`, `pe-`, `start-`, `end-`, `text-start`. Not `ml-` or `text-left` in new code.
- No fixed widths on buttons, tabs or table headers. Long German compounds must wrap (`hyphens: auto` with the right `lang`, or `overflow-wrap: anywhere`).
- Right-to-left only when `docs/i18n.md` lists such a locale; then set `dir` on `<html>` and mirror directional icons only.

### 9. Pseudo-locale test

Add a dev-only locale `en-XA` built from the default catalog: accented letters, about 40% padding, and `[!! … !!]` brackets. Payload content falls back as usual. Any string on screen without brackets is hard-coded. Any cut-off bracket is a layout bug. `en-XA` never reaches production builds or hreflang.

### 10. Catalog check in CI

A script fails the build when: a key used in code is missing in any locale catalog, a catalog has keys no code uses, or a translation's placeholder set differs from the default locale's. Missing translations fall back along the chain at runtime but still fail the check.

## Workflow

1. Gate 1: write `docs/i18n.md`; set Payload `localization` to the same locales and fallback.
2. Add `src/i18n/` helper, catalogs, `[locale]` segments, middleware, and the catalog check.
3. Per UI ticket: add keys with context notes, use the helper, run the pseudo-locale.
4. Per content ticket: mark translatable fields `localized: true`; keep slugs localized when URLs differ.
5. Emails and PDFs (BE-009) render with the recipient's stored locale.
6. Before a locale goes live: native-speaker review of chrome and legal pages (CL-003), then add it to hreflang.

## Deliverables

- `docs/i18n.md`
- `src/i18n/` helper, catalogs per locale, `_context.json`
- `[locale]` route segments, middleware, language switcher
- Payload `localization` config matching `docs/i18n.md`
- Catalog check script wired into the gate
- `en-XA` pseudo-locale (dev only)

## Done evidence (receipt)

`## i18n proof` with PASS / FAIL / NOT TESTED:

- Catalog check output (zero missing, zero unused, zero placeholder mismatch)
- Screenshot path of the changed screen in `en-XA`, no unbracketed text
- Screenshot path in the longest real locale (usually `de`), nothing clipped
- One rendered `<link rel="alternate" hreflang>` block from a public page
- One plural message shown with 0, 1 and 5

## Anti-patterns

- String concatenation or ternaries for plurals
- `toLocaleString()` without an explicit locale, or `MM/DD/YYYY` patterns in code
- Content translations in JSON catalogs, or a second translation package for Payload fields
- Locale chosen by IP, or a switcher that drops the user on the home page
- hreflang to a locale that has no published translation
- Fixed-width buttons sized for English

## Handoff

- **Consumes:** blueprint `Locales:`, Payload config (BE-007), translations from the human or translator.
- **Produces:** locale map for GM-001; locale and formatters for BE-009 and email templates; `lang` attributes for FE-004.

## References

- `knowledge-base/payload-playbook.md` (one default locale; extra locales are Payload field localization; chrome stays in Next)
- `knowledge-base/frontend_playbook.md` (i18n row)
- Payload docs: Localization, i18n; FormatJS `intl-messageformat`; MDN `Intl`; Unicode CLDR plural rules
- GM-001 SEO, BE-009 documents, CL-003 legal pages, FE-004 accessibility
