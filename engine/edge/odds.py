"""Odds maths: implied probabilities, bookmaker margin, and margin removal.

A decimal price of 2.00 implies a 50% chance. A bookmaker's prices for every
outcome of a market add up to more than 100%; the excess is its margin
(the "overround"). Removing it gives the market's own fair probabilities.
"""

from __future__ import annotations

import math
from typing import Sequence

from scipy.optimize import brentq


def implied_probabilities(odds: Sequence[float]) -> list[float]:
    """Raw 1/odds for each outcome (still includes the bookmaker's margin)."""
    _check(odds)
    return [1.0 / o for o in odds]


def margin(odds: Sequence[float]) -> float:
    """Bookmaker margin of a complete market, e.g. 0.05 for 5%."""
    return sum(implied_probabilities(odds)) - 1.0


def fair_probabilities(odds: Sequence[float], method: str = "power") -> list[float]:
    """Remove the margin from a complete market's prices.

    Methods:
      - "multiplicative": scale every 1/odds down equally. Simple, but
        overstates longshots.
      - "power": raise every 1/odds to the same power k so they sum to 1.
        Takes more margin off longshots, matching the favourite-longshot bias.
      - "shin": Shin's model, which assumes some bettors hold inside
        information. Also loads margin onto longshots.
    """
    q = implied_probabilities(odds)
    total = sum(q)
    if method == "multiplicative" or abs(total - 1.0) < 1e-12:
        return [x / total for x in q]
    if method == "power":
        k = brentq(lambda k: sum(x**k for x in q) - 1.0, 0.01, 100.0)
        return [x**k for x in q]
    if method == "shin":
        return _shin(q, total)
    raise ValueError(f"unknown method: {method}")


def fair_odds(probability: float) -> float:
    """The price at which a bet with this win probability breaks even."""
    if not 0.0 < probability <= 1.0:
        raise ValueError("probability must be in (0, 1]")
    return 1.0 / probability


def expected_value(probability: float, odds: float) -> float:
    """Expected profit per unit staked: probability x odds - 1."""
    return probability * odds - 1.0


def _shin(q: list[float], total: float) -> list[float]:
    def probs(z: float) -> list[float]:
        return [
            (math.sqrt(z * z + 4.0 * (1.0 - z) * x * x / total) - z) / (2.0 * (1.0 - z))
            for x in q
        ]

    z = brentq(lambda z: sum(probs(z)) - 1.0, 0.0, 0.99)
    return probs(z)


def _check(odds: Sequence[float]) -> None:
    if not odds:
        raise ValueError("odds must not be empty")
    for o in odds:
        if o <= 1.0:
            raise ValueError(f"decimal odds must be above 1.0, got {o}")
