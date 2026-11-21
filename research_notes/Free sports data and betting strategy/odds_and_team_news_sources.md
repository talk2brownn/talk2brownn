# Free Odds Data and Pre-Match Team News Sources (Football, Basketball, Handball), as of late 2026

Research note, dated 2026-11-21. Method caveat: the session's network blocked direct page fetches of the-odds-api.com, football-data.co.uk and oddspapi.io (DNS refused by the sandbox proxy). Findings therefore rest on web-search extracts of official pages plus third-party pages. Every claim below that is marked **[vendor]** comes from the provider's own marketing. Anything marked **[unverified, prior knowledge]** is background knowledge that this session could not confirm; it sits under Inferences or Gaps, never under Cited Findings. Before building anything, run a live test call or read the current pricing page.

---

## 1. Free odds APIs (current/upcoming/live odds for margin and fair-price computation)

### Takeaway
No single free API covers all three sports, sharp odds and history at a useful volume. In late 2026 the most generous free combination appears to be OddsPapi (250 req/month, vendor-stated Pinnacle and SportyBet coverage, handball, some free historical data), with The Odds API (500 credits/month, has handball keys) and API-Sports (100 req/day, all endpoints incl. odds, injuries and lineups) alongside it. Pinnacle's own API closed to the public on 23 July 2025. odds-api.io paused new free keys in Aug 2026. Betfair's free delayed key is for development only, and Nigeria may be a restricted jurisdiction.

### Cited Findings

**Ranked catalogue: free odds APIs**

| Rank | Source | Free limit | Sports (FB/BB/HB) | Markets | Bookmakers (sharp?) | Historical | Notes / terms |
|---|---|---|---|---|---|---|---|
| 1 | **OddsPapi** (oddspapi.io) | 250 requests/month; each request returns a full fixture board, not priced per market/region; no credit card **[vendor]** | Football, basketball, handball (EHF, Bundesliga, LNH; "70+ bookmakers" for handball) **[vendor]** | Multi-market **[vendor]** | 348–370 books incl. **Pinnacle** and **SportyBet** on the free tier **[vendor]** | `/v4/historical-odds`: every snapshot, up to 3 bookmakers per call, on the free plan, **but** another OddsPapi post says history is a paid add-on (self-contradictory) **[vendor]** | Best candidate for Pinnacle and SportyBet in one feed. Verify sourcing and licence. |
| 2 | **The Odds API** (the-odds-api.com) | 500 credits/month. A call costs markets × regions, so 500 credits is not 500 requests. Historical calls cost 10× | Football (many leagues). Basketball (NBA etc.). **Handball confirmed**: key `handball_germany_bundesliga`, live and upcoming | h2h, spreads, totals (props mostly US sports) | ~40 soft books; Pinnacle and SBOBet described as "Limited" by third parties. Pinnacle on the free plan **unconfirmed** | Snapshots back to 6 Jun 2020, said to be available from the free tier at 10× cost (third-party, conflicting) | `/v4/sports?all=true` is free (no quota). Paid: $30 for 20k credits, $59 for 100k |
| 3 | **API-Sports** (API-Football / API-Basketball / API-Handball) | 100 requests/day per sport API, resets 00:00 UTC. Per-minute limit disputed (30 vs 10) | Separate APIs per sport (api-sports.io family) | Pre-match odds endpoint (1X2, O/U, AH, etc.) | Mostly soft European books | Limited | Free plan gives "access to the entire API", every endpoint incl. **odds, lineups, injuries**. Pro is 7,500/day |
| 4 | **SportsGameOdds** (Amateur) | 2,500 "objects"/month (1 event = 1 object), 10 req/min, **8 leagues, 9 bookmakers** | Mostly US leagues. Has a handball page, but handball on the free plan is unconfirmed | Main lines and props | US-centric | No | Sources conflict on whether a card is needed |
| 5 | **odds-api.io** | 100 req/hour, up to 500/day, but only **2 recreational bookmakers**. Bet365, sharps, exchanges are paid | Multi-sport | — | Covers SportyBet on paid plans; describes its data as "publicly displayed odds" | — | **New free keys paused 27 Aug 2026**. Existing keys keep working |
| 6 | **Betfair Exchange API (delayed key)** | Free delayed app key; snapshots delayed by a variable 1–180 s; for development and testing only. Live key has a **£299 activation fee** | All three sports listed on the exchange | Exchange back/lay (match odds, O/U, AH) | Exchange = sharp-ish market price | See historical section | All commercial use of data/API must be approved by Betfair. Nigeria may be restricted (see below) |
| — | **Pinnacle API** | **Closed to the general public since 23 July 2025**. Bespoke access via api@pinnacle.com only for "select high value bettors & commercial partnerships" | — | — | — | — | Resellers (pinnapi, PinnWire, PinnFeed, Apify actors) re-serve Pinnacle odds. Provenance and licence unverified |
| — | **Smarkets API** | No documentation found | — | — | — | — | Not reachable through this research. Treat as unavailable |

