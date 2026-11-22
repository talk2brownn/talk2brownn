import { useMemo, useState } from 'react';
import { buildLadder, buildMegaSlip } from '../lib/ladder.js';
import { check, edgeOf, pct } from '../lib/value.js';

const naira = (x) => `₦${Math.round(x).toLocaleString('en-NG')}`;

export default function SlipView({ config, selections, stake, setStake, onClear, onSave }) {
  const checked = selections.map((s) => ({ s, r: check(config, s) }));
  const values = checked.filter((x) => x.r.ok).map((x) => x.s);
  const ladder = useMemo(() => buildLadder(config, selections), [config, selections]);
  const mega = useMemo(() => buildMegaSlip(config, selections), [config, selections]);

  return (
    <div className="slip-view">
      <section className="card">
        <h2>Your value picks</h2>
        <p className="muted small">
          Type SportyBet's price next to any market on the Today tab. Picks that pass the value rule appear
          here and feed the ladder. {checked.length - values.length > 0 &&
            `${checked.length - values.length} price${checked.length - values.length === 1 ? '' : 's'} entered did not pass.`}
        </p>
        {values.length === 0 ? (
          <p className="empty">No value picks yet.</p>
        ) : (
          <ul className="legs">
            {values.sort((a, b) => edgeOf(b) - edgeOf(a)).map((s) => (
              <li key={s.key}>
                <span className="sport-tag">{s.sport}</span> {s.match} — <strong>{s.market}</strong> @ {s.odds.toFixed(2)}
                <span className="verdict ok">{pct(edgeOf(s), true)}</span>
              </li>
            ))}
          </ul>
        )}
        <div className="row">
          <label>
            Stake per slip{' '}
            <input className="stake" type="number" inputMode="numeric" min="0" step="50" value={stake}
              onChange={(e) => setStake(Number(e.target.value) || 0)} />
          </label>
          {selections.length > 0 && (
            <button className="link danger" onClick={onClear}>Clear today's prices</button>
          )}
        </div>
      </section>

      <h2 className="section-title">Ladder</h2>
      <p className="muted small section-note">
        Each rung uses the legs with the highest chance of all winning that still reach the target odds, one leg
        per match. A rung stays empty rather than adding a bad leg.
      </p>
      <div className="rungs">
        {ladder.map((slip) => (
          <SlipCard key={slip.target} title={`${slip.target} odds`} slip={slip} stake={stake} onSave={onSave} />
        ))}
      </div>

      <h2 className="section-title">30-game slip</h2>
      <SlipCard title="30-game slip" slip={mega} stake={stake} onSave={onSave} />
    </div>
  );
}

function SlipCard({ title, slip, stake, onSave }) {
  const [copied, setCopied] = useState(false);
  const empty = slip.legs.length === 0;

  const copy = async () => {
    const lines = slip.legs.map((s, i) => `${i + 1}. ${s.match} — ${s.market} @ ${s.odds.toFixed(2)}`);
    lines.push(`Total odds ${slip.totalOdds.toFixed(2)}`);
    try {
      await navigator.clipboard.writeText(lines.join('\n'));
      setCopied(true);
      setTimeout(() => setCopied(false), 1500);
    } catch {
      setCopied(false);
    }
  };

  return (
    <article className={`card rung${empty ? ' empty-rung' : ''}`}>
      <header className="rung-head">
        <h3>{title}</h3>
        {!empty && <span className="odds">{slip.totalOdds.toFixed(2)}</span>}
      </header>
      {empty ? (
        <p className="muted small">{slip.note || 'Enter SportyBet prices to build this slip.'}</p>
      ) : (
        <>
          <dl className="stats">
            <div><dt>Legs</dt><dd>{slip.legs.length}</dd></div>
            <div><dt>Wins about</dt><dd>1 in {formatOneIn(slip.oneIn)}</dd></div>
            <div><dt>Return per ₦1</dt><dd className={slip.expectedReturn >= 1 ? 'pos' : 'neg'}>₦{slip.expectedReturn.toFixed(2)}</dd></div>
            <div><dt>{naira(stake)} pays</dt><dd>{naira(stake * slip.totalOdds)}</dd></div>
          </dl>
          {slip.note && <p className="muted small">{slip.note}</p>}
          <ol className="legs">
            {slip.legs.map((s) => (
              <li key={s.key}>
                {s.match} — <strong>{s.market}</strong> @ {s.odds.toFixed(2)}{' '}
                <span className="muted">({pct(s.probability)})</span>
              </li>
            ))}
          </ol>
          <div className="row">
            <button onClick={copy}>{copied ? 'Copied' : 'Copy slip'}</button>
            <button className="secondary" onClick={() => onSave(title, slip)}>Save to record</button>
          </div>
        </>
      )}
    </article>
  );
}

function formatOneIn(x) {
  if (!Number.isFinite(x)) return '∞';
  if (x < 10) return x.toFixed(1);
  return Math.round(x).toLocaleString('en-NG');
}
