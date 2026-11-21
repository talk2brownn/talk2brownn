"""Demo: re-price Man City vs Fulham from the user's SportyBet screenshots.

Step 1 reads the match's expected goals from SportyBet's own main lines
(double chance and Over/Under 2.5, with the margin removed).
Step 2 prices every side market from that one grid and compares it with
SportyBet's price. A negative edge means SportyBet charges more than its own
main lines imply. Prices were copied from the 21 Nov 2026 screen recording.

Run:  python -m edge.demo
"""

from __future__ import annotations

from .football import FootballMatch, simulate_paths, xg_from_market
from .odds import fair_probabilities


def main() -> None:
    # Double chance 1X / 12 / X2 = 1.12 / 1.16 / 2.80. These three cover each
    # outcome twice, so scale the implied probabilities to sum to 2.
    dc = [1 / 1.12, 1 / 1.16, 1 / 2.80]
    dc = [x * 2 / sum(dc) for x in dc]
    p_home, p_draw, p_away = 1 - dc[2], 1 - dc[1], 1 - dc[0]
    p_over = fair_probabilities([1.41, 3.00], "power")[0]  # Over/Under 2.5
    lam, mu = xg_from_market(p_home, p_away, p_over)
    m = FootballMatch(lam, mu)
    g = m.full
    paths = simulate_paths(lam, mu, n_sims=200_000, seed=21)

    print("Man City vs Fulham, from SportyBet's own main lines")
    print(f"  market-implied: home {p_home:.1%}  draw {p_draw:.1%}  away {p_away:.1%}  over 2.5 {p_over:.1%}")
    print(f"  expected goals: Man City {lam:.2f}  Fulham {mu:.2f}\n")

    clean_sheet = lambda h, a: (h == 0) | (a == 0)  # noqa: E731
    rows = [
        ("Home or Over 2.5", 1.14, g.prob(lambda h, a: (h > a) | (h + a > 2.5))),
        ("Home or Under 2.5", 1.14, g.prob(lambda h, a: (h > a) | (h + a < 2.5))),
        ("Home or GG", 1.06, g.prob(lambda h, a: (h > a) | ((h > 0) & (a > 0)))),
        ("Away or GG", 1.48, g.prob(lambda h, a: (a > h) | ((h > 0) & (a > 0)))),
        ("Draw or GG", 1.53, g.prob(lambda h, a: (h == a) | ((h > 0) & (a > 0)))),
        ("Away or Over 2.5", 1.31, g.prob(lambda h, a: (a > h) | (h + a > 2.5))),
        ("Away or Under 2.5", 2.25, g.prob(lambda h, a: (a > h) | (h + a < 2.5))),
        ("Home or any clean sheet", 1.23, g.prob(lambda h, a: (h > a) | clean_sheet(h, a))),
        ("Draw or any clean sheet", 1.70, g.prob(lambda h, a: (h == a) | clean_sheet(h, a))),
        ("Home win to nil", 2.85, g.win_to_nil("home")),
        ("Away win to nil", 12.00, g.win_to_nil("away")),
        ("Man City over 1.5", 1.36, g.team_over("home", 1.5)),
        ("Man City over 2.5", 2.10, g.team_over("home", 2.5)),
        ("1st half over 0.5", 1.22, m.first_half.total_over(0.5)),
        ("1st half over 1.5", 2.05, m.first_half.total_over(1.5)),
        ("2nd half over 0.5", 1.15, m.second_half.total_over(0.5)),
        ("2nd half over 1.5", 1.68, m.second_half.total_over(1.5)),
        ("Both halves over 1.5", 3.30, m.both_halves_over(1.5)),
        ("Both halves under 1.5", 3.90, m.both_halves_under(1.5)),
        ("Highest scoring half: 2nd", 2.10, m.highest_scoring_half()["second"]),
        ("Highest scoring half: 1st", 3.00, m.highest_scoring_half()["first"]),
        ("Highest scoring half: equal", 4.20, m.highest_scoring_half()["equal"]),
        ("Home scores 2+ in a row", 1.53, paths.goals_in_a_row(2, "home")),
        ("Home scores 3+ in a row", 2.77, paths.goals_in_a_row(3, "home")),
        ("Away scores 2+ in a row", 5.13, paths.goals_in_a_row(2, "away")),
        ("Home leads by 3 at any time", 2.89, paths.lead_by_at_any_time(3, "home")),
        ("Away leads by 1 at any time", 2.72, paths.lead_by_at_any_time(1, "away")),
        ("Away leads by 2 at any time", 7.47, paths.lead_by_at_any_time(2, "away")),
    ]
    print(f"  {'market':32} {'SportyBet':>9} {'fair':>7} {'edge':>7}")
    for name, odds, p in sorted(rows, key=lambda r: r[1] * r[2], reverse=True):
        print(f"  {name:32} {odds:9.2f} {1 / p:7.2f} {p * odds - 1:+7.1%}")
    print("\n  Edge here is measured against SportyBet's own main lines, not against a")
    print("  model of the teams. It shows where SportyBet's side markets charge more")
    print("  (negative) or less (positive) than its main prices imply.")


if __name__ == "__main__":
    main()
