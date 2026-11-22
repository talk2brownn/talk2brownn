"""Daily runs for ice hockey, NFL, rugby and baseball.

Same approach as basketball and handball: read each game's expected scores
off the sharpest available lines (each market from the sharpest bookmaker
offering it), then price every market from one consistent model:
  - hockey: Poisson goal grid, regulation 1X2 plus "incl. OT" winner
  - nfl / rugby: points model with key-number margins (PointsMatch)
  - baseball: negative-binomial runs grid, extra innings split by strength
"""

from __future__ import annotations

from datetime import date

from scipy.stats import norm

from .data.apisports import ApiError, games_on, normalize, odds_for_game
from .hockey import (F5_SHARE, PERIOD_SHARE, baseball_grid, hockey_grid, implied_rates,
                     win_incl_extra)
from .odds import fair_probabilities
from .points import PERIOD_SD_SCALE, SPORT_DEFAULTS, PointsMatch
from .sheet import (PricedGame, _pairs, bookmaker_bets, half_line, implied_margin,
                    implied_total, odds_rows, price_list)

MAX_ODDS_REQUESTS = 40

TIERS = {
    "hockey": ({"nhl", "khl", "shl", "liiga", "del", "national league", "extraliga"},
               {"ahl", "allsvenskan", "del2", "swiss league", "ice hockey league", "icehl",
                "champions hockey league", "mestis", "vhl", "elite league"}),
    "nfl": ({"nfl"}, {"ncaa"}),
    "rugby": ({"premiership rugby", "top 14", "united rugby championship", "super rugby",
               "six nations", "rugby championship", "european rugby champions cup", "nrl",
               "super league", "friendly international", "autumn nations series"},
              {"pro d2", "greene king ipa championship", "european rugby challenge cup",
               "premiership rugby cup"}),
    "baseball": ({"mlb", "npb", "kbo"}, {"lmp", "lidom", "lvbp", "abl", "cpbl", "lbprc"}),
}


def tier_of(sport: str, league: str) -> str:
    a, b = TIERS[sport]
    name = league.lower()
    return "A" if name in a else "B" if name in b else "C"


# ------------------------------------------------------------ reading lines

def _devig(values: list[dict], names: tuple[str, ...]) -> list[float] | None:
    prices = {v["value"]: float(v["odd"]) for v in values if v.get("odd")}
    if not all(n in prices and prices[n] > 1 for n in names):
        return None
    return fair_probabilities([prices[n] for n in names], "power")


def _main_total(values: list[dict]) -> tuple[float, float] | None:
    """The half-point Over/Under line priced closest to even: (line, p_over)."""
    best = None
    for line, (o, u) in _pairs(values, "Over", "Under").items():
        if line != int(line) + 0.5:
            continue
        p = fair_probabilities([o, u])[0]
        if best is None or abs(p - 0.5) < abs(best[1] - 0.5):
            best = (line, p)
    return best


# ------------------------------------------------------------ hockey

