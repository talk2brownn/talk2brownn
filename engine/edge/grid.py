"""A final-score probability grid, shared by football and handball.

grid[i, j] is the probability that the home team scores (min_home + i) and
the away team scores (min_away + j). Every full-time market is a sum over
part of the grid, so all markets priced from one grid agree with each other,
including "A or B" markets and same-match combos (whose legs are correlated).
"""

from __future__ import annotations

from typing import Callable

import numpy as np

Event = Callable[[np.ndarray, np.ndarray], np.ndarray]


class ScoreGrid:
    def __init__(self, matrix: np.ndarray, min_home: int = 0, min_away: int = 0):
        matrix = np.asarray(matrix, dtype=float)
        if matrix.ndim != 2:
            raise ValueError("matrix must be 2-D")
        total = matrix.sum()
        if total <= 0:
            raise ValueError("matrix has no probability mass")
        self.matrix = matrix / total
        home = np.arange(matrix.shape[0]) + min_home
        away = np.arange(matrix.shape[1]) + min_away
        self.home_goals, self.away_goals = np.meshgrid(home, away, indexing="ij")

    def prob(self, event: Event) -> float:
        """Probability of any event written in terms of (home, away) goals.

        Example, "Home or Over 2.5": grid.prob(lambda h, a: (h > a) | (h + a > 2.5))
        """
        mask = np.asarray(event(self.home_goals, self.away_goals), dtype=bool)
        return float(self.matrix[mask].sum())

    # Result markets
    def home_win(self) -> float:
        return self.prob(lambda h, a: h > a)

    def draw(self) -> float:
        return self.prob(lambda h, a: h == a)

    def away_win(self) -> float:
        return self.prob(lambda h, a: h < a)

    def double_chance(self, pick: str) -> float:
        """pick: "1X" (home or draw), "12" (home or away), "X2" (draw or away)."""
        events = {
            "1X": lambda h, a: h >= a,
            "12": lambda h, a: h != a,
            "X2": lambda h, a: h <= a,
        }
        return self.prob(events[pick])

    # Totals
    def total_over(self, line: float) -> float:
        return self.prob(lambda h, a: h + a > line)

    def team_over(self, side: str, line: float) -> float:
        return self.prob(lambda h, a: _side(side, h, a) > line)

    def btts(self) -> float:
        return self.prob(lambda h, a: (h > 0) & (a > 0))

    def win_to_nil(self, side: str) -> float:
        if side == "home":
            return self.prob(lambda h, a: (h > a) & (a == 0))
        return self.prob(lambda h, a: (a > h) & (h == 0))

    def handicap(self, side: str, line: float) -> float:
        """Half-point handicap, e.g. handicap("home", -1.5) = home wins by 2+."""
        if line != int(line) + 0.5 and line != int(line) - 0.5:
            raise ValueError("only half-point lines are supported")
        if side == "home":
            return self.prob(lambda h, a: h + line > a)
        return self.prob(lambda h, a: a + line > h)

    def total_distribution(self) -> dict[int, float]:
        totals = self.home_goals + self.away_goals
        return {int(t): float(self.matrix[totals == t].sum()) for t in np.unique(totals)}


def _side(side: str, h: np.ndarray, a: np.ndarray) -> np.ndarray:
    if side == "home":
        return h
    if side == "away":
        return a
    raise ValueError("side must be 'home' or 'away'")
