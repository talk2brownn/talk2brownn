import itertools
import math

import numpy as np
import pytest

from edge.basketball import BasketballMatch
from edge.football import FootballMatch, Result, fit_dixon_coles, simulate_paths
from edge.handball import handball_grid
from edge.ladder import best_slip, build_ladder, build_mega_slip
from edge.odds import fair_probabilities, margin
from edge.value import Selection, check


# ------------------------------------------------------------------ odds

def test_margin_matches_hand_calculation():
    # Hadsten 1X2 from the user's SportyBet video: about 10%.
    assert margin([1.82, 8.00, 2.35]) == pytest.approx(0.100, abs=0.002)


@pytest.mark.parametrize("method", ["multiplicative", "power", "shin"])
def test_fair_probabilities_sum_to_one(method):
    p = fair_probabilities([1.82, 8.00, 2.35], method)
    assert sum(p) == pytest.approx(1.0)
    assert all(0 < x < 1 for x in p)


def test_power_takes_more_margin_from_longshots():
    mult = fair_probabilities([1.20, 13.0, 5.90], "multiplicative")
    power = fair_probabilities([1.20, 13.0, 5.90], "power")
    assert power[0] > mult[0] and power[1] < mult[1]


# ------------------------------------------------------------------ football grid

def test_grid_is_consistent():
    m = FootballMatch(1.6, 1.1)
    g = m.full
    assert g.home_win() + g.draw() + g.away_win() == pytest.approx(1.0)
    over, home = g.total_over(2.5), g.home_win()
    both = g.prob(lambda h, a: (h > a) & (h + a > 2.5))
    either = g.prob(lambda h, a: (h > a) | (h + a > 2.5))
    assert either == pytest.approx(home + over - both)
    # Home win and Over 2.5 are positively correlated.
    assert both > home * over


def test_half_markets():
    m = FootballMatch(1.6, 1.1)
    hs = m.highest_scoring_half()
    assert sum(hs.values()) == pytest.approx(1.0)
    assert hs["second"] > hs["first"]  # 55% of goals come after the break
    assert m.both_halves_over(1.5) < m.first_half.total_over(1.5)


def test_dixon_coles_recovers_team_strength():
    rng = np.random.default_rng(1)
    teams = [f"T{i}" for i in range(8)]
    attack = dict(zip(teams, np.linspace(-0.4, 0.4, 8)))
    results = []
    for _ in range(6):
        for h, a in itertools.permutations(teams, 2):
            lam = math.exp(attack[h] - 0.5 * attack[a] + 0.25)
            mu = math.exp(attack[a] - 0.5 * attack[h])
            results.append(Result(h, a, rng.poisson(lam), rng.poisson(mu)))
    model = fit_dixon_coles(results, decay=0.0)
    fitted = [model.attack[t] for t in teams]
    assert np.corrcoef(fitted, list(attack.values()))[0, 1] > 0.9
    assert model.home_advantage == pytest.approx(0.25, abs=0.12)


def test_path_markets_are_bounded_by_grid():
    stats = simulate_paths(1.8, 0.9, n_sims=40_000, seed=7)
    g = FootballMatch(1.8, 0.9).full
    # Leading by 1 at some point is at least as likely as winning.
    assert stats.lead_by_at_any_time(1, "home") >= g.home_win() - 0.02
    # Three home goals in a row needs at least three home goals.
    assert stats.goals_in_a_row(3, "home") <= g.team_over("home", 2.5) + 0.01
    assert stats.home_goals.mean() == pytest.approx(1.8, rel=0.1)


# ------------------------------------------------------------------ basketball / handball

def test_basketball_symmetry_and_lines():
    m = BasketballMatch(115, 115)
    assert m.win("home") == pytest.approx(0.5)
    assert m.total_over(230 - 0.5) > 0.5 > m.total_over(230 + 0.5)
    assert m.total_over(115, "1h") == pytest.approx(0.5)
    assert m.win_by_at_least("home", 6) < m.win("home")


def test_handball_grid():
    g = handball_grid(30, 28)
    assert g.home_win() + g.draw() + g.away_win() == pytest.approx(1.0)
    assert 0.04 < g.draw() < 0.12
    assert g.home_win() > g.away_win()


# ------------------------------------------------------------------ value + ladder

def sel(i, odds, p, sport="football", category="main", match=None):
    return Selection(sport, category, match or f"m{i}", f"Match {i}", "Over 2.5", "Yes", odds, p)


