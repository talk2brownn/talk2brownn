# Free Football (Soccer) Data Sources for Prediction Modelling (as of Nov 2026)

Research note on method: run on 2026-11-21. Direct fetches of football-data.co.uk, api-football.com, football-data.org, sportmonks.com, thestatsapi.com and readthedocs.io were **blocked by this session's network allowlist**, so facts about those providers come from search-engine summaries of their official pages, from mirrors, or from third-party reviews. Those are labelled. GitHub pages (StatsBomb, soccerdata, penaltyblog, worldfootballR, transfermarkt-datasets, openfootball, xgabora) were fetched directly. Before relying on any limit or licence term, re-check it on the provider's own page.

---

## Q1. Free historical results and match-stat datasets (top leagues and lower divisions)

### Takeaway
**football-data.co.uk** is still the backbone. It has free CSVs from 2000/01 to the current season, covering results, half-time scores, shots, shots on target, fouls, corners, cards, referee (England) and closing odds from about 20 bookmakers including Pinnacle. Two other sources are free and well maintained: **xgabora/Club-Football-Match-Data** (a cleaned, MIT-licensed merge of football-data and ClubElo, current to September 2026) and **openfootball** (CC0, scores only). The **Transfermarkt datasets** (CC0) add lineups, goal and card events, and market values, but their updates have been paused since July 2026.

