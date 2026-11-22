"""Handball daily run: today's games -> bookmaker lines -> prices.

Expected goals for each team come from the sharpest available total and
handicap lines (Pinnacle where offered). The score grid then prices 1X2,
double chance, handicaps, totals, team totals and 1st-half totals. SportyBet's
handball margins are 8-10%, so the value rule asks for a 7% edge and few
games will produce a pick.
"""

from __future__ import annotations

import math
from datetime import date

from .data.apisports import ApiError, games_on, odds_for_game
from .handball import TEAM_GOALS_SD, handball_grid
from .sheet import PricedGame, bookmaker_bets, odds_rows, half_line, implied_margin, implied_total, price_list

TIER_A = {("Denmark", "Herre Handbold Ligaen"), ("Germany", "Bundesliga"), ("France", "Starligue"),
          ("Spain", "Liga ASOBAL"), ("Europe", "EHF Champions League")}
TIER_B = {("Denmark", "Bambusa Kvindeligaen Women"), ("Norway", "Elkjop-ligaen"),
          ("Norway", "Elkjop-ligaen Women"), ("Sweden", "Handbollsligan"), ("Germany", "2. Bundesliga"),
          ("Europe", "EHF European League"), ("Europe", "EHF Champions League Women"),
          ("Hungary", "NB I"), ("Poland", "Superliga"), ("Portugal", "Andebol 1"),
          ("France", "Proligue"), ("Germany", "Bundesliga Women")}
MAX_ODDS_REQUESTS = 40
SPORT = "handball"
FIRST_HALF_SHARE = 0.49
MATCH_SD = TEAM_GOALS_SD * math.sqrt(2)


def tier_of(country: str, league: str) -> str:
    key = (country, league)
    return "A" if key in TIER_A else "B" if key in TIER_B else "C"


def catalogue(home: float, away: float) -> list[tuple[str, str, float]]:
    g = handball_grid(home, away)
    h1 = handball_grid(home, away, first_half_share=FIRST_HALF_SHARE)
    out = [("Home win", "main", g.home_win()), ("Draw", "main", g.draw()), ("Away win", "main", g.away_win()),
           ("Home or Draw (1X)", "main", g.double_chance("1X")),
           ("Home or Away (12)", "main", g.double_chance("12")),
           ("Draw or Away (X2)", "main", g.double_chance("X2"))]
    margin, total = home - away, home + away
    for k in (1.0, 0.5, 0.0, -0.5):
        line = half_line(-(margin - k * MATCH_SD))
        out.append((f"Home handicap {line:+}", "main", g.handicap("home", line)))
        out.append((f"Away handicap {-line:+}", "main", g.handicap("away", -line)))
    for k in (1.0, 0.6, 0.3, 0.0):
        lo, hi = half_line(total - k * MATCH_SD), half_line(total + k * MATCH_SD)
        out.append((f"Total over {lo}", "main", g.total_over(lo)))
        out.append((f"Total under {hi}", "main", 1 - g.total_over(hi)))
        lo1 = half_line(total * FIRST_HALF_SHARE - k * MATCH_SD * math.sqrt(FIRST_HALF_SHARE))
        out.append((f"1st half over {lo1}", "main", h1.total_over(lo1)))
    for side, name, mean in (("home", "Home", home), ("away", "Away", away)):
        for k in (0.8, 0.4, 0.0):
            lo, hi = half_line(mean - k * TEAM_GOALS_SD), half_line(mean + k * TEAM_GOALS_SD)
            out.append((f"{name} team over {lo}", "main", g.team_over(side, lo)))
            out.append((f"{name} team under {hi}", "main", 1 - g.team_over(side, hi)))
    seen, unique = set(), []
    for e in out:
        if e[0] not in seen:
            seen.add(e[0])
            unique.append(e)
    return unique


def run(today: date | None = None, log=None) -> list[PricedGame]:
    """log: optional callback receiving raw odds rows for the odds logger."""
    today = today or date.today()
    games = [g for g in games_on("handball", today.isoformat()) if g["status"]["short"] == "NS"]
    games.sort(key=lambda g: ("ABC".index(tier_of(g["country"]["name"], g["league"]["name"])), g["date"]))
    out = []
    for g in games[:MAX_ODDS_REQUESTS]:
        tier = tier_of(g["country"]["name"], g["league"]["name"])
        try:
            picked = bookmaker_bets(odds_for_game("handball", g["id"]))
        except ApiError:
            continue
        if not picked:
            continue
        book, bets = picked
        if log:
            log(odds_rows(SPORT, g, book, bets))
        total = implied_total(bets.get("Over/Under", []), MATCH_SD)
        margin = implied_margin(bets.get("Asian Handicap", []), MATCH_SD)
        if total is None or margin is None:
            continue
        home, away = (total + margin) / 2, (total - margin) / 2
        pg = PricedGame("handball", f"hb:{g['id']}", f"{g['country']['name']} {g['league']['name']}",
                        tier, g["date"][:16].replace("T", " "), g["teams"]["home"]["name"],
                        g["teams"]["away"]["name"],
                        {"total": round(total, 1), "margin": round(margin, 1), "bookmaker": book})
        pg.markets = price_list("handball", tier, catalogue(home, away))
        out.append(pg)
    return out
