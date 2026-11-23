// Value check, mirroring engine/edge/value.py. The rules arrive in the day's
// index.json, so the site and the engine always use the same numbers.

export function ruleFor(config, sport, category) {
  return config.rules[`${sport}/${category}`];
}

export function requiredEdge(config, sel) {
  const rule = ruleFor(config, sel.sport, sel.category);
  return rule.edge + (config.tier_buffer[sel.tier] ?? 0.03);
}

export function edgeOf(sel) {
  return sel.probability * sel.odds - 1;
}

// Returns { ok, reason, edge }.
export function check(config, sel, forMega = false) {
  const rule = ruleFor(config, sel.sport, sel.category);
  if (!rule) return { ok: false, reason: 'no rule for this market', edge: 0 };
  let lo = rule.min;
  let hi = rule.max;
  if (forMega) {
    lo = config.mega.min;
    hi = config.mega.max;
  }
  const edge = edgeOf(sel);
  const floor = Math.max(lo, config.absolute_min_odds);
  if (!(sel.odds > 1)) return { ok: false, reason: 'enter a price above 1.00', edge };
  if (sel.odds < floor) return { ok: false, reason: `odds below ${floor.toFixed(2)}`, edge };
  if (sel.odds > hi) return { ok: false, reason: `odds above ${hi.toFixed(2)}`, edge };
  const need = requiredEdge(config, sel);
  if (edge < need) {
    return { ok: false, reason: `edge ${pct(edge, true)} (needs ${pct(need)})`, edge };
  }
  return { ok: true, reason: `edge ${pct(edge, true)}`, edge };
}

// Is the minimum acceptable price inside the market's odds band? Used to
// shortlist candidates before any SportyBet price is entered.
export function inBand(config, game, row) {
  const [, category, , minOdds] = row;
  const rule = ruleFor(config, game.sport, category);
  if (!rule) return false;
  return minOdds >= Math.max(rule.min, config.absolute_min_odds) && minOdds <= rule.max;
}

export function valuePicks(config, selections, forMega = false) {
  return selections
    .filter((s) => check(config, s, forMega).ok)
    .sort((a, b) => edgeOf(b) - edgeOf(a));
}

export function pct(x, signed = false) {
  const s = `${(x * 100).toFixed(1)}%`;
  return signed && x > 0 ? `+${s}` : s;
}
