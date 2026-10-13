#!/usr/bin/env python3
"""
skill_matcher.py — Single source of truth for internal skill matching.

Used by studio.py, generate_ticket_manifest.py, and test_skill_matching.py.
Trigger words align with .quinsy-studio/teams/skill-registry.md.

Staffing (PM-004): `staff_skills` adds the companion skills a ticket needs
(security, privacy, a11y, testing, ...) from signals in the ticket text, so a
ticket is not staffed by its title keywords alone.
"""

import re
from functools import lru_cache
from pathlib import Path
from typing import Dict, Iterable, List, Optional, Tuple

INTERNAL_SKILLS: Dict[str, Dict] = {
    "FE-001": {"name": "UI Component Design", "triggers": [
        "component", "ui-element", "button", "card", "modal", "ui", "interface", "komponente", "form",
        "page", "screen", "wizard", "sidebar", "dashboard"
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
        "test", "testing", "coverage", "unit-test", "e2e", "playwright"
    ]},
    "FE-007": {"name": "Client Security", "triggers": [
        "client security", "content-security-policy", "csp header", "frontend security"
    ]},
    "FE-008": {"name": "i18n and Localization", "triggers": [
        "i18n", "translation", "translate", "localization", "localisation", "multilingual",
        "language switch", "locale routing", "übersetzung", "mehrsprachig"
    ]},
    "BE-001": {"name": "API Design", "triggers": [
        "api", "endpoint", "rest", "graphql", "http"
    ]},
    "BE-002": {"name": "Database Design", "triggers": [
        "database", "schema", "migration", "query", "sql", "postgres"
    ]},
    "BE-003": {"name": "Auth & Authorization", "triggers": [
        "auth", "authentication", "authorization", "login", "jwt", "session", "rbac", "oauth",
        "sign up", "signup", "registration", "password"
    ]},
    "BE-004": {"name": "Error Handling", "triggers": [
        "error", "exception", "retry", "logging"
    ]},
    "BE-005": {"name": "Third-Party Integrations", "triggers": [
        "integration", "webhook", "sendgrid", "email", "e-mail", "smtp"
    ]},
    "BE-006": {"name": "Jobs and Delivery", "triggers": [
        "queue", "worker", "outbox", "bullmq", "background job", "cron"
    ]},
    "BE-007": {"name": "Payload", "triggers": [
        "payload", "collection", "local api", "cms", "localization", "locale"
    ]},
    "BE-008": {"name": "Payments and Billing", "triggers": [
        "payment", "billing", "checkout", "subscription", "stripe", "lemon squeezy",
        "refund", "dunning", "zahlung", "abo"
    ]},
    "BE-009": {"name": "Document Generation", "triggers": [
        "pdf", "invoice", "xrechnung", "zugferd", "e-rechnung", "rechnung", "gobd",
        "document generation"
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
        "technology evaluation", "framework choice", "library choice", "vendor comparison"
    ]},
    "PS-004": {"name": "Feasibility Analysis", "triggers": [
        "feasibility", "risk assessment", "spike"
    ]},
    "GM-001": {"name": "SEO Optimization", "triggers": [
        "seo", "visibility", "ranking", "google", "schema.org", "sichtbarkeit",
        "affiliate", "sponsored", "nofollow"
    ]},
    "GM-002": {"name": "AEO", "triggers": [
        "aeo", "ai search", "chatgpt", "perplexity", "comparison", "vergleich"
    ]},
    "GM-003": {"name": "Content Strategy", "triggers": [
        "content strategy", "content plan", "editorial", "blog", "social media", "newsletter",
        "tone of voice", "copywriting", "marketing copy",
        "plg", "product-led", "viral loop", "referral", "watermark", "activation", "onboarding funnel"
    ]},
    "GM-004": {"name": "Game Development", "triggers": [
        "game", "godot", "unity", "unreal", "platformer", "phaser", "three.js", "pygame", "spiel"
    ]},
    "GM-005": {"name": "Launch and Community", "triggers": [
        "launch", "product hunt", "show hn", "community", "press release", "reddit", "linkedin"
    ]},
    "GM-006": {"name": "Lifecycle Email", "triggers": [
        "newsletter", "lifecycle email", "drip", "email sequence", "welcome email",
        "win-back", "double opt-in", "onboarding email", "list-unsubscribe"
    ]},
    "PM-001": {"name": "User Research", "triggers": [
        "user research", "interview", "survey", "usability"
    ]},
    "PM-002": {"name": "Roadmapping", "triggers": [
        "roadmap", "prioritization", "moscow", "milestone plan"
    ]},
    "PM-003": {"name": "Operating Model", "triggers": [
        "operating model", "team structure", "okr"
    ]},
    "PM-004": {"name": "Ticket Staffing", "triggers": [
        "staffing", "skill assignment", "assign skills", "grooming", "ticket breakdown"
    ]},
    "AI-001": {"name": "AI Integration", "triggers": [
        "ai", "llm", "gpt", "claude", "prompt", "ki", "openai", "anthropic", "embedding", "chatbot"
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
    "AI-005": {"name": "AI-Code Security Audit", "triggers": [
        "prompt injection", "overrideaccess", "access control", "hallucinated package",
        "ai-generated code"
    ]},
    "PE-001": {"name": "Infrastructure", "triggers": [
        "infrastructure", "docker", "cloud", "deploy", "cdn", "coolify", "vps"
    ]},
    "PE-002": {"name": "CI/CD Pipelines", "triggers": [
        "ci/cd", "pipeline", "github actions", "tooling", "project setup"
    ]},
    "PE-003": {"name": "Security Audit", "triggers": [
        "security", "owasp", "penetration", "vulnerability", "xss", "csrf", "bola", "idor", "ssrf"
    ]},
    "PE-004": {"name": "Monitoring & Observability", "triggers": [
        "monitoring", "alerting", "uptime", "sentry"
    ]},
    "PE-005": {"name": "Threat Modeling", "triggers": [
        "threat model", "threat delta", "trust boundary", "stride", "attack surface",
        "multi-tenant", "tenant"
    ]},
    "PE-006": {"name": "Secrets Hygiene", "triggers": [
        "secret", "api key", "credential", "env var", "environment variable", "key rotation",
        "secrets inventory", "next_public_"
    ]},
    "PE-007": {"name": "Incident, Reliability and Breach Response", "triggers": [
        "incident", "outage", "runbook", "postmortem", "backup", "restore", "data breach",
        "disaster recovery", "datenpanne", "restore drill"
    ]},
    "SO-001": {"name": "Studio Tooling Maintenance", "triggers": [
        "studio tools", "studio tooling", "python"
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
    "SO-005": {"name": "Release Reality Check", "triggers": [
        "reality check", "release readiness", "release check", "pre-release", "go-live",
        "end-to-end journey"
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
        "explainer", "hero section", "pricing page", "narrative", "scroll experience", "scrolly",
        "hero image", "illustration", "imagery", "generated image", "og image", "stock photo"
    ]},
    "UX-008": {"name": "Anti-Slop Design & UX", "triggers": [
        "design direction", "direction critique", "anti-slop design", "design critique"
    ]},
    "UX-009": {"name": "UI Finish Gate", "triggers": [
        "ui parity", "finish gate", "visual parity", "pixel parity", "ui polish", "mock fidelity"
    ]},
    "GD-001": {"name": "Hypothesis & experiment design", "triggers": [
        "a/b", "ab test", "hypothesis", "experiment", "conversion", "cro",
        "variant", "split test",
    ]},
    "GD-002": {"name": "Commercial surface mechanics", "triggers": [
        "landing", "pricing page", "pricing table", "checkout", "cart",
        "pdp", "product detail", "product listing", "plp", "catalog",
    ]},
    "GD-003": {"name": "Persona walkthrough", "triggers": [
        "persona walkthrough", "five-second test", "5-second test", "first impression",
        "cognitive walkthrough"
    ]},
    "GD-004": {"name": "In-product growth loops", "triggers": [
        "growth loop", "viral loop", "referral", "invite", "share link", "public link", "watermark",
        "activation", "aha moment", "upgrade path", "network effect", "loop map"
    ]},
    "GM-007": {"name": "Positioning and messaging", "triggers": [
        "positioning", "core message", "tagline", "value proposition", "messaging", "hero copy",
        "persona page", "who is it for", "message hierarchy"
    ]},
}

NON_TICKET_SKILLS = {"cms-migration"}

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
    "BE-007": ["teams/02-backend-systems/skills/payload/SKILL.md"],
    "cms-migration": ["teams/02-backend-systems/skills/cms-migration/SKILL.md"],
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


MAX_TICKET_SKILLS = 8
_SHORT_TRIGGER = 5


@lru_cache(maxsize=None)
def _trigger_re(trigger: str) -> "re.Pattern[str]":
    """Word-start match; short triggers must be a whole word (plural allowed).

    `ai` must not hit `email`/`detail`/`main`, `test` must not hit `latest`,
    `form` must not hit `format`/`platform`.
    """
    word = trigger.strip().lower()
    body = re.escape(word)
    if len(word) < _SHORT_TRIGGER:
        return re.compile(rf"(?<![\w]){body}(?:s|es)?(?![\w])")
    return re.compile(rf"(?<![\w]){body}")


def trigger_hits(trigger: str, text: str) -> bool:
    return bool(_trigger_re(trigger).search(text.lower()))


def match_skills(text: str, max_skills: int = 5) -> List[str]:
    """Match internal skill IDs from ticket/feature text."""
    t = text.lower()
    hits: List[str] = []
    for skill_id, skill in INTERNAL_SKILLS.items():
        if any(trigger_hits(trigger, t) for trigger in skill["triggers"]):
            hits.append(skill_id)
    return hits[:max_skills]


def is_known_skill(skill_id: str) -> bool:
    return skill_id in INTERNAL_SKILLS or skill_id in NON_TICKET_SKILLS


# =============================================================================
# SKILL FILES — the card points the implementer at these, not only playbooks
# =============================================================================

TEAMS_DIR = Path(__file__).resolve().parent.parent / "teams"
_SKILL_ID_LINE = re.compile(r"^\**skill_id:\**\s*`?([A-Z]{2}-\d{3})`?\s*$", re.MULTILINE)
_FIXED_SKILL_FILES = {
    "BE-007": "teams/02-backend-systems/skills/payload/SKILL.md",
    "cms-migration": "teams/02-backend-systems/skills/cms-migration/SKILL.md",
}


@lru_cache(maxsize=1)
def skill_file_index() -> Dict[str, str]:
    """Skill ID -> path relative to `.quinsy-studio/`, read from `skill_id:` lines."""
    index: Dict[str, str] = dict(_FIXED_SKILL_FILES)
    if not TEAMS_DIR.is_dir():
        return index
    for path in sorted(TEAMS_DIR.glob("*/skills/*.md")):
        head = path.read_text(encoding="utf-8", errors="ignore")[:1500]
        match = _SKILL_ID_LINE.search(head)
        if match and match.group(1) not in index:
            index[match.group(1)] = str(path.relative_to(TEAMS_DIR.parent))
    return index


def skill_files_for(skills: Iterable[str]) -> List[str]:
    index = skill_file_index()
    return [index[s] for s in skills if s in index]


# =============================================================================
# STAFFING (PM-004) — companion skills from ticket signals
# =============================================================================

_UI_TYPES = (
    "ui-new-component", "ui-composition", "ui-styling", "marketing-page",
    "workflow-explainer", "ia-feature-placement",
)
_UI_RE = re.compile(
    r"\b(ui|page|screen|view|form|forms|wizard|modal|dialog|button|component|"
    r"layout|dashboard|sidebar|menu|frontend|landing|checkout)\b"
)
_ADMIN_TITLE_RE = re.compile(r"\b(admin|/admin|payload admin)\b")
_SECURITY_RE = re.compile(
    r"\b(auth\w*|login|logout|sign[- ]?up|registration|(?<!utm )(?<!utm-)(?<!risk )register|password|session|jwt|"
    r"rbac|role-based|user roles?|permissions?|access control|access rules?|tenant\w*|"
    r"host resolution|upload\w*|webhooks?|api keys?|access tokens?|overrideaccess|idor)\b"
)
_BOUNDARY_RE = re.compile(
    r"\b(auth\w*|login|sign[- ]?up|registration|tenant\w*|host resolution|upload\w*|"
    r"webhooks?|payment\w*|checkout|public api|admin access|third[- ]party)\b"
)
_PERSONAL_DATA_RE = re.compile(
    r"\b(personal data|leads?|lead[- ](capture|form|generation)|contact form|newsletter|sign[- ]?up|registration|(?<!utm )(?<!utm-)(?<!risk )register|"
    r"email address(es)?|phone|customer data|user data|profile|address|gdpr|dsgvo|"
    r"datenschutz|consent|tracking|analytics)\b"
)
_TRACKING_RE = re.compile(r"\b(tracking|analytics|pixel|cookies?|consent banner|tag manager)\b")
_SECRETS_RE = re.compile(
    r"\b(api keys?|secrets?|credentials?|env vars?|environment variables?|smtp|"
    r"service account|key rotation)\b"
)
_PAYMENT_RE = re.compile(
    r"\b(payments?|billing|checkout|subscriptions?|stripe|lemon squeezy|refunds?|pricing plans?)\b"
)
_TERMS_RE = re.compile(r"\b(checkout|subscriptions?|paid plan|withdrawal|widerruf)\b")
_DOCUMENT_RE = re.compile(r"\b(pdf|invoices?|xrechnung|zugferd|e-rechnung|rechnung)\b")
_I18N_RE = re.compile(
    r"\b(i18n|translations?|translate|locales?|locali[sz]ation|multilingual|hreflang|language)\b"
)
_PUBLIC_PAGE_RE = re.compile(
    r"\b(landing page|homepage|marketing page|marketing site|blog|public page|seo|impressum)\b"
)
_MARKETING_EMAIL_RE = re.compile(
    r"\b(newsletter|drip|email sequence|lifecycle email|welcome email|onboarding email|win-back)\b"
)
_LLM_RE = re.compile(
    r"\b(llm|gpt|claude|openai|anthropic|prompts?|embeddings?|rag|chatbot|ai assistant|generative)\b"
)
_INFRA_RE = re.compile(r"\b(deploy\w*|coolify|vps|production|backups?|restore)\b")
_INCIDENT_RE = re.compile(r"\b(backups?|restore|incident\w*|outage|data breach|disaster recovery)\b")
_COMMERCIAL_RE = re.compile(r"\b(landing|pricing|checkout|cart|pdp|plp|product detail|catalog)\b")
_LEGAL_PAGE_RE = re.compile(r"\b(impressum|privacy policy|datenschutz|terms|agb|legal)\b")
_GROWTH_LOOP_RE = re.compile(
    r"\b(signup|sign-up|onboarding|first run|invite|invitation|referral|share link|sharing|public link|export|embed|watermark|activation|upgrade|paywall|trial)\b",
    re.I,
)

# (skill, required, reason, predicate(text, skills, ticket_type))
# required=True: groom refuses the sprint until the ticket carries the skill or waives it.
StaffingRule = Tuple[str, bool, str, "callable"]


def _is_ui(text: str, skills: List[str], ticket_type: str) -> bool:
    if ticket_type in _UI_TYPES:
        return True
    if any(s in skills for s in ("FE-001", "FE-002", "UX-002", "UX-005")):
        return True
    title = text.split("\n", 1)[0]
    if _ADMIN_TITLE_RE.search(title):
        return False
    return bool(_UI_RE.search(text))


def _is_design_phase(ticket_type: str, design_status: str) -> bool:
    return design_status == "pending" and ticket_type in _UI_TYPES + ("ia-navigation",)


STAFFING_RULES: List[StaffingRule] = [
    ("PE-003", True, "touches auth, access, tenants, uploads or webhooks",
     lambda t, s, k: bool(_SECURITY_RE.search(t))),
    ("PE-005", False, "adds or changes a trust boundary; write the threat delta",
     lambda t, s, k: bool(_BOUNDARY_RE.search(t))),
    ("AI-005", True, "AI-written code on an access-sensitive surface",
     lambda t, s, k: bool(_SECURITY_RE.search(t)) or bool(_LLM_RE.search(t))),
    ("CL-001", True, "collects or processes personal data",
     lambda t, s, k: bool(_PERSONAL_DATA_RE.search(t))),
    ("CL-002", True, "tracking, analytics or cookies need consent",
     lambda t, s, k: bool(_TRACKING_RE.search(t))),
    ("PE-006", True, "handles secrets or credentials",
     lambda t, s, k: bool(_SECRETS_RE.search(t))),
    ("BE-008", True, "takes money or manages subscriptions",
     lambda t, s, k: bool(_PAYMENT_RE.search(t))),
    ("CL-003", True, "paid contract needs AGB and withdrawal terms",
     lambda t, s, k: bool(_TERMS_RE.search(t))),
    ("BE-009", False, "generates documents or invoices",
     lambda t, s, k: bool(_DOCUMENT_RE.search(t))),
    ("FE-004", True, "user-facing UI must meet WCAG 2.2 AA / BFSG",
     lambda t, s, k: _is_ui(t, s, k)),
    ("FE-006", True, "UI behaviour needs tests and evidence",
     lambda t, s, k: _is_ui(t, s, k)),
    ("UX-009", False, "shipped screen is compared with the signed mock",
     lambda t, s, k: _is_ui(t, s, k) and k != "ia-navigation"),
    ("FE-008", False, "user-facing text in more than one language",
     lambda t, s, k: bool(_I18N_RE.search(t))),
    ("GM-001", False, "public page that should be found",
     lambda t, s, k: k == "marketing-page" or bool(_PUBLIC_PAGE_RE.search(t))),
    ("GM-006", True, "marketing email needs opt-in and unsubscribe (UWG § 7)",
     lambda t, s, k: bool(_MARKETING_EMAIL_RE.search(t))),
    ("AI-001", False, "calls an LLM",
     lambda t, s, k: bool(_LLM_RE.search(t))),
    ("PE-001", False, "changes deployment or infrastructure",
     lambda t, s, k: bool(_INFRA_RE.search(t))),
    ("PE-007", False, "backups, restore or incident handling",
     lambda t, s, k: bool(_INCIDENT_RE.search(t))),
    ("GD-002", False, "commercial surface",
     lambda t, s, k: bool(_COMMERCIAL_RE.search(t))),
    ("GM-007", True, "commercial surface carries the core message; problem first (GM-007)",
     lambda t, s, k: k == "marketing-page" or bool(_COMMERCIAL_RE.search(t))),
    ("GM-007", False, "public page uses the positioning vocabulary (GM-007)",
     lambda t, s, k: bool(_PUBLIC_PAGE_RE.search(t)) and not bool(_LEGAL_PAGE_RE.search(t))),
    ("GD-004", False, "flow touches signup, sharing, invites, activation or upgrade — draw the loop",
     lambda t, s, k: bool(_GROWTH_LOOP_RE.search(t))),
]


def staffing_text(title: str, body: str = "") -> str:
    """Title plus Target / Scope / AC / Out of scope — not status logs or boilerplate."""
    keep: List[str] = [title]
    section = ""
    for line in (body or "").splitlines():
        heading = re.match(r"^#{2,3}\s+(.+?)\s*$", line)
        if heading:
            section = heading.group(1).strip().lower()
            continue
        if section in ("target", "scope", "ac", "acceptance criteria", "context", "problem"):
            keep.append(line)
    return "\n".join(keep).lower()


def staff_skills(
    title: str,
    body: str = "",
    skills: Optional[List[str]] = None,
    ticket_type: str = "",
    design_status: str = "",
    waived: Optional[Iterable[str]] = None,
    limit: int = MAX_TICKET_SKILLS,
) -> Dict[str, object]:
    """Return the staffed skill list and why each companion was added.

    Keys: skills, added [(id, reason)], missing_required [(id, reason)],
    dropped [(id, reason)] (over `limit`; the PM must pick or split the ticket).
    """
    current = [s for s in (skills or []) if s]
    text = staffing_text(title, body)
    waived_set = {w.strip() for w in (waived or []) if str(w).strip()}
    wanted: List[Tuple[str, bool, str]] = []
    design_phase = _is_design_phase(ticket_type, design_status)
    for skill_id, required, reason, predicate in STAFFING_RULES:
        if skill_id in current or skill_id in waived_set:
            continue
        if design_phase and skill_id in ("FE-006", "UX-009"):
            continue
        try:
            hit = predicate(text, current, ticket_type)
        except re.error:
            hit = False
        if hit and all(w[0] != skill_id for w in wanted):
            wanted.append((skill_id, required, reason))
    wanted.sort(key=lambda item: not item[1])
    out = list(current)
    added: List[Tuple[str, str]] = []
    dropped: List[Tuple[str, str]] = []
    missing_required = [(sid, reason) for sid, req, reason in wanted if req]
    for skill_id, _required, reason in wanted:
        if len(out) < limit:
            out.append(skill_id)
            added.append((skill_id, reason))
        else:
            dropped.append((skill_id, reason))
    return {
        "skills": out,
        "added": added,
        "missing_required": missing_required,
        "dropped": dropped,
    }


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
