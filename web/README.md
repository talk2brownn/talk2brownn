# Edge website

A static React site (Vite). It reads the day's price sheet from
`public/data/<date>/` (written by `engine/edge/export.py`) and does
everything else in the browser: checking SportyBet prices against the value
rules, building the ladder (2 to 1,000 odds) and the 30-game slip, and keeping
your saved slips on your device.

## Run locally

```bash
cd web
npm install
npm run dev        # http://localhost:5173
npm test           # value check and ladder optimiser tests
npm run build      # production build in dist/
```

To refresh the data locally:

```bash
cd engine
python -m edge.today          # price today's games (all seven sports)
python -m edge.export         # write web/public/data/<today>/
```

## Going live (one-time setup)

1. **GitHub secret.** Repository Settings → Secrets and variables → Actions →
   New repository secret: name `APISPORTS_KEY`, value = your API-Sports key.
   The daily workflow (`.github/workflows/daily-prices.yml`) uses it.
2. **Default branch.** GitHub runs scheduled workflows only from the default
   branch, so the daily job starts once this work is merged there.
3. **Cloudflare Pages.** In the Cloudflare dashboard: Workers & Pages →
   Create → Pages → Connect to Git → choose this repository, then set:
   - Production branch: your default branch
   - Root directory: `web`
   - Build command: `npm ci && npm test && npm run build`
   - Build output directory: `dist`

   Node 22 is picked up from `web/.node-version`. Each daily data commit
   triggers a fresh deploy, and the site gets a free `*.pages.dev` address.

## Pages

- **Today**: every priced game by sport, with a shortlist of markets that can
  be value. Type SportyBet's price to check it.
- **My slip**: your value picks, the ladder and the 30-game slip; copy a slip
  or save it to your record.
- **Record**: saved slips; mark them won, lost or void.
- **How it works**: the value rules and what the numbers mean.
