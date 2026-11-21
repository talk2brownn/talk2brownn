"""Football: Dixon-Coles scoreline model, half splits and path simulation.

Three layers:
  1. fit_dixon_coles: learn each team's attack/defence strength from past
     results, weighting recent matches more (time decay).
  2. FootballMatch: turn two expected-goals numbers into a final-score grid
     (for full-time markets) and per-half grids (for half markets).
  3. simulate_paths: play the match out minute by minute many times, for
     markets that depend on the order of goals ("lead by 2 at any time",
     "3 goals in a row"). Scoring rates shift with the score: the leading
     team eases off and the trailing team pushes (Dixon & Robinson 1998).
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, Sequence

import numpy as np
from scipy.optimize import minimize
from scipy.special import gammaln
from scipy.stats import poisson

from .grid import ScoreGrid

# Share of goals scored in the first half. Several samples put the second
# half at 55-56% of goals, so 0.45 is the default.
FIRST_HALF_SHARE = 0.45
MAX_GOALS = 10


# ---------------------------------------------------------------- grids

def dixon_coles_grid(home_xg: float, away_xg: float, rho: float = 0.0,
                     max_goals: int = MAX_GOALS) -> ScoreGrid:
    """Final-score grid from two Poisson means plus the Dixon-Coles low-score
    correction rho (negative rho makes 0-0 and 1-1 more likely)."""
    goals = np.arange(max_goals + 1)
    m = np.outer(poisson.pmf(goals, home_xg), poisson.pmf(goals, away_xg))
    m[0, 0] *= max(1.0 - home_xg * away_xg * rho, 1e-10)
    m[0, 1] *= max(1.0 + home_xg * rho, 1e-10)
    m[1, 0] *= max(1.0 + away_xg * rho, 1e-10)
    m[1, 1] *= max(1.0 - rho, 1e-10)
    return ScoreGrid(m)


class FootballMatch:
    """All grid-based prices for one match."""

    def __init__(self, home_xg: float, away_xg: float, rho: float = -0.05,
                 first_half_share: float = FIRST_HALF_SHARE):
        if home_xg <= 0 or away_xg <= 0:
            raise ValueError("expected goals must be positive")
        self.home_xg, self.away_xg, self.rho = home_xg, away_xg, rho
        self.first_half_share = first_half_share
        self.full = dixon_coles_grid(home_xg, away_xg, rho)
        s = first_half_share
        self.first_half = dixon_coles_grid(home_xg * s, away_xg * s, 0.0)
        self.second_half = dixon_coles_grid(home_xg * (1 - s), away_xg * (1 - s), 0.0)

    def both_halves_over(self, line: float) -> float:
        return self.first_half.total_over(line) * self.second_half.total_over(line)

    def both_halves_under(self, line: float) -> float:
        return (1 - self.first_half.total_over(line)) * (1 - self.second_half.total_over(line))

    def highest_scoring_half(self) -> dict[str, float]:
        """Probabilities that the 1st half, 2nd half, or neither scores more."""
        d1 = self.first_half.total_distribution()
        d2 = self.second_half.total_distribution()
        out = {"first": 0.0, "second": 0.0, "equal": 0.0}
        for g1, p1 in d1.items():
            for g2, p2 in d2.items():
                key = "first" if g1 > g2 else "second" if g2 > g1 else "equal"
                out[key] += p1 * p2
        return out


def xg_from_market(p_home: float, p_away: float, p_over25: float,
                   rho: float = -0.05) -> tuple[float, float]:
    """Expected goals implied by margin-free 1X2 and Over 2.5 probabilities.

    Lets the engine read a match's strength straight off the market's main
    lines, then price every side market consistently from that grid.
    """
    def loss(x):
        g = dixon_coles_grid(float(np.exp(x[0])), float(np.exp(x[1])), rho)
        return ((g.home_win() - p_home) ** 2 + (g.away_win() - p_away) ** 2
                + (g.total_over(2.5) - p_over25) ** 2)

    res = minimize(loss, x0=[np.log(1.4), np.log(1.1)], method="Nelder-Mead",
                   options={"xatol": 1e-6, "fatol": 1e-12, "maxiter": 2000})
    return float(np.exp(res.x[0])), float(np.exp(res.x[1]))


# ---------------------------------------------------------------- fitting

@dataclass(frozen=True)
class Result:
    home: str
    away: str
    home_goals: int
    away_goals: int
    days_ago: float = 0.0


@dataclass
class DixonColesModel:
    teams: list[str]
    attack: dict[str, float]
    defence: dict[str, float]
    home_advantage: float
    rho: float

    def expected_goals(self, home: str, away: str) -> tuple[float, float]:
        lam = np.exp(self.attack[home] + self.defence[away] + self.home_advantage)
        mu = np.exp(self.attack[away] + self.defence[home])
        return float(lam), float(mu)

    def match(self, home: str, away: str) -> FootballMatch:
        lam, mu = self.expected_goals(home, away)
        return FootballMatch(lam, mu, self.rho)


def fit_dixon_coles(results: Iterable[Result], decay: float = 0.0019) -> DixonColesModel:
    """Fit by weighted maximum likelihood.

    decay is the time-decay rate per day: weight = exp(-decay * days_ago).
    0.0019 gives a half-life of about a year; tune it per league.
    """
    results = list(results)
    if not results:
        raise ValueError("no results to fit")
    teams = sorted({r.home for r in results} | {r.away for r in results})
    idx = {t: i for i, t in enumerate(teams)}
    n = len(teams)
    hi = np.array([idx[r.home] for r in results])
    ai = np.array([idx[r.away] for r in results])
    hg = np.array([r.home_goals for r in results], dtype=float)
    ag = np.array([r.away_goals for r in results], dtype=float)
    w = np.exp(-decay * np.array([r.days_ago for r in results], dtype=float))

    def unpack(x):
        # Attack ratings sum to zero: the last team's attack is implied.
        att = np.append(x[: n - 1], -x[: n - 1].sum())
        dfc = x[n - 1: 2 * n - 1]
        return att, dfc, x[-2], x[-1]

    def neg_log_lik(x):
        att, dfc, home, rho = unpack(x)
        lam = np.exp(att[hi] + dfc[ai] + home)
        mu = np.exp(att[ai] + dfc[hi])
        ll = (hg * np.log(lam) - lam - gammaln(hg + 1)
              + ag * np.log(mu) - mu - gammaln(ag + 1))
        tau = np.ones_like(lam)
        m00 = (hg == 0) & (ag == 0)
        m01 = (hg == 0) & (ag == 1)
        m10 = (hg == 1) & (ag == 0)
        m11 = (hg == 1) & (ag == 1)
        tau[m00] = 1 - lam[m00] * mu[m00] * rho
        tau[m01] = 1 + lam[m01] * rho
        tau[m10] = 1 + mu[m10] * rho
        tau[m11] = 1 - rho
        ll += np.log(np.clip(tau, 1e-10, None))
        return -(w * ll).sum()

    x0 = np.concatenate([np.zeros(n - 1), np.zeros(n), [0.25, -0.05]])
    bounds = [(None, None)] * (2 * n - 1) + [(None, None), (-0.3, 0.3)]
    res = minimize(neg_log_lik, x0, method="L-BFGS-B", bounds=bounds)
    att, dfc, home, rho = unpack(res.x)
    return DixonColesModel(
        teams=teams,
        attack={t: float(att[i]) for t, i in idx.items()},
        defence={t: float(dfc[i]) for t, i in idx.items()},
        home_advantage=float(home),
        rho=float(rho),
    )


# ---------------------------------------------------------------- paths

@dataclass
class PathStats:
    """Per-simulation summaries of how a match unfolded."""

    max_home_lead: np.ndarray
    max_away_lead: np.ndarray
    home_run: np.ndarray  # longest run of consecutive home goals
    away_run: np.ndarray
    home_goals: np.ndarray
    away_goals: np.ndarray

    def lead_by_at_any_time(self, k: int, side: str = "any") -> float:
        if side == "home":
            hit = self.max_home_lead >= k
        elif side == "away":
            hit = self.max_away_lead >= k
        else:
            hit = (self.max_home_lead >= k) | (self.max_away_lead >= k)
        return float(hit.mean())

    def goals_in_a_row(self, n: int, side: str) -> float:
        run = self.home_run if side == "home" else self.away_run
        return float((run >= n).mean())


def simulate_paths(home_xg: float, away_xg: float, n_sims: int = 50_000,
                   first_half_share: float = FIRST_HALF_SHARE,
                   game_state_effect: float = 0.10, seed: int | None = None) -> PathStats:
    """Minute-by-minute Monte Carlo of goal order.

    game_state_effect: a leading team's scoring rate is multiplied by
    (1 - effect) and the trailing team's by (1 + effect).
    """
    rng = np.random.default_rng(seed)
    minute_weight = np.concatenate([
        np.full(45, first_half_share / 45),
        np.full(45, (1 - first_half_share) / 45),
    ])
    h = np.zeros(n_sims, dtype=int)
    a = np.zeros(n_sims, dtype=int)
    max_h_lead = np.zeros(n_sims, dtype=int)
    max_a_lead = np.zeros(n_sims, dtype=int)
    h_run = np.zeros(n_sims, dtype=int)
    a_run = np.zeros(n_sims, dtype=int)
    best_h_run = np.zeros(n_sims, dtype=int)
    best_a_run = np.zeros(n_sims, dtype=int)
    e = game_state_effect
    for w in minute_weight:
        diff = h - a
        h_mult = np.where(diff > 0, 1 - e, np.where(diff < 0, 1 + e, 1.0))
        a_mult = np.where(diff < 0, 1 - e, np.where(diff > 0, 1 + e, 1.0))
        ph = home_xg * w * h_mult
        pa = away_xg * w * a_mult
        u = rng.random(n_sims)
        home_scores = u < ph
        away_scores = (~home_scores) & (u < ph + pa)
        h += home_scores
        a += away_scores
        h_run = np.where(home_scores, h_run + 1, np.where(away_scores, 0, h_run))
        a_run = np.where(away_scores, a_run + 1, np.where(home_scores, 0, a_run))
        best_h_run = np.maximum(best_h_run, h_run)
        best_a_run = np.maximum(best_a_run, a_run)
        max_h_lead = np.maximum(max_h_lead, h - a)
        max_a_lead = np.maximum(max_a_lead, a - h)
    return PathStats(max_h_lead, max_a_lead, best_h_run, best_a_run, h, a)


def results_from_rows(rows: Sequence[dict], date_key: str = "days_ago") -> list[Result]:
    """Convenience: build Result objects from dict rows (e.g. a CSV reader)."""
    return [
        Result(r["home"], r["away"], int(r["home_goals"]), int(r["away_goals"]),
               float(r.get(date_key, 0.0)))
        for r in rows
    ]
