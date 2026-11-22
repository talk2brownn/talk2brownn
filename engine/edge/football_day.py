"""Football daily run: fixtures -> expected goals -> prices for every market.

For each upcoming match:
  1. Model view: Dixon-Coles fitted on the division's last 3 seasons.
  2. Market view: expected goals implied by the Betfair Exchange (or the
     bookmaker average) 1X2 and Over/Under 2.5 prices, margin removed.
  3. Blend the two. The evidence says top-league prices are very hard to
     beat, so the market gets most of the weight, a bit less in lower tiers.
  4. Price the user's favourite markets from one grid plus a goal-path
     simulation, and give each a "minimum SportyBet odds": the lowest price
     at which it would pass the value rule.
"""

from __future__ import annotations

import math
import zlib
from datetime import date

from .data.footballdata import DIVISIONS, MatchRow, load_fixtures, load_history
from .football import (FootballMatch, PathStats, Result, fit_dixon_coles,
                       simulate_paths, xg_from_market)
from .odds import fair_probabilities
from .sheet import PricedGame, PricedMarket, price_list

MARKET_WEIGHT = {"A": 0.8, "B": 0.7, "C": 0.6}


def market_catalogue(m: FootballMatch, p: PathStats) -> list[tuple[str, str, float]]:
    """(market, category, probability) for the user's football favourites."""
    g = m.full
    cs = lambda h, a: (h == 0) | (a == 0)  # noqa: E731  any clean sheet
    gg = lambda h, a: (h > 0) & (a > 0)    # noqa: E731  both teams score
    out = [
        ("Home win", "main", g.home_win()), ("Draw", "main", g.draw()), ("Away win", "main", g.away_win()),
        ("Home or Draw (1X)", "main", g.double_chance("1X")),
        ("Home or Away (12)", "main", g.double_chance("12")),
        ("Draw or Away (X2)", "main", g.double_chance("X2")),
        ("GG (both teams score)", "main", g.btts()), ("NG", "main", 1 - g.btts()),
    ]
    for line in (1.5, 2.5, 3.5):
        out += [(f"Over {line}", "main", g.total_over(line)), (f"Under {line}", "main", 1 - g.total_over(line))]
    for side, name in (("home", "Home"), ("away", "Away")):
        for line in (0.5, 1.5, 2.5):
            p_over = g.team_over(side, line)
            out += [(f"{name} team over {line}", "main", p_over),
                    (f"{name} team under {line}", "main", 1 - p_over)]
    for half, grid in (("1st half", m.first_half), ("2nd half", m.second_half)):
        for line in (0.5, 1.5):
            p_over = grid.total_over(line)
            out += [(f"{half} over {line}", "main", p_over), (f"{half} under {line}", "main", 1 - p_over)]
    out += [
        ("Home or Over 2.5", "combo", g.prob(lambda h, a: (h > a) | (h + a > 2.5))),
        ("Home or Under 2.5", "combo", g.prob(lambda h, a: (h > a) | (h + a < 2.5))),
        ("Away or Over 2.5", "combo", g.prob(lambda h, a: (a > h) | (h + a > 2.5))),
        ("Away or Under 2.5", "combo", g.prob(lambda h, a: (a > h) | (h + a < 2.5))),
        ("Draw or Over 2.5", "combo", g.prob(lambda h, a: (h == a) | (h + a > 2.5))),
        ("Home or GG", "combo", g.prob(lambda h, a: (h > a) | gg(h, a))),
        ("Away or GG", "combo", g.prob(lambda h, a: (a > h) | gg(h, a))),
        ("Draw or GG", "combo", g.prob(lambda h, a: (h == a) | gg(h, a))),
        ("Home or any clean sheet", "combo", g.prob(lambda h, a: (h > a) | cs(h, a))),
        ("Draw or any clean sheet", "combo", g.prob(lambda h, a: (h == a) | cs(h, a))),
        ("Home win to nil", "combo", g.win_to_nil("home")),
        ("Away win to nil", "combo", g.win_to_nil("away")),
        ("1X & Over 1.5", "combo", g.prob(lambda h, a: (h >= a) & (h + a > 1.5))),
        ("1X & Under 3.5", "combo", g.prob(lambda h, a: (h >= a) & (h + a < 3.5))),
        ("X2 & Over 1.5", "combo", g.prob(lambda h, a: (a >= h) & (h + a > 1.5))),
        ("X2 & Under 3.5", "combo", g.prob(lambda h, a: (a >= h) & (h + a < 3.5))),
        ("12 & Over 1.5", "combo", g.prob(lambda h, a: (h != a) & (h + a > 1.5))),
        ("Home & Over 1.5", "combo", g.prob(lambda h, a: (h > a) & (h + a > 1.5))),
        ("Home & Under 3.5", "combo", g.prob(lambda h, a: (h > a) & (h + a < 3.5))),
        ("Away & Over 1.5", "combo", g.prob(lambda h, a: (a > h) & (h + a > 1.5))),
        ("Both halves over 0.5", "combo", m.both_halves_over(0.5)),
        ("Both halves over 1.5", "combo", m.both_halves_over(1.5)),
        ("Both halves under 1.5", "combo", m.both_halves_under(1.5)),
        ("Highest scoring half: 2nd", "combo", m.highest_scoring_half()["second"]),
        ("Any team leads by 2 at any time", "combo", p.lead_by_at_any_time(2)),
        ("Home leads by 2 at any time", "combo", p.lead_by_at_any_time(2, "home")),
        ("Away leads by 1 at any time", "combo", p.lead_by_at_any_time(1, "away")),
        ("Home scores 2+ in a row", "combo", p.goals_in_a_row(2, "home")),
        ("Away scores 2+ in a row", "combo", p.goals_in_a_row(2, "away")),
    ]
    return out


