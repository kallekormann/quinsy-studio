# Skill: Document Generation

> Turns product data into documents that print correctly and stand up to a German tax audit: PDFs rendered from HTML in a background job, invoices with unique sequential numbers, e-invoices in XRechnung or ZUGFeRD for German B2B, and issued documents that never change. Every template is covered by golden-file tests.

## Metadata

```
skill_id: BE-009
name: Document Generation
team: 02-backend-systems
lead_role: Backend Architect
support_roles: [Backend Engineer, Frontend Engineer, Compliance Lead]
phases: [2, 3, 4, 5]
activation_triggers:
  - Ticket produces a PDF, invoice, credit note, quote, report, certificate or export
  - Billing model makes the product the seller (BE-008 rule 8, Stripe)
  - Ticket words: pdf, invoice, rechnung, xrechnung, zugferd, e-rechnung, gobd, print layout
pairs_with: [BE-006, BE-007, BE-008, CL-001, CL-004, FE-008]
```

## When to load

- Gate 1: when the product issues invoices. The architecture doc names the renderer, the e-invoice format and the storage bucket.
- Architecture and implementation phases: every ticket that adds or changes a document template, numbering or retention.
- Not needed when Lemon Squeezy is the merchant of record and the product issues no other documents.

## Rules

### 1. Render in a job, never in the request

A request enqueues a Payload job (BE-006) and returns `202` with the document ID. The job renders, stores the file and sets `status: ready`. The UI polls or shows a "ready" state. Rendering in a route handler blocks the server and times out on large documents.

### 2. One renderer, one template source

- Renderer: headless Chromium through Playwright `page.pdf()`. It runs in a separate worker container or the Python worker; the architecture doc names which. Do not add a second engine (wkhtmltopdf, Puppeteer beside Playwright).
- Template: a React server component rendered to HTML with `renderToStaticMarkup`. The in-app preview route renders the same component. No parallel string template.
- Reuse one browser per worker and a fresh context per job. Close the context in `finally`. Set a render timeout and a page limit.

### 3. Fonts are hosted by us

Fonts are files in the project (`public/fonts/` or the worker image), loaded with `@font-face` and a `file:` or same-origin URL. No Google Fonts CDN (LG München I, 3 O 17493/20, on IP transfer to Google). Wait for `document.fonts.ready` before `page.pdf()`. Check that every font is embedded: `pdffonts out.pdf` shows `emb yes`.

### 4. Print CSS rules

- Page size in a literal rule: `@page { size: A4; margin: 20mm 18mm; }`. CSS variables inside `@page` are ignored by Chromium.
- No `filter`, `backdrop-filter` or blurred shadows in print CSS. They make Chromium rasterise the page. Use borders.
- Tables: `thead { display: table-header-group; }` repeats the header on every page; `tr { break-inside: avoid; }`.
- Headings: `break-after: avoid`. Totals and signature blocks: `break-inside: avoid`.
- Page numbers via Playwright `displayHeaderFooter` and `footerTemplate` with `<span class="pageNumber"></span> / <span class="totalPages"></span>`.
- Pass `tagged: true` to `page.pdf()` so the PDF carries a structure tree. Use real `<h1>`–`<h3>`, `<table>` with `<th scope="col">`, and `alt` on images.
- Dates, numbers and money through `Intl` with the document's locale (FE-008), not hand formatting.

### 5. The renderer is offline

The job gives Chromium finished HTML. Block every request except `file:` and `data:` with `page.route('**/*', …)`. Strip `<script>`, `<iframe>`, `<object>` and `on*` attributes from any user-supplied HTML. This closes SSRF through image URLs.

### 6. Invoice numbers are unique and sequential

§14 Abs. 4 Nr. 4 UStG requires a unique, sequential number. Allocate it from a counter row in the same transaction that writes the invoice:

```sql
UPDATE invoice_counters SET next_value = next_value + 1
WHERE series = $1 RETURNING next_value - 1 AS number;
```

Use the Payload transaction (`req.transactionID`; raw SQL through `payload.db.drizzle`). Do not use a Postgres `SEQUENCE`: sequences skip values on rollback. A series can carry a year prefix (`2026-000123`). Drafts have no number; the number is assigned on `issue`.

### 7. §14 UStG content

An invoice holds: supplier name and address, recipient name and address, supplier Steuernummer or USt-IdNr., issue date, invoice number, quantity and kind of goods or scope of service, time of supply, net amount per tax rate, tax rate and tax amount, and any agreed price reduction. Exempt or reverse-charge invoices carry the reason ("Steuerschuldnerschaft des Leistungsempfängers", or the §19 UStG note). Invoices up to 250 € gross may use the reduced content of §33 UStDV.

