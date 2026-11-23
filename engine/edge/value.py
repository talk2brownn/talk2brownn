"""The value filter: which selections are worth betting at SportyBet's price.

A selection is a value pick when our probability x SportyBet's odds beats 1
by a safety buffer. The buffer is larger where SportyBet's margin is larger,
where our data is thinner (lower league tiers), and for markets the evidence
says are hard to model.
"""

from __future__ import annotations

from dataclasses import dataclass

# (min odds, max odds, minimum edge) per sport and market category.
RULES: dict[tuple[str, str], tuple[float, float, float]] = {
    ("football", "main"): (1.25, 2.20, 0.04),    # O/U, team totals, BTTS, 1X2, DC
    ("football", "combo"): (1.20, 2.20, 0.05),   # "A or B", 1X2/DC & O/U, win to nil
    ("football", "props"): (1.60, 2.20, 0.06),   # corners, cards, fouls, shots
    ("basketball", "main"): (1.35, 2.10, 0.04),  # team totals, halves, quarters, margin
    ("handball", "main"): (1.60, 2.20, 0.07),
    # Added sports: NFL, MLB and NHL prices are among the sharpest anywhere,
    # and SportyBet's margins here are not yet measured, so buffers are wide.
    ("hockey", "main"): (1.35, 2.20, 0.05),
    ("nfl", "main"): (1.40, 2.10, 0.05),
    ("rugby", "main"): (1.40, 2.20, 0.06),
    ("baseball", "main"): (1.40, 2.20, 0.05),
}

# Extra edge required where data is thinner.
TIER_BUFFER = {"A": 0.0, "B": 0.01, "C": 0.02}

ABSOLUTE_MIN_ODDS = 1.10
MEGA_MIN_ODDS, MEGA_MAX_ODDS = 1.12, 1.35


@dataclass(frozen=True)
class Selection:
    sport: str          # "football" | "basketball" | "handball"
    category: str       # "main" | "combo" | "props"
    match_id: str
    match: str          # "Man City vs Fulham"
    market: str         # "Home or Over 2.5"
    pick: str           # "Yes"
    odds: float         # SportyBet decimal price
    probability: float  # our model's probability
    tier: str = "A"     # league tier: "A" full menu, "B", "C"
    kickoff: str = ""

    @property
    def edge(self) -> float:
        """Expected profit per unit staked at SportyBet's price."""
        return self.probability * self.odds - 1.0

    @property
    def required_edge(self) -> float:
        return _rule(self)[2] + TIER_BUFFER.get(self.tier, 0.03)


def check(sel: Selection, for_mega: bool = False) -> tuple[bool, str]:
    """Return (is_value, reason)."""
    lo, hi, _ = _rule(sel)
    if for_mega:
        lo, hi = MEGA_MIN_ODDS, MEGA_MAX_ODDS
    if sel.odds < max(lo, ABSOLUTE_MIN_ODDS):
        return False, f"odds {sel.odds:.2f} below {lo:.2f}"
    if sel.odds > hi:
        return False, f"odds {sel.odds:.2f} above {hi:.2f}"
    if not 0.0 < sel.probability < 1.0:
        return False, "probability out of range"
    if sel.edge < sel.required_edge:
        return False, f"edge {sel.edge:+.1%} below required {sel.required_edge:.1%}"
    return True, f"edge {sel.edge:+.1%}"


def value_picks(selections: list[Selection], for_mega: bool = False) -> list[Selection]:
    """Value picks, best edge first."""
    picks = [s for s in selections if check(s, for_mega)[0]]
    return sorted(picks, key=lambda s: s.edge, reverse=True)


def _rule(sel: Selection) -> tuple[float, float, float]:
    try:
        return RULES[(sel.sport, sel.category)]
    except KeyError:
        raise ValueError(f"no rule for {sel.sport}/{sel.category}") from None
