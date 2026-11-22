"""Basketball daily run: today's games -> Pinnacle lines -> prices.

The evidence says NBA totals and spreads are efficiently priced, so the
engine starts from the sharpest available line (Pinnacle, else the first
bookmaker): expected total and margin give each team's expected points, and
Pinnacle's own 1st-half and quarter lines give the per-game period shares.
Everything else (team totals, halves, quarters, alternative lines, winning
margins) is priced from that. A ratings model from accumulated results is
the next layer.
"""

from __future__ import annotations

from datetime import date

from scipy.stats import norm

from .basketball import MARGIN_SD, TOTAL_SD, BasketballMatch
from .data.apisports import ApiError, games_on, odds_for_game
from .odds import fair_probabilities
from .sheet import PricedGame, bookmaker_bets, odds_rows, half_line, implied_margin, implied_total, price_list

TIER_A = {"nba", "euroleague"}
TIER_B = {"eurocup", "acb", "lega a", "bbl", "lnb", "pro a", "nbl", "cba", "vtb united league",
          "super ligi", "basket league", "aba league", "liga endesa", "lnb pro a", "bsl"}
MAX_ODDS_REQUESTS = 40
SPORT = "basketball"
PERIOD_NAMES = {"game": "Total", "1h": "1st half", "q1": "1st quarter", "q2": "2nd quarter",
                "q3": "3rd quarter", "q4": "4th quarter"}


def tier_of(league: str) -> str:
    name = league.lower()
    return "A" if name in TIER_A else "B" if name in TIER_B else "C"


def catalogue(bm: BasketballMatch) -> list[tuple[str, str, float]]:
    out = [("Home win", "main", bm.win("home")), ("Away win", "main", bm.win("away"))]
    for pts in (6, 11):
        out += [(f"Home by {pts}+", "main", bm.win_by_at_least("home", pts)),
                (f"Away by {pts}+", "main", bm.win_by_at_least("away", pts))]
    for period, label in PERIOD_NAMES.items():
        mean, sd = bm.expected_total(period), bm.total_sd[period]
        for k in (1.0, 0.6, 0.3, 0.0):
            lo, hi = half_line(mean - k * sd), half_line(mean + k * sd)
            out.append((f"{label} over {lo}", "main", bm.total_over(lo, period)))
            out.append((f"{label} under {hi}", "main", 1 - bm.total_over(hi, period)))
    for period in ("game", "1h", "q1"):
        for side, name in (("home", "Home"), ("away", "Away")):
            mean, sd = bm.expected_team(side, period), bm.team_sd[period]
            for k in (0.8, 0.4, 0.0):
                lo, hi = half_line(mean - k * sd), half_line(mean + k * sd)
                tag = "" if period == "game" else f" ({PERIOD_NAMES[period].lower()})"
                out.append((f"{name} team over {lo}{tag}", "main", bm.team_over(side, lo, period)))
                out.append((f"{name} team under {hi}{tag}", "main", 1 - bm.team_over(side, hi, period)))
    return _dedupe(out)


def match_from_lines(bets: dict[str, list]) -> tuple[BasketballMatch, dict] | None:
    total = implied_total(bets.get("Over/Under", []), TOTAL_SD["game"])
    margin = implied_margin(bets.get("Asian Handicap", []), MARGIN_SD)
    if margin is None and "Home/Away" in bets:
        prices = {v["value"]: float(v["odd"]) for v in bets["Home/Away"]}
        if "Home" in prices and "Away" in prices:
            p_home = fair_probabilities([prices["Home"], prices["Away"]])[0]
            margin = MARGIN_SD * norm.ppf(p_home)
    if total is None or margin is None:
        return None
    shares = {}
    for period, bet in (("1h", "Over/Under 1st Half"), ("q1", "Over/Under 1st Qtr"), ("q2", "Over/Under 2nd Qtr")):
        t = implied_total(bets.get(bet, []), TOTAL_SD[period])
        lo, hi = (0.45, 0.55) if period == "1h" else (0.21, 0.29)
        if t is not None and lo <= t / total <= hi:
            shares[period] = t / total
    if "1h" in shares:
        shares["2h"] = 1 - shares["1h"]
    home, away = (total + margin) / 2, (total - margin) / 2
    inputs = {"total": round(total, 1), "margin": round(margin, 1), "shares": shares}
    return BasketballMatch(home, away, shares=shares), inputs


def run(today: date | None = None, log=None) -> list[PricedGame]:
    """log: optional callback receiving raw odds rows for the odds logger."""
    today = today or date.today()
    games = [g for g in games_on("basketball", today.isoformat()) if g["status"]["short"] == "NS"]
    games.sort(key=lambda g: ("ABC".index(tier_of(g["league"]["name"])), g["date"]))
    out, requests = [], 0
    for g in games:
        tier = tier_of(g["league"]["name"])
        if tier == "C" or requests >= MAX_ODDS_REQUESTS:
            continue
        requests += 1
        try:
            picked = bookmaker_bets(odds_for_game("basketball", g["id"]))
        except ApiError:
            continue
        if not picked:
            continue
        book, bets = picked
        if log:
            log(odds_rows(SPORT, g, book, bets))
        built = match_from_lines(bets)
        if not built:
            continue
        bm, inputs = built
        inputs["bookmaker"] = book
        pg = PricedGame("basketball", f"bb:{g['id']}", f"{g['country']['name']} {g['league']['name']}",
                        tier, g["date"][:16].replace("T", " "), g["teams"]["home"]["name"],
                        g["teams"]["away"]["name"], inputs)
        pg.markets = price_list("basketball", tier, catalogue(bm))
        out.append(pg)
    return out


def _dedupe(entries):
    seen, out = set(), []
    for e in entries:
        if e[0] not in seen:
            seen.add(e[0])
            out.append(e)
    return out
