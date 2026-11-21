"""The daily ladder: accumulators built only from value picks.

For each target (2, 5, 10 ... 1,000) the builder picks the set of legs with
the highest chance of all winning while the combined odds still reach the
target. It never adds a leg just to reach a price: if today's value picks
cannot honestly reach a rung, the rung is left empty.

Win chance of a slip = product of leg probabilities. Expected return per unit
staked = product of (probability x odds) for each leg. Margin is charged on
every leg, which is why fewer, stronger legs beat many weak ones.

At most one leg per match: legs from the same match are correlated, and a
same-match combo should be priced as one selection from the scoreline grid.
"""

from __future__ import annotations

import math
from collections import defaultdict
from dataclasses import dataclass, field
from typing import Callable

import numpy as np

from .value import Selection, value_picks

RUNGS = (2, 5, 10, 20, 50, 100, 200, 500, 1000)
MEGA_SIZE = 30
_RESOLUTION = 0.002  # log-odds step used by the optimiser


@dataclass
class Slip:
    target: float | None
    legs: list[Selection] = field(default_factory=list)
    note: str = ""
    bonus: float = 0.0  # SportyBet multi bonus as a fraction of winnings

    @property
    def total_odds(self) -> float:
        return math.prod(s.odds for s in self.legs) if self.legs else 0.0

    @property
    def win_probability(self) -> float:
        return math.prod(s.probability for s in self.legs) if self.legs else 0.0

    @property
    def expected_return(self) -> float:
        """Average amount back per 1 staked (1.00 = break even)."""
        if not self.legs:
            return 0.0
        return self.win_probability * (1 + (self.total_odds - 1) * (1 + self.bonus))

    @property
    def one_in(self) -> float:
        p = self.win_probability
        return 1 / p if p > 0 else math.inf


def best_slip(picks: list[Selection], target: float) -> list[Selection] | None:
    """Highest-probability set of legs (max one per match) reaching target odds.

    A group knapsack solved by dynamic programming: each leg "costs"
    -log(probability) and "fills" log(odds); we fill at least log(target)
    at the lowest cost.
    """
    groups: dict[str, list[Selection]] = defaultdict(list)
    for s in picks:
        groups[s.match_id].append(s)
    group_list = list(groups.values())
    cap = math.ceil(math.log(target) / _RESOLUTION)
    inf = math.inf
    dp = np.full(cap + 1, inf)
    dp[0] = 0.0
    choices = []  # per group: (item index or -1, previous capacity) for each capacity
    for items in group_list:
        new = dp.copy()
        pick = np.full(cap + 1, -1, dtype=int)
        prev = np.arange(cap + 1)
        for k, s in enumerate(items):
            w = int(math.log(s.odds) / _RESOLUTION)  # floor: never overstate odds
            cost = -math.log(s.probability)
            if w <= 0:
                continue
            # Candidate cost of reaching each capacity by adding this leg.
            cand = np.full(cap + 1, inf)
            src = np.arange(cap + 1)
            if w < cap:
                cand[w:cap] = dp[: cap - w] + cost
                src[w:cap] = np.arange(cap - w)
            # Everything at or past the target lands on the target.
            tail = dp[max(cap - w, 0):]
            j = int(np.argmin(tail))
            cand[cap] = tail[j] + cost
            src[cap] = max(cap - w, 0) + j
            better = cand < new - 1e-12
            new[better] = cand[better]
            pick[better] = k
            prev[better] = src[better]
        choices.append((pick, prev))
        dp = new
    if not np.isfinite(dp[cap]):
        return None
    legs, c = [], cap
    for items, (pick, prev) in zip(reversed(group_list), reversed(choices)):
        k = pick[c]
        if k >= 0:
            legs.append(items[k])
            c = prev[c]
    return list(reversed(legs))


def build_ladder(selections: list[Selection], rungs=RUNGS,
                 bonus: Callable[[int], float] | None = None) -> list[Slip]:
    """One slip per rung, from value picks only. Rungs may share legs."""
    picks = value_picks(selections)
    slips = []
    for target in rungs:
        legs = best_slip(picks, target)
        if legs is None:
            slips.append(Slip(target, note="not enough value picks today to reach this rung honestly"))
            continue
        slips.append(Slip(target, legs, bonus=bonus(len(legs)) if bonus else 0.0))
    return slips


def build_mega_slip(selections: list[Selection], size: int = MEGA_SIZE,
                    bonus: Callable[[int], float] | None = None) -> Slip:
    """The daily big slip: up to `size` short-priced value legs, one per match.

    Takes the highest-probability value legs priced 1.12-1.35. Never pads with
    non-value legs; if fewer qualify, the slip is shorter and says so.
    """
    best_per_match: dict[str, Selection] = {}
    for s in value_picks(selections, for_mega=True):
        cur = best_per_match.get(s.match_id)
        if cur is None or s.probability > cur.probability:
            best_per_match[s.match_id] = s
    legs = sorted(best_per_match.values(), key=lambda s: s.probability, reverse=True)[:size]
    note = "" if len(legs) == size else f"only {len(legs)} value legs qualified today (target {size}); not padded"
    return Slip(None, legs, note=note, bonus=bonus(len(legs)) if bonus and legs else 0.0)
