"""Daily command: price today's matches, log odds, and (given SportyBet
prices) list value picks and build the ladder and the 30-game slip.

  python -m edge.today                       # football price sheet
  python -m edge.today --prices prices.csv   # + value picks and ladder

prices.csv columns: home,away,market,odds  (SportyBet prices you saw; team
names and market names as printed in the price sheet).
"""

from __future__ import annotations

import argparse
import csv
import json
from datetime import date
from pathlib import Path

from .data import store
from .data.footballdata import load_fixtures
from .data.http import DATA_DIR
from .football_day import PricedMatch, run, to_dict
from .ladder import build_ladder, build_mega_slip
from .value import Selection, check

OUTPUT_DIR = DATA_DIR.parent / "output"
_META = {"Div", "Date", "Time", "HomeTeam", "AwayTeam", "Referee"}


def log_fixture_odds() -> int:
    con = store.connect()
    rows = []
    for f in load_fixtures():
        for k, v in f.raw.items():
            if k in _META or k == "AHh":
                continue
            price = f.num(k)
            if price and price > 1:
                rows.append(("football-data", "football", f.match_id,
                             f"{f.date.isoformat()} {f.time}", k, price))
    return store.log_odds(con, rows)


def selections_from_prices(matches: list[PricedMatch], path: Path) -> list[Selection]:
    index = {(m.home.lower(), m.away.lower()): m for m in matches}
    sels = []
    with path.open() as fh:
        for row in csv.DictReader(fh):
            m = index.get((row["home"].strip().lower(), row["away"].strip().lower()))
            if not m:
                print(f"  ! no fixture for {row['home']} vs {row['away']}")
                continue
            pm = next((x for x in m.markets if x.market.lower() == row["market"].strip().lower()), None)
            if not pm:
                print(f"  ! unknown market '{row['market']}' for {m.label}")
                continue
            sels.append(Selection("football", pm.category, m.match_id, m.label, pm.market, "Yes",
                                  float(row["odds"]), pm.probability, m.tier, m.kickoff))
    return sels


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--date", type=date.fromisoformat, default=date.today())
    ap.add_argument("--div", action="append", help="limit to division codes, e.g. E0")
    ap.add_argument("--top", type=int, default=3, help="candidates shown per match")
    ap.add_argument("--prices", type=Path, help="CSV of SportyBet prices")
    ap.add_argument("--no-log", action="store_true", help="skip the odds logger")
    args = ap.parse_args()

    if not args.no_log:
        print(f"odds logger: stored {log_fixture_odds()} prices")
    matches = run(args.date, set(args.div) if args.div else None)
    out_dir = OUTPUT_DIR / args.date.isoformat()
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / "football.json").write_text(json.dumps([to_dict(m) for m in matches], indent=1))
    print(f"priced {len(matches)} matches -> {out_dir / 'football.json'}\n")

    for m in matches:
        cands = sorted((x for x in m.markets if x.in_band), key=lambda x: x.probability, reverse=True)
        xs = f"xG {m.xg[0]:.2f}-{m.xg[1]:.2f}"
        print(f"{m.kickoff}  {m.league} (tier {m.tier})  {m.label}  [{xs}]")
        for x in cands[: args.top]:
            print(f"    {x.market:30} chance {x.probability:5.1%}  fair {x.fair_odds:5.2f}  "
                  f"bet only at {x.min_odds:5.2f}+")
    if not args.prices:
        return

    sels = selections_from_prices(matches, args.prices)
    print("\nSportyBet prices checked:")
    for s in sels:
        ok, why = check(s)
        print(f"  {'VALUE' if ok else '  -  '}  {s.match:34} {s.market:28} @ {s.odds:.2f}  ({why})")
    print("\nLadder (value picks only):")
    for slip in build_ladder(sels):
        if not slip.legs:
            print(f"  {slip.target:>5}: empty - {slip.note}")
            continue
        print(f"  {slip.target:>5}: {len(slip.legs)} legs, odds {slip.total_odds:.2f}, "
              f"wins 1 in {slip.one_in:.1f}, returns {slip.expected_return:.2f} per 1 staked")
        for s in slip.legs:
            print(f"           {s.match} - {s.market} @ {s.odds:.2f}")
    mega = build_mega_slip(sels)
    print(f"\n30-game slip: {len(mega.legs)} legs, odds {mega.total_odds:.2f}, "
          f"wins 1 in {mega.one_in:.0f}. {mega.note}")


if __name__ == "__main__":
    main()
