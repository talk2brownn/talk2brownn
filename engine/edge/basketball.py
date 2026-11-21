"""Basketball: totals, team totals, halves, quarters and winning margin.

Each team's projected points (from pace x efficiency ratings, adjusted for
rest and injuries upstream) feed normal distributions. The evidence:
  - final margins around the expectation have a standard deviation near 12;
  - the 1st half is about 50% of the full-game total, each quarter about 25%;
  - one 2,427-game test measured 1st-half totals at SD 11.9 and 1st-quarter
    totals at SD 8.1.
The default SDs below are starting points, to be re-estimated from data.
"""

from __future__ import annotations

from dataclasses import dataclass, field

from scipy.stats import norm

PERIOD_SHARE = {"game": 1.0, "1h": 0.50, "2h": 0.50, "q1": 0.25, "q2": 0.25, "q3": 0.25, "q4": 0.25}

# Standard deviations of the match total by period, and of one team's points.
TOTAL_SD = {"game": 18.0, "1h": 11.9, "2h": 12.5, "q1": 8.1, "q2": 8.1, "q3": 8.1, "q4": 8.8}
TEAM_SD = {"game": 11.5, "1h": 8.0, "2h": 8.5, "q1": 5.6, "q2": 5.6, "q3": 5.6, "q4": 6.1}
MARGIN_SD = 12.0


@dataclass
class BasketballMatch:
    home_points: float
    away_points: float
    total_sd: dict[str, float] = field(default_factory=lambda: dict(TOTAL_SD))
    team_sd: dict[str, float] = field(default_factory=lambda: dict(TEAM_SD))
    margin_sd: float = MARGIN_SD

    def expected_total(self, period: str = "game") -> float:
        return (self.home_points + self.away_points) * PERIOD_SHARE[period]

    def expected_team(self, side: str, period: str = "game") -> float:
        pts = self.home_points if side == "home" else self.away_points
        return pts * PERIOD_SHARE[period]

    def total_over(self, line: float, period: str = "game") -> float:
        return _over(line, self.expected_total(period), self.total_sd[period])

    def team_over(self, side: str, line: float, period: str = "game") -> float:
        return _over(line, self.expected_team(side, period), self.team_sd[period])

    def win(self, side: str) -> float:
        """Win probability including overtime (no draws)."""
        m = self.home_points - self.away_points
        p_home = 1 - norm.cdf(0, m, self.margin_sd)
        return p_home if side == "home" else 1 - p_home

    def win_by_at_least(self, side: str, points: int) -> float:
        """E.g. win_by_at_least("home", 6) for "76ers by 6+"."""
        m = self.home_points - self.away_points
        if side == "away":
            m = -m
        return float(1 - norm.cdf(points - 0.5, m, self.margin_sd))

    def handicap(self, side: str, line: float) -> float:
        m = self.home_points - self.away_points
        if side == "away":
            m = -m
        return float(1 - norm.cdf(-line, m, self.margin_sd))


def _over(line: float, mean: float, sd: float) -> float:
    # Lines are half-points (e.g. 229.5), so there is no push.
    return float(1 - norm.cdf(line, mean, sd))
