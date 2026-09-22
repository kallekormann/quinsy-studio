#!/usr/bin/env python3
import tempfile
import unittest
from pathlib import Path

from studio_execute_leases import (
    acquire_execute_lease,
    list_active_leases,
    max_concurrent_projects,
    other_live_leases,
    release_execute_lease,
)


class ExecuteLeaseTests(unittest.TestCase):
    def test_sixth_project_is_queued(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "leases"
            for i in range(5):
                ok, _ = acquire_execute_lease(
                    f"app-{i}", lease_dir=root, max_projects=5, now=1_000.0, stale_seconds=10_000
                )
                self.assertTrue(ok)
            ok, msg = acquire_execute_lease(
                "app-5", lease_dir=root, max_projects=5, now=1_000.0, stale_seconds=10_000
            )
            self.assertFalse(ok)
            self.assertIn("QUEUED", msg)
            self.assertIn("Did not rewrite isolation", msg)
            self.assertEqual(len(list_active_leases(lease_dir=root, now=1_000.0, stale_seconds=10_000)), 5)

    def test_release_allows_next(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "leases"
            for i in range(5):
                acquire_execute_lease(
                    f"app-{i}", lease_dir=root, max_projects=5, now=1.0, stale_seconds=10_000
                )
            self.assertTrue(release_execute_lease("app-0", lease_dir=root))
            ok, msg = acquire_execute_lease(
                "app-new", lease_dir=root, max_projects=5, now=2.0, stale_seconds=10_000
            )
            self.assertTrue(ok, msg)
            self.assertNotIn("app-0", other_live_leases("app-new", lease_dir=root))

    def test_focus_blocked_when_other_lease_live(self):
        from studio_execute_leases import focus_isolation_blocked

        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "leases"
            acquire_execute_lease("held-app", lease_dir=root, max_projects=5, stale_seconds=10_000)
            msg = focus_isolation_blocked("other-app", lease_dir=root)
            self.assertIsNotNone(msg)
            self.assertIn("held-app", msg)
            self.assertIsNone(focus_isolation_blocked("other-app", force=True, lease_dir=root))
            self.assertIsNone(focus_isolation_blocked("held-app", lease_dir=root))

    def test_same_project_refreshes(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "leases"
            ok, _ = acquire_execute_lease("solo", lease_dir=root, max_projects=1, now=1.0)
            self.assertTrue(ok)
            ok, _ = acquire_execute_lease("solo", lease_dir=root, max_projects=1, now=2.0)
            self.assertTrue(ok)

    def test_max_from_settings(self):
        self.assertEqual(max_concurrent_projects({"parallel": {"max_projects": 5}}), 5)
        self.assertEqual(max_concurrent_projects({"parallel": {"max_projects": 0}}), 1)


if __name__ == "__main__":
    unittest.main()
