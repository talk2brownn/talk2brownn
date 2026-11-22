// Browser storage for the prices you type in and your saved slips. It stays
// on this device only, and some browsers block it (private mode), so every
// read and write is guarded and the site still works without it.

export function load(key, fallback) {
  try {
    const raw = window.localStorage.getItem(key);
    return raw ? JSON.parse(raw) : fallback;
  } catch {
    return fallback;
  }
}

export function save(key, value) {
  try {
    window.localStorage.setItem(key, JSON.stringify(value));
  } catch {
    // Storage unavailable: keep working in memory.
  }
}

export const keys = {
  prices: (day) => `edge:prices:${day}`,
  record: 'edge:record',
  stake: 'edge:stake',
};
