#!/usr/bin/env python3
"""HQ write lock + concurrent-safe flock."""

from __future__ import annotations

import threading
import time
import unittest
from pathlib import Path
import tempfile

from studio_hq_lock import hq_write_lock


class HqLockTests(unittest.TestCase):
    def test_lock_serializes_threads(self):
        order: list[str] = []
        with tempfile.TemporaryDirectory() as tmp:
            cache = Path(tmp)

            def worker(tag: str) -> None:
                with hq_write_lock("test-serial", cache_dir=cache):
                    order.append(f"{tag}-in")
                    time.sleep(0.04)
                    order.append(f"{tag}-out")

            t1 = threading.Thread(target=worker, args=("a",))
            t2 = threading.Thread(target=worker, args=("b",))
            t1.start()
            t2.start()
            t1.join()
            t2.join()
        self.assertEqual(len(order), 4)
        self.assertEqual(order[0].split("-")[0], order[1].split("-")[0])
        self.assertEqual(order[2].split("-")[0], order[3].split("-")[0])


if __name__ == "__main__":
    unittest.main()
