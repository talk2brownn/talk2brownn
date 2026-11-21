# Free Data Sources for Basketball and Handball Prediction Modelling (as of Nov 2026)

Research method note: this session's network blocked direct fetches of most provider sites (balldontlie.io, api-football.com, sports-reference.com, arxiv.org all failed DNS in the sandbox), so findings are based on web-search extracts of official pages, PyPI/CRAN/GitHub pages and documentation. Anything not confirmed by a cited source is placed under Inferences or Gaps. Before you build on any source, check its live docs and terms yourself.

---

## Q1. Basketball (NBA first): which free sources give quarter/half scores, team totals, pace/possessions, ORtg/DRtg, play-by-play (leads / largest lead), rest days, injuries, lineups and referees?

### Takeaway
The most useful free NBA stack in 2026 is: (1) **hoopR / sportsdataverse bulk play-by-play** (ESPN-sourced, 2002–2026, a free download with no IP blocking) for scores, leads and largest lead; (2) **nba_api / pbpstats** (stats.nba.com) for official box scores, advanced ratings, possessions and lineups, which works from a residential connection but **not from cloud servers**; (3) the **NBA's own injury-report PDFs** and **official.nba.com referee assignments** for injuries and referee crews; (4) the **wyattowalsh Kaggle/nbadb** database as a bootstrap historical archive. balldontlie's free tier is too limited (5 req/min, core endpoints only) for serious modelling. Basketball-Reference has the richest pages but forbids scraping.

### Cited Findings

**Ranked catalogue (basketball)**

