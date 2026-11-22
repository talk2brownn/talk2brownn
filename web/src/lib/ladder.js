// Ladder and 30-game slip, mirroring engine/edge/ladder.py.
//
// For each target the optimiser picks the legs (max one per match) with the
// highest chance of all winning whose combined odds still reach the target.
// It never adds a non-value leg to reach a price: unreachable rungs stay empty.

import { valuePicks } from './value.js';

export const RUNGS = [2, 5, 10, 20, 50, 100, 200, 500, 1000];
const RESOLUTION = 0.002; // log-odds step

export function bestSlip(picks, target) {
  const groups = new Map();
  for (const s of picks) {
    if (!groups.has(s.matchId)) groups.set(s.matchId, []);
    groups.get(s.matchId).push(s);
  }
  const list = [...groups.values()];
  const cap = Math.ceil(Math.log(target) / RESOLUTION);
  let dp = new Float64Array(cap + 1).fill(Infinity);
  dp[0] = 0;
  const choices = [];
  for (const items of list) {
    const next = Float64Array.from(dp);
    const pick = new Int32Array(cap + 1).fill(-1);
    const prev = Int32Array.from({ length: cap + 1 }, (_, i) => i);
    items.forEach((s, k) => {
      const w = Math.floor(Math.log(s.odds) / RESOLUTION); // floor: never overstate odds
      if (w <= 0) return;
      const cost = -Math.log(s.probability);
      for (let c = 0; c <= cap; c++) {
        if (dp[c] === Infinity) continue;
        const nc = Math.min(cap, c + w);
        const v = dp[c] + cost;
        if (v < next[nc] - 1e-12) {
          next[nc] = v;
          pick[nc] = k;
          prev[nc] = c;
        }
      }
    });
    choices.push([pick, prev]);
    dp = next;
  }
  if (dp[cap] === Infinity) return null;
  const legs = [];
  let c = cap;
  for (let g = list.length - 1; g >= 0; g--) {
    const [pick, prev] = choices[g];
    const k = pick[c];
    if (k >= 0) {
      legs.push(list[g][k]);
      c = prev[c];
    }
  }
  return legs.reverse();
}

export function summarize(legs) {
  if (!legs || legs.length === 0) {
    return { legs: [], totalOdds: 0, winProbability: 0, expectedReturn: 0, oneIn: Infinity };
  }
  const totalOdds = legs.reduce((x, s) => x * s.odds, 1);
  const winProbability = legs.reduce((x, s) => x * s.probability, 1);
  return {
    legs,
    totalOdds,
    winProbability,
    expectedReturn: winProbability * totalOdds,
    oneIn: 1 / winProbability,
  };
}

export function buildLadder(config, selections, rungs = RUNGS) {
  const picks = valuePicks(config, selections);
  return rungs.map((target) => {
    const legs = bestSlip(picks, target);
    if (!legs) {
      return { target, ...summarize(null), note: 'Not enough value picks to reach this rung honestly.' };
    }
    return { target, ...summarize(legs), note: '' };
  });
}

export function buildMegaSlip(config, selections) {
  const size = config.mega.size;
  const best = new Map();
  for (const s of valuePicks(config, selections, true)) {
    const cur = best.get(s.matchId);
    if (!cur || s.probability > cur.probability) best.set(s.matchId, s);
  }
  const legs = [...best.values()].sort((a, b) => b.probability - a.probability).slice(0, size);
  const note =
    legs.length === size
      ? ''
      : `Only ${legs.length} value legs priced ${config.mega.min.toFixed(2)}–${config.mega.max.toFixed(2)} so far (target ${size}). Never padded.`;
  return { target: null, ...summarize(legs), note };
}