def hockey_entries(bets: dict) -> tuple[list, dict] | None:
    three = _devig(bets.get("3Way Result", []), ("Home", "Draw", "Away"))
    if not three:
        return None
    total = _main_total(bets.get("Over/Under", []))
    h, a = implied_rates(three[0], three[2], total[1] if total else None,
                         total[0] if total else None, hockey_grid, default_total=6.0)
    g, p1 = hockey_grid(h, a), hockey_grid(h, a, PERIOD_SHARE)
    e = [("Home win (regulation)", "main", g.home_win()), ("Draw (regulation)", "main", g.draw()),
         ("Away win (regulation)", "main", g.away_win()),
         ("Home or Draw (1X)", "main", g.double_chance("1X")),
         ("Draw or Away (X2)", "main", g.double_chance("X2")),
         ("Home or Away (12)", "main", g.double_chance("12")),
         ("Home win incl. OT", "main", win_incl_extra(g, "home")),
         ("Away win incl. OT", "main", win_incl_extra(g, "away")),
         ("Both teams score", "main", g.btts()),
         ("Home -1.5", "main", g.handicap("home", -1.5)), ("Away +1.5", "main", g.handicap("away", 1.5)),
         ("Away -1.5", "main", g.handicap("away", -1.5)), ("Home +1.5", "main", g.handicap("home", 1.5))]
    for line in (3.5, 4.5, 5.5, 6.5, 7.5):
        e += [(f"Over {line}", "main", g.total_over(line)), (f"Under {line}", "main", 1 - g.total_over(line))]
    for side, name in (("home", "Home"), ("away", "Away")):
        for line in (1.5, 2.5, 3.5):
            e += [(f"{name} team over {line}", "main", g.team_over(side, line)),
                  (f"{name} team under {line}", "main", 1 - g.team_over(side, line))]
    e += [("1st period over 0.5", "main", p1.total_over(0.5)),
          ("1st period over 1.5", "main", p1.total_over(1.5)),
          ("1st period under 1.5", "main", 1 - p1.total_over(1.5))]
    return e, {"home_goals": round(h, 2), "away_goals": round(a, 2)}


# ------------------------------------------------------------ nfl / rugby

def points_entries(sport: str, bets: dict) -> tuple[list, dict] | None:
    total_sd, margin_sd, team_sd, _, _ = SPORT_DEFAULTS[sport]
    total = implied_total(bets.get("Over/Under", []), total_sd)
    margin = implied_margin(bets.get("Asian Handicap", []), margin_sd)
    if margin is None:
        two = _devig(bets.get("Home/Away", []), ("Home", "Away"))
        margin = margin_sd * norm.ppf(two[0]) if two else None
    if total is None or margin is None:
        return None
    shares = {}
    h1 = implied_total(bets.get("Over/Under 1st Half", []), total_sd * PERIOD_SD_SCALE["1h"])
    if h1 and 0.40 <= h1 / total <= 0.58:
        shares["1h"] = h1 / total
    q1 = implied_total(bets.get("Over/Under 1st Qtr", []), total_sd * PERIOD_SD_SCALE["q1"])
    if q1 and 0.18 <= q1 / total <= 0.30:
        shares["q1"] = q1 / total
    pm = PointsMatch(sport, (total + margin) / 2, (total - margin) / 2, shares)
    e = []
    if sport == "rugby":
        e += [("Home win", "main", pm.home_win()), ("Draw", "main", pm.draw()), ("Away win", "main", pm.away_win()),
              ("Home or Draw (1X)", "main", pm.home_win() + pm.draw()),
              ("Draw or Away (X2)", "main", pm.away_win() + pm.draw())]
        bands = (8, 13)
    else:
        e += [("Home win", "main", pm.win_two_way("home")), ("Away win", "main", pm.win_two_way("away"))]
        bands = (7, 14)
    for pts in bands:
        e += [(f"Home by {pts}+", "main", pm.win_by_at_least("home", pts)),
              (f"Away by {pts}+", "main", pm.win_by_at_least("away", pts))]
    for k in (1.0, 0.5, 0.0, -0.5):
        line = half_line(-(margin - k * margin_sd))
        e += [(f"Home handicap {line:+}", "main", pm.handicap("home", line)),
              (f"Away handicap {-line:+}", "main", pm.handicap("away", -line))]
    periods = [("game", "Total"), ("1h", "1st half")] + ([("q1", "1st quarter")] if sport == "nfl" else [])
    for period, label in periods:
        mean, sd = pm.expected_total(period), total_sd * PERIOD_SD_SCALE[period]
        for k in (1.0, 0.6, 0.3, 0.0):
            lo, hi = half_line(mean - k * sd), half_line(mean + k * sd)
            e += [(f"{label} over {lo}", "main", pm.total_over(lo, period)),
                  (f"{label} under {hi}", "main", 1 - pm.total_over(hi, period))]
    for side, name in (("home", "Home"), ("away", "Away")):
        mean = pm.expected_team(side)
        for k in (0.8, 0.4, 0.0):
            lo, hi = half_line(mean - k * team_sd), half_line(mean + k * team_sd)
            e += [(f"{name} team over {lo}", "main", pm.team_over(side, lo)),
                  (f"{name} team under {hi}", "main", 1 - pm.team_over(side, hi))]
    return e, {"total": round(total, 1), "margin": round(margin, 1), "shares": shares}