1. **hoopR (R) / sportsdataverse-py: ESPN play-by-play and box scores. Rank #1 for free, legally low-risk bulk data**
   - Bulk loader covers "NBA full play-by-play seasons (2002-2026)", loading in about 1–2 minutes via `load_nba_pbp()`. — [hoopR README (CRAN)](https://stat.ethz.ch/CRAN/web/packages/hoopR/readme/README.html)
   - Pulls ESPN live play-by-play and box score data, "with shot locations when available". — [hoopR README](https://stat.ethz.ch/CRAN/web/packages/hoopR/readme/README.html)
   - `load_nba_*()` / `load_mbb_*()` loaders read from the sportsdataverse-data release repos, so you download prebuilt files and do not hit ESPN at all. — [hoopR README](https://stat.ethz.ch/CRAN/web/packages/hoopR/readme/README.html)
   - Version 3.1.0 adds NBA Stats API wrapper functions. Its example `load_nba_pbp` returned 642,472 rows from 1,325 games. — [rdocumentation hoopR 3.1.0](https://www.rdocumentation.org/packages/hoopR/versions/3.1.0); [CRAN index](https://cran.uni-muenster.de/web/packages/hoopR/index.html)
   - Also covers men's college basketball (MBB). — [hoopR CRAN](https://cran.uni-muenster.de/web/packages/hoopR/index.html)

2. **nba_api (Python) to stats.nba.com. Rank #2 (richest official data, but blocked from cloud IPs)**
   - The PyPI docs say stats.nba.com throttles rapid requests and does not respond to many cloud IP ranges (AWS, GCP, Azure, Colab and others). Their suggested fixes are pausing between requests, raising the timeout, or using a proxy (supported through the `NBA_API_PROXY` environment variable). — [nba_api PyPI](https://pypi.org/project/nba-api/)
   - Timeouts have been reported in GitHub issues since at least 2020, e.g. issue #176 "Read timed out". — [swar/nba_api issue #176 mirror](https://github.lx164.workers.dev/swar/nba_api/issues/176)
   - A Hacker News commenter (anecdotal) attributes the failures to Akamai bot protection that rejects requests by TLS fingerprint and silently drops datacenter IPs, and says the "live" endpoints are hosted elsewhere and work from anywhere. — [HN thread](https://news.ycombinator.com/threads?id=gek0z)
   - Running from GitHub Actions also times out. — [StackOverflow archive: nba api timeouts on GitHub workflow](https://kiwix.lema.org/stackoverflow.com_en_all_2023-11/questions/73066785/nba-api-timeouts-when-run-with-github-workflow)

3. **pbpstats (Python): possessions, lineups on floor, enhanced play-by-play from stats.nba.com / data.nba.com**
   - Parses NBA, WNBA and G-League play-by-play. It supports stats.nba.com and data.nba.com endpoints. Latest version seen: 1.3.11. — [libraries.io pbpstats](https://libraries.io/pypi/pbpstats)
   - Version 1.3.4 adds the "lineup on floor for all events". — [pbpstats 1.3.4 PyPI](https://pypi.org/project/pbpstats/1.3.4/)
   - Splits enhanced play-by-play into possessions, with start time, end time, score margin and how the previous possession ended. — [pbpstats docs: possessions](https://pbpstats.readthedocs.io/en/latest/pbpstats.data_loader.stats_nba.possessions.html)
   - The loader raises an error when the same team has the ball on back-to-back possessions, a data-quality check you have to handle. — [pbpstats docs](https://pbpstats.readthedocs.io/en/v1.3.3/pbpstats.data_loader.stats_nba.possessions.html)
   - It depends on the same stats.nba.com access, so the cloud-IP blocking above applies. — [nba_api PyPI](https://pypi.org/project/nba-api/)

4. **wyattowalsh Kaggle "basketball" dataset / nbadb**
   - The `wyattowalsh/nbadb` repo builds and updates the Kaggle NBA Database from stats.nba.com through nba_api. — [github.com/wyattowalsh/nbadb](https://github.com/wyattowalsh/nbadb)
   - Described as updated daily or monthly by cron-scheduled Kaggle Notebooks. — [awesome.ecosyste.ms nbadb](https://awesome.ecosyste.ms/projects/github.com%2Fwyattowalsh%2Fnbadb)
   - A newer README makes DuckDB the primary store, with `nba.sqlite` as a portable export. — [nbadb mirror](https://github.gg22.workers.dev/wyattowalsh/nbadb)
   - The older SQLite version had 16 tables, including `play_by_play`. — [CMSC320 tutorial using wyattowalsh/basketball](https://prathamashar.github.io/NbaAnalysis/CMSC320_Final_Project.html)
   - Related: `shufinskiy/nba_data` (pre-scraped NBA pbp archives) and `mpope9/nba-sql` (builds your own DB, with a refresh mode). — [shufinskiy/nba_data](https://github.com/shufinskiy/nba_data); [mpope9/nba-sql](https://github.com/mpope9/nba-sql)

5. **NBA official injury report PDFs (free, primary source, active Nov 2026)**
   - Published at `ak-static.cms.nba.com/referee/injury/Injury-Report_YYYY-MM-DD_HH_MMAM|PM.pdf`, several times per day. The latest seen is "Injury Report: 11/20/26 09:00 PM". — [NBA injury report PDF 2026-11-20 09:00PM](https://ak-static.cms.nba.com/referee/injury/Injury-Report_2026-11-20_09_00PM.pdf)
   - Fields: game date, game time, matchup, team, player, status (Out / Questionable / Available etc.) and reason. — [Injury report 2026-01-01](https://ak-static.cms.nba.com/referee/injury/Injury-Report_2026-01-01_04_00PM.pdf)

6. **official.nba.com referee assignments (free, primary source)**
   - Assignments are posted at about 9:00 a.m. ET each game day. Each lists the game, crew chief, referee, umpire and alternate. — [NBA Referee Assignments](https://official.nba.com/referee-assignments)
   - The page only shows today's crews. To build referee foul/FT tendencies you have to archive it daily, then join it to box scores (FTA, PF) from nba_api/hoopR. — [NBA Referee Assignments](https://official.nba.com/referee-assignments) (archiving need is an inference, see below)

7. **balldontlie API: free tier too thin for modelling**
   - Free tier: 5 requests per 60 seconds, per sport. All-Star $9.99/mo (60 req/min), GOAT $39.99/mo (600 req/min), All-Access $299.99/mo. — [SourceForge listing](https://sourceforge.net/software/product/BALLDONTLIE/); [balldontlie account API](https://www.balldontlie.io/account/)
   - Free tier covers core endpoints only (teams, players, games). Standings and player stats need $9.99, and odds, props and season stats need $39.99. Source is a competitor's comparison page, so treat as indicative. — [bigballsdata comparison](https://bigballsdata.com/compare/balldontlie-alternative)
   - An API key is now required; the old keyless endpoints are gone. — [publicapis.io balldontlie](https://publicapis.io/balldontlie-api)

8. **API-Sports (API-Basketball): 100 requests/day free, forever**
   - "Free plan available for ever including 100 requests per day for each API", with a reset at 00:00 UTC. — [api-sports.io](https://api-sports.io/); [API-Sports handball page](https://api-sports.io/sports/handball)
   - Paid plans give access to "all endpoints and all competitions". The free plan's competition/season limits are not stated on the page I could see. — [API-Sports handball page](https://api-sports.io/sports/handball)

9. **TheSportsDB: metadata and schedules, weak for stats**
   - Official docs: the free API key is `123`, placed in the URL path. — [TheSportsDB API docs](https://www.thesportsdb.com/docs/api)
   - Free tier is about 30 req/min (HTTP 429 above that). Premium is about $9/mo for 100 req/min. — [sportsapis.dev TheSportsDB](https://sportsapis.dev/apis/thesportsdb); [Teamarr TSDB provider docs](https://pharaoh-labs.github.io/teamarr/reference/providers/tsdb)
   - Free key caps some search results (e.g. team search limited); sources conflict on the details. — [Teamarr](https://www.mintlify.com/Pharaoh-Labs/teamarr/reference/provider-tsdb)

10. **EuroLeague / EuroCup: `euroleague-api` Python package (official EuroLeague API wrapper)**
    - Python wrapper covering EuroLeague (competition code "E") and EuroCup. Modules include `play_by_play_data`, `boxscore_data` and `shot_data` (`ShotData(competition_code).get_game_shot_data(season, game_code)` returns a DataFrame). — [euroleague-api PyPI](https://pypi.org/project/euroleague-api); [v0.0.12](https://pypi.org/project/euroleague-api/0.0.12)
    - Uses endpoints from the EuroLeague swagger platform, plus extra endpoints (e.g. shot data) found in blogs and discussions, so those are less officially supported. — [euroleague-api PyPI 0.0.10](https://pypi.org/project/euroleague-api/0.0.10/)
    - Alternatives: `py-euroleague` (Python, with a live pbp/shot-coordinate client) and `euroleaguer` (R, on CRAN). — [py-euroleague PyPI](https://pypi.org/project/py-euroleague/); [euroleaguer CRAN](https://cran.uni-muenster.de/web/packages/euroleaguer/refman/euroleaguer.html)

11. **Basketball-Reference (Sports Reference): rich but restricted (FLAG)**
    - Bot policy: blocks anyone making more than 20 requests per minute, "regardless of bot type and construction and pages accessed". A block can last up to a day. — [SR bot-traffic page](https://aws.sports-reference.com/bot-traffic.html); [SR blog 2023](https://www.sports-reference.com/blog/category/data/page/4/)
    - The data-use page says spidering violates the site terms. It also says you should not build websites or tools from scraped data, or train generative AI models on it, without permission. — [SR and Data Use](https://www.sports-reference.com/data_use.html)
    - Enforced in practice: scrapers get HTTP 429 errors. — [sportsipy issue #756](https://www.github.com/roclark/sportsipy/issues/756)
    - The site has a 2026-27 season play-by-play page. — [BBRef NBA_2027 pbp](https://www.basketball-reference.com/leagues/NBA_2027_play-by-play.html)

### Inferences
- **Field mapping (NBA):**
  - **Quarter and half scores, team totals:** ESPN data via hoopR includes period-level scoring, and nba_api's `BoxScoreSummaryV2` LineScore gives points per quarter. Half scores = Q1+Q2. (The nba_api endpoint name comes from my prior knowledge, not a source fetched here.)
  - **Pace, possessions, ORtg, DRtg:** nba_api advanced box scores or pbpstats possessions. Or compute them yourself from box scores with the standard formula, Poss ≈ FGA − OREB + TOV + 0.44×FTA.
  - **Leads at any time and largest lead:** take a running score margin over hoopR or pbpstats play-by-play.
  - **Rest days and back-to-backs:** compute from the schedule dates in any games table; no special source is needed.
  - **Starting lineups:** use pbpstats lineup-on-floor, or the starter flags in box scores.
  - **Referee crews:** archive official.nba.com daily, or take officials from nba_api box score summary data.
- **NBA CDN "liveData" JSON:** the HN comment suggests endpoints hosted outside stats.nba.com (commonly `cdn.nba.com/static/json/liveData/...`, which nba_api's `live` module uses) are not cloud-blocked. I could not confirm this with a fetch in this session.
- **Nigeria:** stats.nba.com blocking targets datacenter/cloud IP ranges, not countries (per the nba_api docs). A home connection in Nigeria should generally work; Colab, AWS or a cloud VPS will not. Using a paid residential proxy to get around the block is a grey area under NBA.com terms. The simpler legitimate route is to run nba_api locally and use hoopR bulk files for the cloud.
- **Legal risk ranking (basketball):** lowest risk are the hoopR/sportsdataverse releases, the Kaggle dataset (check its licence), the official injury PDFs and the referee pages (public, low-frequency). Medium risk is nba_api (an unofficial use of NBA.com endpoints; NBA.com terms likely restrict commercial reuse, not verified here). Highest risk is Basketball-Reference scraping, which its data-use page explicitly forbids.
- **Lower leagues and other basketball:** API-Sports (API-Basketball) lists many leagues and is the most practical free multi-league option within 100 req/day. TheSportsDB fills in schedules.

### Gaps
- Could not verify balldontlie's free-tier endpoint list from the official docs, because the site was blocked from this sandbox.
- Could not verify which seasons and leagues API-Basketball's free plan unlocks. Historically the free plan restricted recent seasons; that is not confirmed for 2026.
- NBA.com Terms of Use text not retrieved. Whether stats.nba.com data may be used commercially is unconfirmed.
- The Kaggle licence for wyattowalsh/basketball and its last refresh date in 2026 are not confirmed.
- pbpstats: whether it still works for the 2026-27 season is not confirmed (latest release date unknown).
- No free, ready-made historical referee-tendency dataset was found. You have to build it yourself.

---

## Q2. Handball: free sources for results, half-time scores, team goals, home/away, schedules (Herreligaen, Danish 1. Division men and women, HBL, France, Spain, EHF CL, Japan)

### Takeaway
There is no clean, free, bulk handball dataset. The best legitimate free option is **API-Sports API-Handball (100 requests/day forever)**, but its coverage of the Danish 1. Division (especially women's) must be checked with one `/leagues?country=Denmark` call after signup. For Danish leagues, the federation's own site (**danskhaandbold.dk / hbold.dk**) is the primary source for tables and results. For the EHF Champions League, **official EHF match-report PDFs** carry detailed per-match statistics. For Japan, the league's **League H site (leagueh.jp)** is the official source. Flashscore and Sofascore cover everything but forbid scraping.

### Cited Findings

**Ranked catalogue (handball)**

1. **API-Sports: API-Handball**
   - Free plan: 100 requests per day, reset at 00:00 UTC; unused requests are lost. — [API-Sports handball page](https://api-sports.io/sports/handball)
   - Paid plans: "all endpoints and all competitions". Free-plan competition restrictions are not stated. — [API-Sports handball page](https://api-sports.io/sports/handball)
   - One GitHub project calls `/leagues?country=Denmark` and `/standings` on the free plan for Danish handball, but notes that the response format and free-plan season access are untested. — [GitHub PR: Handball standings from API-Sports](https://github.com/tinerc2-jpg/My-Sports-Hub/pull/6)
   - Some third-party review sites claim "100 calls per month". This contradicts the official per-day figure; trust the official page. — [sportsjobs.online](https://www.sportsjobs.online/blogposts/43)

2. **Dansk Håndbold Forbund official site (danskhaandbold.dk; hbold.dk is the DHF results portal)**
   - Pool standings pages exist at `danskhaandbold.dk/puljer/{id}/stilling`, e.g. one pool with Holstebro Håndbold top on 38 points after 22 matches (season unclear). — [danskhaandbold.dk Pulje 1](https://danskhaandbold.dk/puljer/113843/stilling)
   - 1. Division Kvinder 2026/27 is also tracked by fan and media sites (myhandball.dk, tophaandbold.dk, slutspillet.dk, livesport.com). Their tables disagree on dates, so use the federation as the master source. — [myhandball.dk](https://www.myhandball.dk/1-division-kvinder/); [tophaandbold.dk](https://tophaandbold.dk/stillinger/1-division-kvinder); [livesport.com DK](https://www.livesport.com/dk/handbold/danmark/1-division-kvinder/)

3. **EHF official match reports (Champions League, European League, EURO)**
   - Official EHF match-report PDFs (e.g. Veszprém v Kielce) run 13 pages, with shot breakdowns (goals, saves, misses, posts, blocks), timeouts, officials, punishments and a full event timeline. — [EHF OMS PDF Veszprém v Kielce](https://handballveszprem.hu/_user/file/EHF_OMS_veszprem_kielce.pdf)
   - "Match of the Week" media PDFs include head-to-head records and recent form. — [EHF CLM 2425 MOTW2 Nantes v Kielce](https://ehfec.eurohandball.com/media/aizail3g/clm_2425_motw2_nantes_kielce.pdf)
   - The EHF CL site has all-time statistics pages, updated for the 2026-27 season. — [EHF CL all-time statistics 2026-27](https://ehfcl.eurohandball.com/men/2026-27/history/ehf-champions-league-men-all-time-statistics/)

4. **Academic dataset: German HBL with half-time scores**
   - A 2024 arXiv paper models handball outcomes, including half-time scores, on HBL data for 2017-18 to 2022-23 (1,844 matches). Whether the data is public was not confirmed. — [arXiv 2404.04213](https://arxiv.org/html/2404.04213v1)

5. **Mendeley "Match Score Dataset for Team Ball Sports"**
   - Match scores from major international competitions across 12 team ball sports, handball included. It was scraped from Wikipedia, so it covers international tournaments, not club leagues. — [Mendeley Data](https://data.mendeley.com/datasets/2pt4vmyf27/2); [Lehigh tech report](https://engineering.lehigh.edu/sites/engineering.lehigh.edu/files/_DEPARTMENTS/ise/pdf/tech-papers/24/24T_003.pdf)

6. **TheSportsDB**
   - Has handball league pages (e.g. league 5484). Free key `123`, about 30 req/min. — [TheSportsDB league 5484](https://www.thesportsdb.com/league/5484); [TheSportsDB docs](https://www.thesportsdb.com/docs/api)

7. **Japan Handball League (now "League H")**
   - Wikipedia cites 2025-26 men's and women's league tables on leagueh.jp. Flashscore lists "League H 2026/2027". — [Wikipedia: Japan Handball League](https://en.wikipedia.org/wiki/Japan_Handball_League); [Flashscore League H](https://www.flashscore.de/handball/japan/league-h/)
   - Results also appear on Sofascore, scores24 and Sportradar StatsHub (e.g. Hokkoku Honey Bee 33-33 Kagawa Bank GiraSol, 13 June 2026). — [scores24 Hokkoku Honey Bee](https://scores24.live/en/handball/t-hokkoku-honey-bee); [Sofascore JHL Women](https://sofascore.com/tournament/handball/japan/japan-handball-league-women/19091)

8. **Commercial APIs with half scores (not free, for reference)**
   - Sportradar's handball API includes scores by half plus team and player stats (paid). — [Sportradar handball overview](https://developer.sportradar.com/handball/reference/handball-overview)
   - Highlightly's handball API returns a `firstHalf` score field; its free tier may hide some results. — [Highlightly handball matches docs](https://highlightly.net/handball-api/documentation/matches/)

### Inferences
- For the **Danish 1. Division (men and women)**, API-Sports coverage is uncertain. The reliable fallback is manually or slowly collecting results from the DHF site (danskhaandbold.dk / hbold.dk), which is public federation data. Check the DHF site terms before automating; low-frequency polling of a public federation site is low risk, but that is not verified.
- Half-time scores for HBL, LNH (France), ASOBAL (Spain) and the EHF CL are on the official league and EHF match centres and in EHF PDF reports, but no free bulk download was found. Expect to build your own dataset slowly.
- Home/away and schedules are easiest from API-Sports (free 100/day) or TheSportsDB.

### Gaps
- Could not confirm whether API-Handball's free plan includes the Danish 1. Division Women, or which seasons it unlocks. Needs one live `/leagues?country=Denmark` call.
- No public HBL Spielbericht/handball.net data feed or terms were found. LNH (France) and ASOBAL (Spain) official data access was not researched (no results).
- No Kaggle handball dataset was found in searches.
- The DHF (hbold.dk) terms of use were not retrieved.

---

## Q3. Is there any free source of handball odds history?

### Takeaway
No free, downloadable, legitimately licensed handball odds history was found. OddsPortal and BetExplorer display historical handball odds, but they are web pages with terms that need checking (and likely restrict scraping). OddsPapi has a free API tier, but historical data is a paid add-on.

### Cited Findings
- OddsPortal has archived handball results with historical odds (web only). — [OddsPortal handball results](https://www.oddsportal.com/handball/results/)
- OddsPapi: free tier of 250 requests/month for live and upcoming odds (EHF, Bundesliga, LNH, 70+ bookmakers); historical data is a paid add-on. — [OddsPapi handball odds blog](https://oddspapi.io/blog/?p=2901)
- SportsDataIO sells historical odds for NFL, MLB and NBA, not handball. — [SportsDataIO historical odds](https://sportsdata.io/historical-odds)
- BetExplorer lists handball results, including Japanese teams, and has its own terms of service. — [BetExplorer Ryukyu Corazon results](https://www.betexplorer.com/handball/team/ryukyu-corazon/n7dRImZm/results/); [BetExplorer ToS](https://www.betexplorer.com/terms-of-service.php)
- Third-party paid scrapers (Apify) exist for OddsPortal and Flashscore odds. Using them shifts ToS compliance onto the user. — [Apify oddsportal-scraper](https://apify.com/crawlerbros/oddsportal-scraper.md)

### Inferences
- Legitimate route: start logging odds yourself now from a free live-odds API (OddsPapi free tier) or your own bookmaker's displayed prices. That builds a forward-looking history without scraping.
- football-data.co.uk-style free odds CSVs exist for football but not for handball (not verified for 2026).

### Gaps
- OddsPortal's terms were not retrieved, so its scraping restriction is unverified.
- No academic handball odds dataset was found.

---

## Q4. Legally risky sources (ToS forbid scraping), flagged

### Takeaway
Treat **Flashscore/Livesport**, **Basketball-Reference / Sports Reference**, and likely **Sofascore**, **OddsPortal** and **BetExplorer** as "view only, do not scrape". Flashscore and Sports Reference forbid it explicitly.

### Cited Findings
- **Flashscore:** the terms forbid "embedding, aggregating, scraping or recreating" content without express consent. — [Flashscore terms](https://www.flashscore.com/terms)
- **Flashscore UK:** the terms forbid burdening the server with automated requests, or assisting third parties to do so. — [Flashscore UK terms](https://www.flashscore.co.uk/terms/)
- **Sports Reference:** spidering violates the site terms; no tools or AI training from scraped data without permission; a 20 req/min auto-block. — [SR data use](https://www.sports-reference.com/data_use.html); [SR bot traffic](https://aws.sports-reference.com/bot-traffic.html)
- **Sofascore:** I could only retrieve its privacy/GDPR pages, not its terms. — [Sofascore GDPR & journalism](https://sofascore.com/gdpr-and-journalism)
- **Vendor claim (not legal advice):** an Apify page cites hiQ v. LinkedIn to argue that scraping public data is generally legal, but says users remain responsible for site terms. — [Apify Flashscore scraper](https://apify.com/parsebird/flashscore-scraper)

### Inferences
- Breaking ToS mainly risks IP bans and contract claims, which is most serious for commercial use. For a personal model, the practical risk is blocking. For anything you sell or publish, use licensed or open sources only.
- **stats.nba.com via nba_api** sits in a grey zone: it is widely used and documented, but it is an undocumented NBA.com endpoint, and evading its blocks with proxies raises risk.

### Gaps
- Sofascore and OddsPortal terms were not verified.
- NBA.com terms were not verified.

---

## Q5. Hidden gems

### Takeaway
The strongest under-used free assets are: the **sportsdataverse-data GitHub releases** (pre-built NBA/MBB pbp, no scraping), the **NBA injury-report PDF archive** (timestamped several times daily, so you can reconstruct what was known before tip-off), the **official.nba.com referee assignments**, the **EHF official match-report PDFs** (deep handball stats), **shufinskiy/nba_data** pre-scraped pbp archives, and the **euroleague-api** package.

### Cited Findings
- Bulk-loader release repos for NBA pbp 2002–2026. — [hoopR README](https://stat.ethz.ch/CRAN/web/packages/hoopR/readme/README.html)
- Timestamped injury PDFs, several per day (e.g. 07:00 AM and 09:00 PM on 2026-11-20). — [7AM report](https://ak-static.cms.nba.com/referee/injury/Injury-Report_2026-11-20_07_00AM.pdf); [9PM report](https://ak-static.cms.nba.com/referee/injury/Injury-Report_2026-11-20_09_00PM.pdf)
- Pre-scraped NBA play-by-play archive repo. — [shufinskiy/nba_data](https://github.com/shufinskiy/nba_data)
- EHF match-report PDFs with full event timelines. — [EHF OMS PDF](https://handballveszprem.hu/_user/file/EHF_OMS_veszprem_kielce.pdf)
- Mendeley multi-sport match score dataset (international handball). — [Mendeley Data](https://data.mendeley.com/datasets/2pt4vmyf27/2)

### Inferences
- Timestamped injury PDFs are valuable for leak-free backtesting, because they show the injury status known at each hour before the game.
- The EHF PDFs have a predictable URL pattern but are hosted under random media IDs, so they need to be collected from the match pages.

### Gaps
- Licences for shufinskiy/nba_data and sportsdataverse-data releases were not checked.
- Whether the EHF permits reuse of its PDF statistics was not checked.
