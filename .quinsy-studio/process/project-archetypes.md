# Quinsy Studio — Project Archetypes

> Every archetype defines a specific project structure, technology stack and process adjustments.

## Archetype overview

| Archetype | Description | Complexity | Stack |
|-----------|-------------|------------|-------|
| `saas-application` | B2C/B2B SaaS product | P0–P3 | Next.js, Tailwind, Supabase |
| `ecommerce` | Online shop | P1–P3 | Shopify, Medusa, WooCommerce |
| `content-platform` | Content management, blog, magazine | P0–P2 | WordPress, Strapi, Sanity |
| `marketplace` | Two-sided market (buyer/seller) | P2–P3 | custom, Medusa, Sharetribe |
| `internal-tool` | Internal dashboards, admin tools | P0–P1 | Retool, Next.js, Postgres |
| `api-service` | Backend API, microservice | P1–P2 | Node.js, Go, Rust |
| `mobile-app` | Native/hybrid mobile app | P1–P3 | React Native, Flutter |
| `prototype` | Quick prototype, MVP | P0 | varies |

---

## 1. saas-application

### Profile

```
Archetype: SaaS (software as a service)
Type: B2C micro-SaaS or B2B enterprise
Goal: subscription-based product
```

### Stack recommendation

```
Frontend:    Next.js 14+ (App Router), Tailwind CSS, shadcn/ui
Backend:     Next.js API routes / server actions
Database:    PostgreSQL (Supabase / Neon / Railway)
Auth:        Supabase Auth / Clerk / NextAuth.js
Storage:     Supabase Storage / Cloudflare R2
Deployment:  Vercel / Railway / Fly.io
CI/CD:       GitHub Actions
```

### Process adjustments

- **Phase 0:** fill out the archetype checklist
- **Phase 1:** define the subscription model (free/pro/enterprise)
- **Phase 2:** auth architecture (RBAC, multi-tenant)
- **Phase 3:** design system (tokens, components)
- **Phase 4:** TDD focused on user flows
- **Phase 5:** GDPR compliant (cookie banner, privacy)
- **Phase 6:** staging → production
- **Phase 7:** metrics (retention, MRR, churn)

### Gate adjustments

| Gate | Specific checks |
|------|-----------------|
| Gate 0 | subscription model defined |
| Gate 1 | pricing validated |
| Gate 2 | multi-tenant architecture |
| Gate 3 | design system with tokens |
| Gate 5 | GDPR check, cookie banner |

---

## 2. ecommerce

### Profile

```
Archetype: online shop
Type: D2C, B2C, B2B
Goal: product sales, conversion optimization
```

### Stack recommendation

```
Frontend:    Next.js 14+ / Shopify Hydrogen
Backend:     Shopify / Medusa / WooCommerce
Database:    PostgreSQL / MySQL
Payment:     Stripe / PayPal / Klarna
Storage:     Shopify CDN / Cloudflare R2
Deployment:  Vercel / Shopify Hosting
```

### Process adjustments

- **Phase 0:** define the product catalog
- **Phase 1:** evaluate the payment integration
- **Phase 2:** product data model, inventory management
- **Phase 3:** product pages, checkout flow
- **Phase 4:** performance (core web vitals critical)
- **Phase 5:** PCI-DSS, GDPR, cookie banner
- **Phase 6:** launch with monitoring
- **Phase 7:** conversion tracking, A/B testing

---

## 3. content-platform

### Profile

```
Archetype: content management
Type: blog, magazine, documentation
Goal: create and distribute content
```

### Stack recommendation

```
CMS:         WordPress / Strapi / Sanity / Contentful
Frontend:    Next.js 14+ (ISR) / Astro
Database:    PostgreSQL / MySQL
Storage:     Cloudflare R2 / S3
Deployment:  Vercel / Netlify
```

### Process adjustments

- **Phase 0:** define the content strategy
- **Phase 1:** evaluate the CMS (headless vs. traditional)
- **Phase 2:** content model, taxonomy
- **Phase 3:** page types, templates
- **Phase 4:** SEO optimization, performance
- **Phase 5:** GDPR (comments, newsletter)
- **Phase 6:** content migration
- **Phase 7:** analytics, SEO monitoring

---

## 4. marketplace

### Profile

```
Archetype: two-sided market
Type: C2C, B2C, B2B
Goal: bring suppliers and demanders together
```

### Stack recommendation

