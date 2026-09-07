#!/usr/bin/env python3
from studio_learning_gate import can_infuse_project_sprint, infusion_gate_message, open_lo_tickets


def test_open_lo_list_is_list():
    assert isinstance(open_lo_tickets(), list)


def test_infusion_message_when_open(monkeypatch, tmp_path):
    backlog = tmp_path / "backlog" / "open"
    backlog.mkdir(parents=True)
    (backlog / "LO-0099-test.md").write_text(
        "---\nid: LO-0099\ntitle: Test item\npriority: P1\n---\n",
        encoding="utf-8",
    )
    import studio_learning_gate as gate

    monkeypatch.setattr(gate, "BACKLOG_OPEN", backlog)
    msg = infusion_gate_message()
    assert msg is not None
    assert "LO-0099" in msg
    ok, _ = can_infuse_project_sprint()
    assert ok is True
