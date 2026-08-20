# Quinsy Studio — Projekt-Archetypen

> Jeder Archetyp definiert eine spezifische Projektstruktur, Technologie-Stack und Prozess-Anpassungen.

## Archetyp-Übersicht

| Archetyp | Beschreibung | Komplexität | Stack |
|----------|-------------|-------------|-------|
| `saas-application` | B2C/B2B SaaS-Produkt | P0–P3 | Next.js, Tailwind, Supabase |
| `ecommerce` | Online-Shop | P1–P3 | Shopify, Medusa, WooCommerce |
| `content-platform` | Content-Management, Blog, Magazin | P0–P2 | WordPress, Strapi, Sanity |
| `marketplace` | Zweiseitiger Markt (Buyer/Seller) | P2–P3 | Custom, Medusa, Sharetribe |
| `internal-tool` | Interne Dashboards, Admin-Tools | P0–P1 | Retool, Next.js, Postgres |
| `api-service` | Backend-API, Microservice | P1–P2 | Node.js, Go, Rust |
| `mobile-app` | Native/Hybrid Mobile App | P1–P3 | React Native, Flutter |
| `prototype` | Schneller Prototyp, MVP | P0 | Varies |

---

## 1. saas-application

### Profil

```
Archetyp: SaaS (Software as a Service)
Typ: B2C Micro-SaaS oder B2B Enterprise
Ziel: Subscription-basiertes Produkt
```

### Stack-Empfehlung

```
Frontend:    Next.js 14+ (App Router), Tailwind CSS, shadcn/ui
Backend:     Next.js API Routes / Server Actions
Datenbank:   PostgreSQL (Supabase / Neon / Railway)
Auth:        Supabase Auth / Clerk / NextAuth.js
Storage:     Supabase Storage / Cloudflare R2
Deployment:  Vercel / Railway / Fly.io
CI/CD:       GitHub Actions
```

### Prozess-Anpassungen

- **Phase 0:** Archetyp-Checkliste ausfüllen
- **Phase 1:** Subscription-Modell definieren (Free/Pro/Enterprise)
- **Phase 2:** Auth-Architektur (RBAC, Multi-Tenant)
- **Phase 3:** Design System (Tokens, Komponenten)
- **Phase 4:** TDD mit Fokus auf User-Flows
- **Phase 5:** DSGVO-konform (Cookie-Banner, Datenschutz)
- **Phase 6:** Staging → Production
- **Phase 7:** Metriken (Retention, MRR, Churn)

### Gate-Anpassungen

| Gate | Spezifische Prüfungen |
|------|----------------------|
| Gate 0 | Subscription-Modell definiert |
| Gate 1 | Pricing validiert |
| Gate 2 | Multi-Tenant-Architektur |
| Gate 3 | Design System mit Tokens |
| Gate 5 | DSGVO-Check, Cookie-Banner |

---

## 2. ecommerce

### Profil

```
Archetyp: Online-Shop
Typ: D2C, B2C, B2B
Ziel: Produktverkauf, Conversion-Optimierung
```

### Stack-Empfehlung

```
Frontend:    Next.js 14+ / Shopify Hydrogen
Backend:     Shopify / Medusa / WooCommerce
Datenbank:   PostgreSQL / MySQL
Payment:     Stripe / PayPal / Klarna
Storage:     Shopify CDN / Cloudflare R2
Deployment:  Vercel / Shopify Hosting
```

### Prozess-Anpassungen

- **Phase 0:** Produktkatalog definieren
- **Phase 1:** Payment-Integration evaluieren
- **Phase 2:** Produkt-Datenmodell, Bestandsverwaltung
- **Phase 3:** Produktseiten, Checkout-Flow
- **Phase 4:** Performance (Core Web Vitals kritisch)
- **Phase 5:** PCI-DSS, DSGVO, Cookie-Banner
- **Phase 6:** Launch mit Monitoring
- **Phase 7:** Conversion-Tracking, A/B-Testing

---

## 3. content-platform

### Profil

```
Archetyp: Content-Management
Typ: Blog, Magazin, Dokumentation
Ziel: Content erstellen und verbreiten
```

### Stack-Empfehlung

```
CMS:         WordPress / Strapi / Sanity / Contentful
Frontend:    Next.js 14+ (ISR) / Astro
Datenbank:   PostgreSQL / MySQL
Storage:     Cloudflare R2 / S3
Deployment:  Vercel / Netlify
```

### Prozess-Anpassungen

- **Phase 0:** Content-Strategie definieren
- **Phase 1:** CMS evaluieren (Headless vs. Traditional)
- **Phase 2:** Content-Modell, Taxonomie
- **Phase 3:** Seitentypen, Templates
- **Phase 4:** SEO-Optimierung, Performance
- **Phase 5:** DSGVO (Kommentare, Newsletter)
- **Phase 6:** Content-Migration
- **Phase 7:** Analytics, SEO-Monitoring

---

## 4. marketplace

### Profil

```
Archetyp: Zweiseitiger Markt
Typ: C2C, B2C, B2B
Ziel: Anbieter und Nachfrager zusammenbringen
```

### Stack-Empfehlung