Sources for the table rows:
- OddsPapi free tier is 250 req/month, includes Pinnacle and history, no card — [OddsPapi blog: Free Odds API](https://oddspapi.io/blog/?p=144); [OddsPapi Pinnacle page](https://oddspapi.io/sportsbooks/pinnacle); [OddsPapi historical closing-line post](https://oddspapi.io/blog/?p=5269); contradicted by [OddsPapi "Best Odds APIs 2026"](https://oddspapi.io/blog/?p=2926)
- OddsPapi handball coverage — [OddsPapi handball blog](https://oddspapi.io/blog/?p=2901); [OddsPapi sports coverage](https://oddspapi.io/sports/)
- OddsPapi lists SportyBet — [OddsPapi SportyBet page](https://oddspapi.io/sportsbooks/sportybet)
- The Odds API: 500 credits is not 500 requests; historical calls cost 10× — [OddsPapi blog on The Odds API free tier](https://oddspapi.io/blog/the-odds-api-free-tier-limits) (competitor source); [SportsGameOdds vs The Odds API](https://sportsgameodds.com/compare/the-odds-api) (competitor source); paid plans — [The Odds API homepage](https://the-odds-api.com/)
- The Odds API handball (Bundesliga key `handball_germany_bundesliga`) — [The Odds API Handball-Bundesliga page](https://the-odds-api.com/sports/handball-bundesliga-odds.html). This contradicts an OddsPapi claim that The Odds API has no handball — [OddsPapi handball blog](https://oddspapi.io/blog/?p=2901)
- The Odds API sports list endpoint, with the `all` parameter — [apis.io The Odds API Sports API](https://apis.io/apis/the-odds-api/the-odds-api-sports-api/); [oddsapiR toa_sports_keys](https://search.r-project.org/CRAN/refmans/oddsapiR/html/toa_sports_keys.html)
- API-Football free plan gives the entire API at 100/day — [API-Football pricing](https://www.api-football.com/pricing); [API-Football beginner guide](https://www.api-football.com/news/post/how-to-get-started-with-api-football-the-complete-beginners-guide); the free tier burns out quickly under polling — [Sportmonks: hidden cost of free APIs](https://www.sportmonks.com/blogs/hidden-cost-free-sports-apis/) (competitor)
- SportsGameOdds Amateur: 2,500 objects, 8 leagues, 9 books — [SportsGameOdds FAQ](https://sportsgameodds.com/docs/faq); [SportsGameOdds rate limits](https://sportsgameodds.com/docs/info/rate-limiting); [SportsGameOdds pricing](https://sportsgameodds.com/pricing)
- odds-api.io free plan and pause of new free keys — [odds-api.io free pricing](https://odds-api.io/pricing/free); [odds-api.io free odds API blog](https://odds-api.io/blog/free-odds-api)
- Betfair delayed key (1–180 s, dev/testing), live key £299, commercial use needs approval — [Betfair developer docs: application keys](https://betfair-developer-docs.atlassian.net/wiki/x/URAp); [Betfair Data Scientists: app key](https://betfair-datascientists.github.io/api/apiappkey/)
- Pinnacle API closed 23 Jul 2025 — [pinnacleapi-documentation (GitHub, official)](https://github.com/pinnacleapi/pinnacleapi-documentation); [odds-api.io: Pinnacle shutdown alternatives](https://odds-api.io/blog/pinnacle-api-shutdown-alternatives); [dev.to: Pinnacle killed its public API](https://dev.to/ryankr/pinnacle-killed-its-public-api-heres-how-to-get-pinnacle-odds-in-2026-with-code-39pe)
- Pinnacle resellers — [sportsapis.dev pinnapi review](https://sportsapis.dev/apis/pinnapi); [PinnWire review](https://sportsapis.dev/apis/pinnwire)
- Smarkets: only a generic review found, saying it is "not available in all countries" — [ghanasoccernet Smarkets review](https://ghanasoccernet.com/ng/review/smarkets-review/)

**Betfair and Nigeria**
- No official Betfair source confirming Nigeria's status was found. A VPN vendor's list places Nigeria among Betfair-restricted countries (undated, unsourced) — [vpncentral: Betfair restricted countries](https://vpncentral.com/betfair-restricted-countries/). Using a VPN to get round geo-restrictions would breach Betfair terms and is **not** a legitimate route.

### Inferences
- A practical free stack for a Nigeria-based engine would be: **OddsPapi** (Pinnacle and SportyBet reference prices, handball), **The Odds API** (backup soft-book consensus, handball Bundesliga), and **API-Sports** per sport (odds, plus injuries and lineups on the same key). Combined free volume is small: 250 + roughly 100–500 effective calls per month + 100/day per sport. The engine must poll sparingly, for example one snapshot at T-24h and one at T-1h to T-15min per fixture, and cache results.
- With Pinnacle's public API gone, any "free Pinnacle" feed is a reseller or scraper. Licence and provenance risk sits with the user. Prefer providers that state a licence or commercial relationship.
- Credit maths for The Odds API: one call for 1X2 + totals across EU + UK regions costs 2 × 2 = 4 credits, so about 125 such calls per month. That is roughly 4 upcoming-odds pulls per day across all leagues for one sport.

### Gaps
- The Odds API's current exact bookmaker list for the `eu` region (whether Pinnacle and Betfair Exchange are returned on free keys) could not be fetched. **[unverified, prior knowledge]**: historically, `eu` region included Pinnacle, Betfair Exchange, Marathonbet and Matchbook; and full handball keys may include EHF Champions League and others. Confirm with `GET /v4/sports?all=true`.
- Whether OddsPapi's Pinnacle and SportyBet data is licensed or scraped, and its exact free-tier historical policy (sources conflict).
- Smarkets API status and availability in Nigeria: no information found.
- Official Betfair restricted-jurisdiction list (Nigeria): not found. Ask Betfair support.
- API-Handball and API-Basketball free-tier odds depth was not separately verified. The 100/day figure is confirmed for API-Football only; **[unverified, prior knowledge]** the API-Sports family uses the same free model across sports.

---

## 2. Free historical odds (backtesting and closing odds)

### Takeaway
football-data.co.uk remains the core free source for football historical and closing odds: CSV per league-season with multiple bookmakers, market average/max, and closing odds (columns with a "C" suffix, e.g. PSCH = Pinnacle closing home). Whether Pinnacle columns continued after Pinnacle's July 2025 API closure must be checked. Basketball and handball lack an equivalent free, clean, licensed archive. Betfair BASIC historical data is free but only 1-minute last-traded prices. OddsPortal's terms forbid scraping.

### Cited Findings

**Ranked catalogue: historical odds**

| Rank | Source | Sports | Content | Access/licence |
|---|---|---|---|---|
| 1 | **football-data.co.uk** | Football (~22 European leagues + "extra" leagues) | Results, match stats, odds from several books + market Max/Avg. **Closing odds = bookmaker code + "C"** (e.g. PSCH/PSCD/PSCA = Pinnacle closing). Asian handicap and closing odds for major leagues from 2005/06 (secondary source) | Free CSV download. See Gaps re terms |
| 2 | **OddsPapi historical endpoint** | All incl. handball | Snapshot series per fixture (≤3 books/call) **[vendor]**, enough to rebuild a closing line | Free tier (contested), 250 req/month |
| 3 | **The Odds API historical** | FB/BB/HB (from Jun 2020) | Snapshots at chosen timestamps; 10× credit cost | Roughly 8 multi-market snapshots per month on 500 free credits (third-party estimate) |
| 4 | **Betfair Historic Data, BASIC** | All exchange markets | **Free**, but only last traded price at 1-minute intervals, **no volume**, no ladder; "generally of little value" (betcode FAQ). ADVANCED (1 s + volume) and PRO (50 ms) are paid | Must "purchase" the £0 package at historicdata.betfair.com with a Betfair account, so the account-jurisdiction issue applies |
| 5 | **Kaggle "Beat the Bookie" worldwide football dataset** | Football, ~1,000 leagues | Odds series: 31,074 matches (Sep 2015–Mar 2016, 553 leagues) + 82,786 matches (Mar–Nov 2016, 658 leagues), with continuous odds movement. Associated paper used 32 bookmakers | Free; dated (2015–16) so useful only for methodology and backtest of closing-vs-average strategies |
| 6 | **d1on/beatthebookie (GitHub)** | Football | Closing-odds CSVs and scripts | Free (check repo licence) |
| 7 | **SportsBookReviewsOnline NBA archive** | NBA | Opening/closing moneylines, spreads, totals (Excel) used in R packages for 2017–2020 | Current status unconfirmed. SportsDataIO's historical odds archive is paid |
| 8 | **Covers / SportsOddsHistory** | NBA etc. | Free archive, but visible NBA content is mainly futures/series prices back to 1969, not game lines | Free to view |
| 9 | **OddsPortal archive** | FB/BB/HB incl. handball | Large odds archive incl. closing odds | **Terms forbid scraping or aggregation without express consent and automated load (Livesport s.r.o.)**. Manual viewing only |

Sources:
- football-data.co.uk closing odds use the "C" suffix and PSCH = Pinnacle closing home — [dm13450: Odds and Winning](https://dm13450.github.io/2019/01/10/Odds-and-Winning.html); [data explanation (copy of notes.txt)](https://alexandrugris.github.io/assets/data_explanation.txt); AH and closing odds from 2005/06 — [sports-models-kb: football-data.co.uk](https://sports-models-kb.pages.dev/football-data-co-uk) (secondary). The same page suggests football-data Pinnacle closing columns as a fallback after the Pinnacle API change — [sports-models-kb Pinnacle API](https://sports-models-kb.pages.dev/pinnacle-api)
- Betfair BASIC: free, 1-min LTP, no volume; Advanced/Pro paid — [Betfair Data Scientists: Historical Data Sources](https://betfair-datascientists.github.io/modelling/dataSources); [Using the historic data site](https://betfair-datascientists.github.io/data/usingHistoricDataSite); "little value" — [betcode FAQ: using data](https://betcode-org.github.io/faq/using-data)
- Beat the Bookie dataset sizes — [Lisandro79/BeatTheBookie GitHub](https://github.com/Lisandro79/BeatTheBookie); paper (arXiv 1710.02824, Kaplan/Mogollón/Ruiz? see paper) — [arXiv 1710.02824](https://pdf.arxiv.org/pdf/1710.02824); Kaggle link — [Sportmonks blog on Kaggle competitions](https://www.sportmonks.com/blogs/football-predictions-kaggle-competition); closing-odds CSVs — [d1on/beatthebookie](https://github.com/d1on/beatthebookie)
- SBRO NBA archive used for 2017–2020 data — [bettingtools nba_data.R](https://rdrr.io/github/pwu97/bettingtools/src/R/nba_data.R); SportsDataIO archive is paid via sales — [SportsDataIO historical data guide](https://sportsdata.io/help/historical-data-integration-guide); Covers archive — [Covers Sports Odds History](https://www.covers.com/sportsoddshistory/?p=505)
- OddsPortal terms (no scraping/aggregation without express consent; no automated load) — [OddsPortal General Terms of Use](https://www.oddsportal.com/terms/); commercial reuse restricted, "legal gray area" — [ScrapeHero](https://www.scrapehero.com/scraping-odds-portal/). Open-source scrapers exist, e.g. [OddsHarvester](https://github.com/jordantete/OddsHarvester), but they don't make scraping permitted.

### Inferences
- **[unverified, prior knowledge]** football-data.co.uk column families: `B365H/D/A`, `BWH`, `IWH`, `PSH` (Pinnacle), `WHH`, `VCH`, `MaxH`, `AvgH`, `BFEH` (Betfair Exchange, added in later seasons). Over/Under 2.5: `B365>2.5`, `P>2.5`, `Max>2.5`, `Avg>2.5`. Asian handicap: `AHh` (line), `B365AHH`, `PAHH`, `MaxAHH`, `AvgAHH`. Closing versions insert "C" (e.g. `PSCH`, `PC>2.5`, `PCAHH`, `AvgCH`). Several books (e.g. Interwetten, VC) were dropped in recent seasons. The site's notes say data is free for personal use and not for redistribution. **Verify against https://www.football-data.co.uk/notes.txt.** It could not be fetched from this sandbox.
- Football backtesting with Pinnacle closing odds is therefore free and well-established. NBA and handball backtests will need either paid archives or the self-built snapshot logging described next.
- **Best long-term free path:** log your own snapshots daily (OddsPapi / The Odds API / API-Sports odds) into a database from now on. Within one season this yields an owned closing-odds archive, incl. SportyBet prices, that no free archive provides.

### Gaps
- Whether football-data.co.uk still publishes Pinnacle (PS/PSC) columns for 2025/26 and 2026/27, after Pinnacle restricted its API in July 2025. This is critical for CLV benchmarking and could not be verified.
- Exact football-data.co.uk licence wording (not fetched).
- Kaggle dataset licence and the exact bookmaker count tied to the Kaggle upload.
- Whether sportsbookreviewsonline.com's NBA archive is still online and updated past 2022–23.
- No free, licensed handball historical odds archive was found apart from OddsPortal (scraping forbidden) and the API historical endpoints.

---

## 3. Sharp benchmark and margin-removal methods

### Takeaway
Pinnacle closing odds (and Betfair Exchange prices in liquid markets) are the industry and academic reference for "true" probability and closing-line value. Turning any book's odds into fair probabilities needs a margin-removal method. penaltyblog ships 7 methods (multiplicative default, additive, power, Shin, differential margin weighting, odds ratio, logarithmic). The R `implied` package offers the equivalents.

### Cited Findings
- Analysts commonly use Pinnacle closing lines as the efficiency benchmark and measure CLV against them; academic betting-efficiency papers frequently use them as the reference — [completesports: how Pinnacle sets sharp lines](https://www.completesports.com/how-pinnacle-sets-the-sharpest-lines/); [sports-models-kb: Pinnacle CLV](https://sports-models-kb.pages.dev/closing-line-value-pinnacle) (secondary). One non-peer-reviewed NFL props study found Pinnacle the most accurate of DraftKings, ESPN BET, BetMGM and Pinnacle — [shaanchanchani: sportsbook props accuracy](https://shaanchanchani.github.io/articles/sportsbook-props)
- The Beat-the-Bookie paper derived a profitable method by comparing a book's odds to the consensus average of many bookmakers (average-odds as a "fair" proxy) — [Sportmonks blog](https://www.sportmonks.com/blogs/football-predictions-kaggle-competition); [arXiv 1710.02824](https://pdf.arxiv.org/pdf/1710.02824)
- penaltyblog `implied` methods: MULTIPLICATIVE (default), ADDITIVE, POWER, SHIN, DIFFERENTIAL_MARGIN_WEIGHTING, ODDS_RATIO, LOGARITHMIC. "Each method represents a different theory of how the bookmaker's margin is applied". API: `calculate_implied(odds, method=ImpliedMethod.SHIN, odds_format=...)`, with fitted parameters (e.g. Shin z) in `method_params` — [penaltyblog docs: implied](https://penaltyblog.readthedocs.io/en/latest/implied/implied.html)
- Additive removes an equal share of the margin from each outcome and can yield negative probabilities for longshots. Power models book probabilities as a power function of true ones. Shin solves for an insider-trading parameter z in (0,1) so the probabilities sum to 1. Odds-ratio method is attributed to Cheung (2015) — [R implied package vignette](https://search.r-project.org/CRAN/packages/implied/vignettes/introduction.html); [implied_probabilities reference](https://search.r-project.org/CRAN/refmans/implied/html/implied_probabilities.html)
- Pinnacle's own margin is ~1.5–2%, so beating its close requires an edge of that size (forum, anecdotal) — [SBR forum: closing lines benchmark](https://www.sportsbookreview.com/forum/handicapper-think-tank/1387398-what-closing-lines-to-use-as-benchmark)

### Inferences
- Engine design: (a) compute each book's overround as Σ(1/odds) − 1. (b) Derive fair probabilities from the sharpest available price (Pinnacle via a reseller, Betfair, or the football-data closing Pinnacle/Avg columns historically) with Shin or power. These handle favourite-longshot bias better than multiplicative. (c) Use those as the calibration target and CLV reference. (d) Compare model and SportyBet prices for value. Where no sharp price exists (most handball, Nigerian-specific props), a de-margined multi-book average is the fallback benchmark.
- Shin and power are generally preferred for 1X2 (longshot bias). Multiplicative and additive are adequate for two-way near-even markets (totals, AH).

### Gaps
- No peer-reviewed paper directly quantifying Pinnacle closing accuracy was retrieved in this session. The specific Journal of Sports Sciences finding referenced in secondary sources was not verified.
- penaltyblog's own descriptions of differential-margin-weighting and odds-ratio were not retrieved.

---

## 4. SportyBet / Nigerian bookmaker odds

### Takeaway
SportyBet has no official public odds API or data feed, and no affiliate programme was found. Two third-party aggregators claim SportyBet coverage: OddsPapi (free tier) and odds-api.io (paid; describes its data as "publicly displayed odds", i.e. probably scraped). Directly scraping SportyBet is likely against its terms (not verified).

### Cited Findings
- OddsPapi lists SportyBet as a covered bookmaker, with a 250 req/month free tier — [OddsPapi SportyBet page](https://oddspapi.io/sportsbooks/sportybet)
- odds-api.io covers SportyBet, states it is "independent... not affiliated with SportyBet", and sources "publicly displayed odds" from 265+ books — [odds-api.io SportyBet page](https://odds-api.io/sportsbooks/sportybet)
- A Parse.bot marketplace listing offers a SportyBet booking-code endpoint (it creates betslip codes, not an odds feed, and is not a SportyBet product) — [parse.bot SportyBet API](https://parse.bot/marketplace/b0c4782f-8591-441b-92ee-6cf4b190317b/sportybet-com-ng-api)
- Nigerian books reportedly source their odds feeds from suppliers like Betradar/Sportradar (forum, unverified) — [TechCabal forum](https://radar.techcabal.com/t/help-how-do-nigerian-sports-betting-bookmarking-sites-get-their-data/14448)
- SportyBet review/profile (owner and licence context) — [ratingbet SportyBet NG](https://ratingbet.com/en-ng/bookmakers/sportybet/); [CB Insights SportyBet](https://www.cbinsights.com/company/sportybet)

### Inferences
- The legitimate low-risk options are: (1) the OddsPapi free tier for SportyBet prices (accepting the vendor's sourcing risk), or (2) a user manually reading SportyBet prices for the specific bets under consideration. Since the user is the bettor, comparing the model's fair price to the SportyBet price shown at bet time needs no feed at all.
- Since Nigerian soft books often price off the same supplier feeds plus margin, the SportyBet margin can be estimated by comparing a sample of manual readings against a consensus feed.

### Gaps
- SportyBet's ToS on automated access and the existence of any SportyBet affiliate/partner programme: not found.
- Whether any Nigerian odds-comparison site (e.g. Oddspedia NG) licenses SportyBet odds: not found.

---

## 5. Free pre-match team news (lineups, injuries, suspensions, referees)

### Takeaway
The most legitimate free sources are official publishers: the NBA's official injury report PDFs (timestamped, updated through the day with mandated filing windows), Premier League "Match officials for Matchweek N" articles, and club/league sites. API-Football's free tier includes `injuries` and `fixtures/lineups` endpoints (100 req/day). Transfermarkt, Rotowire and OddsPortal-type sites are commonly scraped, but scraping is ToS-risky. NewsAPI's free plan is development-only with a 24 h delay.

### Cited Findings

**Ranked catalogue: team news**

| Rank | Source | Sport | What | Access / terms |
|---|---|---|---|---|
| 1 | **NBA Official Injury Report** (official.nba.com) | Basketball (NBA) | Timestamped PDFs at `ak-static.cms.nba.com/referee/injury/Injury-Report_YYYY-MM-DD_HH_MMAM.pdf`. Statuses (Out/Questionable/…), "NOT YET SUBMITTED". Log shows 15-minute increments. Teams must file game-day reports 11 a.m.–1 p.m. local time (8–10 a.m. for tip-offs ≤5 p.m.). A 2026-27 season page exists | Free public PDFs. Parse with a PDF library at polite frequency |
| 2 | **API-Football injuries + lineups** | Football | `injuries` endpoint lists players likely to miss a match (added 2021). Lineups endpoint. Free plan includes all endpoints | 100 req/day free |
| 3 | **Premier League official "Match officials for Matchweek N"** | Football (EPL) | Referee, assistants, 4th official, VAR per match. 2026/27 MW1 article published (Stuart Attwell led the round) | Free news articles. Other leagues publish similar notices (unverified) |
| 4 | **ESPN injuries pages** | NBA etc. | Team-by-team injury tables | Free to view. Third-party, scraping ToS-restricted (not verified) |
| 5 | **Transfermarkt** | Football | Injury histories and current absences. Used in research (21,598 injuries of 11,507 players) | Primary terms not retrieved. Scraper vendors say users are responsible for ToS compliance. Treat as **scraping-restricted** |
| 6 | **NewsAPI.org Developer plan** | All | $0, **24-hour article delay**, search ≤1 month old, 100 requests/day, **dev/testing only — not for production**. Paid from $449/mo | Too delayed for pre-kickoff news |
| 7 | **GDELT DOC API** | All | Not verified in this session | See Gaps |

Sources:
- NBA injury report page and filing rules — [official.nba.com NBA Injury Report 2025-26](https://official.nba.com/nba-injury-report-2025-26/); sample PDFs — [Injury Report 2026-02-18 10:15AM](https://ak-static.cms.nba.com/referee/injury/Injury-Report_2026-02-18_10_15AM.pdf), [Injury Report 2026-04-11 12:00PM](https://ak-static.cms.nba.com/referee/injury/Injury-Report_2026-04-11_12_00PM.pdf); 2026-27 page — [official.nba.com 2026-27](https://official.nba.com/nba-injury-rep)
- API-Football injuries endpoint — [API-Football: New Endpoint Injuries](https://www.api-football.com/news/post/new-endpoint-injuries); free plan gives all endpoints incl. lineups — [API-Football pricing](https://www.api-football.com/pricing); [RapidAPI API-Football pricing](https://rapidapi.com/api-sports/api/api-football/pricing)
- Premier League match-official articles — [Match officials for Matchweek 1 (2026/27)](https://www.premierleague.com/en/news/4688925/match-officials-for-matchweek-1); [Matchweek 33 2025/26](https://www.premierleague.com/en/news/4618058/match-officials-for-matchweek-33-of-2025-26-premier-league-season)
- ESPN NBA injuries — [ESPN NBA injuries](https://www.espn.com/nba/injuries)
- Transfermarkt injury research use — [PubMed 34916169](https://pubmed.ncbi.nlm.nih.gov/34916169/); ToS responsibility language — [Apify Transfermarkt scraper](https://apify.com/junipr/transfermarkt-scraper.md)
- NewsAPI free plan terms — [NewsAPI pricing](https://newsapi.org/pricing)

### Inferences
- For football, combine the API-Football `injuries` call (one per fixture-day per league) with the `lineups` call about 60–20 min before kickoff, when official XIs are released. For basketball, parse the NBA PDF closest to tip-off. For handball (EHF, Bundesliga, LNH), no free structured injury feed was found. Rely on official club/league news pages and press (manual or RSS where offered).
- Referee data has the most value for football cards and penalties markets. Official league announcements (EPL publishes them days before each matchweek) are the legitimate route. worldreferee.com was not reached in this session.
- Rotowire and Covers: their terms were not retrieved. Both are commercial content sites and should be treated as "view manually, do not scrape" until their terms are checked.

### Gaps
- GDELT DOC 2.0 API free terms and latency were not retrieved. **[unverified, prior knowledge]**: GDELT is free and open with ~15-minute update cadence, useful for keyword alerts ("injury", club names) but noisy.
- Rotowire, Covers, Transfermarkt and worldreferee.com terms of use were not retrieved.
- API-Basketball and API-Handball injury/lineup coverage on free plans was not verified.
- Official referee-appointment pages for other leagues (LaLiga, Serie A, Bundesliga, EHF, NBA referee assignments, the last of which official.nba.com publishes daily per prior knowledge, unverified here).

---

## 6. ToS / legitimacy flags (summary)

### Takeaway
The following are flagged as scraping-forbidden or terms-restricted. Use only via official APIs, licensed resellers or manual viewing: OddsPortal (explicit terms), Pinnacle site and guest endpoints (public API closed, so scraping it circumvents that), Betfair (commercial data use needs approval; VPN use from restricted countries breaches terms), NewsAPI free (no production use), and Transfermarkt, SportyBet, ESPN, Rotowire and Covers (terms not verified; assume no scraping).

### Cited Findings
- OddsPortal terms: no scraping, aggregation or automated load without express consent — [OddsPortal Terms](https://www.oddsportal.com/terms/)
- Pinnacle API closed to the public; bespoke access only — [pinnacleapi-documentation](https://github.com/pinnacleapi/pinnacleapi-documentation). An Apify page claims a Pinnacle "guest API" is public with no key; this conflicts with Pinnacle's statement and is unverified — [Apify lergassy Pinnacle actor](https://apify.com/lergassy/pinnacle-odds-api.md)
- Betfair: commercial data use must be approved — [Betfair developer docs](https://betfair-developer-docs.atlassian.net/wiki/x/URAp)
- NewsAPI free plan is dev/testing only — [NewsAPI pricing](https://newsapi.org/pricing)
- odds-api.io sources "publicly displayed odds" (likely scraping-based; licence risk inherited) — [odds-api.io SportyBet page](https://odds-api.io/sportsbooks/sportybet)

### Inferences
- For personal, non-commercial modelling, the legal risk of ToS breaches is mainly civil (account bans, IP blocks) per commentary — [roundproxies](https://roundproxies.com/blog/scrape-sports-betting-sites/). It is still not "legitimate access" under this brief, so scrapers should be excluded from the engine design.

### Gaps
- Nigerian law and regulator (NLRC / Lagos State Lotteries and Gaming Authority) rules on using bookmaker odds data were not researched.
