import { describe, expect, it } from 'vitest';
import { bestSlip, buildLadder, buildMegaSlip } from './ladder.js';
import { check } from './value.js';

const config = {
  rules: {
    'football/main': { min: 1.25, max: 2.2, edge: 0.04 },
    'football/combo': { min: 1.2, max: 2.2, edge: 0.05 },
    'handball/main': { min: 1.6, max: 2.2, edge: 0.07 },
  },
  tier_buffer: { A: 0, B: 0.01, C: 0.02 },
  absolute_min_odds: 1.1,
  mega: { min: 1.12, max: 1.35, size: 30 },
};

const sel = (i, odds, probability, extra = {}) => ({
  sport: 'football', category: 'main', matchId: `m${i}`, match: `Match ${i}`,
  market: 'Over 2.5', odds, probability, tier: 'A', ...extra,
});

describe('value check', () => {
  it('matches the engine rules', () => {
    expect(check(config, sel(1, 1.9, 0.56)).ok).toBe(true);
    expect(check(config, sel(2, 1.9, 0.53)).ok).toBe(false);
    expect(check(config, sel(3, 1.05, 0.99)).ok).toBe(false);
    expect(check(config, sel(4, 1.9, 0.56, { sport: 'handball' })).ok).toBe(false);
  });
});

describe('ladder', () => {
  it('finds the best slip (checked by brute force)', () => {
    const picks = [];
    let seed = 7;
    const rand = () => ((seed = (seed * 16807) % 2147483647) / 2147483647);
    for (let i = 0; i < 9; i++) {
      const o = 1.3 + rand() * 0.9;
      picks.push(sel(i, o, (1.06 + rand() * 0.06) / o));
    }
    picks.push(sel(99, 1.6, 0.68, { matchId: 'm0' }));
    const target = 10;
    const got = bestSlip(picks, target);
    let best = 0;
    for (let mask = 1; mask < 1 << picks.length; mask++) {
      const legs = picks.filter((_, i) => mask & (1 << i));
      if (new Set(legs.map((s) => s.matchId)).size < legs.length) continue;
      const odds = legs.reduce((x, s) => x * s.odds, 1);
      if (odds >= target) best = Math.max(best, legs.reduce((x, s) => x * s.probability, 1));
    }
    const p = got.reduce((x, s) => x * s.probability, 1);
    expect(got.reduce((x, s) => x * s.odds, 1)).toBeGreaterThanOrEqual(target);
    expect(new Set(got.map((s) => s.matchId)).size).toBe(got.length);
    expect(p).toBeCloseTo(best, 2);
  });

  it('leaves unreachable rungs empty', () => {
    const picks = [0, 1, 2].map((i) => sel(i, 1.8, 0.6));
    const [r2, r5, r10] = buildLadder(config, picks, [2, 5, 10]);
    expect(r2.legs.length).toBeGreaterThan(0);
    expect(r5.legs.length).toBeGreaterThan(0);
    expect(r10.legs.length).toBe(0);
  });

  it('never pads the 30-game slip', () => {
    const good = Array.from({ length: 12 }, (_, i) => sel(i, 1.25, 0.85, { category: 'combo' }));
    const bad = Array.from({ length: 10 }, (_, i) => sel(100 + i, 1.25, 0.79, { category: 'combo' }));
    const mega = buildMegaSlip(config, [...good, ...bad]);
    expect(mega.legs.length).toBe(12);
    expect(mega.note).toContain('Only 12');
    expect(mega.expectedReturn).toBeGreaterThan(1);
  });
});
