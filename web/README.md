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

The site lives on Cloudflare Pages in the project `edge-picks`
(https://edge-picks-9le.pages.dev). GitHub Actions builds and deploys it.

1. **GitHub secrets.** Repository Settings → Secrets and variables → Actions →
   New repository secret:
   - `APISPORTS_KEY`: your API-Sports key.
   - `CLOUDFLARE_API_TOKEN`: a Cloudflare API token with
     *Account → Cloudflare Pages → Edit*.
2. **Default branch.** GitHub runs scheduled workflows only from the default
   branch, so the daily job starts once this work is merged there.
3. **First run.** Actions → *Daily prices* → *Run workflow*. It prices today's
   games, commits the data and deploys the site. After that it runs every
   morning at 06:17 Lagos time.

Changes to `web/` pushed to `main` deploy through *Deploy site*
(`.github/workflows/deploy-site.yml`), which can also be run by hand.

## Pages

- **Today**: every priced game by sport, with a shortlist of markets that can
  be value. Type SportyBet's price to check it.
- **My slip**: your value picks, the ladder and the 30-game slip; copy a slip
  or save it to your record.
- **Record**: saved slips; mark them won, lost or void.
- **How it works**: the value rules and what the numbers mean.
