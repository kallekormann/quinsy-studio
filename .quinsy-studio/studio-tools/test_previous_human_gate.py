#!/usr/bin/env python3
import unittest

from pre_impl_workflow import previous_human_gate_block


class PreviousGateTests(unittest.TestCase):
    def test_gate_1_refuses_when_gate_0_pending(self):
        msg = previous_human_gate_block({"human_gates": {}}, 1)
        self.assertIsNotNone(msg)
        self.assertIn("Gate 0", msg)

    def test_gate_1_ok_when_gate_0_approved(self):
        status = {"human_gates": {"0": {"status": "approved"}}}
        self.assertIsNone(previous_human_gate_block(status, 1))

    def test_reapprove_gate_1_allowed_even_if_called_again(self):
        status = {
            "human_gates": {
                "0": {"status": "approved"},
                "1": {"status": "approved"},
            }
        }
        self.assertIsNone(previous_human_gate_block(status, 1))

    def test_reapprove_does_not_require_rewriting_gate_0_when_already_on_gate_1(self):
        status = {"human_gates": {"1": {"status": "approved"}}}
        self.assertIsNone(previous_human_gate_block(status, 1))

    def test_2b_ok_when_legacy_2_approved(self):
        status = {"human_gates": {"2": {"status": "approved"}}}
        self.assertIsNone(previous_human_gate_block(status, "2b"))

    def test_2a_ok_when_gate_1_approved(self):
        status = {"human_gates": {"1": {"status": "approved"}}}
        self.assertIsNone(previous_human_gate_block(status, "2a"))


if __name__ == "__main__":
    unittest.main()