def test_value_filter():
    assert check(sel(1, 1.90, 0.56))[0]           # +6.4% edge
    assert not check(sel(2, 1.90, 0.53))[0]       # +0.7%: not enough
    assert not check(sel(3, 1.05, 0.99))[0]       # below the odds floor
    assert not check(sel(4, 1.90, 0.56, "handball"))[0]  # handball needs 7%


def test_best_slip_matches_brute_force():
    rng = np.random.default_rng(3)
    picks = []
    for i in range(9):
        o = float(rng.uniform(1.3, 2.2))
        picks.append(sel(i, o, (1.06 + rng.uniform(0, 0.06)) / o))
    picks.append(sel(99, 1.6, 0.68, match="m0"))  # second leg on match m0
    target = 10
    got = best_slip(picks, target)
    best_p = 0
    for r in range(1, len(picks) + 1):
        for combo in itertools.combinations(picks, r):
            if len({s.match_id for s in combo}) < r:
                continue
            if math.prod(s.odds for s in combo) >= target:
                best_p = max(best_p, math.prod(s.probability for s in combo))
    assert got is not None
    assert math.prod(s.odds for s in got) >= target
    assert len({s.match_id for s in got}) == len(got)
    assert math.prod(s.probability for s in got) == pytest.approx(best_p, rel=0.01)


def test_ladder_leaves_unreachable_rungs_empty():
    picks = [sel(i, 1.8, 0.6) for i in range(3)]  # max combined odds ~5.8
    slips = build_ladder(picks, rungs=(2, 5, 10))
    assert slips[0].legs and slips[1].legs
    assert not slips[2].legs and "not enough" in slips[2].note


def test_mega_slip_never_pads():
    picks = [sel(i, 1.25, 0.85, category="combo") for i in range(12)]
    picks += [sel(100 + i, 1.25, 0.79, category="combo") for i in range(10)]  # no edge
    slip = build_mega_slip(picks)
    assert len(slip.legs) == 12
    assert "only 12" in slip.note
    assert slip.expected_return > 1


# ------------------------------------------------------------------ daily pipeline

def test_catalogue_complements_and_blend():
    from edge.football_day import blend, market_catalogue, price_match
    m = FootballMatch(1.7, 1.0)
    cat = {name: p for name, _, p in market_catalogue(m, simulate_paths(1.7, 1.0, 5000, seed=1))}
    assert cat["Over 2.5"] + cat["Under 2.5"] == pytest.approx(1.0)
    assert cat["GG (both teams score)"] + cat["NG"] == pytest.approx(1.0)
    assert cat["Home or Over 2.5"] >= max(cat["Home win"], cat["Over 2.5"])
    priced = price_match(m, "A", n_sims=5000)
    assert all(x.min_odds > x.fair_odds for x in priced)
    assert blend((1.0, 1.0), (4.0, 1.0), 0.5) == pytest.approx((2.0, 1.0))
    assert blend(None, (1.2, 0.9), 0.8) == (1.2, 0.9)


def test_reading_bookmaker_lines():
    from edge.sheet import implied_margin, implied_total
    # A fair 50/50 total at 213.5 implies an expected total of 213.5.
    vals = [{"value": "Over 213.5", "odd": "1.95"}, {"value": "Under 213.5", "odd": "1.95"},
            {"value": "Over 214", "odd": "1.90"}, {"value": "Under 214", "odd": "2.00"}]
    assert implied_total(vals, 18) == pytest.approx(213.5)
    # Home -4.5 at even money: home expected to win by 4.5.
    hc = [{"value": "Home -4.5", "odd": "1.91"}, {"value": "Away -4.5", "odd": "1.91"}]
    assert implied_margin(hc, 12) == pytest.approx(4.5)
    # Home favoured to cover -4.5 -> expected margin above 4.5.
    hc2 = [{"value": "Home -4.5", "odd": "1.60"}, {"value": "Away -4.5", "odd": "2.40"}]
    assert implied_margin(hc2, 12) > 4.5


def test_basketball_and_handball_catalogues():
    from edge.basketball_day import catalogue as bb_cat
    from edge.handball_day import catalogue as hb_cat
    bb = {n: p for n, _, p in bb_cat(BasketballMatch(112, 106))}
    assert bb["Home win"] + bb["Away win"] == pytest.approx(1.0)
    assert all(0 < p < 1 for p in bb.values())
    hb = {n: p for n, _, p in hb_cat(30, 27)}
    assert hb["Home win"] + hb["Draw"] + hb["Away win"] == pytest.approx(1.0)
