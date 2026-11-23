import { useCallback, useEffect, useMemo, useState } from 'react';
import AboutView from './components/AboutView.jsx';
import GameCard from './components/GameCard.jsx';
import RecordView from './components/RecordView.jsx';
import SlipView from './components/SlipView.jsx';
import { SPORTS, dayLabel, kickoffParts, loadDay, marketKey } from './lib/data.js';
import { keys, load, save } from './lib/storage.js';
import { check } from './lib/value.js';

const VIEWS = [
  { id: 'today', label: 'Today' },
  { id: 'slip', label: 'My slip' },
  { id: 'record', label: 'Record' },
  { id: 'about', label: 'How it works' },
];

// Kickoffs are Lagos time (UTC+1, no daylight saving).
const hasStarted = (kickoff) => new Date(`${kickoff.replace(' ', 'T')}:00+01:00`) <= new Date();

export default function App() {
  const [data, setData] = useState(null);
  const [error, setError] = useState('');
  const [view, setView] = useState('today');
  const [sport, setSport] = useState('all');
  const [tier, setTier] = useState('all');
  const [query, setQuery] = useState('');
  const [hideStarted, setHideStarted] = useState(true);
  const [prices, setPrices] = useState({});
  const [record, setRecord] = useState(() => load(keys.record, []));
  const [stake, setStakeState] = useState(() => load(keys.stake, 100));

  useEffect(() => {
    loadDay()
      .then((d) => {
        setData(d);
        setPrices(load(keys.prices(d.day), {}));
      })
      .catch((e) => setError(String(e)));
  }, []);

  const setPrice = useCallback(
    (key, value) => {
      setPrices((prev) => {
        const next = { ...prev };
        if (value === '') delete next[key];
        else next[key] = value;
        save(keys.prices(data.day), next);
        return next;
      });
    },
    [data],
  );

  const allGames = useMemo(() => (data ? Object.values(data.games).flat() : []), [data]);

  // Every market with a SportyBet price typed in becomes a selection.
  const selections = useMemo(() => {
    if (!data) return [];
    const byKey = new Map();
    for (const g of allGames) for (const row of g.m) byKey.set(marketKey(g, row[0]), [g, row]);
    return Object.entries(prices)
      .map(([key, raw]) => {
        const found = byKey.get(key);
        const odds = parseFloat(raw);
        if (!found || !(odds > 1)) return null;
        const [g, [market, category, probability]] = found;
        return {
          key, sport: g.sport, category, matchId: g.id, match: `${g.home} vs ${g.away}`,
          market, odds, probability, tier: g.tier, kickoff: g.kickoff,
        };
      })
      .filter(Boolean);
  }, [data, allGames, prices]);

  const valueCount = data ? selections.filter((s) => check(data.config, s).ok).length : 0;

  const games = useMemo(() => {
    const q = query.trim().toLowerCase();
    return allGames
      .filter((g) => sport === 'all' || g.sport === sport)
      .filter((g) => tier === 'all' || g.tier === tier)
      .filter((g) => !hideStarted || !hasStarted(g.kickoff))
      .filter((g) => !q || `${g.home} ${g.away} ${g.league}`.toLowerCase().includes(q))
      .sort((a, b) => a.kickoff.localeCompare(b.kickoff) || a.league.localeCompare(b.league));
  }, [allGames, sport, tier, query, hideStarted]);

  const saveSlip = (title, slip) => {
    const entry = {
      id: `${Date.now()}`, day: data.day, title, stake, status: 'pending',
      totalOdds: slip.totalOdds, winProbability: slip.winProbability,
      legs: slip.legs.map(({ match, market, odds, probability, sport }) => ({ match, market, odds, probability, sport })),
    };
    const next = [...record, entry];
    setRecord(next);
    save(keys.record, next);
  };
  const updateRecord = (next) => {
    setRecord(next);
    save(keys.record, next);
  };
  const setStake = (v) => {
    setStakeState(v);
    save(keys.stake, v);
  };
  const clearPrices = () => {
    setPrices({});
    save(keys.prices(data.day), {});
  };

  if (error) {
    return (
      <main className="shell">
        <p className="card">Could not load today's prices: {error}</p>
      </main>
    );
  }
  if (!data) {
    return (
      <main className="shell">
        <p className="loading">Loading today's prices…</p>
      </main>
    );
  }

  const counts = Object.fromEntries(SPORTS.map((s) => [s.id, (data.games[s.id] || []).length]));

  return (
    <>
      <header className="top">
        <div className="shell top-inner">
          <div className="brand">
            <span className="logo" aria-hidden>◆</span> Edge
            <span className="date">{dayLabel(data.day, data.day)} · {new Date(`${data.day}T12:00:00`).toLocaleDateString('en-GB', { day: 'numeric', month: 'short' })}</span>
          </div>
          <nav className="tabs" aria-label="Sections">
            {VIEWS.map((v) => (
              <button key={v.id} className={view === v.id ? 'active' : ''} onClick={() => setView(v.id)}>
                {v.label}
                {v.id === 'slip' && valueCount > 0 && <span className="badge">{valueCount}</span>}
              </button>
            ))}
          </nav>
        </div>
      </header>

      <main className="shell">
        {view === 'today' && (
          <>
            <div className="chips" role="tablist" aria-label="Sport">
              <button className={sport === 'all' ? 'chip active' : 'chip'} onClick={() => setSport('all')}>
                All <span className="count">{allGames.length}</span>
              </button>
              {SPORTS.map((s) => (
                <button key={s.id} className={sport === s.id ? 'chip active' : 'chip'} onClick={() => setSport(s.id)}
                  disabled={!counts[s.id]}>
                  <span aria-hidden>{s.icon}</span> {s.label} <span className="count">{counts[s.id]}</span>
                </button>
              ))}
            </div>
            <div className="filters">
              <input type="search" placeholder="Search team or league" value={query} onChange={(e) => setQuery(e.target.value)} />
              <select value={tier} onChange={(e) => setTier(e.target.value)} aria-label="League tier">
                <option value="all">All tiers</option>
                <option value="A">Tier A</option>
                <option value="B">Tier B</option>
                <option value="C">Tier C</option>
              </select>
              <label className="toggle">
                <input type="checkbox" checked={hideStarted} onChange={(e) => setHideStarted(e.target.checked)} /> Hide started
              </label>
            </div>
            <p className="muted small hint">
              Shortlist per game = markets that could be value at a sensible SportyBet price. Type SportyBet's price
              to check it; green picks go to <button className="link inline" onClick={() => setView('slip')}>My slip</button>.
            </p>
            {games.length === 0 && <p className="empty">No games match these filters.</p>}
            <Board games={games} today={data.day} config={data.config} prices={prices} setPrice={setPrice} />
          </>
        )}
        {view === 'slip' && (
          <SlipView config={data.config} selections={selections} stake={stake} setStake={setStake}
            onClear={clearPrices} onSave={saveSlip} />
        )}
        {view === 'record' && (
          <RecordView record={record}
            setStatus={(id, status) => updateRecord(record.map((r) => (r.id === id ? { ...r, status } : r)))}
            remove={(id) => updateRecord(record.filter((r) => r.id !== id))} />
        )}
        {view === 'about' && <AboutView config={data.config} />}
        <footer className="foot muted small">
          Prices generated {new Date(data.config.generated_at).toLocaleString('en-GB', { timeZone: 'Africa/Lagos' })} (Lagos).
          18+ · No bet is safe · Bet only what you can afford to lose.
        </footer>
      </main>
    </>
  );
}

function Board({ games, today, config, prices, setPrice }) {
  let lastDay = '';
  return games.map((g) => {
    const { date } = kickoffParts(g.kickoff);
    const heading = date !== lastDay ? <h2 className="day" key={`d-${date}`}>{dayLabel(date, today)}</h2> : null;
    lastDay = date;
    return [
      heading,
      <GameCard key={g.id} game={g} config={config} prices={prices} setPrice={setPrice} started={hasStarted(g.kickoff)} />,
    ];
  });
}
