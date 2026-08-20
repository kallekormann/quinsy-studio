# Skill: PWA Implementation

> Service worker, offline support, web app manifest, push notifications

## Metadata

```
skill_id: FE-005
name: PWA Implementation
team: 01-frontend-experience
lead_role: Frontend Architect
support_roles: [Frontend Engineer, Platform Architect]
phases: [3, 4, 5]
activation_triggers:
  - Ticket contains "PWA", "offline", "service worker", "installable"
  - Archetype requires PWA (saas-application)
  - Phase 3 plans offline support
```

---

## Verhaltensregeln

### 1. Web app manifest

```markdown
Required fields:
  - name: full name
  - short_name: name on home screen
  - start_url: /
  - display: standalone
  - background_color: theme background
  - theme_color: theme primary
  - icons: 192x192 + 512x512 (at least)
```

### 2. Service worker strategy

```markdown
Cache strategies by resource type:

Static assets (JS, CSS, fonts):
  → cache-first (fast, reliable)
  → cache name: "static-v{version}"
  → TTL: 1 year (immutable)

Images:
  → cache-first with network fallback
  → cache name: "images-v{version}"
  → TTL: 30 days

API calls:
  → network-first with cache fallback
  → cache name: "api-v{version}"
  → TTL: 5 minutes

HTML (navigation):
  → network-first with offline fallback
  → offline fallback: /offline.html
```

### 3. Offline support

```markdown
Required offline scenarios:
  - App shell is always available
  - Last saved data is visible
  - Offline notice is shown
  - Background sync for queue

Nice-to-have:
  - Offline form submission (queue)
  - Offline search in cached content
```

### 4. Update management

```markdown
Service worker update:
  - new worker installed → wait
  - SKIP_WAITING only on user interaction
  - show an update banner
  - cache invalidation on version update
```

---

## Anti-Patterns

### ❌ Forbidden

```markdown
- Service worker without an update strategy
- Everything in one cache (no separation)
- No offline fallback
- Cache without versioning
- Push notifications without explicit consent
```

### ✅ Instead

```markdown
- Versioned caches per resource type
- Network-first for dynamic content
- Offline fallback page
- Background sync for offline actions
- Granular cache strategies
```

---

## References

- `.quinsy-studio/knowledge-base/frontend_playbook.md` — frontend rules
- `templates/docker/` — docker setup
