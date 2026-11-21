"""football-data.co.uk: free results, match stats, xG and odds.

- Season files (mmz4281/{season}/{div}.csv): results, half-time scores,
  shots, corners, fouls, cards, referee, xG (from 2026/27) and opening and
  closing odds from about 8 bookmakers including the Betfair Exchange.
- fixtures.csv: this week's upcoming matches with the same odds columns.

Team names are identical in both, so history and fixtures join cleanly.
"""

from __future__ import annotations

import csv
import io
from dataclasses import dataclass
from datetime import date, datetime

from .http import fetch

BASE = "https://www.football-data.co.uk"

# Division code -> (name, tier). Tier A: full SportyBet market menu and the
# richest data; B: core markets; C: main lines only.
DIVISIONS: dict[str, tuple[str, str]] = {
    "E0": ("England Premier League", "A"), "SP1": ("Spain La Liga", "A"),
    "D1": ("Germany Bundesliga", "A"), "I1": ("Italy Serie A", "A"),
    "F1": ("France Ligue 1", "A"),
    "E1": ("England Championship", "B"), "D2": ("Germany 2. Bundesliga", "B"),
    "I2": ("Italy Serie B", "B"), "SP2": ("Spain Segunda", "B"),
    "F2": ("France Ligue 2", "B"), "N1": ("Netherlands Eredivisie", "B"),
    "B1": ("Belgium Pro League", "B"), "P1": ("Portugal Liga", "B"),
    "T1": ("Turkey Super Lig", "B"), "G1": ("Greece Super League", "B"),
    "SC0": ("Scotland Premiership", "B"),
    "E2": ("England League One", "C"), "E3": ("England League Two", "C"),
    "EC": ("England National League", "C"), "SC1": ("Scotland Championship", "C"),
    "SC2": ("Scotland League One", "C"), "SC3": ("Scotland League Two", "C"),
}


@dataclass
class MatchRow:
    div: str
    date: date
    time: str
    home: str
    away: str
    raw: dict[str, str]

    def num(self, key: str) -> float | None:
        v = self.raw.get(key, "")
        try:
            return float(v)
        except ValueError:
            return None

    @property
    def match_id(self) -> str:
        return f"{self.div}:{self.date.isoformat()}:{self.home}:{self.away}"


def season_code(d: date) -> str:
    """European seasons start in July: 21 Nov 2026 -> '2627'."""
    start = d.year if d.month >= 7 else d.year - 1
    return f"{start % 100:02d}{(start + 1) % 100:02d}"


def previous_seasons(d: date, n: int) -> list[str]:
    start = d.year if d.month >= 7 else d.year - 1
    return [f"{(start - k) % 100:02d}{(start - k + 1) % 100:02d}" for k in range(n)]


def load_season(div: str, season: str, max_age_hours: float = 12.0) -> list[MatchRow]:
    """Finished matches for one division and season. Missing files -> []."""
    try:
        body = fetch(f"{BASE}/mmz4281/{season}/{div}.csv", f"fd/{season}/{div}.csv", max_age_hours)
    except Exception:
        return []
    return [r for r in _parse(body) if r.raw.get("FTHG", "") != ""]


def load_history(div: str, today: date, seasons: int = 3) -> list[MatchRow]:
    rows: list[MatchRow] = []
    for i, s in enumerate(previous_seasons(today, seasons)):
        # Past seasons never change, so cache them for a long time.
        rows += load_season(div, s, max_age_hours=12.0 if i == 0 else 24 * 30)
    return sorted(rows, key=lambda r: r.date)


def load_fixtures(max_age_hours: float = 3.0) -> list[MatchRow]:
    body = fetch(f"{BASE}/fixtures.csv", "fd/fixtures.csv", max_age_hours)
    return [r for r in _parse(body) if r.div in DIVISIONS]


def _parse(body: bytes) -> list[MatchRow]:
    text = body.decode("utf-8-sig", errors="replace")
    out = []
    for raw in csv.DictReader(io.StringIO(text)):
        if not raw.get("HomeTeam"):
            continue
        d = _date(raw.get("Date", ""))
        if d is None:
            continue
        out.append(MatchRow(raw.get("Div", ""), d, raw.get("Time", ""),
                            raw["HomeTeam"].strip(), raw["AwayTeam"].strip(), raw))
    return out


def _date(s: str) -> date | None:
    for fmt in ("%d/%m/%Y", "%d/%m/%y"):
        try:
            return datetime.strptime(s.strip(), fmt).date()
        except ValueError:
            continue
    return None