```
Frontend:    Next.js 14+ / React
Backend:     Node.js / Ruby on Rails
Datenbank:   PostgreSQL
Search:      Elasticsearch / Algolia
Payment:     Stripe Connect
Deployment:  AWS / GCP / Railway
```

### Prozess-Anpassungen

- **Phase 0:** Marktmechanismen definieren (Matching, Pricing)
- **Phase 1:** Chicken-and-Egg-Problem analysieren
- **Phase 2:** User-Rollen (Buyer, Seller, Admin)
- **Phase 3:** Listings, Search, Checkout
- **Phase 4:** Trust & Safety, Reviews
- **Phase 5:** Payment-Compliance, DSGVO
- **Phase 6:** Soft Launch mit Beta-Usern
- **Phase 7:** Netzwerk-Effekte monitoren

---

## 5. internal-tool

### Profil

```
Archetyp: Internes Tool
Typ: Dashboard, Admin, CRM
Ziel: Interne Prozesse effizienter machen
```

### Stack-Empfehlung

```
Frontend:    Next.js / Retool / Tooljet
Backend:     Next.js API Routes
Datenbank:   PostgreSQL / Supabase
Auth:        LDAP / SSO / NextAuth.js
Deployment:  Internal / Vercel
```

### Prozess-Anpassungen

- **Phase 0:** User-Flows definieren
- **Phase 1:** Bestehende Tools evaluieren
- **Phase 2:** Einfache Architektur
- **Phase 3:** Funktionalität > Design
- **Phase 4:** TDD, aber weniger strikt
- **Phase 5:** Interne Security-Policies
- **Phase 6:** Internes Deployment
- **Phase 7:** User-Feedback

---

## 6. api-service

### Profil

```
Archetyp: Backend-API
Typ: REST, GraphQL, gRPC
Ziel: Service für andere Anwendungen
```

### Stack-Empfehlung

```
Runtime:     Node.js / Go / Rust / Python
Framework:   Express / Fastify / Gin / Axum
Datenbank:   PostgreSQL / MongoDB
Cache:       Redis
Docs:        OpenAPI / GraphQL Schema
Deployment:  Docker / Kubernetes / Railway
```

### Prozess-Anpassungen

- **Phase 0:** API-Kontrakt definieren
- **Phase 1:** Last-Testing
- **Phase 2:** API-Design (REST/GraphQL)
- **Phase 3:** SDK/Client-Generierung
- **Phase 4:** TDD mit Fokus auf Integration
- **Phase 5:** Security-Audit, Rate-Limiting
- **Phase 6:** Versioning, Deprecation-Policy
- **Phase 7:** Monitoring, SLA

---

## 7. mobile-app

### Profil

```
Archetyp: Mobile Anwendung
Typ: Native, Hybrid, PWA
Ziel: App-Store-Produkt
```

### Stack-Empfehlung

```
Framework:   React Native / Flutter / Swift/Kotlin
Backend:     Node.js / Firebase / Supabase
Datenbank:   PostgreSQL / Firestore
Auth:        Firebase Auth / Supabase Auth
Deployment:  App Store / Play Store / EAS
```

### Prozess-Anpassungen

- **Phase 0:** Plattform-Strategie (iOS/Android/Beide)
- **Phase 1:** App-Store-Richtlinien prüfen
- **Phase 2:** Offline-First-Architektur
- **Phase 3:** Native Look & Feel
- **Phase 4:** Performance (60 FPS kritisch)
- **Phase 5:** App-Store-Review, DSGVO
- **Phase 6:** Beta-Testing (TestFlight)
- **Phase 7:** Crash-Reporting, Analytics

---

## 8. prototype

### Profil

```
Archetyp: Schneller Prototyp
Typ: MVP, Proof of Concept
Ziel: Idee validieren
```

### Stack-Empfehlung

```
Frontend:    Next.js / Vite / CodeSandbox
Backend:     Serverless / Supabase
Datenbank:   Supabase / Firebase
Deployment:  Vercel / Netlify
```

### Prozess-Anpassungen

- **Phase 0:** Minimale Anforderungen
- **Phase 1:** Quick & Dirty Validierung
- **Phase 2:** Vereinfachte Architektur
- **Phase 3:** Schnelles Design
- **Phase 4:** Code > Tests (Temporär)
- **Phase 5:** Minimale QA
- **Phase 6:** Sofortiges Deployment
- **Phase 7:** Lernen, nicht optimieren

---

## Archetyp-Wahl

```bash
# Archetyp bei Projektstart setzen
./studio init <project> --archetype saas-application

# Archetyp ändern (erfordert ADR)
./studio set-archetype <project> ecommerce
```

---

## Archetyp-Checkliste (Phase 0)

```markdown
# Archetyp-Checkliste — <Project>

## Gewählter Archetyp: [saas-application]

- [ ] Archetyp definiert
- [ ] Komplexitäts-Level geschätzt
- [ ] Stack-Empfehlung überprüft
- [ ] Prozess-Anpassungen notiert
- [ ] Gate-Anpassungen dokumentiert
```

---

## Referenzen

- `.quinsy-studio/process/lifecycle.md` — Phasen
- `./studio init <project> --archetype <type>` — Projekt initialisieren
