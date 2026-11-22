"""API-Sports client (free plan) for basketball, handball and football.

Free plan facts, checked on 22 Nov 2026:
  - 100 requests per day per sport.
  - Games by date work for the current season (all leagues in one request,
    with quarter or half scores).
  - Whole-season downloads only for seasons 2022-2024 (used for calibration).
  - Odds by game id work for current games, from about 9 bookmakers
    including Pinnacle, with half, quarter and team-total lines.

The key is never stored in code: this environment's network proxy adds it to
requests for these hosts. The header below is a placeholder it overwrites.
Every response is cached, so re-running a day costs no extra requests.
"""

from __future__ import annotations

import json
import os
from urllib.parse import urlencode

from .http import fetch

HOSTS = {
    "basketball": "https://v1.basketball.api-sports.io",
    "handball": "https://v1.handball.api-sports.io",
    "football": "https://v3.football.api-sports.io",
    "hockey": "https://v1.hockey.api-sports.io",
    "rugby": "https://v1.rugby.api-sports.io",
    "nfl": "https://v1.american-football.api-sports.io",
    "baseball": "https://v1.baseball.api-sports.io",
}
_KEY_HEADER = {"x-apisports-key": os.environ.get("APISPORTS_KEY", "proxy-injected")}


class ApiError(RuntimeError):
    pass


def get(sport: str, endpoint: str, max_age_hours: float = 6.0, **params) -> list[dict]:
    query = urlencode(sorted(params.items()))
    url = f"{HOSTS[sport]}/{endpoint}?{query}"
    name = f"apisports/{sport}/{endpoint}/{query.replace('&', '_').replace('=', '-') or 'all'}.json"
    body = fetch(url, name, max_age_hours, headers=_KEY_HEADER)
    data = json.loads(body)
    errors = data.get("errors")
    if errors:
        # Do not keep error responses in the cache.
        from .http import CACHE_DIR
        (CACHE_DIR / name).unlink(missing_ok=True)
        raise ApiError(f"{sport}/{endpoint}: {errors}")
    return data.get("response") or []


def games_on(sport: str, day: str, max_age_hours: float = 2.0) -> list[dict]:
    """All games on a date (YYYY-MM-DD), in Lagos time."""
    return get(sport, "games", max_age_hours, date=day, timezone="Africa/Lagos")


def odds_for_game(sport: str, game_id: int, max_age_hours: float = 2.0) -> list[dict]:
    """Bookmaker odds for one game: [{bookmakers: [{name, bets: [{name, values}]}]}]."""
    return get(sport, "odds", max_age_hours, game=game_id)


def season_games(sport: str, league: int, season: str) -> list[dict]:
    """A whole past season (free plan: 2022-2024). Cached for 30 days."""
    return get(sport, "games", 24 * 30, league=league, season=season)


def normalize(sport: str, g: dict) -> dict:
    """One shape for every sport: id, date, status, country, league, home, away.

    The American football API nests id/date/status under "game"."""
    if "game" in g:
        info = g["game"]
        d = info["date"]
        return {"id": info["id"], "date": f"{d['date']} {d['time']}", "status": info["status"]["short"],
                "country": (g["league"].get("country") or {}).get("name") or "",
                "league": g["league"]["name"], "home": g["teams"]["home"]["name"],
                "away": g["teams"]["away"]["name"]}
    return {"id": g["id"], "date": g["date"][:16].replace("T", " "), "status": g["status"]["short"],
            "country": (g.get("country") or {}).get("name") or "", "league": g["league"]["name"],
            "home": g["teams"]["home"]["name"], "away": g["teams"]["away"]["name"]}
