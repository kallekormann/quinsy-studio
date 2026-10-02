#!/usr/bin/env python3
"""Ideation desk: store, budget, score, shortlist, promote."""

from __future__ import annotations

import sqlite3
import tempfile
import unittest
from datetime import datetime
from pathlib import Path

from studio_ideate import Desk, dispatch


def _evidence(desk: Desk, pid: str, count: int = 3) -> None:
    for i in range(count):
        desk.add_evidence(
            pid,
            {
                "source": f"forum-{i}",
                "url": f"https://example{i}.com/thread",
                "date": "2026-06-01",
                "count": "4",
                "paraphrase": f"people pay for a workaround {i}",
                "author": f"author-{i}",
                "thread": f"thread-{i}",
            },
        )


def _score_all(desk: Desk, iid: str, value: str = "4") -> None:
    for name, _weight in __import__("studio_ideate", fromlist=["DIMENSIONS"]).DIMENSIONS:
        desk.score(iid, name, value, "https://example.com/src 2026-06-01")


class IdeationDeskTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        self.templates = Path(__file__).resolve().parents[1] / "studio-templates" / "ideation"
        self.now = datetime(2026, 10, 1, 9, 0, 0)
        self.desk = Desk(self.root, self.templates, today=self.now.date(), now=self.now)

    def tearDown(self):
        self.tmp.cleanup()

    def test_seed_and_duplicate_from_index_keywords(self):
        message = self.desk.start("nl parents", "small", {}, False)
        self.assertIn("SECTION: signals", message)
        self.assertTrue((self.root / "ideation" / "rubric.md").exists())
        created = self.desk.add_problem(
            {
                "sentence": "Parents cannot share a school form without uploading it",
                "keywords": "school, form, upload",
                "segment": "parents",
                "region": "NL",
                "language": "nl",
            }
        )
        self.assertIn("P-001", created)
        with self.assertRaises(Exception):
            self.desk.add_problem(
                {
                    "sentence": "A different wording",
                    "keywords": "school, form, pdf",
                    "segment": "parents",
                }
            )

    def test_unverified_and_same_thread_do_not_count(self):
        self.desk.seed()
        self.desk.add_problem(
            {
                "sentence": "Tradespeople retype invoices",
                "keywords": "invoice, retype, trade",
                "segment": "trades",
            }
        )
        self.desk.add_evidence("P-001", {"source": "web", "paraphrase": "no url"})
        self.desk.add_evidence(
            "P-001",
            {
                "source": "reddit",
                "url": "https://reddit.com/a",
                "date": "2026-01-02",
                "paraphrase": "first",
                "author": "ann",
                "thread": "same",
            },
        )
        self.desk.add_evidence(
            "P-001",
            {
                "source": "reddit",
                "url": "https://news.ycombinator.com/b",
                "date": "2026-01-03",
                "paraphrase": "same thread other domain",
                "author": "bob",
                "thread": "same",
            },
        )
        _meta, body = self.desk._read(self.root / "ideation" / "problems" / "P-001.md")
        self.assertEqual(self.desk.independent_count(body), 1)

    def test_promote_requires_approval_and_writes_intake(self):
        self.desk.start("forms", "small", {}, True)
        self.desk.add_problem(
            {
                "sentence": "People pay a freelancer to file a form",
                "keywords": "form, freelancer, file",
                "segment": "families",
                "region": "NL",
                "language": "nl",
            }
        )
        _evidence(self.desk, "P-001")
        self.desk.add_competitor({"name": "Formly", "category": "forms"})
        self.desk.add_idea(
            {
                "title": "Form file listing",
                "problems": "P-001",
                "shape": "marketplace listing",
                "host": "Notion",
                "pitch": "A listing that files the form inside Notion. Neighbors already charge for templates.",
                "competitors": "C-001",
                "closest-product": "Formly",
                "closest-price": "9 EUR",
                "blue": ["templates", "drop upload", "keep the host", "dutch parents"],
            }
        )
        _score_all(self.desk, "I-001", "4")
        code, message = dispatch(
            ["promote"],
            root=self.root,
            templates=self.templates,
            today=self.now.date(),
            now=self.now,
        )
        self.assertEqual(code, 2)
        self.assertIn("not approved", message)
        self.desk.present()
        self.desk.approve(["I-001"])
        code, message = dispatch(
            ["promote"],
            root=self.root,
            templates=self.templates,
            today=self.now.date(),
            now=self.now,
        )
        self.assertEqual(code, 2)
        self.assertIn("PRD is missing", message)
        self.desk.shape(
            "I-001",
            {
                "problem": "Families pay a freelancer to file a form they already have on paper, and they do it again every year.",
                "solution": "A listing files that form. Neighbors already charge for templates.",
                "architecture": "The listing reads the form they already filled. It does not invent a new form.",
                "experience": "They pick the form, check the fields, and send it.",
                "steps": "They pick the form they already have. The listing checks every required field. The listing sends the finished form to the office.",
                "mvp": "The first chunk lets them pick one form they already have and send that form. That chunk is the whole first build.",
                "later": "Later chunks cover the other forms the same family already files. The first chunk does not include those other forms.",
            },
        )
        self.desk.build(
            "I-001",
            {
                "user": "The person picks the form they already have, checks every field on it, and sends that form.",
                "system": "The system reads the form they already filled, checks the required fields, and sends it to the office.",
                "backend": "An account, a form record, the field values on that form, and a send log for each form.",
                "infrastructure": "A web app, a database for the form and its fields, and a way to deliver the finished form.",
                "modules": (
                    "M0 Form send. Bootstrap focuses on M0. The person sends one form. "
                    "Not in this module: the other forms. "
                    "M1 Other forms. The person sends the rest. Not in this module: a new office."
                ),
            },
        )
        code, message = dispatch(
            ["promote"],
            root=self.root,
            templates=self.templates,
            today=self.now.date(),
            now=self.now,
        )
        self.assertEqual(code, 0, message)
        self.assertTrue((self.root / "intake" / "form-file-listing.md").exists())
        text = (self.root / "intake" / "form-file-listing.md").read_text(encoding="utf-8")
        self.assertIn("## Scope modules", text)
        self.assertIn("## User tasks", text)
        self.assertIn("## System tasks", text)
        self.assertIn("## Backend", text)
        self.assertIn("## Infrastructure", text)
        self.assertIn("Bootstrap focuses on", text)
        self.assertNotIn("Deliver the one job", text)
        self.assertNotIn("[", text)

    def test_budget_wrap_up_and_hard_stop(self):
        self.desk.start("gap", "small", {}, True)
        for _i in range(7):
            self.desk.search("reddit", "new")
        with self.assertRaises(Exception) as caught:
            self.desk.search("reddit", "new")
        self.assertIn("wrap-up", str(caught.exception))
        # fresh session at the hard cap
        desk = Desk(self.root, self.templates, today=self.now.date(), now=self.now)
        # close is already closed by wrap? wrap does not close. Open a forced new one.
        desk.start("second", "small", {"max-searches": "2"}, True)
        desk.search("hn", "new")
        message = desk.search("hn", "empty")
        self.assertIn("incomplete", message)
        short = (self.root / "ideation" / "shortlist" / "2026-10-01.md").read_text(encoding="utf-8")
        self.assertIn("incomplete: budget reached", short)

    def test_file_cap_fails_loudly(self):
        self.desk.seed()
        budgets = self.root / "ideation" / "budgets.yaml"
        text = budgets.read_text(encoding="utf-8").replace("problem_file_bytes: 25600", "problem_file_bytes: 80")
        budgets.write_text(text, encoding="utf-8")
        with self.assertRaises(Exception) as caught:
            self.desk.add_problem(
                {
                    "sentence": "A sentence that is long enough to blow a tiny cap on the problem file itself",
                    "keywords": "tiny, cap, file",
                }
            )
        self.assertIn("exceeds", str(caught.exception))
        self.assertFalse((self.root / "ideation" / "problems" / "P-001.md").exists())

    def test_wedge_caps_competitor_weakness(self):
        self.desk.seed()
        self.desk.add_problem(
            {
                "sentence": "Teams still forward email by hand",
                "keywords": "email, forward, hand",
                "segment": "teams",
            }
        )
        self.desk.add_competitor({"name": "Incumbent", "category": "mail"})
        self.desk.add_idea(
            {
                "title": "Mail helper",
                "problems": "P-001",
                "shape": "SaaS",
                "competitors": "C-001",
                "crowdedness": "crowded",
            }
        )
        with self.assertRaises(Exception) as caught:
            self.desk.score("I-001", "competitor_weakness", "4", "https://example.com 2026-06-01")
        self.assertIn("wedge", str(caught.exception))

    def test_discard_reason_blocks_rediscovery(self):
        self.desk.seed()
        self.desk.add_problem(
            {
                "sentence": "Cyclists lose the route gpx",
                "keywords": "cycle, route, gpx",
                "segment": "cyclists",
            }
        )
        self.desk.discard("P-001", "already a free official file")
        with self.assertRaises(Exception) as caught:
            self.desk.add_problem(
                {
                    "sentence": "Cyclists lose the route gpx",
                    "keywords": "bike, map, file",
                    "segment": "cyclists",
                }
            )
        self.assertIn("discarded", str(caught.exception))
        self.assertIn("already a free official file", str(caught.exception))

    def test_import_skips_unsourced_pains(self):
        db_path = self.root / "incubator.db"
        conn = sqlite3.connect(db_path)
        conn.execute("CREATE TABLE pain_points (id TEXT, description TEXT, frequency INT, source_ids TEXT, created_at TEXT)")
        conn.execute("CREATE TABLE raw_signals (id TEXT, source_url TEXT, date_posted TEXT, scraped_at TEXT, author TEXT, source_type TEXT, title TEXT)")
        conn.execute(
            "INSERT INTO pain_points VALUES ('p1', 'Users cannot export the ledger', 2, '[\"s1\"]', '2026-01-01')"
        )
        conn.execute(
            "INSERT INTO raw_signals VALUES ('s1', 'https://example.com/pain', '2026-05-01', NULL, 'ada', 'hn', 'thread-a')"
        )
        conn.execute(
            "INSERT INTO pain_points VALUES ('p2', 'No source on this pain', 1, '[]', '2026-01-01')"
        )
        conn.execute(
            "INSERT INTO pain_points VALUES ('p3', 'Zoom fatigue during standups', 1, 'https://www.g2.com/products/zoom/reviews', '2026-04-11T19:01:58')"
        )
        conn.execute(
            "INSERT INTO raw_signals VALUES ('s3', 'https://www.g2.com/products/zoom/reviews', NULL, '2026-04-11T18:52:41', 'G2 user', 'g2', 'zoom reviews')"
        )
        conn.commit()
        conn.close()
        message = self.desk.import_incubator(db_path)
        self.assertIn("Imported 2", message)
        self.assertIn("Skipped 1", message)
        body = (self.root / "ideation" / "problems" / "P-001.md").read_text(encoding="utf-8")
        self.assertNotIn("verbatim", body.lower())

    def test_present_without_shape_is_incomplete(self):
        self.desk.start("nl parents", "normal", {}, True)
        self.desk.search("hn", "new")
        self.desk.add_problem(
            {
                "sentence": "Families retype the school form",
                "keywords": "form, family, school",
            }
        )
        self.desk.add_idea(
            {
                "title": "Form listing",
                "problems": "P-001",
                "shape": "marketplace listing",
                "pitch": "Families retype the school form. A listing sends the form.",
            }
        )
        message = self.desk.present()
        self.assertIn("Incomplete", message)
        self.assertIn("shape missing: I-001", message)

    def test_present_without_research_is_incomplete(self):
        self.desk.start("nl parents", "normal", {}, True)
        message = self.desk.present()
        self.assertIn("Incomplete", message)
        self.assertIn("no searches recorded", message)
        text = (self.root / "ideation" / "shortlist" / "2026-10-01.md").read_text(encoding="utf-8")
        self.assertIn("incomplete:", text)
        self.assertIn("judged globally", text.lower())
        self.assertNotIn("of 3 ideas", text)

    def test_small_budget_can_finish_one_sourced_idea(self):
        self.desk.start("nl parents", "small", {}, True)
        self.desk.search("hn", "new")
        message = self.desk.present()
        self.assertNotIn("small budget", message)
        self.assertNotIn("Incomplete", message)

    def test_one_sourced_idea_can_finish(self):
        self.desk.start("nl parents", "normal", {}, True)
        self.desk.search("hn", "new")
        self.desk.add_competitor({"name": "Formly", "category": "forms"})
        topics = (
            ("People pay a freelancer to file a form", "form, freelancer, filing", "form"),
            ("Clubs wait months for a permit stamp", "permit, clerk, queue", "permit"),
            ("Associations miss a grant deadline", "grant, council, delay", "grant"),
        )
        for index, (sentence, keywords, keyword) in enumerate(topics):
            self.desk.add_problem(
                {
                    "sentence": sentence,
                    "keywords": keywords,
                    "segment": "families",
                    "region": "NL",
                    "language": "nl",
                }
            )
            pid = f"P-00{index + 1}"
            _evidence(self.desk, pid)
            self.desk.add_idea(
                {
                    "title": f"{keyword} listing",
                    "problems": pid,
                    "shape": "marketplace listing",
                    "pitch": f"Families struggle to file a {keyword}. A listing files that {keyword}.",
                    "competitors": "C-001",
                    "blue": ["templates", "drop upload", "keep the host", "dutch parents"],
                }
            )
            self.desk.shape(
                f"I-00{index + 1}",
                {
                    "problem": f"Families struggle to file a {keyword}.",
                    "solution": "A listing already files that form.",
                    "architecture": "The listing reads the form they already have.",
                    "experience": "They pick the form and send it.",
                    "steps": "They pick the form. The listing sends it.",
                    "mvp": "The first chunk sends the form.",
                    "later": "Later chunks cover the other forms.",
                },
            )
        message = self.desk.present()
        self.assertNotIn("Incomplete", message)
        text = (self.root / "ideation" / "shortlist" / "2026-10-01.md").read_text(encoding="utf-8")
        self.assertNotIn("incomplete:", text)

    def test_stop_writes_no_shortlist(self):
        self.desk.start("nl parents", "normal", {}, True)
        message = self.desk.stop("loop test")
        self.assertIn("No shortlist", message)
        self.assertFalse((self.root / "ideation" / "shortlist").exists() and any((self.root / "ideation" / "shortlist").glob("*.md")))
        self.assertIsNone(self.desk._open_session())

    def test_show_prints_the_idea_path(self):
        self.desk.seed()
        self.desk.add_problem(
            {
                "sentence": "Cyclists lose the route gpx",
                "keywords": "cycle, route, gpx",
            }
        )
        self.desk.add_idea(
            {
                "title": "Route card",
                "problems": "P-001",
                "shape": "mini web app",
                "pitch": "Cyclists lose the route file. A card shows the missing file.",
            }
        )
        text = self.desk.show("I-001")
        self.assertIn("ideation/ideas/I-001.md", text)
        self.assertIn("Route card", text)

    def test_empty_score_does_not_burn_the_pass(self):
        self.desk.start("nl parents", "small", {}, True)
        self.desk.add_problem(
            {
                "sentence": "Cyclists lose the route gpx",
                "keywords": "cycle, route, gpx",
            }
        )
        self.desk.add_idea(
            {
                "title": "Route card",
                "problems": "P-001",
                "shape": "mini web app",
                "pitch": "Cyclists lose the route file. A card shows the missing file.",
            }
        )
        self.desk.score("I-001", "fit", "empty", "no stored source")
        self.desk.score("I-001", "fit", "3", "https://example.com/src 2026-06-01")
        with self.assertRaises(Exception) as caught:
            self.desk.score("I-001", "fit", "4", "https://example.com/src 2026-06-01")
        self.assertIn("pass cap", str(caught.exception))

    def test_clinical_domain_cannot_validate_and_a_trade_web_app_can(self):
        self.desk.seed()
        self.desk.add_problem(
            {
                "sentence": "Shops lose the booking when the client does not show",
                "keywords": "shop, booking, show",
            }
        )
        _evidence(self.desk, "P-001")
        self.desk.add_competitor({"name": "Holdbook", "category": "booking"})
        clinical = self.desk.add_idea(
            {
                "title": "Medicine list",
                "problems": "P-001",
                "shape": "mini web app",
                "domain": "clinical",
                "competitors": "C-001",
                "pitch": "A family keeps medicines in one head. A list shares them.",
            }
        )
        self.assertIn("I-001", clinical)
        _score_all(self.desk, "I-001", "4")
        meta, _body = self.desk._read(self.root / "ideation" / "ideas" / "I-001.md")
        self.assertEqual(meta.get("knockout"), "medicine-out-of-reach")
        self.assertNotEqual(meta.get("status"), "validated")
        self.desk.add_idea(
            {
                "title": "Booking hold",
                "problems": "P-001",
                "shape": "mini web app",
                "domain": "trade",
                "competitors": "C-001",
                "pitch": "A shop loses the slot. A hold keeps the booking.",
            }
        )
        _score_all(self.desk, "I-002", "4")
        self.desk.score("I-002", "time_to_mvp", "3", "full web app in about two months")
        meta, _body = self.desk._read(self.root / "ideation" / "ideas" / "I-002.md")
        self.assertEqual(meta.get("status"), "validated")
        self.assertEqual(meta.get("knockout"), "")
        self.desk.score("I-002", "fit", "0", "needs a license this builder does not hold")
        meta, _body = self.desk._read(self.root / "ideation" / "ideas" / "I-002.md")
        self.assertEqual(meta.get("knockout"), "out-of-reach")
        self.assertNotEqual(meta.get("status"), "validated")

    def test_brief_asks_before_search_and_market_is_checked_later(self):
        banner = self.desk.start("", "normal", {}, True)
        self.assertIn("SECTION: brief", banner)
        with self.assertRaises(Exception) as caught:
            self.desk.search("hn", "new")
        self.assertIn("brief", str(caught.exception).lower())
        accepted = self.desk.start("clinic scheduling", "normal", {"market": "France"}, False)
        self.assertIn("SECTION: signals", accepted)
        self.assertIn("MARKET: France", accepted)
        self.desk.add_problem(
            {
                "sentence": "Clinics retype the referral fax",
                "keywords": "clinic, referral, fax",
            }
        )
        self.desk.add_idea(
            {
                "title": "Referral card",
                "problems": "P-001",
                "shape": "mini web app",
                "pitch": "Clinics retype the referral. A card keeps the referral.",
            }
        )
        with self.assertRaises(Exception) as caught:
            self.desk.qualify("I-001", "global", "no country")
        self.assertIn("applies or outside", str(caught.exception))
        self.desk.qualify("I-001", "outside", "sources are not in France")
        self.desk.shape(
            "I-001",
            {
                "problem": "Clinics retype the referral.",
                "solution": "A card already holds it.",
                "architecture": "The card reads the referral they already received.",
                "experience": "They open the card and send it on.",
                "steps": "They open the card. They send it on.",
                "mvp": "The first chunk sends the referral.",
                "later": "Later chunks cover the other clinics.",
            },
        )
        self.desk.search("hn", "new")
        message = self.desk.present()
        self.assertNotIn("Incomplete", message)
        text = (self.root / "ideation" / "shortlist" / "2026-10-01.md").read_text(encoding="utf-8")
        self.assertIn("Stated market: France", text)
        self.assertIn("does not apply", text)


if __name__ == "__main__":
    unittest.main()
