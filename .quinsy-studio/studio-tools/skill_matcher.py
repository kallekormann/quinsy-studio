#!/usr/bin/env python3
"""
skill_matcher.py — Single source of truth for internal skill matching.

Used by studio.py, generate_ticket_manifest.py, and test_skill_matching.py.
Trigger words align with .quinsy-studio/teams/skill-registry.md.
"""

from typing import Dict, List

INTERNAL_SKILLS: Dict[str, Dict] = {
    "FE-001": {"name": "UI Component Design", "triggers": [
        "component", "ui-element", "button", "card", "modal", "ui", "interface", "komponente", "form"
    ]},
    "FE-002": {"name": "Design System", "triggers": [
        "design system", "design tokens", "color palette", "typography", "theme", "dark mode",
        "tokens", "palette", "farbpalette", "typografie"
    ]},
    "FE-003": {"name": "Performance Optimization", "triggers": [
        "performance", "load time", "speed", "bundle", "core web vitals", "ladezeit", "cache"
    ]},
    "FE-004": {"name": "Accessibility", "triggers": [
        "a11y", "accessibility", "wcag", "screenreader", "screen reader", "barrierefreiheit"
    ]},
    "FE-005": {"name": "PWA Implementation", "triggers": [
        "pwa", "offline", "service worker", "manifest", "installable"
    ]},
    "FE-006": {"name": "Frontend Testing", "triggers": [
        "test", "testing", "coverage", "unit-test", "e2e"
    ]},
    "FE-007": {"name": "Client Security", "triggers": [
        "client security", "content-security-policy", "csp header", "frontend security"
    ]},
    "BE-001": {"name": "API Design", "triggers": [
        "api", "endpoint", "rest", "graphql", "http"
    ]},
    "BE-002": {"name": "Database Design", "triggers": [
        "database", "schema", "migration", "query", "sql", "postgres"
    ]},
    "BE-003": {"name": "Auth & Authorization", "triggers": [
        "auth", "login", "jwt", "session", "rbac", "oauth"
    ]},
    "BE-004": {"name": "Error Handling", "triggers": [
        "error", "exception", "retry", "logging"
    ]},
    "BE-005": {"name": "Third-Party Integrations", "triggers": [
        "integration", "webhook", "stripe", "sendgrid", "payment"
    ]},
    "BE-006": {"name": "Jobs and Delivery", "triggers": [
        "queue", "worker", "outbox", "bullmq", "background job"
    ]},
    "CL-001": {"name": "GDPR Compliance", "triggers": [
        "gdpr", "dsgvo", "data protection", "privacy", "datenschutz",
        "ccpa", "click-wrap", "consent log", "right to be forgotten"
    ]},
    "CL-002": {"name": "Cookie Banner", "triggers": [
        "cookie", "consent", "banner", "tracking"
    ]},
    "CL-003": {"name": "Imprint & ToS", "triggers": [
        "imprint", "terms of service", "tos", "withdrawal", "impressum", "agb", "widerruf",
        "eula", "subscription agreement"
    ]},
    "CL-004": {"name": "Zero-Data Architecture", "triggers": [
        "zero-data", "data minimization", "deletion concept", "dpa", "datenminimierung"
    ]},
    "PS-001": {"name": "Product Strategy", "triggers": [
        "strategy", "vision", "roadmap", "monetization", "strategie", "monetarisierung"
    ]},
    "PS-002": {"name": "Architecture Decisions", "triggers": [
        "adr", "architecture", "tech-stack", "build vs buy", "architektur", "tech stack"
    ]},
    "PS-003": {"name": "Technology Evaluation", "triggers": [
        "evaluation", "framework", "library"
    ]},
    "PS-004": {"name": "Feasibility Analysis", "triggers": [
        "feasibility", "risk", "scope"
    ]},
    "GM-001": {"name": "SEO Optimization", "triggers": [
        "seo", "visibility", "ranking", "google", "schema.org", "sichtbarkeit",
        "affiliate", "sponsored", "nofollow"
    ]},
    "GM-002": {"name": "AEO", "triggers": [
        "aeo", "ai search", "chatgpt", "perplexity", "comparison", "vergleich"
    ]},
    "GM-003": {"name": "Content Strategy", "triggers": [
        "content", "blog", "social", "newsletter", "tone of voice", "copy",
        "plg", "product-led", "viral loop", "referral", "watermark", "activation", "onboarding funnel"
    ]},
    "GM-004": {"name": "Game Development", "triggers": [
        "game", "godot", "unity", "unreal", "platformer", "phaser", "three.js", "pygame", "spiel"
    ]},
    "PM-001": {"name": "User Research", "triggers": [
        "research", "interview", "survey", "usability"
    ]},
    "PM-002": {"name": "Roadmapping", "triggers": [
        "roadmap", "prioritization", "planning", "moscow"
    ]},
    "PM-003": {"name": "Operating Model", "triggers": [
        "operating model", "team structure", "process", "okr"
    ]},
    "AI-001": {"name": "AI Integration", "triggers": [
        "ai", "llm", "gpt", "claude", "prompt", "ki"
    ]},
    "AI-002": {"name": "Anti-Slop Audit", "triggers": [
        "anti-slop", "slop", "ai-code", "code quality"
    ]},
    "AI-003": {"name": "Automation Pipelines", "triggers": [
        "durable workflow", "orchestrator", "inngest", "temporal", "infusion",
        "agent job"
    ]},
    "AI-004": {"name": "Eval and Context", "triggers": [
        "eval", "rag", "context window", "prompt cache", "agent evaluation"
    ]},
    "PE-001": {"name": "Infrastructure", "triggers": [
        "infrastructure", "docker", "cloud", "deploy", "cdn"
    ]},
    "PE-002": {"name": "CI/CD Pipelines", "triggers": [
        "ci/cd", "pipeline", "github actions", "build"
    ]},
    "PE-003": {"name": "Security Audit", "triggers": [
        "security", "owasp", "penetration", "vulnerability", "xss", "csrf", "bola", "idor", "ssrf"
    ]},
    "PE-004": {"name": "Monitoring & Observability", "triggers": [
        "monitoring", "alerting", "uptime", "sentry"
    ]},
    "SO-001": {"name": "Studio Tooling Maintenance", "triggers": [
        "studio tools", "python", "tooling", "maintenance"
    ]},
    "SO-002": {"name": "Process Optimization", "triggers": [
        "process", "sprint discipline", "optimization", "metrics", "prozess", "optimierung", "metriken"
    ]},
    "SO-003": {"name": "Dual-Loop Learning", "triggers": [
        "learning", "retro", "knowledge", "promotion", "dual-loop"
    ]},
    "SO-004": {"name": "Documentation Governance", "triggers": [
        "documentation", "readme", "changelog", "docs", "doku"
    ]},
    "UX-001": {"name": "Product Design", "triggers": [
        "product design", "user flow", "jobs to be done", "end-to-end flow", "desktop app",
        "mobile app", "webapp", "browser extension", "platform"
    ]},
    "UX-002": {"name": "UX Design", "triggers": [
        "interaction", "microcopy", "error state", "ux design", "form flow", "wireframe",
        "modal", "dialog", "dropdown", "settings panel", "new component", "menu",
        "micro-interaction", "delight", "empty state", "loading state", "milestone", "confetti"
    ]},
    "UX-003": {"name": "Information Architecture", "triggers": [
        "information architecture", "navigation", "nav structure", "wayfinding", "ia ", "labeling"
    ]},
    "UX-004": {"name": "UX Research", "triggers": [
        "persona", "usability test", "mental model", "user research", "interview"
    ]},
    "UX-005": {"name": "Visual UI Design", "triggers": [
        "visual design", "typography", "color theory", "layout", "gestalt", "golden ratio",
        "new component", "ui component", "component design"
    ]},
    "UX-006": {"name": "Brand Guardian", "triggers": [
        "brand", "brand voice", "visual identity", "brand consistency", "tone",
        "component", "modal", "ui component"
    ]},
    "UX-007": {"name": "Visual Storyteller", "triggers": [
        "homepage", "landing page", "marketing page", "storyboard", "workflow diagram",
        "explainer", "hero section", "pricing page", "narrative", "scroll experience", "scrolly"
    ]},
    "GD-001": {"name": "Hypothesis & experiment design", "triggers": [
        "a/b", "ab test", "hypothesis", "experiment", "conversion", "cro",
        "variant", "split test",
    ]},
    "GD-002": {"name": "Commercial surface mechanics", "triggers": [
        "landing", "pricing page", "pricing table", "checkout", "cart",
        "pdp", "product detail", "product listing", "plp", "catalog",
    ]},
}