# ------------------------------------------------------------ baseball

def baseball_entries(bets: dict) -> tuple[list, dict] | None:
    two = _devig(bets.get("Home/Away", []), ("Home", "Away"))
    if not two:
        return None
    total = _main_total(bets.get("Over/Under", []))
    h, a = implied_rates(two[0], two[1], total[1] if total else None, total[0] if total else None,
                         baseball_grid, default_total=8.8, two_way=True)
    g, f5 = baseball_grid(h, a), baseball_grid(h, a, F5_SHARE)
    e = [("Home win", "main", win_incl_extra(g, "home")), ("Away win", "main", win_incl_extra(g, "away")),
         ("Home -1.5 (run line)", "main", g.handicap("home", -1.5)),
         ("Away +1.5 (run line)", "main", g.handicap("away", 1.5)),
         ("Away -1.5 (run line)", "main", g.handicap("away", -1.5)),
         ("Home +1.5 (run line)", "main", g.handicap("home", 1.5)),
         ("First 5 innings: home", "main", f5.home_win()), ("First 5 innings: away", "main", f5.away_win())]
    mean = h + a
    for k in (-3, -2, -1, 0, 1, 2):
        line = half_line(mean + k)
        e += [(f"Over {line}", "main", g.total_over(line)), (f"Under {line}", "main", 1 - g.total_over(line))]
    for k in (-1, 0, 1):
        line = half_line(mean * F5_SHARE + k)
        e += [(f"First 5 innings over {line}", "main", f5.total_over(line)),
              (f"First 5 innings under {line}", "main", 1 - f5.total_over(line))]
    for side, name, m in (("home", "Home", h), ("away", "Away", a)):
        for k in (-1, 0):
            line = half_line(m + k)
            e += [(f"{name} team over {line}", "main", g.team_over(side, line)),
                  (f"{name} team under {line + 1}", "main", 1 - g.team_over(side, line + 1))]
    return e, {"home_runs": round(h, 2), "away_runs": round(a, 2)}


BUILDERS = {
    "hockey": hockey_entries,
    "nfl": lambda bets: points_entries("nfl", bets),
    "rugby": lambda bets: points_entries("rugby", bets),
    "baseball": baseball_entries,
}


def run(sport: str, today: date | None = None, log=None) -> list[PricedGame]:
    today = today or date.today()
    games = [normalize(sport, g) for g in games_on(sport, today.isoformat())]
    games = [g for g in games if g["status"] == "NS" and tier_of(sport, g["league"]) != "C"]
    games.sort(key=lambda g: (tier_of(sport, g["league"]), g["date"]))
    out = []
    for g in games[:MAX_ODDS_REQUESTS]:
        tier = tier_of(sport, g["league"])
        try:
            picked = bookmaker_bets(odds_for_game(sport, g["id"]))
        except ApiError:
            continue
        if not picked:
            continue
        book, bets = picked
        if log:
            log(odds_rows(sport, {"id": g["id"], "date": g["date"]}, book, bets))
        built = BUILDERS[sport](bets)
        if not built:
            continue
        entries, inputs = built
        inputs["bookmaker"] = book
        seen, unique = set(), []
        for x in entries:
            if x[0] not in seen:
                seen.add(x[0])
                unique.append(x)
        pg = PricedGame(sport, f"{sport}:{g['id']}", f"{g['country']} {g['league']}".strip(), tier,
                        g["date"], g["home"], g["away"], inputs)
        pg.markets = price_list(sport, tier, unique)
        out.append(pg)
    return out
