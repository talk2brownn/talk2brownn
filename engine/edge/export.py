"""Export the day's price sheet for the website.

Writes compact JSON the browser can load quickly on mobile data:
  <out>/latest.json                 {"date": "YYYY-MM-DD"}
  <out>/<date>/index.json           sports, counts, value rules, generated time
  <out>/<date>/<sport>.json         games with [market, category, probability, min odds]

  python -m edge.export --date 2026-11-22 --out ../web/public/data
"""

from __future__ import annotations

import argparse
import json
from datetime import date, datetime, timezone
from pathlib import Path
from zoneinfo import ZoneInfo

from .today import OUTPUT_DIR, SPORTS
from .value import ABSOLUTE_MIN_ODDS, MEGA_MAX_ODDS, MEGA_MIN_ODDS, RULES, TIER_BUFFER

DEFAULT_OUT = Path(__file__).resolve().parents[2] / "web" / "public" / "data"


LAGOS = ZoneInfo("Africa/Lagos")


def lagos_kickoff(game: dict) -> str:
    """API-Sports times are already Lagos time; football-data.co.uk gives UK time."""
    if game["sport"] != "football":
        return game["kickoff"]
    try:
        uk = datetime.strptime(game["kickoff"], "%Y-%m-%d %H:%M").replace(tzinfo=ZoneInfo("Europe/London"))
    except ValueError:
        return game["kickoff"]
    return uk.astimezone(LAGOS).strftime("%Y-%m-%d %H:%M")


def compact(game: dict) -> dict:
    return {
        "id": game["match_id"], "sport": game["sport"], "league": game["league"],
        "tier": game["tier"], "kickoff": lagos_kickoff(game), "home": game["home"],
        "away": game["away"], "inputs": game["inputs"],
        "m": [[x["market"], x["category"], round(x["probability"], 4), round(x["min_odds"], 2)]
              for x in game["markets"]],
    }


def export(day: date, out: Path) -> dict:
    src = OUTPUT_DIR / day.isoformat()
    dst = out / day.isoformat()
    dst.mkdir(parents=True, exist_ok=True)
    counts = {}
    for sport in SPORTS:
        f = src / f"{sport}.json"
        if not f.exists():
            continue
        games = [compact(g) for g in json.loads(f.read_text())]
        games.sort(key=lambda g: (g["kickoff"], g["league"]))
        (dst / f"{sport}.json").write_text(json.dumps(games, separators=(",", ":")))
        counts[sport] = len(games)
    index = {
        "date": day.isoformat(),
        "generated_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "sports": counts,
        "rules": {f"{s}/{c}": {"min": lo, "max": hi, "edge": e} for (s, c), (lo, hi, e) in RULES.items()},
        "tier_buffer": TIER_BUFFER,
        "absolute_min_odds": ABSOLUTE_MIN_ODDS,
        "mega": {"min": MEGA_MIN_ODDS, "max": MEGA_MAX_ODDS, "size": 30},
    }
    (dst / "index.json").write_text(json.dumps(index, indent=1))
    (out / "latest.json").write_text(json.dumps({"date": day.isoformat()}))
    return index


def archive_odds(day: date, dest: Path) -> int:
    """Save every odds snapshot logged on `day` as a gzipped CSV, so the price
    history survives even when the machine running the engine does not."""
    import csv
    import gzip

    from .data import store

    con = store.connect()
    rows = con.execute("SELECT * FROM odds_snapshots WHERE substr(taken_at, 1, 10) = ?",
                       (day.isoformat(),)).fetchall()
    dest.mkdir(parents=True, exist_ok=True)
    with gzip.open(dest / f"{day.isoformat()}.csv.gz", "wt", newline="") as fh:
        csv.writer(fh).writerows(rows)
    return len(rows)


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--date", type=date.fromisoformat, default=date.today())
    ap.add_argument("--out", type=Path, default=DEFAULT_OUT)
    ap.add_argument("--archive-odds", type=Path, help="also save today's odds snapshots here")
    args = ap.parse_args()
    index = export(args.date, args.out)
    print(f"exported {sum(index['sports'].values())} games for {index['date']} -> {args.out}")
    if args.archive_odds:
        print(f"archived {archive_odds(args.date, args.archive_odds)} odds snapshots -> {args.archive_odds}")


if __name__ == "__main__":
    main()