### Cited Findings
**football-data.co.uk (Joseph Buchdahl)**
- Free CSVs cover 2000/01 to the current 2025/26 season. They include pre-closing and closing odds from nearly 20 bookmakers, Pinnacle among them. The market-best closing odds start only from 2019/20. — [Substack "A view from the Pinnacle"](https://networked.substack.com/p/a-view-from-the-pinnacle); [Apify listing describing the CSVs](https://apify.com/mirthful_radish/football-odds-historical)
- The CSV files are updated within a few days of each match round. This comes from a third-party description. — [Apify listing](https://apify.com/mirthful_radish/football-odds-historical)
- The columns, per a mirrored notes.txt, include Div, Date, Time, HomeTeam, AwayTeam, FTHG/FTAG/FTR, HTHG/HTAG/HTR, Referee, HS/AS (shots), HST/AST (shots on target), HF/AF (fouls committed), HC/AC (corners), HY/AY and HR/AR (cards), and odds columns. — [Mirror of notes.txt](https://alexandrugris.github.io/assets/data_explanation.txt); [Cornell project using EPL CSV with Referee, HY, AY, HR, AR](https://pages.github.coecis.cornell.edu/info2950-s23/project-marvelous-buneary/appendicies.html); [Datahub schema (HR = Home Team Red Cards)](https://datahub.io/football/english-premier-league)
- **Not included:** goal minutes, xG, possession, throw-ins, goal kicks, tackles and lineups. The column list above has none of them.

**xgabora/Club-Football-Match-Data (GitHub)** (lesser-known, high value)
- It holds 238,858 matches across 38 league and division codes in 27 countries, from 28 July 2000 to 3 September 2026. That includes all of 2025/26 and the opening rounds of 2026/27. — [GitHub](https://github.com/xgabora/Club-Football-Match-Data-2000-2025)
- The fields are HomeElo/AwayElo, Form3/Form5, full-time and half-time goals and results, shots, shots on target, fouls, corners, yellow and red cards, Bet365 1X2, O/U 2.5 and AH odds, and max odds across about 17 bookmakers. It also has six match-cluster probability columns, which are blank for the latest 8,301 rows. There is a separate file of 273,972 Elo snapshots. — [GitHub](https://github.com/xgabora/Club-Football-Match-Data-2000-2025)
- The repository is MIT-licensed, but the underlying data comes from Football-Data.co.uk and ClubElo, whose terms are not stated there. — [GitHub](https://github.com/xgabora/Club-Football-Match-Data-2000-2025)

**openfootball / football.json**
- It covers the EPL, Championship, League One and League Two; the Bundesliga, 2. Bundesliga and 3. Liga; La Liga and Segunda; Serie A and B; and Ligue 1 and 2, "and much more". Season folders run from 2010-11 to 2026-27. — [GitHub](https://github.com/openfootball/football.json)
- The fields are round, date, team1, team2 and the full-time score. Half-time and scorers are not shown in the JSON example. — [GitHub](https://github.com/openfootball/football.json)
- It is CC0 (public domain). The latest season updates automatically every day at 05:00 UTC from the upstream Football.TXT files, which depend on volunteer contributions. — [GitHub](https://github.com/openfootball/football.json)

**Transfermarkt datasets (dcaribou/transfermarkt-datasets; Kaggle "player-scores")**
- There are 12 tables: competitions (65), clubs (790+), players (50k+), games (88k+), appearances (1.89M+), player_valuations (650k+), club_games (177k+), game_events (1.27M+), game_lineups (3.17M+), transfers (175k+), countries and national_teams. — [GitHub](https://github.com/dcaribou/transfermarkt-datasets)
- It is CC0-1.0. You can get it from Kaggle (kaggle.com/datasets/davidcariboo/player-scores), as a single DuckDB file, or as gzipped CSVs. — [GitHub](https://github.com/dcaribou/transfermarkt-datasets)
- **Status:** updates are paused with no resumption date. The pipeline stopped working in mid-July 2026, so the data is current to 6 July 2026. The 2026/27 squads are not covered. — [GitHub](https://github.com/dcaribou/transfermarkt-datasets)

**ClubElo**
- soccerdata's ClubElo reader pulls CSV data from `http://api.clubelo.com`. The source carries no league names. — [soccerdata ClubElo docs](https://soccerdata.readthedocs.io/en/latest/datasources/ClubElo.html)

### Inferences
- For a betting engine, the most useful free base table is football-data.co.uk, or the xgabora merge. It has results, half-time results, shots, shots on target, corners, fouls and cards, plus closing odds for checking value against the market.
- The Transfermarkt `game_events` and `game_lineups` tables are probably the best free source of goal minutes and lineups at scale. The pause in updates means you would need your own current-season source.
- From memory and not verified this session: football-data.co.uk's "extra leagues" (Argentina, Brazil, USA, Nordics and others) carry results and odds but not match stats.

### Gaps
- I could not fetch football-data.co.uk directly, so its terms of use and its full 2025/26 league list are unverified. The same goes for exactly which divisions carry stats (my understanding is the English top five tiers and the major European top divisions).
- I did not verify the Kaggle "European Soccer Database" (Hugo Mathien). From memory it covers 2008–2016 only, is static, and its scraping origin is unclear.
- I did not verify worldfootball.net terms or access.

---

## Q2. Legitimate free xG, shot-level and event data, and the 2025–26 changes

### Takeaway
**FBref lost all Opta advanced data (xG, progressive passing and similar) on 20 January 2026.** **Understat** (top 5 leagues plus the RFPL, 2014/15 onward) is now the main free club xG source, though access is unofficial and there are no published API terms. Fully licensed, free event data is limited to **StatsBomb Open Data**, which keeps expanding (Women's Euro 2025, five top women's leagues in May 2026). The others are **Wyscout/Pappalardo** (2017/18, CC BY 4.0) and the small tracking samples from **SkillCorner** and **Metrica**.

### Cited Findings
**FBref (Sports Reference)**
- On 20 January 2026 FBref removed its advanced stats, including xG and progressive passing, after Opta ended the arrangement. Basic results, tables and scoring stats remain. StatsPerform told The Athletic that FBref had violated the agreement. — [Awful Announcing](https://awfulannouncing.com/soccer/sports-reference-pulls-advanced-data-agreement-violation-dispute.html); [The IX](https://www.theixsports.com/the-ix-soccer/fbrefs-loss-advanced-stats-womens-soccer-data-accessibility/)
- Shortly before the split, Opta's parent signed a betting-data deal to supply sportsbooks exclusively. — [Awful Announcing](https://awfulannouncing.com/soccer/sports-reference-pulls-advanced-data-agreement-violation-dispute.html)
- Sports Reference's data-use policy warns that spidering violates its terms and conditions. — [Sports-Reference data use](https://www.sports-reference.com/data_use.html)

**Understat**
- It covers the EPL, La Liga, Bundesliga, Serie A, Ligue 1 and RFPL from 2014/15. Data is embedded as JSON in the pages or served from internal endpoints (e.g. `/getLeagueData/{league}/{season}`). There is no official API. — [Apify Understat actor](https://apify.com/mirthful_radish/understat-xg-football-scraper); [worldfootballR README (leagues)](https://github.com/JaseZiv/worldfootballR)
- A 2026 roundup recommends Understat for xG and xA in the top five leagues now that FBref has lost its xG. — [TheStatsAPI blog (competitor, via search)](https://www.thestatsapi.com/blog/best-football-statistics-websites)
- soccerdata v1.9.0 moved to Understat's "new JSON API endpoints", which suggests Understat changed its site in 2026. — [soccerdata releases](https://github.com/probberechts/soccerdata/releases)
- I found no Understat terms of service.

**StatsBomb (Hudl Statsbomb) Open Data**
- It provides match, event and lineup JSON, plus 360 freeze-frame data for selected matches. The licence requires crediting "StatsBomb" and using its logo. — [GitHub statsbomb/open-data](https://github.com/statsbomb/open-data)
- Free releases include Women's Euro 2025 event and 360 data (July 2025) and "Five Top Women's Leagues" (WSL, Liga F, Frauen-Bundesliga, Serie A, NWSL), announced 27 May 2026. — [Hudl blog: Women's Euro 2025](https://www.hudl.com/blog/hudl-statsbomb-free-euro-2025-data); [Hudl blog: five women's leagues](https://www.hudl.com/blog/statsbomb-free-womens-data-wsl-ligaf-bundesliga-seriea-nwsl)
- statsbombpy reads the open data with no authentication. Using it means agreeing to StatsBomb's User Agreement. Goals are Shot events with `shot_outcome == "Goal"`, and timestamps reset each period. The statsbombpy README says the open data excludes 360 metrics, which conflicts with the open-data repo's statement that 360 data covers selected matches. — [statsbombpy](https://github.com/statsbomb/statsbombpy)

**Wyscout public dataset (Pappalardo et al., 2019, Scientific Data)**
- It holds every spatio-temporal event for a full season of seven competitions: 2017/18 PL, La Liga, Serie A, Bundesliga and Ligue 1, plus World Cup 2018 and Euro 2016. It is on Figshare (doi 10.6084/m9.figshare.c.4415000; last version January 2020) under CC BY 4.0. The CC BY claim comes from a GitHub mirror. — [Figshare](https://figshare.com/collections/Soccer_match_event_dataset/4415000/2); [PMC paper](https://pmc.ncbi.nlm.nih.gov/articles/PMC6817871); [octosport mirror](https://www.github.com/octosport/wyscout-soccer-match-event-dataset)

**Tracking samples**
- SkillCorner Open Data has a 10-match broadcast-tracking sample from the 2024/25 A-League, earlier 9 matches from 2019/20. A third-party index lists it as MIT-licensed. — [SkillCorner opendata](https://skillcorner.github.io/opendata/); [ecosyste.ms](https://awesome.ecosyste.ms/projects/github.com%2FSkillCorner%2Fopendata)
- Metrica sample-data has a few anonymised matches with tracking and event data, published as a sample of their product. I found no licence statement. — [GitHub metrica-sports/sample-data](https://github.com/metrica-sports/sample-data)

### Inferences
- For a betting model, StatsBomb, Wyscout, SkillCorner and Metrica are mainly useful for **building and calibrating your own xG model** or learning event structure. They are not ongoing feeds for current men's club seasons.
- Understat is the only free, ongoing club xG source for the big five, and it carries legal and technical risk: no official API, no stated terms, and endpoint changes in 2026. It is best treated as "use politely, personal research only, expect breakage".

### Gaps
- I could not confirm the current full competition list in StatsBomb's `competitions.json`, or whether men's club seasons were added in 2026.
- I found no free source of Opta-grade xG for lower divisions.

---

## Q3. Minute-level goal timing and half-level stats

### Takeaway
Free goal-minute data is available from **Transfermarkt datasets** (`game_events`, through July 2026), **StatsBomb/Wyscout** (event timestamps, limited competitions), **OpenLigaDB** (German leagues, live, no key), **Football Charts** (goal timing for 93 leagues, free with attribution) and **API-Football's free tier** (fixture events). Half-time scores, but not half-level stats, are in football-data.co.uk.

### Cited Findings
- OpenLigaDB is free with no key or authentication. Each match includes a goals array with matchMinute, scorer, penalty and own-goal flags. Example: `api.openligadb.de/getmatchdata/bl1`. Data is entered by volunteers without editorial review, so live goals can lag or contain errors. — [freeapihub OpenLigaDB](https://freeapihub.com/apis/openligadb-api); [Apify OpenLigaDB scraper schema](https://apify.com/parseforge/openligadb-football-matches-scraper.md); [matrix-db directory](https://matrix-db-api-directory.pages.dev/api/openligadb)
- Football Charts offers free results, fixtures, tables, **goal timing**, a public baseline model and Monte Carlo projections for 93 leagues in 42 countries. A key raises the limits to 5,000 a day and 60 a minute. The free tier covers the current and previous season. Terms allow personal and research use with attribution but no resale. There are no odds, and xG is unconfirmed. It is also an MCP server (`footballcharts-mcp`). — [mcpservers.org listing](https://mcpservers.org/servers/www-football-charts-com-developers)
- StatsBomb events carry period and timestamp, and the timestamp resets each period. — [statsbombpy](https://github.com/statsbomb/statsbombpy)
- The Transfermarkt `game_events` table has 1.27M+ rows. — [GitHub](https://github.com/dcaribou/transfermarkt-datasets)
- football-data.co.uk has HTHG/HTAG/HTR (half-time score) but no per-half shots or corners. — [notes mirror](https://alexandrugris.github.io/assets/data_explanation.txt)
- Sportradar StatsHub referee pages show card breakdowns by half and by home or away team. They are web views only, and reuse terms are unknown. — [Sportradar StatsHub example](https://statshub.sportradar.com/sportradar/en/sport/1/tournament/36/referee)

### Inferences
- Markets such as "lead by X at any time", "goals in a row" and "score in both halves" need goal minutes. The best free historical base is Transfermarkt `game_events` (2012-ish to July 2026, many leagues), with API-Football's free events endpoint or Football Charts for current fixtures.
- Half-level shot and corner stats are essentially unavailable free at scale. Only event data (StatsBomb or Wyscout) lets you compute them.

### Gaps
- I did not verify the exact `game_events` field names (minute, type, description) or the season range.
- I did not verify the Football Charts goal-timing granularity (exact minutes vs. 15-minute buckets).

---

## Q4. Throw-ins, goal kicks, tackles, fouls by team, and referee statistics

### Takeaway
**Fouls by team and the referee name** are free in football-data.co.uk (the referee column is reliably present for England). **Throw-ins and goal kicks** are only available free from event data: StatsBomb open data and the Wyscout public dataset. I found no free, ongoing match-level throw-in or goal-kick feed for current club seasons. Referee card averages can be **derived** from the football-data.co.uk Referee, HY/AY, HR/AR and HF/AF columns.

### Cited Findings
- football-data.co.uk has Referee, HF/AF (fouls committed), HY/AY and HR/AR. — [Cornell project](https://pages.github.coecis.cornell.edu/info2950-s23/project-marvelous-buneary/appendicies.html); [notes mirror](https://alexandrugris.github.io/assets/data_explanation.txt)
- My search for free throw-in and goal-kick data returned nothing beyond event-data providers. — [search result summary: Sportradar StatsHub referee pages and the R `mverse` soccer dataset only](https://search.r-project.org/CRAN/refmans/mverse/html/soccer.html)
- Sportradar StatsHub (public pages hosted for bookmakers) shows per-referee card totals and averages, by half and by home or away. Export and reuse terms are unknown. — [StatsHub](https://statshub.sportradar.com/sportradar/en/sport/1/tournament/36/referee)
- SportMonks documents referee statistic types, but only in its paid or limited API. — [SportMonks referee statistics docs](https://docs.sportmonks.com/v3/definitions/types/statistics/referee-statistics)
- StatsBomb events include pass types (throw-in, goal kick, corner) and duels and tackles. The format docs are in the repo's `doc` folder. — [GitHub statsbomb/open-data](https://github.com/statsbomb/open-data)

### Inferences
- A referee model (cards and fouls per ref) is feasible free for England and probably some other football-data.co.uk leagues: group by Referee and average HY+AY, HF+AF and HR+AR.
- Throw-in and goal-kick markets cannot be modelled from free ongoing data. Any such feed you find is likely to come from scraping a ToS-restricted site (see Q7).
- API-Football's `/fixtures/statistics` (fouls, corners, offsides, possession, etc.) is likely the best free per-match source for current seasons within its 100 calls a day. This is from memory and the exact field list was not verified.

### Gaps
- I did not verify whether football-data.co.uk's Referee column is populated outside England.
- I found no free source of tackles at match level for current seasons apart from API-Football (unverified) and StatsBomb's limited competitions.

---

## Q5. Free tiers of commercial APIs

### Takeaway
- **API-Football:** 100 requests a day, all endpoints and competitions, but recent seasons only.
- **football-data.org:** 12 competitions, 10 calls a minute, with scores and tables only. Lineups and bookings need a paid tier.
- **SportMonks:** Danish Superliga and Scottish Premiership only, 180 calls per hour per endpoint.
- **TheSportsDB:** key "123", about 30 a minute, with limited results.
- **OpenLigaDB:** no key, German-focused.
- **Football Charts:** 93 leagues, current and previous season.

### Cited Findings
**API-Football / API-Sports**
- The free plan gives 100 requests a day, resets at 00:00 UTC, and includes all endpoints and competitions. One summary says 10 a minute and another says 30 a minute, so the per-minute figure conflicts. — [API-Football beginner's guide](https://www.api-football.com/news/post/how-to-get-started-with-api-football-the-complete-beginners-guide); [API-Football pricing](https://www.api-football.com/pricing); [skills.sh](https://skills.sh/silkyland/thscore-api-skill/api-football-v3)
- Free is limited to recent seasons, while paid unlocks deeper history. The exact cutoff is not published in the sources found. In a 2026 blog post a developer bought a one-time paid plan (7,500 calls) to backfill all seasons, then migrated to SportMonks. — [beginner's guide](https://www.api-football.com/news/post/how-to-get-started-with-api-football-the-complete-beginners-guide); [2026 migration blog](https://saugki1773.github.io/data-engineering-blog/2026/04/25/switching-api-providers.html)

**football-data.org**
- Official policy: free gives 10 requests a minute, Standard 30 a minute, and higher plans 60 a minute. Over the limit you get HTTP 429, and the `X-Requests-Available-Minute` header shows the calls left. — [football-data.org API policies](https://docs.football-data.org/general/v4/policies.html)
- Free covers 12 competitions: CL, PL, La Liga, Bundesliga, Serie A, Ligue 1, Eredivisie, Primeira Liga, Championship, Brasileirão, World Cup and Euros. It has fixtures, tables and delayed scores. Third-party listings put live scores at €12 a month and lineups, scorers, bookings and squads ("Deep Data") at €29 a month. — [SportMonks comparison page (competitor)](https://www.sportmonks.com/football-api/alternatives/football-data-org/); [TheStatsAPI (competitor)](https://www.thestatsapi.com/blog/football-data-org-free-tier-limits-2026)

**SportMonks**
- The free plan covers the Scottish Premiership plus play-offs and the Danish Superliga plus play-offs, with "Standard data features", at 180 API calls per hour per endpoint. There is also a free trial for new customers, and paid plans run about 3,000 calls per hour per entity. — [SportMonks free plan](https://www.sportmonks.com/football-api/free-plan); [SportMonks football API](https://www.sportmonks.com/football-api/); [SportMonks FAQ](https://sportmonks.com/faq)

**TheSportsDB**
- The free key is `123` (official docs), with about 30 requests a minute and limited results on most endpoints. Premium is about $9 a month via Patreon, with 100 a minute, the v2 API and 2-minute livescores. Some older pages cite key "3". — [TheSportsDB docs](https://www.thesportsdb.com/docs/api); [sportsapis.dev review](https://sportsapis.dev/apis/thesportsdb)

**OpenLigaDB:** free, with no key. Covered in Q3. — [freeapihub](https://freeapihub.com/apis/openligadb-api)

**Football Charts:** free, 93 leagues, current and previous season, personal and research use with attribution. Covered in Q3. — [mcpservers.org](https://mcpservers.org/servers/www-football-charts-com-developers)

### Inferences
- The best free per-match stats feed for current fixtures is API-Football at 100 calls a day. That is roughly one league's weekend of fixtures plus stats. Use it for **forward** data and football-data.co.uk for history.
- football-data.org's free tier is good for fixtures and results scaffolding but has no match stats.
- SportMonks free is useful for prototyping against a production-grade schema on two small leagues.

### Gaps
- I could not verify whether API-Football's free tier includes odds, injuries and predictions endpoints for current seasons (it claims "all endpoints"), or the exact season cutoff.
- I did not research the Sportradar trial terms. Sportradar trials are typically 30 days, for evaluation only, and not for production. This is unverified.
- Nigeria: I found no evidence of geographic blocking by any of these APIs. All are global HTTP APIs, and payment for paid tiers may be the practical barrier. This is unverified.

---

## Q6. Open-source wrapper libraries

### Takeaway
**soccerdata** (Python) is actively maintained with weekly CalVer releases (v2026.43.0, 19 October 2026). **worldfootballR** (R) is **archived and unmaintained**. **penaltyblog** (MIT) is the most betting-focused library, with Dixon-Coles, Bayesian models, odds de-margining and scrapers. **statsbombpy** is official and gives keyless access to the open data.

### Cited Findings
- **soccerdata** sources: Club Elo, ESPN, FBref, Football-Data.co.uk, Sofascore, SoFIFA, Understat and WhoScored. It warns users to comply with the sites' ToS and that site changes break it. — [GitHub](https://github.com/probberechts/soccerdata)
- soccerdata releases:
  - v1.9.0 (12 April 2026) **removed FotMob support at FotMob's request**, moved FBref and SoFIFA to Selenium to bypass Cloudflare, bypassed Sofascore TLS fingerprinting, and moved Understat to new JSON endpoints.
  - v1.9.1 (24 July 2026) added a SeleniumBase CAPTCHA solver for WhoScored, SoFIFA and FBref.
  - v2026.43.0 (19 October 2026) introduced automated weekly CalVer releases.

  — [soccerdata releases](https://github.com/probberechts/soccerdata/releases)
- soccerdata's FAQ says the legal status of scraping "remains unclear". In the EU, scraping is not per se prohibited, but data mining tools are legally risky, and breaching a site's terms is a separate risk. — [soccerdata FAQ](https://soccerdata.readthedocs.io/en/stable/_sources/faq.rst.txt)
- **worldfootballR** is archived and read-only, and "will no longer be maintained". Its CRAN version is "very much out of date". It covered FBref, Transfermarkt and Understat and dropped Fotmob in v0.6.4. — [GitHub](https://github.com/JaseZiv/worldfootballR)
- **penaltyblog** (MIT) has:
  - Poisson, bivariate Poisson and Dixon-Coles models (Cython), and Bayesian and hierarchical models.
  - Elo, Massey, Colley and Pi ratings.
  - AH and O/U probabilities, and implied probabilities with overround removed.
  - Scrapers for Football Charts, Understat, Club Elo and FPL.
  - Streaming access to StatsBomb (including open data) and Opta.

  — [GitHub](https://github.com/martineastwood/penaltyblog)
- **statsbombpy** reads the open data with no credentials, while the paid API needs a login. — [GitHub](https://github.com/statsbomb/statsbombpy)

### Inferences
- The fact that soccerdata needs CAPTCHA solvers and Cloudflare bypasses for FBref, WhoScored and SoFIFA is itself a red flag: those sites actively resist automated access. Using those readers likely conflicts with the sites' terms.
- A clean, low-risk stack would be: penaltyblog for models; football-data.co.uk, ClubElo and Football Charts for data; statsbombpy for xG-model training; and API-Football free for current stats.

### Gaps
- I did not verify the current versions or status of mplsoccer (visualisation only) or understatapi.
- I could not confirm penaltyblog's latest PyPI version or date.

---

## Q7. Legally risky sources (ToS restrict or forbid scraping). Flagged, not recommended.

### Takeaway
**FotMob** explicitly forbids scraping, and soccerdata removed it at FotMob's request in 2026. **FBref/Sports-Reference** says spidering violates its terms. **Squawka** prohibits commercial screen-scraping. **Sofascore, WhoScored and Flashscore** actively block bots (Cloudflare, TLS fingerprinting, CAPTCHAs), and I could not fetch their scraping clauses. Treat them all as off-limits for automated collection.

### Cited Findings
- FotMob's ToS (September 2023): use of its data "for any purpose, including but not limited to scraping, reproduction, redistribution, or commercial purposes, without the express written consent of FotMob is strictly prohibited." — [fotmob.com/tos.txt](https://www.fotmob.com/tos.txt)
- soccerdata removed FotMob "at FotMob's request" (v1.9.0, 2026). — [soccerdata releases](https://github.com/probberechts/soccerdata/releases)
- Sports-Reference (FBref): spidering violates its terms and conditions. — [SR data use](https://www.sports-reference.com/data_use.html)
- Squawka prohibits "any automated system or software to extract data from this website for commercial purposes". — [Squawka](https://www.squawka.com/us/?p=67)
- Flashscore and Soccerway publish terms of use. Their exact scraping clauses were not retrieved. — [Flashscore terms](https://www.flashscore.com/terms); [Soccerway terms](https://gh.soccerway.com/terms)
- Sofascore has a help article on sports data API availability, which suggests it does not offer a public API. Its scraping terms were not retrieved. soccerdata bypasses its TLS fingerprinting. — [Sofascore help](https://sofascore.helpscoutdocs.com/article/129-sports-data-api-availability); [soccerdata releases](https://github.com/probberechts/soccerdata/releases)
- Understat has no stated terms, and paid Apify scrapers resell its data. The legal position is ambiguous. — [Apify](https://apify.com/mirthful_radish/understat-xg-football-scraper)

### Inferences
- Third-party Apify actors resell scraped Sofascore, Understat, football-data.org and OpenLigaDB data. Paying for them does not make the underlying access legitimate.
- FBref's remaining basic stats are still subject to its no-spidering rule. Manual CSV export ("Share & Export") for personal use is the safer route.

### Gaps
- The verbatim scraping clauses of Sofascore, WhoScored and Flashscore were not retrieved.
- Nigeria: I found no source on geo-restrictions for any of these data sites. Some betting-adjacent sites may geo-block, but this is unverified.

---

## Ranked catalogue (synthesis for the report writer)

1. **football-data.co.uk.** Free CSVs from 2000 onward. Results, half-time, shots, shots on target, fouls, corners, cards, referee and closing odds from about 20 bookmakers. It is active for 2025/26. The licence was not verified.
2. **xgabora Club-Football-Match-Data.** Football-data plus ClubElo merged, 239k matches, to September 2026, MIT (underlying terms apply).
3. **API-Football free.** 100 a day, all endpoints, recent seasons. The best free source of current per-match stats, events and lineups.
4. **Transfermarkt datasets.** CC0. Lineups, goal and card minutes, values. Frozen at July 2026.
5. **StatsBomb Open Data and statsbombpy.** Licensed event data and 360 for selected matches. Use it to train xG. Expanding (women's leagues in 2026).
6. **Understat.** The only free ongoing big-five xG (2014 onward). Unofficial access, endpoints changed in 2026, ToS unknown.
7. **ClubElo API.** Free Elo CSVs.
8. **Football Charts API.** 93 leagues, goal timing, model probabilities. Free for personal and research use with attribution. Lesser-known.
9. **football-data.org free.** 12 competitions, 10 a minute, scores and tables only.
10. **openfootball.** CC0 scores, daily auto-update.
11. **OpenLigaDB.** German leagues, goal minutes, no key.
12. **Wyscout/Pappalardo 2017/18.** CC BY 4.0 events, static.
13. **SportMonks free.** Two leagues, 180 calls per hour per endpoint.
14. **TheSportsDB.** Key 123, metadata and basic results.
15. **SkillCorner and Metrica tracking samples.** For research only.

**Flagged or avoid for automated use:** FotMob (explicit ban), FBref (no-spidering rule and Opta data gone), Sofascore, WhoScored, Flashscore, Squawka.
