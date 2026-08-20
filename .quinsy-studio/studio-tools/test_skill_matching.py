#!/usr/bin/env python3
"""
Quinsy Studio — Skill-Matching-Test

Prüft, ob Beispiel-Tickets korrekt auf interne Skills (Trigger-Wörter aus der
Skill-Registry) UND externe Skills (Mappings aus den Team-Skill-Dateien)
gemappt werden.

Verwendung:
    python3 test_skill_matching.py
"""

import re
import sys
from pathlib import Path

STUDIO_ROOT = Path(__file__).parent.parent.parent
TEAMS_DIR = STUDIO_ROOT / ".quinsy-studio" / "teams"
REGISTRY = TEAMS_DIR / "skill-registry.md"
EXTERNAL = STUDIO_ROOT / ".quinsy-studio" / "external-skills"

# =============================================================================
# Interne Skill-Trigger (aus der Skill-Registry)
# =============================================================================

INTERNAL_SKILLS = {
    "FE-001": {"name": "UI Component Design", "triggers": ["komponente", "component", "ui-element", "button", "card", "modal"]},
    "FE-002": {"name": "Design System", "triggers": ["design tokens", "farbpalette", "typografie", "theme", "dark mode"]},
    "FE-003": {"name": "Performance Optimization", "triggers": ["performance", "ladezeit", "speed", "bundle", "core web vitals"]},
    "FE-004": {"name": "Accessibility", "triggers": ["a11y", "barrierefreiheit", "accessibility", "wcag", "screenreader"]},
    "FE-005": {"name": "PWA Implementation", "triggers": ["pwa", "offline", "service worker", "manifest", "installierbar"]},
    "FE-006": {"name": "Frontend Testing", "triggers": ["test", "testing", "coverage", "unit-test", "e2e"]},
    "BE-001": {"name": "API Design", "triggers": ["api", "endpoint", "rest", "graphql", "http"]},
    "BE-002": {"name": "Database Design", "triggers": ["database", "schema", "migration", "query", "sql", "postgres"]},
    "BE-003": {"name": "Auth & Authorization", "triggers": ["auth", "login", "jwt", "session", "rbac", "oauth"]},
    "BE-004": {"name": "Error Handling", "triggers": ["error", "exception", "fehlerbehandlung", "retry", "logging"]},
    "BE-005": {"name": "Third-Party Integrations", "triggers": ["integration", "webhook", "stripe", "sendgrid", "payment"]},
    "CL-001": {"name": "DSGVO Compliance", "triggers": ["dsgvo", "gdpr", "datenschutz", "privacy"]},
    "CL-002": {"name": "Cookie Banner", "triggers": ["cookie", "consent", "banner", "tracking"]},
    "CL-003": {"name": "Impressum & AGB", "triggers": ["impressum", "agb", "nutzungsbedingungen", "widerruf"]},
    "CL-004": {"name": "Zero-Data Architecture", "triggers": ["zero-data", "datenminimierung", "löschkonzept", "avv"]},
    "PS-001": {"name": "Product Strategy", "triggers": ["strategie", "vision", "roadmap", "monetarisierung"]},
    "PS-002": {"name": "Architecture Decisions", "triggers": ["adr", "architektur", "tech-stack", "build vs buy"]},
    "PS-003": {"name": "Technology Evaluation", "triggers": ["evaluation", "framework", "library", "migration"]},
    "PS-004": {"name": "Feasibility Analysis", "triggers": ["machbarkeit", "feasibility", "risiko", "scope"]},
    "GM-001": {"name": "SEO Optimization", "triggers": ["seo", "sichtbarkeit", "ranking", "google", "schema.org"]},
    "GM-002": {"name": "AEO", "triggers": ["aeo", "ai search", "chatgpt", "perplexity", "vergleich"]},
    "GM-003": {"name": "Content Strategy", "triggers": ["content", "blog", "social", "newsletter", "tone of voice"]},
    "PM-001": {"name": "User Research", "triggers": ["research", "interview", "survey", "usability"]},
    "PM-002": {"name": "Roadmapping", "triggers": ["roadmap", "priorisierung", "planning", "moscow"]},
    "PM-003": {"name": "Operating Model", "triggers": ["operating model", "team-struktur", "prozess", "okr"]},
    "AI-001": {"name": "AI Integration", "triggers": ["ai", "llm", "gpt", "claude", "prompt", "ki-integration"]},
    "AI-002": {"name": "Anti-Slop Audit", "triggers": ["anti-slop", "slop", "ai-code", "code-qualität"]},
    "AI-003": {"name": "Automation Pipelines", "triggers": ["ci/cd", "pipeline", "automatisierung", "github actions"]},
    "PE-001": {"name": "Infrastructure", "triggers": ["infrastructure", "docker", "cloud", "deploy", "cdn"]},
    "PE-002": {"name": "CI/CD Pipelines", "triggers": ["ci/cd", "pipeline", "github actions", "build"]},
    "PE-003": {"name": "Security Audit", "triggers": ["security", "owasp", "penetration", "vulnerability"]},
    "PE-004": {"name": "Monitoring & Observability", "triggers": ["monitoring", "alerting", "uptime", "sentry"]},
    "SO-001": {"name": "Studio Tooling Maintenance", "triggers": ["studio tools", "python", "tooling", "wartung"]},
    "SO-002": {"name": "Process Optimization", "triggers": ["prozess", "sprint-disziplin", "optimierung", "metriken"]},
    "SO-003": {"name": "Dual-Loop Learning", "triggers": ["learning", "retro", "knowledge", "promotion", "dual-loop"]},
    "SO-004": {"name": "Documentation Governance", "triggers": ["doku", "documentation", "readme", "changelog"]},
    "GM-004": {"name": "Game Development", "triggers": ["game", "godot", "unity", "unreal", "platformer", "spiel", "phaser", "three.js", "pygame"]},
}

