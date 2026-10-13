#!/usr/bin/env python3
"""Security and quality gate checks (agency integration L4, L5, L7, L8, L12)."""

from __future__ import annotations

import subprocess
import tempfile
import unittest
from datetime import date
from pathlib import Path

import architecture_checks as arch
import quality_checks as quality
import security_checks as sec
import ship_checks as ship

TEMPLATE = Path(__file__).resolve().parent.parent / "studio-templates" / "payload" / "app"


def _write(root: Path, rel: str, body: str) -> Path:
    path = root / rel
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(body, encoding="utf-8")
    return path


class TemplateIsCleanTests(unittest.TestCase):
    def test_payload_template_passes_every_security_check(self):
        for name in sec.CHECKS:
            with self.subTest(check=name):
                self.assertEqual(sec.run_check(name, TEMPLATE), [])


class SecurityCheckTests(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.root = Path(self._tmp.name)

    def tearDown(self):
        self._tmp.cleanup()

    def test_secret_scan_finds_tokens_but_never_reads_env(self):
        _write(self.root, "src/lib/stripe.ts", "const key = 'sk_live_" + "a" * 24 + "'\n")
        _write(self.root, ".env", "STRIPE_SECRET_KEY=sk_live_" + "b" * 24 + "\n")
        findings = sec.secret_scan(self.root)
        self.assertEqual(len(findings), 1)
        self.assertIn("src/lib/stripe.ts:1", findings[0])

    def test_client_env_leak(self):
        _write(self.root, ".env.example", "NEXT_PUBLIC_STRIPE_SECRET_KEY=\nNEXT_PUBLIC_STRIPE_PUBLISHABLE_KEY=\n")
        _write(self.root, "src/app/Widget.tsx", "'use client'\nconst k = process.env.PAYLOAD_SECRET\nconst e = process.env.NODE_ENV\n")
        findings = sec.client_env_leak(self.root)
        self.assertEqual(len(findings), 2)
        self.assertTrue(any("NEXT_PUBLIC_STRIPE_SECRET_KEY" in f for f in findings))
        self.assertTrue(any("process.env.PAYLOAD_SECRET in a client component" in f for f in findings))

    def test_insecure_env_fallback(self):
        _write(self.root, "src/a.ts", "const s = process.env.PAYLOAD_SECRET || 'dev'\nconst b = process.env.S3_BUCKET || 'media'\n")
        findings = sec.insecure_env_fallback(self.root)
        self.assertEqual(len(findings), 1)
        self.assertIn("PAYLOAD_SECRET", findings[0])

    def test_docker_secret_leak(self):
        _write(self.root, "Dockerfile", "FROM node\nARG STRIPE_SECRET_KEY\nCOPY . .\n")
        _write(self.root, "docker-compose.yml", "services:\n  app:\n    environment:\n      PAYLOAD_SECRET: hunter2hunter\n      DATABASE_URL: ${DATABASE_URL}\n")
        findings = sec.docker_secret_leak(self.root)
        self.assertEqual(len(findings), 3)
        _write(self.root, ".dockerignore", ".env*\n")
        self.assertEqual(len(sec.docker_secret_leak(self.root)), 2)

    def test_payload_access(self):
        _write(self.root, "src/collections/Posts.ts", "export const Posts: CollectionConfig = {\n  slug: 'posts',\n  fields: [],\n}\n")
        _write(self.root, "src/collections/Notes.ts", "export const Notes: CollectionConfig = {\n  access: {\n    update: () => true,\n  },\n}\n")
        findings = sec.payload_access(self.root)
        self.assertTrue(any("Posts.ts: collection has no `access`" in f for f in findings))
        self.assertTrue(any("`update: () => true`" in f for f in findings))

    def test_local_api_override(self):
        _write(self.root, "src/app/(app)/page.tsx", "await payload.find({ collection: 'notes', user })\nawait payload.find({ collection: 'posts', overrideAccess: true })\n")
        findings = sec.local_api_override(self.root)
        self.assertEqual(len(findings), 1)
        self.assertIn("page.tsx:1", findings[0])

    def test_webhook_signature(self):
        _write(self.root, "src/app/api/webhooks/stripe/route.ts", "export async function POST(req) { const body = await req.json() }\n")
        self.assertTrue(sec.webhook_signature(self.root))
        _write(self.root, "src/app/api/webhooks/stripe/route.ts", "export async function POST(req) { const raw = await req.text(); await stripeProvider.handleWebhook(raw, sig) }\n")
        self.assertEqual(sec.webhook_signature(self.root), [])

    def test_exceptions_waive_until_expiry(self):
        _write(self.root, "src/app/(app)/page.tsx", "await payload.find({ collection: 'posts' })\n")
        _write(
            self.root, "docs/security/exceptions.md",
            "| check | path | reason | expires |\n|---|---|---|---|\n"
            "| local_api_override | src/app/(app)/page.tsx | public list | 2026-12-31 |\n",
        )
        self.assertEqual(sec.run_check("local_api_override", self.root, today=date(2026, 10, 12)), [])
        self.assertTrue(sec.run_check("local_api_override", self.root, today=date(2027, 1, 1)))
        self.assertTrue(sec.expired_exceptions(self.root, today=date(2027, 1, 1)))


class QualityCheckTests(unittest.TestCase):
    def test_a11y_and_e2e_and_api(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.assertEqual(quality.a11y_axe(root), ([], "no product pages"))
            _write(root, "src/app/(app)/page.tsx", "export default function Page() { return null }\n")
            findings, _ = quality.a11y_axe(root)
            self.assertTrue(any("no axe test" in f for f in findings))
            _write(root, "e2e/smoke.spec.ts", "import AxeBuilder from '@axe-core/playwright'\ntest.only('x', async () => { await page.waitForTimeout(500) })\n")
            self.assertEqual(quality.a11y_axe(root)[0], [])
            self.assertEqual(len(quality.e2e_hygiene(root)[0]), 2)
            _write(root, "src/app/api/notes/route.ts", "export async function POST(req) { const b = await req.json(); return Response.json({ m: err.message }) }\n")
            self.assertEqual(len(quality.api_contract(root)[0]), 2)

    def test_clean_fixtures_pass(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            _write(root, "e2e/smoke.spec.ts", "test('x', async () => { await expect(page.getByRole('button')).toBeVisible() })\n")
            self.assertEqual(quality.e2e_hygiene(root), ([], ""))
            _write(
                root, "src/app/api/notes/route.ts",
                "export async function POST(req) { const b = Schema.parse(await req.json()); "
                "return Response.json({ code: 'bad_input', message: 'Invalid note' }) }\n",
            )
            self.assertEqual(quality.api_contract(root), ([], ""))

    def test_perf_budget(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            _write(root, "src/app/Chart.tsx", "'use client'\nimport moment from 'moment'\nexport const C = () => <img src='/a.png' />\n")
            self.assertEqual(len(quality.perf_budget(root)[0]), 2)
            _write(root, "src/app/Chart.tsx", "import Image from 'next/image'\nexport const C = () => <Image src='/a.png' alt='' sizes='100vw' />\n")
            self.assertEqual(quality.perf_budget(root), ([], ""))


class WarningCheckTests(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.root = Path(self._tmp.name)

    def tearDown(self):
        self._tmp.cleanup()

    def test_llm_sink(self):
        _write(self.root, "src/app/Answer.tsx", "import { generateText } from 'ai'\nexport const A = ({ t }) => <div dangerouslySetInnerHTML={{ __html: t }} />\n")
        self.assertEqual(len(sec.llm_sink(self.root)), 1)
        _write(self.root, "src/app/Answer.tsx", "import { generateText } from 'ai'\nexport const A = ({ t }) => <p>{t}</p>\n")
        self.assertEqual(sec.llm_sink(self.root), [])

    def test_sensitive_log(self):
        _write(self.root, "src/lib/auth.ts", "console.log('login', password)\n")
        self.assertEqual(len(sec.sensitive_log(self.root)), 1)
        _write(self.root, "src/lib/auth.ts", "console.log('login', { userId })\n")
        self.assertEqual(sec.sensitive_log(self.root), [])

    def test_security_headers(self):
        _write(self.root, "next.config.mjs", "export default {}\n")
        self.assertEqual(len(sec.security_headers(self.root)), 1)
        _write(
            self.root, "next.config.mjs",
            "const h = ['Content-Security-Policy', 'Strict-Transport-Security', 'X-Content-Type-Options', 'Referrer-Policy']\n",
        )
        self.assertEqual(sec.security_headers(self.root), [])


class NpmAuditPolicyTests(unittest.TestCase):
    def _run(self, code, out):
        import run_qa_gate
        from unittest import mock

        done = subprocess.CompletedProcess(args="npm audit", returncode=code, stdout=out, stderr="")
        with mock.patch.object(run_qa_gate.subprocess, "run", return_value=done):
            return run_qa_gate.check_npm_audit_policy(Path("."))

    def test_clean_audit_passes(self):
        result = self._run(0, "found 0 vulnerabilities")
        self.assertTrue(result.passed)
        self.assertFalse(result.not_tested)

    def test_high_advisory_fails(self):
        result = self._run(1, "1 high severity vulnerability")
        self.assertFalse(result.passed)

    def test_offline_is_not_tested(self):
        result = self._run(1, "npm ERR! code ENOTFOUND")
        self.assertTrue(result.not_tested)

    def test_exceptions_waive_high_advisory(self):
        import run_qa_gate
        from unittest import mock

        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "docs" / "security").mkdir(parents=True)
            (root / "docs" / "security" / "exceptions.md").write_text(
                "| check | path | reason | expires |\n"
                "| npm_audit_policy | next | Next 16 is breaking | 2026-12-31 |\n"
            )
            done = subprocess.CompletedProcess(
                args="npm audit", returncode=1, stdout="1 high", stderr=""
            )
            with mock.patch.object(run_qa_gate.subprocess, "run", return_value=done):
                result = run_qa_gate.check_npm_audit_policy(root)
            self.assertTrue(result.passed)
            self.assertIn("waived", result.output)


class ArchitecturePacketTests(unittest.TestCase):
    def test_gate_1_needs_threat_model_headings(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.assertEqual(len(arch.gate_1_security_issues(root)), 3)
            body = "\n".join(f"## {h}\ncontent line for {h} that is long enough" for h in arch.THREAT_MODEL_HEADINGS)
            _write(root, "docs/security/threat-model.md", body * 2)
            _write(root, "docs/security/data-map.md", "| category | purpose | basis | stored | retention | processor |\n" * 2)
            _write(root, "docs/security/secrets-inventory.md", "| Name | Purpose | Owner | Where | Rotation |\n" * 2)
            self.assertEqual(arch.gate_1_security_issues(root), [])
            self.assertTrue(arch.gate_1_workflow_issues(root))

    def test_threat_delta_none_refused_for_webhook(self):
        ticket = "---\ntitle: Stripe webhook\n---\n## Scope\nAdd the Stripe webhook route.\n"
        self.assertTrue(arch.threat_delta_issues("threat delta: none — nothing new\n", ticket))
        self.assertTrue(arch.threat_delta_issues("threat delta: none\n", "---\ntitle: Copy\n---\nText only"))
        self.assertEqual(arch.threat_delta_issues("threat delta: none — copy change only\n", "---\ntitle: Copy\n---\nText only"), [])
        self.assertEqual(arch.threat_delta_issues("## Threat delta\n- new boundary\n", ticket), [])

    def test_flow_ticket_links_workflow_cases(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            ticket = "---\ntitle: Signup flow\n---\n## AC\n- TC-01 email taken shows inline error\n"
            self.assertTrue(arch.workflow_issues(root, "no link", ticket))
            _write(root, "docs/workflows/WORKFLOW-signup.md", "## Branches\n- TC-01 email taken\n- TC-02 weak password\n")
            self.assertEqual(arch.workflow_issues(root, "see docs/workflows/WORKFLOW-signup.md", ticket), [])
            self.assertTrue(arch.workflow_issues(root, "see docs/workflows/WORKFLOW-signup.md", ticket.replace("TC-01", "x")))


class ShipCheckTests(unittest.TestCase):
    def test_pre_ship_main(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            subprocess.run(["git", "init", "-q", str(root)], check=True)
            _write(root, ".env.example", "PAYLOAD_SECRET=\nSTRIPE_WEBHOOK_SECRET=\nSITE_URL=\n")
            _write(root, "docker-compose.yml", "services:\n  db:\n    image: postgres:16\n    ports:\n      - \"5432:5432\"\n")
            _write(root, "src/old.ts", "const k = 'sk_live_" + "c" * 24 + "'\n")
            subprocess.run(["git", "-C", str(root), "add", "-A"], check=True)
            subprocess.run(["git", "-C", str(root), "-c", "user.email=t@t", "-c", "user.name=t", "commit", "-qm", "x"], check=True)
            (root / "src" / "old.ts").write_text("const k = process.env.STRIPE_SECRET_KEY\n")
            issues = ship.pre_ship_main_issues(root)
            self.assertTrue(any("Stripe live key added in commit" in i for i in issues))
            self.assertTrue(any("secrets-inventory.md missing" in i for i in issues))
            self.assertTrue(any("incident-runbook.md missing" in i for i in issues))
            self.assertTrue(any("publishes 5432:5432" in i for i in issues))
            _write(root, "docs/security/secrets-inventory.md", "| PAYLOAD_SECRET | … |\n")
            self.assertTrue(any("lacks: STRIPE_WEBHOOK_SECRET" in i for i in ship.inventory_issues(root)))


class RealityCheckTests(unittest.TestCase):
    REPORT = (
        "# Reality check — SPRINT-03\n\nVerdict: {verdict}\n"
        "Dev URL: https://dev.example.test  ·  Commit: {sha}  ·  Date: 2026-10-12\n\n"
        "## Journey\n| # | Step | 1440 | 390 | Evidence |\n|---|---|---|---|---|\n"
        "| 1 | Open / | PASS | {narrow} | reality-check/j1.png |\n\n"
        "## Done tickets\n| Ticket | Claim | Result | Evidence |\n|---|---|---|---|\n| T-012 | save | PASS | PATCH 200 |\n\n"
        "## Automatic-fail triggers\n{triggers}\n"
    )

    def _report(self, **kw):
        values = {"verdict": "READY", "sha": "abc1234", "narrow": "PASS", "triggers": "- none fired"}
        values.update(kw)
        return self.REPORT.format(**values)

    def test_report_rules(self):
        from reality_check import report_issues

        with tempfile.TemporaryDirectory() as tmp:
            sdir = Path(tmp)
            self.assertTrue(any("evidence missing" in i for i in report_issues(self._report(), sdir)))
            _write(sdir, "reality-check/j1.png", "png")
            self.assertEqual(report_issues(self._report(), sdir), [])
            self.assertTrue(any("READY with a NOT TESTED" in i for i in report_issues(self._report(narrow="NOT TESTED — no device"), sdir)))
            fired = "- 5xx on /board"
            self.assertTrue(any("any trigger means FAILED" in i for i in report_issues(self._report(triggers=fired), sdir)))
            self.assertTrue(any("name the bug ticket" in i for i in report_issues(self._report(verdict="FAILED", triggers=fired), sdir)))
            self.assertEqual(report_issues(self._report(verdict="FAILED", triggers=fired + " → DEMO-0101"), sdir), [])

    def test_state_goes_stale_on_new_commit(self):
        from reality_check import reality_state

        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "proj"
            sdir = Path(tmp) / "sprint"
            subprocess.run(["git", "init", "-q", str(root)], check=True)
            _write(root, "a.txt", "1")
            git = ["git", "-C", str(root), "-c", "user.email=t@t", "-c", "user.name=t"]
            subprocess.run(git + ["add", "-A"], check=True)
            subprocess.run(git + ["commit", "-qm", "one"], check=True)
            sha = subprocess.run(["git", "-C", str(root), "rev-parse", "HEAD"], capture_output=True, text=True).stdout.strip()
            self.assertEqual(reality_state(sdir, root), "missing")
            _write(sdir, "reality-check.md", self._report(verdict="FAILED", sha=sha[:7]))
            self.assertEqual(reality_state(sdir, root), "failed")
            _write(root, "a.txt", "2")
            subprocess.run(git + ["commit", "-qam", "fix"], check=True)
            self.assertEqual(reality_state(sdir, root), "stale")

    def test_execute_runs_reality_check_before_review(self):
        from unittest.mock import patch

        from studio_execute import decide_from_state

        status = {
            "human_gates": {k: {"status": "approved"} for k in ("0", "1", "2")},
            "current_sprint": "SPRINT-01",
            "sprint_hitl": {"review_status": "pending", "scope_status": "approved", "groom_status": "approved"},
        }
        tickets = [{"id": "T-1", "status": "done", "deps": []}]
        kwargs = dict(open_los=[], amendment_actions=[], prd_exists=True)
        with patch("reality_check.reality_state", return_value="missing"):
            self.assertEqual(decide_from_state("demo", status, tickets, **kwargs).kind, "REALITY_CHECK")
        with patch("reality_check.reality_state", return_value="ready"):
            step = decide_from_state("demo", status, tickets, **kwargs)
            self.assertEqual(step.kind, "VERIFY")
            self.assertIn("--inform", step.command)
        with patch("reality_check.reality_state", return_value="needs-work"):
            step = decide_from_state("demo", status, tickets, **kwargs)
            self.assertEqual(step.kind, "VERIFY")
            self.assertIn("NEEDS WORK", step.reason)
        with patch("reality_check.reality_state", return_value="failed"):
            step = decide_from_state("demo", status, tickets, **kwargs)
            self.assertEqual(step.kind, "VERIFY")
            self.assertIn("FAILED", step.reason)


if __name__ == "__main__":
    unittest.main()
