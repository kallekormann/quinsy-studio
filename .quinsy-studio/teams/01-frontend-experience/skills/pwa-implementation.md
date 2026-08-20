# Skill: PWA Implementation

> Service Worker, Offline-Unterstützung, Web App Manifest, Push Notifications

## Metadata

```
skill_id: FE-005
name: PWA Implementation
team: 01-frontend-experience
lead_role: Frontend Architect
support_roles: [Frontend Engineer, Platform Architect]
phases: [3, 4, 5]
activation_triggers:
  - Ticket enthält "PWA", "Offline", "Service Worker", "Installierbar"
  - Archetyp erfordert PWA (saas-application)
  - Phase 3 plant Offline-Support
```

---

## Verhaltensregeln

### 1. Web App Manifest

```markdown
Pflichtfelder:
  - name: Vollständiger Name
  - short_name: Name auf Homescreen
  - start_url: /
  - display: standalone
  - background_color: Theme-Background
  - theme_color: Theme-Primary
  - icons: 192x192 + 512x512 (mindestens)
```

### 2. Service Worker Strategie

```markdown
Cache-Strategien nach Ressource-Typ:

Statische Assets (JS, CSS, Fonts):
  → Cache-First (schnell, zuverlässig)
  → Cache-Name: "static-v{version}"
  → TTL: 1 Jahr (immutable)

Bilder:
  → Cache-First mit Network-Fallback
  → Cache-Name: "images-v{version}"
  → TTL: 30 Tage

API Calls:
  → Network-First mit Cache-Fallback
  → Cache-Name: "api-v{version}"
  → TTL: 5 Minuten

HTML (Navigation):
  → Network-First mit Offline-Fallback
  → Offline-Fallback: /offline.html
```

### 3. Offline-Unterstützung

```markdown
Pflicht-Offline-Szenarien:
  - App-Shell ist immer verfügbar
  - Letzte gespeicherte Daten sind sichtbar
  - Offline-Hinweis wird angezeigt
  - Background Sync für Queue

Nice-to-have:
  - Offline-Formular-Submission (Queue)
  - Offline-Suche in cache-Inhalten
```

### 4. Update-Management

```markdown
Service Worker Update:
  - New Worker installiert → Wait
  -SKIP_WAITING nur bei User-Interaction
  - Update-Banner anzeigen
  - Cache-Invalidierung bei Version-Update
```

---

## Anti-Patterns

### ❌ Verboten

```markdown
- Service Worker ohne Update-Strategie
- Alles in einem Cache (keine Trennung)
- Kein Offline-Fallback
- Cache ohne Versionierung
- PUSH-Notifications ohne explizite Zustimmung
```

### ✅ Stattdessen

```markdown
- Versionierte Caches pro Ressource-Typ
- Network-First für dynamische Inhalte
- Offline-Fallback-Page
- Background Sync für Offline-Aktionen
- Granulare Cache-Strategien
```

---

## Referenzen

- `.quinsy-studio/knowledge-base/frontend_playbook.md` — Frontend-Regeln
- `templates/docker/` — Docker-Setup