# =============================================================================
# Externe Skill-Mappings (Domain → externe Pfade)
# =============================================================================

EXTERNAL_MAPPINGS = {
    "FE-001": ["design/skills (hallmark audit)", "design_awesome/skills/<stil>", "all_domains/design-and-ui-ux/frontend-design"],
    "FE-002": ["design/skills (hallmark)", "design_awesome/skills/<stil>"],
    "GM-001": ["marketing_aeo/skills/seo-audit", "marketing_aeo/skills/schema", "marketing_aeo/skills/programmatic-seo", "marketing_aeo/skills/site-architecture"],
    "GM-002": ["marketing_aeo/skills/ai-seo", "marketing_aeo/skills/schema", "geo_visibility/SKILL.md", "marketing_aeo/skills/competitors"],
    "GM-003": ["marketing_aeo/skills/copywriting", "marketing_aeo/skills/content-strategy", "marketing_aeo/skills/product-marketing", "marketing_aeo/skills/customer-research", "marketing_aeo/skills/emails"],
    "CL-002": ["compliance_cookies/skills/cookiecomply"],
    "BE-002": ["all_domains/database/database-schema-design", "all_domains/database/query-optimization", "all_domains/database/database-migration"],
    "PE-003": ["all_domains/security/security-audit", "all_domains/security/threat-modeling", "all_domains/security/dependency-scanning"],
    "PE-001": ["all_domains/devops-and-infrastructure/docker-compose-setup", "all_domains/devops-and-infrastructure/infrastructure-as-code"],
    "BE-001": ["all_domains/api-and-integration/api-design", "all_domains/api-and-integration/oauth-2-0-setup"],
    "CL-001": ["all_domains/legal-and-compliance/compliance-checklist-generation", "all_domains/legal-and-compliance/privacy-policy-drafting"],
    "PM-002": ["all_domains/productivity-and-workflow/project-management"],
    "GM-004": ["gamedev (Router: Engine + Task)"],
}

# =============================================================================
# Beispiel-Tickets
# =============================================================================

TEST_TICKETS = [
    {
        "id": "NUDG-1001",
        "title": "Landing Page mit neuem Design-System und Typografie",
        "text": "Landing Page bauen: Design Tokens, Farbpalette, Typografie, Dark Mode. Komponenten: Button, Card, Modal. Hallmark-Design gegen AI-Slop prüfen.",
        "expect_internal": ["FE-002", "FE-001"],
        "expect_external": ["design/skills", "design_awesome"],
    },
    {
        "id": "NUDG-1002",
        "title": "SEO-Audit und AEO-Optimierung für AI-Search",
        "text": "SEO-Audit durchführen: Sichtbarkeit, Ranking, Schema.org. AEO: ChatGPT und Perplexity Zitate, Vergleichsseiten. pSEO-Architektur.",
        "expect_internal": ["GM-001", "GM-002"],
        "expect_external": ["marketing_aeo/skills/ai-seo", "marketing_aeo/skills/seo-audit", "geo_visibility"],
    },
    {
        "id": "NUDG-1003",
        "title": "Cookie-Banner mit DSGVO-Compliance",
        "text": "Cookie-Banner implementieren: Consent, Tracking-Opt-in, DSGVO, Datenschutz. Widerruf-Möglichkeit.",
        "expect_internal": ["CL-002", "CL-001"],
        "expect_external": ["cookiecomply"],
    },
    {
        "id": "NUDG-1004",
        "title": "PostgreSQL Schema und Query-Optimierung",
        "text": "Database Schema entwerfen: Migration, Query, SQL, Indexierung für PostgreSQL.",
        "expect_internal": ["BE-002"],
        "expect_external": ["database-schema-design"],
    },
    {
        "id": "NUDG-1005",
        "title": "Security-Audit vor Release",
        "text": "Security-Audit: OWASP, Penetration, Vulnerability-Scan, Dependency-Scanning.",
        "expect_internal": ["PE-003"],
        "expect_external": ["security-audit", "threat-modeling"],
    },
    {
        "id": "NUDG-1006",
        "title": "Godot 2D Platformer mit Double Jump",
        "text": "Game bauen: Godot 2D Bewegung, Platformer-Level, Tilemap.",
        "expect_internal": ["GM-004"],
        "expect_external": ["gamedev"],
    },
    {
        "id": "NUDG-1007",
        "title": "Copywriting für Pricing-Seite",
        "text": "Copywriting: Conversion-Copy für Pricing, Angebot, Newsletter-Sequenz. Content-Strategie.",
        "expect_internal": ["GM-003"],
        "expect_external": ["marketing_aeo/skills/copywriting"],
    },
]


