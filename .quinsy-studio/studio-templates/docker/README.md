# Docker-Basis-Template

Dieses Verzeichnis enthält das **Basis-Docker-Template** des Studios mit den Essentials
(PostgreSQL, Redis, optionaler App-Service). Es wird beim Projekt-Setup als Grundlage
in den Projektordner kopiert und dort projektspezifisch erweitert.

## Ablauf (Base → Project)

1. **Studio hält die Essentials:** `docker-compose.yml`, `.env.example` — generisch,
   parametrisiert mit `{{PROJECT_NAME}}`.
2. **Projekt-Setup kopiert die Basis:** `./studio env <project> init` (oder
   `python3 .quinsy-studio/studio-tools/init_project_env.py <project>`)
   → Ergebnis: `projects/<name>/docker/docker-compose.yml` + `.env.example`
   mit dem echten Projektnamen.
3. **Projekt erweitert NUR im Projektordner:** Zusätzliche Services (Mailpit, MinIO,
   Queue-Worker), Build-Kontexte, eigene Volumes gehören nach
   `projects/<name>/docker/` — das Template bleibt generisch.

## Platzhalter

| Platzhalter       | Ersetzt durch          |
|-------------------|------------------------|
| `{{PROJECT_NAME}}` | Projektname            |

## Regeln

- **NIEMALS** projektspezifische Config ins Template committen.
- **Keine** festen Passwörter/Secrets im Template (nur Dev-Defaults, via `.env` überschreibbar).
- Wenn ein Projekt eine Verbesserung braucht, die *universell* nützlich ist
  (z.B. ein Healthcheck, ein neuer Basis-Service) → Template aktualisieren
  (Global Loop), nicht nur das Projekt (Local Loop).
