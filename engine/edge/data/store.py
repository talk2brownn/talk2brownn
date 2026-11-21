"""SQLite store: the odds logger and the record of every pick.

The research found free sharp odds history ends with football and handball
has none at all, so recording prices ourselves (SportyBet's included) is the
asset that makes the models testable. Every run appends a snapshot; nothing
is overwritten.
"""

from __future__ import annotations

import sqlite3
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterable

from .http import DATA_DIR

DB_PATH = DATA_DIR / "edge.db"

SCHEMA = """
CREATE TABLE IF NOT EXISTS odds_snapshots (
    taken_at TEXT NOT NULL,
    source   TEXT NOT NULL,      -- e.g. football-data, sportybet, api-sports
    sport    TEXT NOT NULL,
    match_id TEXT NOT NULL,
    kickoff  TEXT,
    market   TEXT NOT NULL,      -- source column or market name, e.g. BFEH, Home or Over 2.5
    price    REAL NOT NULL
);
CREATE INDEX IF NOT EXISTS ix_odds_match ON odds_snapshots(match_id, market, taken_at);

CREATE TABLE IF NOT EXISTS picks (
    created_at  TEXT NOT NULL,
    sport       TEXT NOT NULL,
    match_id    TEXT NOT NULL,
    match       TEXT NOT NULL,
    kickoff     TEXT,
    market      TEXT NOT NULL,
    probability REAL NOT NULL,
    fair_odds   REAL NOT NULL,
    min_odds    REAL NOT NULL,
    taken_odds  REAL,            -- SportyBet price actually available, if known
    result      TEXT             -- won / lost / void, filled after the match
);
"""


def connect(path: Path = DB_PATH) -> sqlite3.Connection:
    path.parent.mkdir(parents=True, exist_ok=True)
    con = sqlite3.connect(path)
    con.executescript(SCHEMA)
    return con


def now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def log_odds(con: sqlite3.Connection, rows: Iterable[tuple[str, str, str, str, str, float]],
             taken_at: str | None = None) -> int:
    """rows: (source, sport, match_id, kickoff, market, price)."""
    t = taken_at or now()
    data = [(t, *r) for r in rows]
    con.executemany("INSERT INTO odds_snapshots VALUES (?,?,?,?,?,?,?)", data)
    con.commit()
    return len(data)