```
Frontend:    Next.js 14+ / React
Backend:     Node.js / Ruby on Rails
Database:    PostgreSQL
Search:      Elasticsearch / Algolia
Payment:     Stripe Connect
Deployment:  AWS / GCP / Railway
```

### Process adjustments

- **Phase 0:** define the market mechanisms (matching, pricing)
- **Phase 1:** analyze the chicken-and-egg problem
- **Phase 2:** user roles (buyer, seller, admin)
- **Phase 3:** listings, search, checkout
- **Phase 4:** trust & safety, reviews
- **Phase 5:** payment compliance, GDPR
- **Phase 6:** soft launch with beta users
- **Phase 7:** monitor network effects

---

## 5. internal-tool

### Profile

```
Archetype: internal tool
Type: dashboard, admin, CRM
Goal: make internal processes more efficient
```

### Stack recommendation

```
Frontend:    Next.js / Retool / Tooljet
Backend:     Next.js API routes
Database:    PostgreSQL / Supabase
Auth:        LDAP / SSO / NextAuth.js
Deployment:  internal / Vercel
```

### Process adjustments

- **Phase 0:** define the user flows
- **Phase 1:** evaluate existing tools
- **Phase 2:** simple architecture
- **Phase 3:** functionality > design
- **Phase 4:** TDD, but less strict
- **Phase 5:** internal security policies
- **Phase 6:** internal deployment
- **Phase 7:** user feedback

---

## 6. api-service

### Profile

```
Archetype: backend API
Type: REST, GraphQL, gRPC
Goal: service for other applications
```

### Stack recommendation

```
Runtime:     Node.js / Go / Rust / Python
Framework:   Express / Fastify / Gin / Axum
Database:    PostgreSQL / MongoDB
Cache:       Redis
Docs:        OpenAPI / GraphQL schema
Deployment:  Docker / Kubernetes / Railway
```

### Process adjustments

- **Phase 0:** define the API contract
- **Phase 1:** load testing
- **Phase 2:** API design (REST/GraphQL)
- **Phase 3:** SDK/client generation
- **Phase 4:** TDD focused on integration
- **Phase 5:** security audit, rate limiting
- **Phase 6:** versioning, deprecation policy
- **Phase 7:** monitoring, SLA

---

## 7. mobile-app

### Profile

```
Archetype: mobile application
Type: native, hybrid, PWA
Goal: app-store product
```

### Stack recommendation

```
Framework:   React Native / Flutter / Swift/Kotlin
Backend:     Node.js / Firebase / Supabase
Database:    PostgreSQL / Firestore
Auth:        Firebase Auth / Supabase Auth
Deployment:  App Store / Play Store / EAS
```

### Process adjustments

- **Phase 0:** platform strategy (iOS/Android/both)
- **Phase 1:** check app-store guidelines
- **Phase 2:** offline-first architecture
- **Phase 3:** native look & feel
- **Phase 4:** performance (60 FPS critical)
- **Phase 5:** app-store review, GDPR
- **Phase 6:** beta testing (TestFlight)
- **Phase 7:** crash reporting, analytics

---

## 8. prototype

### Profile

```
Archetype: quick prototype
Type: MVP, proof of concept
Goal: validate the idea
```

### Stack recommendation

```
Frontend:    Next.js / Vite / CodeSandbox
Backend:     serverless / Supabase
Database:    Supabase / Firebase
Deployment:  Vercel / Netlify
```

### Process adjustments

- **Phase 0:** minimal requirements
- **Phase 1:** quick & dirty validation
- **Phase 2:** simplified architecture
- **Phase 3:** fast design
- **Phase 4:** code > tests (temporary)
- **Phase 5:** minimal QA
- **Phase 6:** immediate deployment
- **Phase 7:** learn, don't optimize

---

## Archetype selection

```bash
# Set the archetype at project start
./studio init <project> --archetype saas-application

# Change the archetype (requires an ADR)
./studio set-archetype <project> ecommerce
```

---

## Archetype checklist (phase 0)

```markdown
# Archetype Checklist — <Project>

## Selected archetype: [saas-application]

- [ ] Archetype defined
- [ ] Complexity level estimated
- [ ] Stack recommendation reviewed
- [ ] Process adjustments noted
- [ ] Gate adjustments documented
```

---

## References

- `.quinsy-studio/process/lifecycle.md` — phases
- `./studio init <project> --archetype <type>` — initialize a project
