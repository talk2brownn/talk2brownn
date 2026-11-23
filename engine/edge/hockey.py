"""Ice hockey and baseball: score grids for low-scoring sports.

Hockey: regulation goals per team are close to Poisson, so the football
grid applies directly (no low-score correction). Ties after 60 minutes go to
overtime and shootouts; the "incl. OT" winner splits the tie in proportion to
each team's regulation strength. Late empty-net goals make 2+ goal margins a
little more common than Poisson predicts; this first version does not model
that, so favourite puck lines (-1.5) are priced slightly short.

Baseball: runs are over-dispersed (big innings), so each team's runs use a
negative binomial. Ties after 9 innings go to extra innings and are split by
strength. First 5 innings carry about 55% of runs.
"""

from __future__ import annotations

import numpy as np
from scipy.optimize import minimize
from scipy.stats import nbinom

from .football import dixon_coles_grid
from .grid import ScoreGrid

PERIOD_SHARE = 1 / 3          # each hockey period
BASEBALL_DISPERSION = 6.0     # negative binomial size; lower = more big innings
F5_SHARE = 0.55


def hockey_grid(home_goals: float, away_goals: float, share: float = 1.0) -> ScoreGrid:
    return dixon_coles_grid(home_goals * share, away_goals * share, rho=0.0, max_goals=12)


def baseball_grid(home_runs: float, away_runs: float, share: float = 1.0,
                  size: float = BASEBALL_DISPERSION) -> ScoreGrid:
    runs = np.arange(0, 31)

    def pmf(mean):
        mean *= share
        return nbinom.pmf(runs, size, size / (size + mean))

    return ScoreGrid(np.outer(pmf(home_runs), pmf(away_runs)))


def win_incl_extra(g: ScoreGrid, side: str) -> float:
    """Winner including overtime / extra innings: ties split by strength."""
    h, d, a = g.home_win(), g.draw(), g.away_win()
    share = h / (h + a) if h + a > 0 else 0.5
    return h + d * share if side == "home" else a + d * (1 - share)


def implied_rates(p_home: float, p_away: float, p_over: float | None, line: float | None,
                  grid_fn, default_total: float, two_way: bool = False) -> tuple[float, float]:
    """Home and away scoring rates matching margin-free market probabilities.

    p_home / p_away are regulation (3-way) win probabilities for hockey or
    with two_way=True, winner probabilities including extra time/innings
    (baseball moneylines). p_over is for `line`.
    """
    def loss(x):
        g = grid_fn(float(np.exp(x[0])), float(np.exp(x[1])))
        if two_way:
            err = (win_incl_extra(g, "home") - p_home) ** 2
        else:
            err = (g.home_win() - p_home) ** 2 + (g.away_win() - p_away) ** 2
        if p_over is not None and line is not None:
            err += (g.total_over(line) - p_over) ** 2
        else:
            err += 0.01 * (np.exp(x[0]) + np.exp(x[1]) - default_total) ** 2
        return err

    half = np.log(default_total / 2)
    res = minimize(loss, x0=[half, half], method="Nelder-Mead",
                   options={"xatol": 1e-5, "fatol": 1e-12, "maxiter": 2000})
    return float(np.exp(res.x[0])), float(np.exp(res.x[1]))
