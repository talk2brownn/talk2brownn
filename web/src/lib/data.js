// Loads the day's price sheet exported by engine/edge/export.py.

export const SPORTS = [
  { id: 'football', label: 'Football', icon: '⚽' },
  { id: 'basketball', label: 'Basketball', icon: '🏀' },
  { id: 'handball', label: 'Handball', icon: '🤾' },
  { id: 'hockey', label: 'Ice hockey', icon: '🏒' },
  { id: 'nfl', label: 'NFL', icon: '🏈' },
  { id: 'rugby', label: 'Rugby', icon: '🏉' },
  { id: 'baseball', label: 'Baseball', icon: '⚾' },
];

const BASE = `${import.meta.env.BASE_URL}data`;

async function getJson(url) {
  const res = await fetch(url, { cache: 'no-cache' });
  if (!res.ok) throw new Error(`${res.status} loading ${url}`);
  return res.json();
}

export async function loadDay(date) {
  const day = date ?? (await getJson(`${BASE}/latest.json`)).date;
  const config = await getJson(`${BASE}/${day}/index.json`);
  const entries = await Promise.all(
    Object.keys(config.sports).map(async (sport) => [sport, await getJson(`${BASE}/${day}/${sport}.json`)]),
  );
  return { day, config, games: Object.fromEntries(entries) };
}

export function marketKey(game, market) {
  return `${game.id}|${market}`;
}

// Kickoff strings are "YYYY-MM-DD HH:MM" in Lagos time.
export function kickoffParts(kickoff) {
  const [d, t] = kickoff.split(' ');
  return { date: d, time: t ?? '' };
}

export function dayLabel(dateStr, today) {
  if (dateStr === today) return 'Today';
  const d = new Date(`${dateStr}T12:00:00`);
  const t = new Date(`${today}T12:00:00`);
  const diff = Math.round((d - t) / 86400000);
  if (diff === 1) return 'Tomorrow';
  return d.toLocaleDateString('en-GB', { weekday: 'short', day: 'numeric', month: 'short' });
}

// One-line summary of what a game's prices were built from.
export function inputsSummary(game) {
  const i = game.inputs || {};
  if (i.xg) return `Expected goals ${i.xg[0].toFixed(2)} – ${i.xg[1].toFixed(2)}`;
  if (i.home_goals != null) return `Expected goals ${i.home_goals.toFixed(2)} – ${i.away_goals.toFixed(2)}`;
  if (i.home_runs != null) return `Expected runs ${i.home_runs.toFixed(2)} – ${i.away_runs.toFixed(2)}`;
  if (i.total != null) {
    const home = (i.total + i.margin) / 2;
    const away = (i.total - i.margin) / 2;
    return `Expected score ${home.toFixed(1)} – ${away.toFixed(1)}`;
  }
  return '';
}

export function sourceSummary(game) {
  const i = game.inputs || {};
  if (game.sport === 'football') {
    const parts = [];
    if (i.xg_market) parts.push('exchange prices');
    if (i.xg_model) parts.push('our results model');
    return parts.length ? `From ${parts.join(' + ')}` : '';
  }
  return i.bookmaker ? `From ${i.bookmaker} lines` : '';
}