### 8. E-invoices for German B2B

- Since 1 January 2025 every German business must be able to receive e-invoices. Issuing becomes mandatory from 1 January 2027 for businesses with more than 800,000 € prior-year turnover, and for all from 1 January 2028. Small invoices (§33 UStDV) are exempt.
- An e-invoice is structured data following EN 16931. A plain PDF is not one.
- Formats: **XRechnung** (XML only, UBL or CII syntax; required for public-sector buyers, with Leitweg-ID) or **ZUGFeRD** 2.x / Factur-X at profile EN 16931 or higher (PDF/A-3 with embedded CII XML). Profiles MINIMUM and BASIC WL do not qualify.
- Build the XML from typed invoice data, not from the PDF. Validate it with the KoSIT validator (XRechnung) or Mustang (ZUGFeRD) in CI and in the job. An invalid file is not stored as issued.
- B2C invoices may stay PDF.

### 9. GoBD: issued means frozen

- An `invoices` collection has `status`: `draft` | `issued` | `cancelled`. A `beforeChange` hook refuses any change to an issued invoice except setting `cancelled` with a link to its credit note. `delete` access is `false` for everyone.
- Corrections are a new document: a cancellation invoice or credit note that references the original number.
- Store the issued file in a private upload collection on S3/R2, with its SHA-256 on the invoice record. For e-invoices store the XML in its original format; the XML is the legal document.
- Retention: invoices 8 years (§14b UStG, §147 AO as changed by the Bürokratieentlastungsgesetz IV, from 2025). Books and annual statements 10 years. A DSGVO erasure request does not delete invoices inside the retention period (Art. 17 Abs. 3 lit. b DSGVO); CL-004 records that.
- Write the steps (numbering, storage, correction) into `docs/compliance/verfahrensdokumentation.md`.

### 10. Golden-file tests

- Fixtures in `tests/documents/fixtures/*.json`. Expected outputs in `tests/documents/golden/`.
- Freeze clock, locale, time zone and fonts. Strip or fix PDF `CreationDate` and `ModDate`.
- Compare: page count, extracted text (`pdftotext -layout`), and the e-invoice XML (canonical diff). A pixel diff (`pdftoppm` plus a tolerance) is optional.
- Fixtures cover: one line, many lines across three pages, long names, reverse charge, §19 note, credit note.
- Updating a golden file needs a reason in the commit message.

## Workflow

1. Write the document spec in the architecture doc: fields, data source, locale, numbering series, format (PDF, XRechnung, ZUGFeRD), retention.
2. Build the template component and its preview route. Add fixtures.
3. Build the job: render, validate, hash, store, set status.
4. Add numbering and the GoBD hook before the first issued invoice.
5. Add golden tests and the validator step to CI.

## Deliverables

- Template component plus preview route
- Render job and private document collection
- `invoices` and `invoice_counters` with access and the freeze hook (when invoicing)
- E-invoice XML builder and validator step (German B2B)
- Golden fixtures and tests
- `docs/compliance/verfahrensdokumentation.md` section

## Done evidence (receipt)

`## Document proof` with PASS / FAIL / NOT TESTED:

- Golden tests green; list the fixtures
- `pdffonts` output shows every font embedded
- Page count of the three-page fixture, with the header repeated on page 2
- Validator output for the e-invoice fixture (KoSIT or Mustang), zero errors
- Two parallel issues in a test produce two consecutive numbers, no duplicate
- Update of an issued invoice is refused (status code and message)

## Anti-patterns

- `window.print()` or a request-time render
- A second HTML template for the PDF that drifts from the preview
- Fonts or images loaded from a third-party URL at render time
- Invoice numbers from `SEQUENCE`, `MAX(number) + 1` or a timestamp
- Editing or deleting an issued invoice
- Calling a ZUGFeRD MINIMUM file an e-invoice
- Snapshot tests that include the creation date

## Handoff

- **Consumes:** invoice data from BE-008 (Stripe model), locale and formatters from FE-008, storage adapter from BE-007.
- **Produces:** document IDs and download routes for FE; retention rows for CL-004; the document boundary for PE-005.

## References

- `knowledge-base/payload-playbook.md` (jobs, storage), BE-006, BE-007, BE-008, CL-001, CL-004
- UStG §§14, 14b; UStDV §33; AO §147; BMF letters on e-invoicing (2024, 2025); GoBD (BMF)
- EN 16931; XRechnung (KoSIT); ZUGFeRD / Factur-X (FeRD); Playwright `page.pdf()` docs
