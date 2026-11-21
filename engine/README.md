# Edge engine

The pricing core of the prediction site. For football, basketball and handball it:

1. works out what each market is truly worth;
2. keeps only the selections where SportyBet's price beats that by a safety buffer (the **value picks**);
3. builds the daily ladder (2 · 5 · 10 · 20 · 50 · 100 · 200 · 500 · 1,000) and the **30-game slip** from value picks only, leaving a rung empty or the big slip short rather than padding it with bad legs.

No bet is safe. Margin is charged on every leg, so the engine's main job is refusing bad bets.

## Modules

| File | What it does |
|---|---|
| `edge/odds.py` | Bookmaker margin, and margin removal (multiplicative, power, Shin) |
| `edge/grid.py` | Final-score probability grid; prices any market as a sum over the grid, so "A or B" markets and same-match combos are priced correctly |
| `edge/football.py` | Dixon-Coles model fitted from results with time decay; expected goals read off market prices; half grids; minute-by-minute simulation for "lead by X at any time" and "goals in a row" |
| `edge/basketball.py` | Team points to totals, team totals, 1st half, quarters, winning margin and handicaps |
| `edge/handball.py` | Team goals to a score grid; all handball markets come from it |
| `edge/value.py` | Value filter: odds band and minimum edge per sport and market type, plus extra edge for lower league tiers |
| `edge/ladder.py` | Ladder optimiser (highest win chance that reaches each target, max one leg per match) and the 30-game slip |
| `edge/demo.py` | Re-prices Man City vs Fulham from SportyBet screenshots |

## Value rules

| Sport | Market type | Odds band | Minimum edge |
|---|---|---|---|
| Football | Main (O/U, team totals, BTTS, 1X2, DC) | 1.25–2.20 | 4% |
| Football | Combos ("A or B", 1X2/DC & O/U, win to nil) | 1.20–2.20 | 5% |
| Football | Stat markets (corners, cards, fouls, shots) | 1.60–2.20 | 6% |
| Basketball | Team totals, halves, quarters, margin | 1.35–2.10 | 4% |
| Handball | All | 1.60–2.20 | 7% |

- **League tier:** tier B leagues need 1 point more edge, tier C 2 points more.
- **Odds floor:** no leg below 1.10.
- **30-game slip:** legs priced 1.12–1.35, and each one must still clear its edge rule.

## Run

```bash
cd engine
pip install numpy scipy pytest
python -m pytest        # tests
python -m edge.demo     # Man City vs Fulham example
```
