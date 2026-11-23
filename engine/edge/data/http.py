"""Small cached downloader. Files are kept under engine/data/cache/ and only
re-downloaded when older than max_age_hours, so we stay polite to free
sources and within API limits."""

from __future__ import annotations

import time
import urllib.request
from pathlib import Path

DATA_DIR = Path(__file__).resolve().parents[2] / "data"
CACHE_DIR = DATA_DIR / "cache"
USER_AGENT = "edge-engine/0.1 (personal research)"


def fetch(url: str, name: str, max_age_hours: float = 12.0,
          headers: dict[str, str] | None = None) -> bytes:
    path = CACHE_DIR / name
    if path.exists() and time.time() - path.stat().st_mtime < max_age_hours * 3600:
        return path.read_bytes()
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT, **(headers or {})})
    with urllib.request.urlopen(req, timeout=60) as resp:
        body = resp.read()
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(body)
    return body
