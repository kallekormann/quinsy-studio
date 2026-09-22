"""Exclusive lock for studio HQ JSON/markdown writers (parallel chats)."""

from __future__ import annotations

import fcntl
import threading
from contextlib import contextmanager
from pathlib import Path
from typing import Iterator, Optional

QUINSY_STUDIO = Path(__file__).parent.parent
CACHE_DIR = QUINSY_STUDIO / ".cache"

_local = threading.local()
_name_rlocks: dict[str, threading.RLock] = {}
_rlock_guard = threading.Lock()


def _rlock_for(name: str) -> threading.RLock:
    with _rlock_guard:
        if name not in _name_rlocks:
            _name_rlocks[name] = threading.RLock()
        return _name_rlocks[name]


@contextmanager
def hq_write_lock(name: str = "hq", *, cache_dir: Optional[Path] = None) -> Iterator[Path]:
    """Process-wide exclusive lock; re-entrant in the same thread (load-modify-save)."""
    rlock = _rlock_for(name)
    rlock.acquire()
    depths: dict = getattr(_local, "depth", None) or {}
    depth = int(depths.get(name, 0))
    depths[name] = depth + 1
    _local.depth = depths
    lock_path = (cache_dir or CACHE_DIR) / f"{name}.lock"
    fh = None
    try:
        if depth == 0:
            lock_path.parent.mkdir(parents=True, exist_ok=True)
            fh = open(lock_path, "a+", encoding="utf-8")
            fcntl.flock(fh.fileno(), fcntl.LOCK_EX)
            _local.files = getattr(_local, "files", {})
            _local.files[name] = fh
        yield lock_path
    finally:
        depths[name] = depth
        if depth == 0:
            held = getattr(_local, "files", {}).pop(name, fh)
            if held is not None:
                try:
                    fcntl.flock(held.fileno(), fcntl.LOCK_UN)
                except OSError:
                    pass
                held.close()
        rlock.release()