def match_internal(text: str) -> list:
    """Matcht ein Ticket gegen interne Trigger-Wörter."""
    t = text.lower()
    hits = []
    for skill_id, skill in INTERNAL_SKILLS.items():
        for trigger in skill["triggers"]:
            if trigger in t:
                hits.append(skill_id)
                break
    return hits


def match_external(internal_hits: list) -> list:
    """Liefert externe Skills für gematchte interne Skills."""
    ext = []
    for sid in internal_hits:
        for e in EXTERNAL_MAPPINGS.get(sid, []):
            if e not in ext:
                ext.append(e)
    return ext


def verify_external_on_disk(ext_path: str) -> bool:
    """Prüft, ob die externe Quelle tatsächlich auf Disk existiert."""
    # Spezialfälle: generische Mappings, die keine konkrete Datei bezeichnen
    if any(s in ext_path for s in ["skills (hallmark", "skills/<", "(Router:", "SKILL.md"]):
        # Domain ist das erste Wort (z.B. "gamedev (Router: ...)" → gamedev)
        domain = ext_path.split("/")[0].split()[0]
        return (EXTERNAL / domain).exists()

    # Normalisiere Pfad (z.B. "marketing_aeo/skills/ai-seo" → external-skills/marketing_aeo/skills/ai-seo)
    parts = ext_path.split("/")
    domain = parts[0]
    rest = "/".join(parts[1:])
    base = EXTERNAL / domain
    if not base.exists():
        return False
    if not rest:
        return True
    # Prüfe ob irgendein Pfad-Präfix existiert (case-insensitive)
    current = base
    for part in rest.split("/"):
        candidates = [p for p in current.iterdir() if p.name.lower().startswith(part.lower())] if current.exists() else []
        if not candidates:
            return False
        current = candidates[0]
    return True


def main():
    print("=" * 62)
    print("  QUINSY STUDIO — SKILL-MATCHING-TEST")
    print("=" * 62)

    total = 0
    passed = 0
    ext_checked = 0
    ext_ok = 0

    for ticket in TEST_TICKETS:
        total += 1
        text = f"{ticket['title']} {ticket['text']}"
        internal_hits = match_internal(text)
        external_hits = match_external(internal_hits)

        exp_in = set(ticket["expect_internal"])
        exp_ext = set(ticket["expect_external"])
        got_in = set(internal_hits)
        got_ext = set(external_hits)

        in_ok = exp_in.issubset(got_in)
        # Substring-basierter Check: erwarteter externer Skill muss in einem
        # gematchten externen Skill stecken (z.B. "ai-seo" ∈ "marketing_aeo/skills/ai-seo")
        ext_ok_this = all(
            any(exp in e for e in got_ext) for exp in exp_ext
        )
        ok = in_ok and ext_ok_this

        print(f"\n  [{ticket['id']}] {ticket['title']}")
        print(f"    Intern:  {'✓' if in_ok else '✗'} {sorted(got_in)} (erwartet {sorted(exp_in)})")
        print(f"    Extern:  {'✓' if ext_ok_this else '✗'} {sorted(got_ext)} (erwartet {sorted(exp_ext)})")

        # Externe Quellen auf Disk prüfen
        for e in sorted(got_ext):
            ext_checked += 1
            on_disk = verify_external_on_disk(e)
            if on_disk:
                ext_ok += 1
            print(f"    Disk:    {'✓' if on_disk else '✗'} {e}")

        if ok:
            passed += 1

    print("\n" + "=" * 62)
    print(f"  ERGEBNIS: {passed}/{total} Tickets korrekt gematcht")
    print(f"  Externe Quellen auf Disk: {ext_ok}/{ext_checked}")
    if passed == total and ext_ok == ext_checked:
        print("  ✅ ALLE TESTS BESTANDEN")
    else:
        print("  ❌ TESTS FEHLGESCHLAGEN")
    print("=" * 62)

    return 0 if (passed == total and ext_ok == ext_checked) else 1


if __name__ == "__main__":
    sys.exit(main())