def price_match(m: FootballMatch, tier: str, n_sims: int = 20_000, seed: int = 0) -> list[PricedMarket]:
    paths = simulate_paths(m.home_xg, m.away_xg, n_sims=n_sims, seed=seed)
    return price_list("football", tier, market_catalogue(m, paths))


def market_xg(row: MatchRow) -> tuple[float, float] | None:
    """Expected goals implied by exchange prices, else the bookmaker average.

    Exchange quotes on thin markets are sometimes stray (e.g. Over 2.5 at
    1.01), so a price set is used only if its margins are plausible and the
    resulting expected goals are within football's normal range.
    """
    for prefix, over, under in (("BFE", "BFE>2.5", "BFE<2.5"), ("Avg", "Avg>2.5", "Avg<2.5")):
        x = [row.num(prefix + k) for k in "HDA"]
        o, u = row.num(over), row.num(under)
        if not (all(v and v > 1 for v in x) and o and u and o > 1 and u > 1):
            continue
        if not (_plausible_margin(x) and _plausible_margin([o, u])):
            continue
        ph, _, pa = fair_probabilities(x, "power")
        po = fair_probabilities([o, u], "power")[0]
        xg = xg_from_market(ph, pa, po)
        if all(0.15 <= g <= 4.5 for g in xg):
            return xg
    return None


def _plausible_margin(odds: list[float]) -> bool:
    m = sum(1 / o for o in odds) - 1
    return -0.03 <= m <= 0.15


def run(today: date | None = None, divisions: set[str] | None = None,
        n_sims: int = 20_000) -> list[PricedGame]:
    today = today or date.today()
    fixtures = [f for f in load_fixtures() if f.date >= today
                and (divisions is None or f.div in divisions)]
    models = {}
    out = []
    for f in sorted(fixtures, key=lambda r: (r.date, r.time, r.div)):
        league, tier = DIVISIONS[f.div]
        if f.div not in models:
            hist = load_history(f.div, today)
            results = [Result(r.home, r.away, int(r.num("FTHG")), int(r.num("FTAG")),
                              (today - r.date).days) for r in hist]
            models[f.div] = fit_dixon_coles(results) if len(results) > 100 else None
        model = models[f.div]
        xg_model = None
        if model and f.home in model.attack and f.away in model.attack:
            xg_model = model.expected_goals(f.home, f.away)
        xg_mkt = market_xg(f)
        xg = blend(xg_model, xg_mkt, MARKET_WEIGHT[tier])
        if xg is None:
            continue
        rho = model.rho if model else -0.05
        fm = FootballMatch(xg[0], xg[1], rho)
        inputs = {"division": f.div, "xg": [round(x, 2) for x in xg],
                  "xg_model": [round(x, 2) for x in xg_model] if xg_model else None,
                  "xg_market": [round(x, 2) for x in xg_mkt] if xg_mkt else None}
        pm = PricedGame("football", f.match_id, league, tier, f"{f.date.isoformat()} {f.time}",
                        f.home, f.away, inputs)
        pm.markets = price_match(fm, tier, n_sims, seed=zlib.crc32(f.match_id.encode()))
        out.append(pm)
    return out


def blend(model: tuple[float, float] | None, market: tuple[float, float] | None,
          w_market: float) -> tuple[float, float] | None:
    """Weighted average in log space (i.e. a weighted geometric mean)."""
    if model is None:
        return market
    if market is None:
        return model
    return tuple(math.exp(w_market * math.log(mk) + (1 - w_market) * math.log(md))
                 for md, mk in zip(model, market))  # type: ignore[return-value]
