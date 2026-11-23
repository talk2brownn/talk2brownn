const naira = (x) => `${x < 0 ? '−' : ''}₦${Math.abs(Math.round(x)).toLocaleString('en-NG')}`;

export default function RecordView({ record, setStatus, remove }) {
  const settled = record.filter((r) => r.status === 'won' || r.status === 'lost');
  const won = settled.filter((r) => r.status === 'won');
  const staked = settled.reduce((x, r) => x + r.stake, 0);
  const returned = won.reduce((x, r) => x + r.stake * r.totalOdds, 0);
  const expected = settled.reduce((x, r) => x + r.stake * r.winProbability * r.totalOdds, 0);

  return (
    <div className="record-view">
      <section className="card">
        <h2>Track record</h2>
        <p className="muted small">
          Slips you save are kept on this device. Mark each one when it settles. Judge the engine on hundreds of
          slips, not a few: short-run results are mostly luck.
        </p>
        <dl className="stats">
          <div><dt>Settled</dt><dd>{settled.length}</dd></div>
          <div><dt>Won</dt><dd>{won.length}</dd></div>
          <div><dt>Staked</dt><dd>{naira(staked)}</dd></div>
          <div><dt>Profit</dt><dd className={returned - staked >= 0 ? 'pos' : 'neg'}>{naira(returned - staked)}</dd></div>
          <div><dt>ROI</dt><dd>{staked ? `${(((returned - staked) / staked) * 100).toFixed(1)}%` : '–'}</dd></div>
          <div><dt>Model expected</dt><dd>{naira(expected - staked)}</dd></div>
        </dl>
      </section>

      {record.length === 0 && <p className="empty">No saved slips yet. Use "Save to record" on a slip.</p>}
      {[...record].reverse().map((r) => (
        <article key={r.id} className={`card record ${r.status}`}>
          <header className="rung-head">
            <h3>{r.title} · {r.day}</h3>
            <span className="odds">{r.totalOdds.toFixed(2)}</span>
          </header>
          <p className="muted small">
            {r.legs.length} legs · stake {naira(r.stake)} · model chance 1 in {Math.round(1 / r.winProbability).toLocaleString('en-NG')}
          </p>
          <ol className="legs">
            {r.legs.map((s, i) => (
              <li key={i}>{s.match} — <strong>{s.market}</strong> @ {s.odds.toFixed(2)}</li>
            ))}
          </ol>
          <div className="row">
            {['pending', 'won', 'lost', 'void'].map((st) => (
              <button key={st} className={r.status === st ? '' : 'secondary'} onClick={() => setStatus(r.id, st)}>
                {st[0].toUpperCase() + st.slice(1)}
              </button>
            ))}
            <button className="link danger" onClick={() => remove(r.id)}>Delete</button>
          </div>
        </article>
      ))}
    </div>
  );
}
