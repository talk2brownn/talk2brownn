"""Daily command: price today's games in every sport (football, basketball,
handball, ice hockey, NFL, rugby, baseball), log every odds
snapshot, and (given SportyBet prices) list value picks and build the ladder
and the 30-game slip.

  python -m edge.today                          # all seven sports
  python -m edge.today --sport basketball       # one sport
  python -m edge.today --prices prices.csv      # + value picks, ladder, big slip

prices.csv columns: sport,home,away,market,odds  (the SportyBet prices you
saw; team and market names exactly as printed in the price sheet).
"""

from __future__ import annotations

import argparse
import csv
import json
from datetime import date
from pathlib import Path

from . import basketball_day, football_day, handball_day, multisport_day
from .data import store
from .data.footballdata import load_fixtures
from .data.http import DATA_DIR
from .ladder import build_ladder, build_mega_slip
from .sheet import PricedGame
from .value import Selection, check

OUTPUT_DIR = DATA_DIR.parent / "output"
SPORTS = ("football", "basketball", "handball", "hockey", "nfl", "rugby", "baseball")
_META = {"Div", "Date", "Time", "HomeTeam", "AwayTeam", "Referee", "AHh", "AHCh"}


def football_odds_rows() -> list[tuple]:
    rows = []
    for f in load_fixtures():
        for k in f.raw:
            price = None if k in _META else f.num(k)
            if price and price > 1:
                rows.append(("football-data", "football", f.match_id,
                             f"{f.date.isoformat()} {f.time}", k, price))
    return rows


def price_sport(sport: str, day: date, divisions: set[str] | None, con) -> list[PricedGame]:
    log = (lambda rows: store.log_odds(con, rows)) if con else None
    if sport == "football":
        if log:
            log(football_odds_rows())
        return football_day.run(day, divisions)
    if sport == "basketball":
        return basketball_day.run(day, log)
    if sport == "handball":
        return handball_day.run(day, log)
    return multisport_day.run(sport, day, log)


def selections_from_prices(games: list[PricedGame], path: Path) -> list[Selection]:
    index = {(g.sport, g.home.lower(), g.away.lower()): g for g in games}
    sels = []
    with path.open() as fh:
        for row in csv.DictReader(fh):
            key = (row["sport"].strip().lower(), row["home"].strip().lower(), row["away"].strip().lower())
            g = index.get(key)
            if not g:
                print(f"  ! no {key[0]} game for {row['home']} vs {row['away']}")
                continue
            pm = next((x for x in g.markets if x.market.lower() == row["market"].strip().lower()), None)
            if not pm:
                print(f"  ! unknown market '{row['market']}' for {g.label}")
                continue
            sels.append(Selection(g.sport, pm.category, g.match_id, g.label, pm.market, "Yes",
                                  float(row["odds"]), pm.probability, g.tier, g.kickoff))
    return sels


def print_sheet(games: list[PricedGame], top: int) -> None:
    for g in games:
        cands = sorted((x for x in g.markets if x.in_band), key=lambda x: x.probability, reverse=True)
        print(f"{g.kickoff}  {g.league} (tier {g.tier})  {g.label}")
        for x in cands[:top]:
            print(f"    {x.market:34} chance {x.probability:5.1%}  fair {x.fair_odds:5.2f}  "
                  f"bet only at {x.min_odds:5.2f}+")


def print_ladder(sels: list[Selection]) -> None:
    print("\nSportyBet prices checked:")
    for s in sels:
        ok, why = check(s)
        print(f"  {'VALUE' if ok else '  -  '}  {s.match:36} {s.market:30} @ {s.odds:.2f}  ({why})")
    print("\nLadder (value picks only):")
    for slip in build_ladder(sels):
        if not slip.legs:
            print(f"  {slip.target:>5}: empty - {slip.note}")
            continue
        print(f"  {slip.target:>5}: {len(slip.legs)} legs, odds {slip.total_odds:.2f}, "
              f"wins 1 in {slip.one_in:.1f}, returns {slip.expected_return:.2f} per 1 staked")
        for s in slip.legs:
            print(f"           [{s.sport}] {s.match} - {s.market} @ {s.odds:.2f}")
    mega = build_mega_slip(sels)
    print(f"\n30-game slip: {len(mega.legs)} legs, odds {mega.total_odds:.2f}, "
          f"wins 1 in {mega.one_in:.0f}. {mega.note}")


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--date", type=date.fromisoformat, default=date.today())
    ap.add_argument("--sport", choices=SPORTS, action="append", help="default: all three")
    ap.add_argument("--div", action="append", help="football division codes, e.g. E0")
    ap.add_argument("--top", type=int, default=3, help="candidates shown per game")
    ap.add_argument("--prices", type=Path, help="CSV of SportyBet prices")
    ap.add_argument("--no-log", action="store_true", help="skip the odds logger")
    args = ap.parse_args()

    con = None if args.no_log else store.connect()
    out_dir = OUTPUT_DIR / args.date.isoformat()
    out_dir.mkdir(parents=True, exist_ok=True)
    all_games: list[PricedGame] = []
    for sport in args.sport or SPORTS:
        games = price_sport(sport, args.date, set(args.div) if args.div else None, con)
        (out_dir / f"{sport}.json").write_text(json.dumps([g.to_dict() for g in games], indent=1))
        print(f"\n=== {sport}: {len(games)} games priced -> {out_dir / (sport + '.json')}\n")
        print_sheet(games, args.top)
        all_games += games
    if args.prices:
        print_ladder(selections_from_prices(all_games, args.prices))


if __name__ == "__main__":
    main()
