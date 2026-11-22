"""Points sports (rugby, NFL): totals and winning margins.

Totals and team points use normal distributions. The winning margin uses a
distribution over whole points: a normal shape, reweighted by key-number
weights where a sport's scoring makes some margins much more common. In the
NFL, field goals (3) and converted touchdowns (7) make margins of 3 and 7
far more frequent than a smooth curve predicts. The default weights are a
first approximation, to be calibrated on the 2022-2024 seasons.
"""

from __future__ import annotations

from dataclasses import dataclass, field

import numpy as np
from scipy.stats import norm

# Relative frequency multipliers for exact margins (both signs).
NFL_KEY_NUMBERS = {0: 0.05, 1: 0.8, 2: 0.8, 3: 2.1, 4: 1.15, 6: 1.2, 7: 1.6, 10: 1.25, 14: 1.2}
RUGBY_KEY_NUMBERS = {0: 0.8}

SPORT_DEFAULTS = {
    # total_sd, margin_sd, team_sd, first-half share, key numbers
    "nfl": (10.0, 13.5, 7.5, 0.49, NFL_KEY_NUMBERS),
    "rugby": (13.0, 13.0, 9.0, 0.47, RUGBY_KEY_NUMBERS),
}
PERIOD_SD_SCALE = {"game": 1.0, "1h": 0.72, "q1": 0.52}


@dataclass
class PointsMatch:
    sport: str
    home_points: float
    away_points: float
    shares: dict[str, float] = field(default_factory=dict)

    def __post_init__(self):
        total_sd, margin_sd, team_sd, h1, keys = SPORT_DEFAULTS[self.sport]
        self.total_sd, self.margin_sd, self.team_sd = total_sd, margin_sd, team_sd
        self.shares = {"game": 1.0, "1h": h1, "q1": h1 / 2, **self.shares}
        margins = np.arange(-80, 81)
        mean = self.home_points - self.away_points
        pmf = norm.cdf(margins + 0.5, mean, margin_sd) - norm.cdf(margins - 0.5, mean, margin_sd)
        weights = np.array([keys.get(abs(int(m)), 1.0) for m in margins])
        pmf = pmf * weights
        self.margins, self.margin_pmf = margins, pmf / pmf.sum()

    # Results and margins
    def home_win(self) -> float:
        return float(self.margin_pmf[self.margins > 0].sum())

    def draw(self) -> float:
        return float(self.margin_pmf[self.margins == 0].sum())

    def away_win(self) -> float:
        return float(self.margin_pmf[self.margins < 0].sum())

    def win_two_way(self, side: str) -> float:
        """Winner with draws excluded (as in markets where a tie is void or
        settled by overtime): the win share of decided games."""
        h, a = self.home_win(), self.away_win()
        return h / (h + a) if side == "home" else a / (h + a)

    def handicap(self, side: str, line: float) -> float:
        """Half-point lines, e.g. handicap("home", -6.5) = home wins by 7+."""
        m = self.margins if side == "home" else -self.margins
        return float(self.margin_pmf[m + line > 0].sum())

    def win_by_at_least(self, side: str, points: int) -> float:
        m = self.margins if side == "home" else -self.margins
        return float(self.margin_pmf[m >= points].sum())

    # Totals
    def expected_total(self, period: str = "game") -> float:
        return (self.home_points + self.away_points) * self.shares[period]

    def expected_team(self, side: str, period: str = "game") -> float:
        pts = self.home_points if side == "home" else self.away_points
        return pts * self.shares[period]

    def total_over(self, line: float, period: str = "game") -> float:
        sd = self.total_sd * PERIOD_SD_SCALE[period]
        return float(1 - norm.cdf(line, self.expected_total(period), sd))

    def team_over(self, side: str, line: float, period: str = "game") -> float:
        sd = self.team_sd * PERIOD_SD_SCALE[period]
        return float(1 - norm.cdf(line, self.expected_team(side, period), sd))
