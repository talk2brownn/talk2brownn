"""Shared pieces of the daily price sheet for every sport.

- PricedGame / PricedMarket: what the site and the CLI display.
- price_list: probability -> fair odds and the minimum SportyBet price that
  would pass the value rule for that sport, market type and league tier.
- Reading bookmaker lines: expected totals and margins implied by a
  bookmaker's Over/Under and handicap prices (API-Sports odds format).
"""

from __future__ import annotations

import statistics
from dataclasses import asdict, dataclass, field

from scipy.stats import norm

from .odds import fair_probabilities
from .value import ABSOLUTE_MIN_ODDS, RULES, TIER_BUFFER


@dataclass
class PricedMarket:
    market: str
    category: str
    probability: float
    fair_odds: float
    min_odds: float          # bet only if SportyBet offers at least this
    in_band: bool            # min_odds falls inside the value-rule odds band


@dataclass
class PricedGame:
    sport: str
    match_id: str
    league: str
    tier: str
    kickoff: str
    home: str
    away: str
    inputs: dict = field(default_factory=dict)   # what the prices were built from
    markets: list[PricedMarket] = field(default_factory=list)

    @property
    def label(self) -> str:
        return f"{self.home} vs {self.away}"

    def to_dict(self) -> dict:
        d = asdict(self)
        d["label"] = self.label
        return d


def price_list(sport: str, tier: str, entries: list[tuple[str, str, float]]) -> list[PricedMarket]:
    out = []
    for name, category, prob in entries:
        prob = float(min(max(prob, 1e-6), 1 - 1e-6))
        lo, hi, edge = RULES[(sport, category)]
        min_odds = (1 + edge + TIER_BUFFER.get(tier, 0.03)) / prob
        in_band = bool(max(lo, ABSOLUTE_MIN_ODDS) <= min_odds <= hi)
        out.append(PricedMarket(name, category, prob, 1 / prob, min_odds, in_band))
    return out


# ------------------------------------------------------------ bookmaker lines

def _pairs(values: list[dict], a: str, b: str) -> dict[float, tuple[float, float]]:
    """{line: (price_a, price_b)} for values like 'Over 213.5' / 'Home -1'."""
    got: dict[float, dict[str, float]] = {}
    for v in values:
        try:
            side, line = v["value"].rsplit(" ", 1)
            got.setdefault(float(line), {})[side] = float(v["odd"])
        except (ValueError, KeyError):
            continue
    return {line: (d[a], d[b]) for line, d in got.items() if a in d and b in d and d[a] > 1 and d[b] > 1}


def implied_total(values: list[dict], sd: float) -> float | None:
    """Expected total implied by Over/Under prices (half-point lines only)."""
    means = []
    for line, (o, u) in _pairs(values, "Over", "Under").items():
        if line != int(line) + 0.5:
            continue
        p_over = fair_probabilities([o, u], "multiplicative")[0]
        means.append(line + sd * norm.ppf(p_over))
    return statistics.median(means) if means else None


def implied_margin(values: list[dict], sd: float) -> float | None:
    """Expected home margin implied by handicap prices. API-Sports quotes the
    line from the home side: 'Home -1' / 'Away -1' are the two sides of a
    home -1 handicap."""
    means = []
    for line, (h, a) in _pairs(values, "Home", "Away").items():
        if line != int(line) + 0.5 and line != int(line) - 0.5:
            continue
        p_home = fair_probabilities([h, a], "multiplicative")[0]
        means.append(-line + sd * norm.ppf(p_home))
    return statistics.median(means) if means else None


def bookmaker_bets(odds_response: list[dict], prefer: str = "Pinnacle") -> tuple[str, dict[str, list]] | None:
    """The preferred bookmaker's bets as {bet name: values}, else the first."""
    if not odds_response:
        return None
    books = odds_response[0].get("bookmakers") or []
    if not books:
        return None
    book = next((b for b in books if b["name"] == prefer), books[0])
    return book["name"], {bet["name"]: bet["values"] for bet in book["bets"]}


def half_line(x: float) -> float:
    """Nearest .5 line, e.g. 213.2 -> 213.5."""
    return round(x - 0.5) + 0.5


def odds_rows(sport: str, game: dict, book: str, bets: dict[str, list]) -> list[tuple]:
    """Flatten one bookmaker's lines for the odds logger:
    (source, sport, match_id, kickoff, market, price)."""
    prefix = {"basketball": "bb", "handball": "hb", "football": "fb"}[sport]
    rows = []
    for bet, values in bets.items():
        for v in values:
            try:
                rows.append((f"api-sports:{book}", sport, f"{prefix}:{game['id']}", game["date"][:16],
                             f"{bet} | {v['value']}", float(v["odd"])))
            except (KeyError, ValueError):
                continue
    return rows