TEAM_MAPPING = {
    "FE": "01-frontend-experience",
    "BE": "02-backend-systems",
    "CL": "03-compliance-legal",
    "PS": "04-product-strategy-architecture",
    "GM": "05-growth-marketing-content",
    "PM": "06-product-management-operating-model",
    "AI": "07-ai-autonomous-systems",
    "PE": "08-platform-enterprise-engineering",
    "SO": "09-studio-operations-evolution",
    "UX": "10-product-design-experience",
    "GD": "11-growth-design",
}

EXTERNAL_MAPPINGS: Dict[str, List[str]] = {
    "FE-001": [
        "design/skills (hallmark audit)",
        "design_awesome/skills/<style>",
        "all_domains/design-and-ui-ux/frontend-design",
    ],
    "FE-007": ["knowledge-base/skill-extensions/frontend-security-auditor.md"],
    "FE-002": [
        "design/skills (hallmark)",
        "design_awesome/skills/<style>",
    ],
    "UX-001": ["design-agent/ux-design-process", "design-agent/ux-desktop-app", "design-agent/ux-web-app", "design-agent/ux-knowledge-work"],
    "UX-002": ["design-agent/ux-interaction-patterns", "design-agent/ux-form-design", "knowledge-base/skill-extensions/delight-micro-interactions.md", "knowledge-base/skill-extensions/figma-token-handoff.md"],
    "UX-003": ["design-agent/ux-information-architecture"],
    "UX-004": ["design-agent/ux-mental-models", "design-agent/ux-design-process"],
    "UX-005": [
        "design-agent/ux-visual-design",
        "design-agent/ux-typography",
        "design-agent/ux-color-theory",
        "design-agent/taste-skill",
    ],
    "UX-006": ["design-agent/brandkit", "design-agent/design-brand-guardian"],
    "UX-007": ["design-agent/design-visual-storyteller", "marketing_aeo/skills/copywriting", "knowledge-base/skill-extensions/email-design.md"],
    "GD-001": [
        "marketing_aeo/skills/ab-testing",
        "marketing_aeo/skills/cro",
    ],
    "GD-002": ["marketing_aeo/skills/cro"],
    "BE-001": [
        "all_domains/api-and-integration/api-design",
        "all_domains/api-and-integration/oauth-2-0-setup",
    ],
    "BE-002": [
        "all_domains/database/database-schema-design",
        "all_domains/database/query-optimization",
        "all_domains/database/database-migration",
    ],
    "CL-001": [
        "all_domains/legal-and-compliance/compliance-checklist-generation",
        "all_domains/legal-and-compliance/privacy-policy-drafting",
        "knowledge-base/skill-extensions/privacy-legal-compliance.md",
    ],
    "CL-002": [
        "compliance_cookies/skills/cookiecomply",
        "knowledge-base/skill-extensions/cookie-compliance.md",
    ],
    "CL-003": ["knowledge-base/skill-extensions/tos-architect.md"],
    "GM-001": [
        "marketing_aeo/skills/seo-audit",
        "marketing_aeo/skills/schema",
        "marketing_aeo/skills/programmatic-seo",
        "marketing_aeo/skills/site-architecture",
        "marketing_aeo/skills/customer-research",
        "knowledge-base/skill-extensions/affiliate-compliance.md",
    ],
    "GM-002": [
        "marketing_aeo/skills/ai-seo",
        "marketing_aeo/skills/schema",
        "geo_visibility/SKILL.md",
        "marketing_aeo/skills/competitors",
    ],
    "GM-003": [
        "marketing_aeo/skills/copywriting",
        "marketing_aeo/skills/content-strategy",
        "marketing_aeo/skills/product-marketing",
        "marketing_aeo/skills/customer-research",
        "marketing_aeo/skills/emails",
        "knowledge-base/skill-extensions/product-led-growth.md",
        "knowledge-base/skill-extensions/email-design.md",
    ],
    "GM-004": ["gamedev/router/SKILL.md (gamedev Router: Engine + Task)"],
    "PE-001": [
        "all_domains/devops-and-infrastructure/docker-compose-setup",
        "all_domains/devops-and-infrastructure/infrastructure-as-code",
    ],
    "PE-003": [
        "all_domains/security/security-audit",
        "all_domains/security/threat-modeling",
        "all_domains/security/dependency-scanning",
        "knowledge-base/skill-extensions/frontend-security-auditor.md",
        "knowledge-base/skill-extensions/backend-security-auditor.md",
    ],
    "PS-001": ["knowledge-base/skill-extensions/product-led-growth.md"],
    "PM-002": ["all_domains/productivity-and-workflow/project-management"],
}


