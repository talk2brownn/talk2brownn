"""Handball: each team's goals as a discretised normal distribution.

One study found a team's handball goals fit a binomial better than a Poisson;
with ~25-30 goals a team, a binomial is close to a normal with a standard
deviation around 4. Home advantage (about 2 goals in the studies found) is
expected to be inside the projected goals passed in. The output is the same
ScoreGrid football uses, so every market (1X2, double chance, handicap,
totals, team totals) comes from one consistent grid.
"""

from __future__ import annotations

import numpy as np
from scipy.stats import norm

from .grid import ScoreGrid

TEAM_GOALS_SD = 4.0


def handball_grid(home_goals: float, away_goals: float, sd: float = TEAM_GOALS_SD,
                  first_half_share: float = 1.0) -> ScoreGrid:
    """Final-score (or half, via first_half_share) grid for a handball match."""
    h_mean, a_mean = home_goals * first_half_share, away_goals * first_half_share
    h_sd, a_sd = sd * np.sqrt(first_half_share), sd * np.sqrt(first_half_share)
    lo = int(max(0, min(h_mean, a_mean) - 6 * max(h_sd, a_sd)))
    hi = int(max(h_mean, a_mean) + 6 * max(h_sd, a_sd)) + 1
    goals = np.arange(lo, hi + 1)
    ph = norm.cdf(goals + 0.5, h_mean, h_sd) - norm.cdf(goals - 0.5, h_mean, h_sd)
    pa = norm.cdf(goals + 0.5, a_mean, a_sd) - norm.cdf(goals - 0.5, a_mean, a_sd)
    return ScoreGrid(np.outer(ph, pa), min_home=lo, min_away=lo)
