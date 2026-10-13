#!/usr/bin/env python3
"""Session bind, leases, and Cursor hook decisions (LO-0419–0424)."""

import tempfile
import unittest
from pathlib import Path

from studio_agent_sessions import bind_session, bound_project, clear_session, session_id_from_hook
from studio_execute_leases import acquire_execute_lease
from studio_session_hooks import hook_response, inject_session, read_decision, shell_decision


CURSOR = {"runtime": "cursor"}
CLAUDE = {"runtime": "claude"}


class SessionStoreTests(unittest.TestCase):
    def test_conversation_id_is_the_session(self):
        self.assertEqual(
            session_id_from_hook({"conversation_id": "chat-a", "generation_id": "turn-1"}),
            "chat-a",
        )
        self.assertEqual(session_id_from_hook({"session_id": "chat-a"}), "chat-a")

    def test_two_sessions_bind_two_projects(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            projects = root / "projects"
            sessions = root / "sessions"
            for name in ("alpha", "beta"):
                (projects / name).mkdir(parents=True)
            ok, _ = bind_session("alpha", "chat-a", session_dir=sessions, projects_dir=projects, settings=CURSOR)
            self.assertTrue(ok)
            ok, _ = bind_session("beta", "chat-b", session_dir=sessions, projects_dir=projects, settings=CURSOR)
            self.assertTrue(ok)
            self.assertEqual(bound_project("chat-a", session_dir=sessions), "alpha")
            self.assertEqual(bound_project("chat-b", session_dir=sessions), "beta")
            self.assertTrue(clear_session("chat-a", session_dir=sessions))
            self.assertEqual(bound_project("chat-a", session_dir=sessions), "")
            self.assertEqual(bound_project("chat-b", session_dir=sessions), "beta")

    def test_non_cursor_runtime_refuses_bind(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "projects" / "alpha").mkdir(parents=True)
            sessions = root / "sessions"
            ok, msg = bind_session(
                "alpha", "chat-a", session_dir=sessions, projects_dir=root / "projects", settings=CLAUDE
            )
            self.assertFalse(ok)
            self.assertIn("not cursor", msg)
            self.assertEqual(list(sessions.glob("*.json")), [])


class LeaseSessionTests(unittest.TestCase):
    def test_second_session_cannot_take_the_same_project(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            ok, _ = acquire_execute_lease("alpha", lease_dir=root, session_id="chat-a", max_projects=5, now=1.0)
            self.assertTrue(ok)
            ok, msg = acquire_execute_lease("alpha", lease_dir=root, session_id="chat-b", max_projects=5, now=2.0)
            self.assertFalse(ok)
            self.assertIn("REFUSED", msg)
            ok, _ = acquire_execute_lease("beta", lease_dir=root, session_id="chat-b", max_projects=5, now=2.0)
            self.assertTrue(ok)

    def test_same_session_refreshes(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            acquire_execute_lease("alpha", lease_dir=root, session_id="chat-a", max_projects=1, now=1.0)
            ok, msg = acquire_execute_lease("alpha", lease_dir=root, session_id="chat-a", max_projects=1, now=2.0)
            self.assertTrue(ok, msg)


class HookDecisionTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        self.projects = self.root / "projects"
        self.sessions = self.root / "sessions"
        for name in ("alpha", "beta"):
            (self.projects / name).mkdir(parents=True)
        bind_session("alpha", "chat-a", session_dir=self.sessions, projects_dir=self.projects, settings=CURSOR)

    def tearDown(self):
        self.tmp.cleanup()

    def test_bound_chat_cannot_read_sibling(self):
        denied = read_decision(
            {"conversation_id": "chat-a", "file_path": str(self.projects / "beta" / "readme.md")},
            studio_root=self.root,
            session_dir=self.sessions,
            settings=CURSOR,
        )
        self.assertEqual(denied["permission"], "deny")
        allowed = read_decision(
            {"conversation_id": "chat-a", "file_path": str(self.projects / "alpha" / "readme.md")},
            studio_root=self.root,
            session_dir=self.sessions,
            settings=CURSOR,
        )
        self.assertEqual(allowed["permission"], "allow")

    def test_secret_is_denied_even_in_the_bound_project(self):
        denied = read_decision(
            {"conversation_id": "chat-a", "file_path": str(self.projects / "alpha" / ".env")},
            studio_root=self.root,
            session_dir=self.sessions,
            settings=CURSOR,
        )
        self.assertEqual(denied["permission"], "deny")

    def test_non_cursor_runtime_allows_the_sibling_read(self):
        allowed = read_decision(
            {"conversation_id": "chat-a", "file_path": str(self.projects / "beta" / "readme.md")},
            studio_root=self.root,
            session_dir=self.sessions,
            settings=CLAUDE,
        )
        self.assertEqual(allowed["permission"], "allow")

    def test_sibling_git_is_denied(self):
        denied = shell_decision(
            {"conversation_id": "chat-a", "command": f"git -C {self.projects / 'beta'} status"},
            studio_root=self.root,
            session_dir=self.sessions,
            settings=CURSOR,
        )
        self.assertEqual(denied["permission"], "deny")
        allowed = shell_decision(
            {"conversation_id": "chat-a", "command": f"git -C {self.projects / 'alpha'} status"},
            studio_root=self.root,
            session_dir=self.sessions,
            settings=CURSOR,
        )
        self.assertEqual(allowed["permission"], "allow")

    def test_unbound_session_start_does_not_guess_a_project(self):
        message = hook_response(
            {"hook_event_name": "sessionStart", "session_id": "chat-new"},
            studio_root=self.root,
            session_dir=self.sessions,
            settings=CURSOR,
        )
        self.assertIn("not bound", message["additional_context"])
        self.assertNotIn("alpha", message["additional_context"])

    def test_shell_studio_command_gains_session_id(self):
        result = inject_session(
            {
                "tool_name": "Shell",
                "conversation_id": "chat-a",
                "tool_input": {"command": "./studio execute alpha"},
            },
            settings=CURSOR,
        )
        self.assertEqual(result["updated_input"]["command"], "./studio execute alpha --session chat-a")

    def test_non_cursor_does_not_inject_session(self):
        result = inject_session(
            {
                "tool_name": "Shell",
                "conversation_id": "chat-a",
                "tool_input": {"command": "./studio execute alpha"},
            },
            settings=CLAUDE,
        )
        self.assertNotIn("updated_input", result)


if __name__ == "__main__":
    unittest.main()