def match_skills(text: str, max_skills: int = 5) -> List[str]:
    """Match internal skill IDs from ticket/feature text."""
    t = text.lower()
    hits: List[str] = []
    for skill_id, skill in INTERNAL_SKILLS.items():
        for trigger in skill["triggers"]:
            if trigger in t:
                hits.append(skill_id)
                break
    seen = set()
    unique = []
    for skill_id in hits:
        if skill_id not in seen:
            seen.add(skill_id)
            unique.append(skill_id)
    return unique[:max_skills]


def team_for_skills(skills: List[str]) -> str:
    """Determine team folder from skill IDs.

    GD-* is a pairing skill: commercial tickets stay on Team 10 unless another
    non-GD prefix wins first.
    """
    for skill in skills:
        prefix = skill.split("-")[0]
        if prefix == "GD":
            continue
        if prefix in TEAM_MAPPING:
            return TEAM_MAPPING[prefix]
    if any(str(s).startswith("GD-") for s in skills or []):
        return "10-product-design-experience"
    return "01-frontend-experience"


def external_skills_for(internal_hits: List[str]) -> List[str]:
    """Return external skill paths for matched internal skills."""
    ext: List[str] = []
    for skill_id in internal_hits:
        for path in EXTERNAL_MAPPINGS.get(skill_id, []):
            if path not in ext:
                ext.append(path)
    return ext
