# Evidence-Based Football (Soccer) Betting: Modelling Methods and Market Patterns (as of Nov 2026)

> Research-process note: in this session the fetch tool could not reach sciencedirect.com, researchgate.net, arxiv.org, papers.ssrn.com or ida.felk.cvut.cz (host not allowed by the session's network). Findings below come from search-engine extracts of those pages and from reachable sources; numbers are reported as given in those extracts. Items I know from background knowledge but could not re-verify this session are listed under **Gaps** as "leads to verify", not as cited findings. Worked numbers labelled "(my calculation)" are illustrative arithmetic, not sourced claims.

## 1. Models: which perform best out-of-sample, and how to blend with de-vigged market odds

### Takeaway
Goal-count models in the Maher/Dixon-Coles family (with a low-score correction and exponential time-decay) are the reliable, cheap baseline; rating systems (pi-ratings, Elo-style) and xG/shot-based inputs add information over raw goals, but recent careful tests find that a well-specified Dixon-Coles model adds **zero** incremental information to the Shin-de-vigged *closing* price in a major league (Serie A, 7,220 matches). Practical edge therefore comes from (a) betting before the close, (b) inputs the market under-weights, and (c) less-efficient leagues/markets, not from out-predicting the closing line with goals-only models.

### Cited Findings
**Goal-count model family**
- Dixon & Coles (1997) extended Maher (1982) by adding a dependence parameter (rho) that adjusts the probabilities of the low scores 0-0, 1-0, 0-1, 1-1. The net effect is more low-scoring draws than independent Poisson gives — [dashee87 (Dixon-Coles and time-weighting tutorial)](https://dashee87.github.io/football/python/predicting-football-results-with-statistical-modelling-dixon-coles-and-time-weighting/); [penaltyblog docs: Dixon and Coles](https://docs.pena.lt/y/models/dixon_coles.html)
- Dixon-Coles time-decay: matches are weighted by exp(-xi·t). The original paper used xi = 0.0065 per day (half-life ≈ ln2/0.0065 ≈ 107 days, my calculation). Penaltyblog recommends tuning xi by looping over values and picking the one with the lowest RPS — [dashee87](https://dashee87.github.io/football/python/predicting-football-results-with-statistical-modelling-dixon-coles-and-time-weighting/); [penaltyblog DC tutorial](http://www.pena.lt/y/2021/06/24/predicting-football-results-using-python-and-dixon-and-coles/)
- The optimal decay varies by league and era. A 2026 Serie A study selected xi = 0.002/day (half-life ≈ 347 days), "appreciably slower" than Dixon-Coles' 0.0065 — [Pitcan 2026, arXiv:2608.11505](https://arxiv.org/abs/2608.11505)
- Example fitted values from penaltyblog's docs: rho ≈ -0.079 and home advantage ≈ 0.231 on the log scale (≈ +26% home scoring rate) — [penaltyblog docs: Dixon and Coles](https://docs.pena.lt/y/models/dixon_coles.html)
- Penaltyblog's 2025 comparison covered Poisson, Dixon-Coles, bivariate Poisson, zero-inflated Poisson, negative binomial and Weibull count copula. It reports Dixon-Coles as best (lowest RPS), with tuned time-weighting lowering RPS further — [penaltyblog: "Football Prediction Models: Which Ones Work the Best?" (Mar 2025)](https://pena.lt/y/2025/03/10/which-model-should-you-use-to-predict-football-matches/)
- Penaltyblog's practical advice: use Dixon-Coles if you want something "fast and reliable", try the Bayesian models if you have more compute, and backtest on your own data — [penaltyblog v0.5.1 post](http://pena.lt/y/2022/11/04/penaltyblog-python-package-v5/)
- In another comparison across five leagues, Dixon-Coles came first, then the bivariate Weibull count model, then independent Poisson. This is a search-extract summary; the original paper is not identified — [search summary; see dashee87/opisthokonta context](https://opisthokonta.net/?cat=48)
- The negative binomial is documented as the choice when goal data are overdispersed. Penaltyblog v1.11 (Jun 2026) ships faster Weibull-copula fitting, neutral-venue support and a pretrained xT model — [penaltyblog NB docs](https://docs.pena.lt/y/models/negative_binomial.html); [penaltyblog v1.11.0](https://pena.lt/y/2026/06/09/penaltyblog-1.11.0/)

**Large comparative review**
- Hubáček, Šourek & Železný, "Forty years of score-based soccer match outcome prediction: an experimental review," *IMA Journal of Management Mathematics* (2021/22), DOI 10.1093/imaman/dpab029. It benchmarks statistical models (double Poisson and family), rating systems (Elo-like, pi-ratings) and graph-based models. The search extracts did not give its final RPS ranking — [record](https://nlistsp.inflibnet.ac.in/vufind/Search2Record/10.1093_imaman_dpab029/Description); [MathSport 2019 version](http://ida.felk.cvut.cz/zelezny/pubs/MathSport2019a.pdf); [slides](http://www2.stat-athens.aueb.gr/~jbn/conferences/MathSport_presentations/TRACK%20B/B5%20-%20Prediction%20in%20Football%20(Soccer)/Hubacek%20-%20Score-based%20soccer%20match%20outcome%20modeling.pdf)
- The winning model of the 2017 Soccer Prediction Challenge (Hubáček et al.) used a boosted-tree learner on an ensemble of score-derived features plus simpler rating and statistical models — [Optimal sports betting strategies in practice (arXiv:2107.08827)](https://arxiv.org/pdf/2107.08827); [Berrar et al., Machine Learning 2019](https://link.springer.com/article/10.1007/s10994-018-5741-1)
- A 2021 CTU thesis, summarising that line of work, reports that detailed match statistics help and that classification models suited the task better than Poisson-based models. This is a secondary source — [Vaknin 2021 thesis](https://dspace.cvut.cz/bitstream/handle/10467/95294/F3-DP-2021-Vaknin-Erik-Predicting-Score-Related-Events-in-Soccer.pdf)

**Ratings**
- Constantinou & Fenton (2013), pi-ratings, *JQAS* 9(1):37-50. Their abstract says pi-ratings "outperform considerably" Elo and were profitable over five EPL seasons (2007/08-2011/12) even after the bookmaker margin. A related poster reports +2.87% to +9.48% profit in 2010/11 at discrepancy thresholds of 5% or more, depending on the bookmaker. I found no independent replication of the profit — [pi-ratings paper PDF](http://www.constantinou.info/downloads/papers/pi-ratings.pdf); [JQAS vol 9 issue 1](https://www.degruyterbrill.com/journal/key/jqas/9/1/html); [QMUL poster](https://eecs.qmul.ac.uk/~norman/RIM/posters/ROD_Poster_2012_Constantinou.pdf)
- Constantinou (2022) applied pi-ratings plus Bayesian networks to the **Asian handicap** market (*Journal of Sports Analytics*) — [doi:10.3233/JSA-200588](https://doi.org/10.3233/JSA-200588); [arXiv:2003.09384](https://arxiv.org/pdf/2003.09384)
- The evaluation metric itself is contested: Wheatcroft argues against the RPS as the default score for football forecasts, favouring the ignorance (log) score — [arXiv:1908.08980](https://arxiv.org/pdf/1908.08980)

**xG and process inputs**
- In a game-by-game replication (American Soccer Analysis, 2022), xG had the highest peak correlation with future points per game among the metrics tested, ahead of goal ratio — [ASA Replication Project](https://www.americansocceranalysis.com/home/2022/7/19/the-replication-project-is-xg-the-best-predictor-of-future-results)
- Wilkens (2026, SAGE journal; SSRN 5381388) studied a Bundesliga xG model over 11 seasons. Its forecasts were slightly less well calibrated than market odds but gave "consistent, albeit modest" profit. Profit varied a lot by season and bet type, and was strongest on home wins — [Wilkens 2026](https://journals.sagepub.com/doi/10.1177/22150218261416681); [SSRN](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=5381388)
- A blog test found xG more predictive than goals and better in a value-bet simulation. Not peer-reviewed — [Beat the Bookie blog, 2021](https://beatthebookie.blog/2021/06/07/the-predictive-power-of-xg/)

**Blending with the market (the key 2026 result)**
- Pitcan (Aug 2026, arXiv:2608.11505) studied Serie A, 7,220 matches, 2007/08-2025/26. In a logarithmic opinion pool with the Shin-de-vigged closing price, the fitted weight on Dixon-Coles is **0.000**: log-loss rises monotonically with that weight on both the validation and the test period.
  - The market beat Dixon-Coles on RPS (0.1905 vs 0.1972) in all 7 test seasons.
  - Dixon-Coles was better calibrated (calibration slope 0.995 vs 1.103 for the market) but less sharp.
  - A shots-on-target process model got weight 0.35 against the goals model, so it carries information the goals model lacks, but weight 0.000 against the market.
  - The author attributes part of the gap to team news in the closing price.
  - Preprint, not peer-reviewed.
  - [arXiv:2608.11505](https://arxiv.org/abs/2608.11505); [Pith summary](https://pith.science/paper/2608.11505)
- Hubáček, Šourek & Železný (2019, *IJF* 35(2):783-796) optimised for accuracy **and** for low correlation with bookmaker probabilities, and reported better profit than accuracy-only models. They used CNNs on player-level statistics and portfolio-theory staking. The follow-up Hubáček & Šír (2023, *IJF* 39(2):691-719), "Beating the market with a bad predictive model," proves that the decorrelation objective is desirable — [IJF 2019 PDF](http://ida.felk.cvut.cz/zelezny/pubs/ijf.2019.pdf); [abstract page](https://ida.fel.cvut.cz/papers/hubacek2019exploiting.html); [Hubáček & Šír 2023](https://ideas.repec.org/a/eee/intfor/v39y2023i2p691-719.html)
- A practitioner corners pipeline blends the negative-binomial model mean 50/50 with the market-implied mean taken from the over/under price ladder. This is an example of market-anchored blending — [GitHub football-corners-predictor](https://github.com/Git4AlexD/football-corners-predictor)

### Inferences
- **Recommended stack (inference from the above):**
  1. Dixon-Coles or bivariate-type goals model with a tuned xi, fitted on xG / non-penalty xG and shots-on-target, plus a goals component.
  2. Convert to a scoreline matrix.
  3. Combine with the de-vigged sharp price (Shin or power method) through a log-opinion pool or logistic stacking. Fit the market weight on out-of-sample data; expect it to be high (0.6 to 1.0) in top leagues.
  4. Bet only where the blended price beats the available price by more than a threshold. Judge success by CLV, not short-run P&L.
- In top-5 leagues the closing line is effectively unbeatable by public-data goals models. The value of a model there is speed: getting on early prices before the market converges. In weaker leagues the model's weight should be higher.
- Decorrelation from the bookmaker matters more than raw accuracy. A model that copies the market cannot profit even when it is "accurate".

### Gaps
- Could not extract the final RPS table of the IMA 2021/22 review (site blocked).
- Leads to verify (background knowledge, not re-verified this session):
  - Karlis & Ntzoufras (2003, *JRSS D*) bivariate Poisson with diagonal inflation for draws.
  - Baio & Blangiardo (2010, *J. Applied Statistics*) Bayesian hierarchical model with shrinkage.
  - Hvattum & Arntzen (2010, *IJF*) Elo as covariate.
  - Ley, Van de Wiele & Van Eetvelde (2019, *Statistical Modelling*), where bivariate Poisson with time-decay was best among maximum-likelihood strength models.
  - Boshnakov, Kharrat & McHale (2017, *IJF*) bivariate Weibull count model.
  - Wunderlich & Memmert (2018, *PLOS ONE*) betting-odds rating system.
  - Štrumbelj (2014, *IJF*), where Shin de-vigging beats basic normalisation.

## 2. Market efficiency: favourite-longshot bias, league tiers, CLV, late information

### Takeaway
Big-five-league 1X2 markets are close to efficient. Apparent biases (favourite-longshot, home) are small, time-varying and often no more frequent than chance would produce. The favourite-longshot bias has weakened over time and is mostly exploitable only with **best-price shopping** in a minority of leagues. Closing line value is the best-supported skill metric. Team news is priced into the close. There is essentially **no peer-reviewed evidence on women's-football market efficiency**.

### Cited Findings
- Angelini & De Angelis (2019, *IJF* 35(2):712-721) used odds from 41 bookmakers on 11 European leagues over 11 years. Using the best odds across bookmakers, 7 markets were efficient and 4 showed inefficiencies (favourite-longshot bias type) implying profit opportunities. These are the working-paper counts — [Semantic Scholar](https://www.semanticscholar.org/paper/Efficiency-of-Online-Football-Betting-Markets-Angelini-Angelis/8ee46d12a25901c9a458af60dac19d1f9fb25a91); [SSRN 3070329](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=3070329)
- Winkelmann, Ötting & Deutscher studied 14 seasons of the big-five leagues. Biases "do not persist systematically over time and across leagues". A Monte Carlo test shows the number of inefficient league-seasons "barely exceeds what would be expected in an efficient market" — [SSRN 3672233](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=3672233)
- A 2024 top-5 study (search extract) likewise found pre-match inefficiencies "neither persistent nor systematic across leagues". Another study found markets became more efficient over time, with a significant decrease in the favourite-longshot bias — [search summary of FLB literature incl. IJF 2024 "A tale of two markets"](https://www.sciencedirect.com/science/article/pii/S0169207024000670)
- English data 2002-2006: positive favourite-longshot bias for home and away odds, but a *negative* longshot bias on draw odds (draws underpriced as longshots). Some in-play-based work finds a *reverse* bias (underdogs underpriced pre-match) — [Efficiency in betting markets: English football](https://www.researchgate.net/publication/291191792_Efficiency_in_Betting_Markets_Evidence_From_English_Football); [Angelini, De Angelis & Singleton, in-play efficiency](https://centaur.reading.ac.uk/98329/1/information_efficiency_angelini_de_angelis_singleton.pdf)
- Earlier UK fixed-odds football showed the same favourite-longshot bias as horse racing — [FLB & market efficiency in UK football betting](https://www.academia.edu/5755424/The_Favourite_Longshot_Bias_and_Market_Efficiency_in_UK_Football_Betting)
- Constantinou & Fenton (2013b) confirm favourite-longshot bias in European football and profit by betting favourites. Most favourite-longshot-bias studies in football use small samples; one larger study covers 163,992 odds on 41,003 matches (10 leagues, 12 seasons) — [Radboud thesis review](https://theses.ubn.ru.nl/server/api/core/bitstreams/d22fdc12-9ca7-452c-b87b-5b756e3a0bd8/content)
- Gross & Rebeggiani found the European football betting market "surprisingly close" to the efficiency benchmark — [IJFS 2014](https://ideas.repec.org/a/gam/jijfss/v2y2014i2p193-202d35451.html)
- **Shock-driven mispricing:** bookmakers mispriced the vanished home advantage in the Bundesliga after the COVID-19 break — [Winkelmann, Deutscher & Ötting, arXiv:2008.05417](https://arxiv.org/pdf/2008.05417); [COVID-19 & betting markets, arXiv:2109.07581](https://arxiv.org/pdf/2109.07581)
- **Using bookmakers' own consensus:** Kaunitz, Zhong & Kreiner (2017) bet when a soft book's odds deviated from the consensus-implied probability. They report sustained profits, but bookmakers "began to severely limit our accounts" — [arXiv:1710.02824](https://arxiv.org/pdf/1710.02824)
- **Closing line value:** Buchdahl's analysis of about 87,960 Pinnacle football price pairs found a near one-to-one relationship between the ratio of an earlier price to the no-vig closing price and long-run yield. With a 5% edge, CLV can show a significant signal in about 50 bets, while confirming profit takes several thousand. Buchdahl notes some profitable bettors do not beat the close. These figures come via secondary summaries — [Pinnacle Odds Dropper: Buchdahl on CLV](https://www.pinnacleoddsdropper.com/blog/closing-line-value--clv-demystified-by-expert-joseph-buchdahl); [Buchdahl strategy summary](https://www.pinnacleoddsdropper.com/blog/joseph-buchdahl's-betting-strategy); [Pinnacle: market efficiency](https://www.pinnacle.com/betting-resources/en/educational/how-to-solve-a-problem-like-efficiency-part-one/rn8j5rnqj2p8t68p)
- A counter-example to CLV as the only measure: a tennis tipster made 8.9% ROI over 3,000 bets against an expected -0.2% from closing prices — [Sports Trading Network](https://www.sportstradingnetwork.com/article/do-pinnacle-closing-prices-in-tennis-tell-the-full-story-can-you-win-in-the-long-run-without-beating-them/)
- **Late information:**
  - On Pinnacle, opening-to-closing odds changes are significantly correlated with results for all outcomes, and strategies that profit at opening odds are "significantly less profitable" at final odds (CBS master's thesis). So the close absorbs information, including team news — [CBS thesis](https://research-api.cbs.dk/ws/portalfiles/portal/60750333/237159_final_digital.pdf)
  - The Pitcan (2026) Serie A study attributes the market's edge partly to team news the model never sees — [arXiv:2608.11505](https://arxiv.org/abs/2608.11505)
- **In-play:**
  - Bundesliga high-frequency data were used to test whether odds move before goals — [arXiv:2505.21275](https://arxiv.org/pdf/2505.21275)
  - Live prices generally underreact to ordinary news and overreact to surprising news — [Reading EMDP 2019-20](https://www.reading.ac.uk/web/files/economics/emdp201920.pdf)
  - Earlier: goal arrival and efficiency in soccer betting — [Information and Efficiency: Goal Arrival](https://www.researchgate.net/publication/228338838_Information_and_Efficiency_Goal_Arrival_in_Soccer_Betting)
- **Women's football:** no efficiency study was found. Betting on women's football grew at about 20% CAGR from 2017 to 2022 (German Sport University Cologne / IBIA) — [IMGL magazine](https://www.imgl.org/publications/imgl-magazine-volume-3-no-1/betting-on-womens-sports-realizing-the-untapped-potential/)

### Inferences
- **Where to look for edge, in order of evidence strength:**
  1. Lower-liquidity leagues and markets where the favourite-longshot bias or other bias persists against *best available* odds.
  2. Regime shifts the market adapts to slowly (COVID home advantage is the canonical case).
  3. Soft books that lag the sharp consensus (Kaunitz et al.), which is self-limiting because of account restrictions.
- **The "back heavy favourites" rule** is supported in some leagues and periods but is not persistent. Treat it as a hypothesis to re-test each season, not a rule.
- **Women's leagues and lower divisions:** by analogy with the less-efficient leagues in Angelini & De Angelis, thinner markets with lower limits are *likely* less efficient. This is untested for women's football, and limits there are low.
- **Team news timing:** a pre-lineup model must either forecast lineups or bet only after lineups, about 60 to 75 minutes before kick-off, when soft books may lag the sharp move. The second point is a hypothesis.

### Gaps
- No direct peer-reviewed test of the favourite-longshot bias in football **totals** (O/U 2.5) was found.
- Could not retrieve the 2024 *IJF* "tale of two markets" findings (blocked).
- No women's-football efficiency study found.
- No rigorous starting-XI announcement event study for football found.
- Leads to verify: Cain, Law & Peel (2000, *Scottish J. Political Economy*), favourite-longshot bias in correct-score betting; Direr (2013, *Applied Economics*), heavy-favourite profitability; Forrest, Goddard & Simmons (2005, *IJF*), odds-setters as forecasters.

## 3. Deriving market prices from a scoreline matrix, and in-play / path-dependent markets

### Takeaway
Any full-time goals market is a sum over the joint scoreline matrix P(h, a). Half-based markets need separate half intensities: the second half carries about 55-56% of goals. Path-dependent markets (lead by X at any time, N goals in a row, next goal) need a time-inhomogeneous, score-state-dependent goal process simulated minute by minute.

### Cited Findings
- Penaltyblog models return a probability grid from which 1X2, totals, BTTS, Asian handicaps and correct scores are derived — [penaltyblog Poisson docs](https://docs.pena.lt/y/models/poisson.html); [penaltyblog DC docs](https://docs.pena.lt/y/models/dixon_coles.html)
- **Second half scores more:**
  - About 10,885 goals in 4,560 matches across the EPL, Ligue 1, Serie A and La Liga (2008-11): 55.1% in the second half vs 44.9% in the first (p < 0.001), with the highest rate in the final 15 minutes — [Springer, Sport Sciences for Health 2013](https://link.springer.com/article/10.1007/s11332-013-0154-9)
  - English top 4 divisions 2016/17-2020/21: 55.7% second half (Championship 56.6%) — [sportsbettingtrends](https://www.sportsbettingtrends.co.uk/football/first-v-second-half-goals/)
  - Caley: about 56% second half since 2005/06, range 54% (21/22) to 58% (18/19), with no long-run trend — [Expecting Goals, "The Game of Two Halves"](https://www.expectinggoals.com/p/the-game-of-two-halves)
  - 2025/26, 24 leagues, 7,174 matches: 1H mean 1.18 goals, 2H mean 1.47 (55.4%), and the second half higher in every league. This is a betting site, not peer-reviewed — [freebetoffers](https://www.freebetoffers.org.uk/average-first-half-vs-second-half-goals-in-major-football/)
- **Game-state effects:**
  - Dixon & Robinson (1998, *The Statistician* 47:523-538): a bivariate non-homogeneous Poisson birth process in which home and away scoring rates depend on the current score and on time.
  - Secondary sources report that a one-goal lead lowers the leader's scoring rate and raises the trailer's (a "comeback" effect), reversing at a three-goal lead. Trailing teams have elevated second-half scoring (Silva & Swartz 2016).
  - [arXiv:2611.15378 (modified Glicko, 2026)](https://arxiv.org/pdf/2611.15378); [market-initialised AFT in-play model, arXiv:2605.16066](https://arxiv.org/pdf/2605.16066); [effect of first goal on second, arXiv:1207.6796](https://arxiv.org/pdf/1207.6796)
- Market-initialised in-play models (2026) start goal intensities from pre-match market prices and then update. Bayesian in-play models exist for live outcome probabilities — [arXiv:2605.16066](https://arxiv.org/pdf/2605.16066); [Applied Sciences 2020, Bayesian in-play model](https://www.mdpi.com/2076-3417/10/8/2904)
- Stochastic match-simulation framework — [arXiv:2312.04338](https://arxiv.org/pdf/2312.04338)

### Inferences (formulas and worked example; my calculations)
**Recipe** for a matrix M[h, a] (h, a = 0..10), renormalised after the Dixon-Coles tau adjustment:
- 1X2: sum over h > a, h = a, h < a.
- Double Chance = 1 - P(the excluded outcome).
- Team total O/U k: sum over the marginal of h (or a).
- Match O/U k.5: sum over h + a > k.
- BTTS: sum over h ≥ 1 and a ≥ 1.
- Win to nil (home): h > a and a = 0.
- "A or B" (e.g. Home or Over 2.5) = P(A) + P(B) - P(A and B), computed as **one** sum over the union region, never from the marginals.
- Combos such as Home & Over 2.5: sum over the intersection region.
- Asian handicaps: sum over goal-difference regions; quarter lines split stake across adjacent lines, and pushes are refunded.

**Worked example** (λH = 1.6, λA = 1.1, rho = -0.08):

| Market | Probability |
|---|---|
| Home | 0.480 |
| Draw | 0.268 |
| Away | 0.252 |
| Over 2.5 | 0.506 |
| BTTS | 0.542 |
| Home or Over 2.5 | 0.690 |
| Home & Over 2.5 | 0.296 |
| Home win to nil | 0.256 |

Home & Over 2.5 = 0.296 is much larger than the naive P(H) × P(O2.5) = 0.243. That gap is why correlated same-game legs must be priced from the joint matrix.

**Half markets:** model each half as its own Poisson with team rates scaled by about 0.45 and 0.55 (fit by league). Using the league-average half means 1.18 and 1.47 as independent Poisson:

| Market | Probability |
|---|---|
| Highest-scoring half: 2nd | about 0.438 |
| Highest-scoring half: 1st | about 0.304 |
| Highest-scoring half: tie | about 0.258 |
| Both halves Over 0.5 | about 0.533 |
| Both halves Under 1.5 | about 0.380 |

HT/FT needs the joint distribution of the half-time score and the second-half increment. Independent half Poissons are a reasonable first pass. Add game-state adjustments for the second half.

**Path-dependent markets** (lead by 2 at any time, team to score 3 in a row, next goal, comeback): simulate with Monte Carlo at minute resolution.
- Intensity: λ_team(t) = base_rate × time_profile(t) × state_multiplier(score difference, time) × red-card multiplier.
- time_profile(t) rises across the match, peaks in the final 15 minutes, and includes stoppage-time mass at 45+ and 90+.
- State multipliers come from Dixon-Robinson-type fits: the trailing team's rate goes up, the leading team's goes down.
- Calibrate so that simulated full-time marginals match the pre-match scoreline model and the market's O/U line.
- Ignoring game-state effects overstates the probability of "lead by 2+" and of streak markets for favourites, because a leading favourite eases off.

### Gaps
- No peer-reviewed estimates were retrieved for exact score-state multipliers or a minute-level intensity curve with stoppage-time mass. The Dixon-Robinson parameter values were not accessible.
- No market-efficiency studies found for "highest-scoring half", HT/FT or "lead by X" markets.

## 4. Prop markets: corners, cards, fouls, shots, throw-ins, goal kicks, tackles

### Takeaway
Match-stat counts are overdispersed. Negative binomial (or compound / geometric Poisson, or a negative-binomial GAM) beats Poisson. Predictors are team style rates (for and against), expected dominance taken from match odds, and the referee for cards and fouls. Academic evidence of systematic bookmaker mispricing in props is thin: one corner study shows simulated profit but cannot beat the bookmaker on RPS. Most "referee edge" claims come from vendor blogs.

### Cited Findings
- **Corners, Yip et al. (arXiv:2112.13001, c. 2021-22):** compared naive Poisson, negative binomial and geometric-Poisson. The best model, a negative binomial with a match-varying shape, gave the highest simulated betting profit (about 5.8%, Sharpe 3.07), but could **not** beat the bookmaker on RPS — [arXiv:2112.13001](https://arxiv.org/pdf/2112.13001); [v3 html](https://arxiv.org/html/2112.13001v3)
- A Lund master's thesis uses negative binomial regression for total corners because of overdispersion, and tests efficiency of the O/U corners market — [LUP 9127007](https://lup.lub.lu.se/student-papers/search/publication/9127007)
- Minute-by-minute event data (arXiv 2508.04008, 2025): for corners and shot attempts, a negative binomial GAM with smoothing splines beat zero-inflated Poisson — [arXiv:2508.04008](https://arxiv.org/pdf/2508.04008)
- **Cards / referee:** Buraimo, Forrest & Simmons ("The Twelfth Man? Refereeing bias in English and German soccer"):
  - Pre-match odds predict cards: the stronger home favourite gets fewer yellows and the underdog more.
  - Referee bias favours home teams.
  - They note the market moved strongly toward efficiency after the UK betting-tax abolition in 2001.
  - [Holy Cross RePEc PDF](https://college.holycross.edu/hcs/RePEc/spe/BuraimoForrestSimmons_Refereeing.pdf)
- Vendor (non-peer-reviewed) referee spreads, EPL 2025/26: 2.74 to 4.68 yellows per game, and 30.0 to 49.8 booking points per game across regular referees. Blogs claim soft books price at league-average referee rates while sharp books adjust. Unverified — [statpair cards](https://statpair.com/blog/betting-cards-yellow-red-statistical-analysis); [statpair booking points](https://statpair.com/blog/booking-points-betting-card-points-system); [kiqiq referee markets](https://kiqiq.com/blog/how-referees-affect-card-markets)
- Booking-points conventions differ: UK standard is yellow = 10, red = 25, but some books use 1/2. Check the rules, including whether a second yellow counts as 10 + 25 or 25 only — [statpair booking points](https://statpair.com/blog/booking-points-betting-card-points-system); [betmana glossary](https://betmana.co.uk/glossary/referee-stats/)
- Practical pipeline: corner negative-binomial GLM with league fixed effects, blended 50/50 with the market-implied mean, evaluated against closing lines — [GitHub football-corners-predictor](https://github.com/Git4AlexD/football-corners-predictor)

### Inferences
**Per-stat recipe:** E[X] = exp(league intercept + team-for rate + opponent-against rate + home + f(expected dominance from 1X2 or handicap odds) + referee effect for cards/fouls + derby/importance). Use the negative binomial with dispersion fitted per stat and league. Price O/U from the negative binomial CDF; split team corners with a bivariate or copula model.

**Notes per stat:**
- **Corners:** favourites take more corners. Trailing teams take more corners late, so the game-state effect again favours in-play simulation.
- **Cards:** use the referee random effect with shrinkage. Underdogs and away teams get more cards (Buraimo et al.). Derbies and high-stakes matches raise counts.
- **Fouls / tackles:** the possession share of the opponent drives your defensive actions. The team with less of the ball makes more tackles and fouls.
- **Throw-ins, goal kicks:** these depend on pitch dimensions, style (direct vs possession) and the opponent's shot volume (goal kicks come after off-target shots).

**Edge thesis:** soft-book props are priced with high margins (Section 5), so even a good model needs a large edge. Shrinkage toward the market mean, plus line-shopping, is essential.

### Gaps
- No peer-reviewed evidence found on bookmaker efficiency for cards, fouls, shots, throw-ins, goal kicks or tackles markets.
- The "14% of card variance explained by referee" claim seen on a blog had no traceable source, so it is excluded.
- Lead to verify: Wheatcroft (2020/21) "GAP ratings" papers, *J. Sports Analytics* and *IJF* "A profitable model for predicting the over/under market in football", which forecast match statistics (shots, corners) and O/U 2.5 profitably across many leagues. I could not access them this session.

## 5. Bookmaker margins by market type; accumulators; correlated same-game legs

### Takeaway
Margins rise from sharp main lines (about 2-3%) to soft-book main lines (about 5-8%) to props and bet-builders (double digits). In accumulators the margin compounds multiplicatively. Bet builders / same-game parlays add a correlation markup. Industry data show same-game-parlay hold rising from 13.1% to 18.5% (2019 to 2023).

### Cited Findings
- Same-game parlay share of stakes rose from 19.2% (2019) to 24.3% (2023), and same-game parlay margins rose from 13.1% to 18.5% (Flutter, citing Deutsche Bank) — [iGamingNews: SGP margin engine](https://www.igamingnews.biz/same-game-parlay-sportsbook-margin-engine/)
- Compounding: a single -110 bet carries about 4.5% margin, a 3-leg parlay about 13%, a 4-leg about 17%. This is consistent with 1 - 0.955^n for independent legs. A claim of over 40% for 8 legs is overstated; the formula gives about 31% — [thebettingstrategy](https://thebettingstrategy.com/are-parlay-bets-worth-it/); [Wikipedia: Parlay](https://en.wikipedia.org/wiki/Parlay)
- Same-game parlays carry higher built-in hold than singles or standard parlays because correlation pricing gives books room to shade. Estimates range from about 15-20% at 5 legs to claims above 20-30% (UNLV attribution unverified) — [Pinnacle Odds Dropper: SGP guide](https://www.pinnacleoddsdropper.com/blog/same-game-parlay); [rg.org](https://rg.org/news/gambling-industry/why-same-game-parlays-sportsbook-gold-mine)

### Inferences (my calculations)
Effective accumulator margin = 1 - (1/(1+m))^n for per-leg overround m:

| Per-leg overround m | 1 leg | 2 legs | 3 legs | 4 legs | 5 legs | 8 legs | 10 legs |
|---|---|---|---|---|---|---|---|
| 2% (sharp) | 2.0% | 3.9% | 5.8% | 7.6% | 9.4% | 14.7% | 18.0% |
| 5% (soft) | 4.8% | 9.3% | 13.6% | 17.7% | 21.6% | 32.3% | 38.6% |
| 7% (props) | 6.5% | 12.7% | 18.4% | 23.7% | 28.7% | 41.8% | 49.2% |

- **Positive-correlation legs:** in the Section 3 example, Home & Over 2.5 is 0.296 against an independence product of 0.243, so the fair price is 3.38 rather than 4.12.
  - If a book multiplies leg prices (some acca engines do this; bet-builders usually do not), positively correlated legs are *underpriced* relative to the fair joint price. That is the classic correlated-parlay edge.
  - Bet-builders explicitly price correlation, then add the markup above.
- **Only accumulate legs that each carry a positive expected edge.** EV multiplies: (1+e1)(1+e2)... Variance and limits rise fast.

### Gaps
- No academic, football-specific survey of margins by market type was found (main line vs corners vs cards vs player props) with sample sizes.
- Pinnacle-type main-line margins (about 2-3%) are widely cited but were not retrieved with a primary source this session.

## 6. What does NOT work

### Takeaway
Form streaks, "due" results (gambler's fallacy), staking systems such as martingale, and unverified tipster records are not supported. If anything, markets *overreact* to form, so a contrarian lean has modest evidence. Profit claims without CLV evidence or out-of-sample testing should be discounted.

### Cited Findings
- **Overreaction to form:** Wheatcroft (2020, *JQAS*) finds soccer match odds overreact to favourable and unfavourable runs of form, where form is measured relative to expectations implied by odds. Betting against the overreaction is profitable in his tests — [JQAS doi:10.1515/jqas-2019-0009](https://www.degruyterbrill.com/document/doi/10.1515/jqas-2019-0009/html?lang=en); [LSE Research Online PDF](https://researchonline.lse.ac.uk/id/eprint/115490/1/10.1515_jqas_2019_0009.pdf)
- **Bettors chase streaks:** a Czech 2018-2023 study shows bettors disproportionately back teams on winning streaks. NFL work finds that betting against streaks did not yield excess returns in an efficient market — [Charles University thesis](https://dspace.cuni.cz/bitstream/handle/20.500.11956/190557/130387538.pdf?sequence=1&isAllowed=y); [Testing contrarian strategies in the NFL](https://www.researchgate.net/publication/227574371_Testing_Contrarian_Strategies_in_the_National_Football_League); [Moskowitz, Asset Pricing and Sports Betting](https://w4.stern.nyu.edu/finance/docs/pdfs/Seminars/moskowitz_seminar_paper.pdf)
- **Bettor losses:** heavier and more complex betting (e.g. accumulators) is associated with larger losses — [Newall et al. 2018, "Why do some soccer bettors lose more money than others?"](https://wrap.warwick.ac.uk/id/eprint/101329/1/WRAP-why-some-soccer-bettors-lose-money-than-others-Newall-2018.pdf)
- **Staking:** an experimental review of Kelly, fractional Kelly and risk-constrained staking (Hubáček & Šír) shows full Kelly is too aggressive under model uncertainty. Fractional or risk-constrained Kelly is the practical choice — [arXiv:2107.08827](https://arxiv.org/pdf/2107.08827)
- **Profitable but limited:** even a demonstrably profitable consensus-deviation strategy got accounts restricted (Kaunitz et al.), so soft-book edges are capacity-limited — [arXiv:1710.02824](https://arxiv.org/pdf/1710.02824)
- **Betting returns are a noisy accuracy measure:** P&L needs thousands of bets to confirm a 5% edge, whereas CLV converges faster — [Buchdahl via Pinnacle Odds Dropper](https://www.pinnacleoddsdropper.com/blog/closing-line-value--clv-demystified-by-expert-joseph-buchdahl)

### Inferences
- **Martingale and other progression staking** cannot turn a negative-EV bet positive. With a 5% margin every bet loses 5% on average regardless of sizing, and martingale only adds ruin risk, especially against stake limits. This is standard probability; no football-specific paper was retrieved.
- **Pure form streaks and "team is due":** goals are close to independent across matches once strength is controlled. Since odds already overreact to form, backing hot teams is the wrong side of the documented bias.
- **Tipster records:** require a verified, timestamped record with CLV against a sharp close over 500 or more bets. Selection and survivorship bias dominate public tipster leaderboards.

### Gaps
- No peer-reviewed football-specific tipster-performance study was retrieved this session.
- Lead to verify: Buchdahl, *Squares & Sharps, Suckers & Sharks* (2016), and his Pinnacle articles on tipster significance testing (t-test / p-value on yields).
- Wunderlich & Memmert (2020, *IJF*), "Are betting returns a useful measure of accuracy in (sports) forecasting?", is a lead to verify.
