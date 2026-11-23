import { useMemo, useState } from 'react';
import { inputsSummary, kickoffParts, marketKey, sourceSummary } from '../lib/data.js';
import { check, inBand, pct } from '../lib/value.js';

const TOP = 4;

export default function GameCard({ game, config, prices, setPrice, started }) {
  const [open, setOpen] = useState(false);
  const [query, setQuery] = useState('');
  const { time } = kickoffParts(game.kickoff);

  const candidates = useMemo(
    () => game.m.filter((row) => inBand(config, game, row)).sort((a, b) => b[2] - a[2]).slice(0, TOP),
    [game, config],
  );
  const priced = game.m.filter((row) => prices[marketKey(game, row[0])]);
  const shown = open
    ? game.m.filter((row) => row[0].toLowerCase().includes(query.toLowerCase()))
    : mergeUnique(candidates, priced);

  return (
    <article className={`card game${started ? ' started' : ''}`}>
      <header className="game-head">
        <div className="game-meta">
          <span className="time">{time}</span>
          <span className="league">{game.league}</span>
          <span className={`tier tier-${game.tier}`} title="League tier: A full market menu and best data, C main lines only">
            Tier {game.tier}
          </span>
          {started && <span className="tag">Started</span>}
        </div>
        <h3 className="teams">
          {game.home} <span className="vs">vs</span> {game.away}
        </h3>
        <p className="inputs">
          {inputsSummary(game)}
          {sourceSummary(game) && <span className="muted"> · {sourceSummary(game)}</span>}
        </p>
      </header>

      {shown.length === 0 && !open && (
        <p className="muted small">No market falls inside the value bands for this game.</p>
      )}
      {open && (
        <input
          className="search"
          type="search"
          placeholder={`Search ${game.m.length} markets`}
          value={query}
          onChange={(e) => setQuery(e.target.value)}
        />
      )}
      <ul className="markets">
        {shown.map((row) => (
          <MarketRow key={row[0]} game={game} row={row} config={config} prices={prices} setPrice={setPrice} />
        ))}
      </ul>
      <button className="link" onClick={() => setOpen(!open)}>
        {open ? 'Show shortlist' : `All ${game.m.length} markets`}
      </button>
    </article>
  );
}

function MarketRow({ game, row, config, prices, setPrice }) {
  const [market, category, probability, minOdds] = row;
  const key = marketKey(game, market);
  const raw = prices[key] ?? '';
  const odds = parseFloat(raw);
  const result =
    odds > 1
      ? check(config, { sport: game.sport, category, odds, probability, tier: game.tier })
      : null;

  return (
    <li className={`market${result ? (result.ok ? ' is-value' : ' no-value') : ''}`}>
      <div className="market-main">
        <span className="market-name">{market}</span>
        <span className="market-nums">
          <span title="Our estimated chance">{pct(probability)}</span>
          <span className="muted" title="Fair odds: break-even price">fair {(1 / probability).toFixed(2)}</span>
          <span className="need" title="Lowest SportyBet price that counts as value">bet at {minOdds.toFixed(2)}+</span>
        </span>
      </div>
      <div className="market-entry">
        <label className="sr-only" htmlFor={key}>SportyBet price for {market}</label>
        <input
          id={key}
          className="price"
          type="number"
          inputMode="decimal"
          step="0.01"
          min="1.01"
          placeholder="Price"
          value={raw}
          onChange={(e) => setPrice(key, e.target.value)}
        />
        {result && (
          <span className={`verdict ${result.ok ? 'ok' : 'bad'}`}>
            {result.ok ? `VALUE ${pct(result.edge, true)}` : result.reason}
          </span>
        )}
      </div>
    </li>
  );
}

function mergeUnique(a, b) {
  const seen = new Set();
  return [...a, ...b].filter((row) => (seen.has(row[0]) ? false : seen.add(row[0])));
}
