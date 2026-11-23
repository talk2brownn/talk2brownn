# Basketball (NBA first) and Handball Modelling, Accumulator Maths, Staking and Skill Measurement (as of Nov 2026)

Research method note: done with web search only. arxiv.org and web.williams.edu could not be fetched from this session (network allowlist), so arXiv papers and Thorp's PDF are cited from search-result abstracts and summaries, not full texts. Many quantitative "betting" figures on the web come from affiliate/tipster blogs with no stated method. They are labelled **[blog]** below and should be treated as hypotheses, not evidence.

## Basketball: modelling totals, halves/quarters, margins, situational factors, and market efficiency

### Takeaway
Standard practice is to model the margin as roughly normal around the closing spread, with an SD of about 11.6–12 points (Stern's figure as relayed by Gelman; Winston). Expected points are pace × efficiency. The first half takes about 50% of the full-game total and Q1 about 25%. Peer-reviewed tests mostly find NBA sides and totals close to efficient. The one repeated anomaly is an early-season totals bias, toward unders in week one in one study. Home advantage has shrunk to about 54–57% home wins and about 1.6–3 points. Rest is worth about 1.3–2.3 points of margin.

### Cited Findings
**Margin and total distributions**
- Hal Stern's estimate of the SD of NBA score differentials around the point spread is 11.6 points, relayed second-hand by Andrew Gelman's statistics blog. The blog's author calls normality "an approximation." — [Statistical Modeling, Causal Inference (Columbia)](https://statmodeling.stat.columbia.edu/2016/10/28/warriors-suck-bayesian-exploration/)
- Wayne Winston (author of *Mathletics*) explains why the SD of NBA scores about the spread is about 12 points, building it up from the variability of field-goal outcomes. — [mathletics / Wayne Winston](https://waynewinston.com/wordpress/p_2333/)
- For comparison: Stern's 1991 NFL model uses a normal margin around the spread with SD 13.86. A later NFL study found 13.588. College basketball shows an overall SD of about 10.3. — [arXiv 2212.08116 summary](https://arxiv.org/pdf/2212.08116); [arXiv 1211.4000](https://arxiv.org/pdf/1211.4000); [The Only Colors](https://www.theonlycolors.com/2020/4/27/21226073/the-variance-of-college-basketball-how-big-is-it-and-where-does-it-come-from)

**Half and quarter shares of the total**
- One public NBA simulator measured the 2025-26 first-half share of total points at 50.0–50.3%. After calibration, its predicted share moved from 49.5% to 50.0%. — [andrewjohncorey1/nba-sim-data (GitHub)](https://github.com/andrewjohncorey1/nba-sim-data) **[hobbyist, low credibility]**
- One hobbyist repository checked 2,427 games from 2024-25 and 2025-26. It found 1st-half total ≈ 0.502 × full-game line (SD 11.9) and 1st-quarter total ≈ 0.253 × line (SD 8.1). The same repo's searches found no team-specific Q1/H1 share "edge" that cleared a 95% interval against the market. — [MJACode/betting-model PR #1206](https://github.com/MJACode/betting-model/pull/1206); [PR #1024](https://github.com/MJACode/betting-model/pull/1024) **[hobbyist; not peer-reviewed]**
- One blog gives quarter shares of roughly Q1 26–27%, Q2 24–25%, Q3 25–26% and Q4 22–24%. It also says books price first halves near a 50/50 split. The Q4 figure looks inconsistent with a ~50% first-half share and a fourth quarter that includes late fouling, so this is unverified. — [nbabettingsystem.com](https://nbabettingsystem.com/articles/nba-first-quarter-and-first-half-betting/) **[blog]**

**Totals-market efficiency and over/under bias**
- Paul, Weinbach & Wilson (*Quarterly Review of Economics and Finance* 44(4), 2004) studied NBA totals from 1995-96 to 2001-02. On high totals the under returned significantly more than the over, consistent with overs being over-bet. Betting unders was still not profitable enough to beat the vig in general. — [IDEAS/RePEc](https://ideas.repec.org/a/eee/quaeco/v44y2004i4p624-632.html)
- Compton & Sigler applied likelihood-ratio tests to 2000-01 to 2007-08. They found NBA spreads and totals efficient. — summarised in [The Sport Journal, "NBA Gambling Inefficiencies: A Second Look"](https://thesportjournal.org/article/nba-gambling-inefficiencies-a-second-look/)
- Early-season bias: totals lines are significantly biased in the early weeks of the season. In 2009–2012, 58.2% of first-week games finished under the total. After the opening weeks the market was "generally very efficient." — [Early Season NBA Over/Under Bias, J. Prediction Markets (UWF)](https://ircommons.uwf.edu/esploro/outputs/journalArticle/Early-season-NBA-overunder-bias/99380090347306600); [ubplj.org](https://www.ubplj.org/index.php/jpm/article/view/601); see also [Finance Research Letters, "Learning, price formation and the early season bias in the NBA"](https://www.sciencedirect.com/science/article/abs/pii/S1544612307000177)
- Over 12 seasons, 48.7% of NBA games went over the closing total and 50.0% went under (the rest were pushes). The author reads this as close to efficient. — [Sports Trading Network](https://www.sportstradingnetwork.com/article/is-there-bias-in-the-nba-total-points-betting-market/)
- A blog says betting against early-season totals hit 56.72%. — [nbabettingsystem.com](https://nbabettingsystem.com/articles/nba-betting-market-efficiency/) **[blog; method unstated]**

**Home advantage decline**
- Reported 2024-25 home win rates are about 54.3% (one source) or about 54% (another), against roughly 58–60% historically and about 60% in 2000–2013. One source gives an average 2024-25 home margin of just 1.62 points. Another says 2025-26 regular season home win% is about 56–58%, worth about 2.5–3.0 points. The cited mechanisms are fewer home free throws (≈1.0 pt), 3-point shooting travelling well, and better travel and load management. — [sparkletechnologies analysis](https://sparkletechnologies.com/blog/nba-disappearing-home-court-advantage); [basketballbetstrategi.com](https://basketballbetstrategi.com/articles/home-court-advantage-nba-betting/); [olympus-bets](https://app.olympus-bets.com/guides/home-court-advantage) **[blogs; figures conflict, 54% vs 57%]**
- In the 1999-2000 season, home-court advantage was 3.62 points. — [Entine & Small, "The Role of Rest in the NBA Home-Court Advantage" (Wharton)](https://faculty.wharton.upenn.edu/wp-content/uploads/2012/04/Nba.pdf)

**Rest, back-to-backs, travel**
- Entine & Small estimate that 3+ days of rest vs a back-to-back is worth 2.26 points (1999-2000 data). Another study (2004–06) found 3+ rest days improve margin by up to 1.77 points per game. — [Wharton PDF](https://faculty.wharton.upenn.edu/wp-content/uploads/2012/04/Nba.pdf); [NESSIS 2007](https://www.nessis.org/nessis07/Dylan_Small.pdf)
- A more recent analysis estimates +1.33 points of margin per extra rest day (SE 0.44, t=3.01). — [NBAAnalytic "The Rest Ledger"](https://nbaanalytic.com/articles/the-rest-ledger.html)
- A peer-reviewed study (PMC) found that match location mattered after 1–2 days of rest but not for back-to-backs. — [PMC7925613](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC7925613/)
- Teams averaged 14.9 back-to-back sets each in 2024-25, fewer than in earlier eras, which shrinks the aggregate effect. A blog claims a back-to-back defence concedes +1.5–2.5 pts/100 possessions. — [nbabettingstrategy.com](https://nbabettingstrategy.com/articles/nba-game-context-analysis/) **[blog]**

**Referees**
- The only source found claims a 1–3 point totals adjustment by referee crew, with no sample size or out-of-sample test given. — [nbabettingsystem.com referee article](https://nbabettingsystem.com/articles/nba-referee-tendencies-and-betting/) **[blog; anecdotal]**

**Largest lead / comebacks / in-game win probability**
- Inpredictable (Mike Beuoy) publishes play-by-play win-probability models used by ESPN and The Pudding. — [ESPN "No lead is safe"](https://africa.espn.com/nba/story/_/id/39698420/no-lead-safe-nba-big-comebacks-blown-leads); [The Pudding 2017](https://pudding.cool/2017/03/comeback)
- A play-by-play dashboard splits 1996-97 to 2016-17 from 2017-18 to 2024-25. Win probability for a team down 20 rose from about 2.9% to about 5.3% ("20 is the new 18"). The model ignores team strength and home court. — [nba-comeback-dashboard](https://nba-comeback-dashboard.github.io/analysis/20_is_new_18.html)
- ESPN's "20 is the old 12" makes the same point: in the 3-point era, leads are less safe than historical models imply. — [ESPN](https://www.espn.com.au/nba/story/_/id/39698420/no-lead-safe-nba-big-comebacks-blown-leads)

### Inferences
- **Core model:** expected total ≈ (pace_A + pace_B)/2 adjusted × (ORtg_A vs DRtg_B + ORtg_B vs DRtg_A)/100. Then map to probabilities with Normal(μ = projection, σ). Use σ_margin ≈ 12. A σ for totals was not found in a credible source and needs to be estimated from your own data; hobbyist data suggests σ ≈ 12 for 1H totals and ≈ 8 for Q1. Under a normal model, P(cover by k points off the line) = Φ(k/12), so each point of disagreement with the line is worth about 3.3% win probability near the centre. A 2-point model edge on a spread therefore takes about 56.6% win probability vs 52.4% breakeven at −110.
- **Period lines:** use 1H ≈ 0.50 × full total and Q1 ≈ 0.25 × full total as baselines. The evidence found does not support team-specific quarter-share edges.
- **Alternate lines / "lead by X at any time":** these need simulation of the scoring path (possession-level Monte Carlo or Inpredictable-style models), not end-of-game distributions. A "lead at any time" event is always at least as likely as "win by X at the end." Market prices for these props are not covered by any credible public study.
- **"Incl. overtime" totals:** OT adds about 5 minutes (≈ +10–12% of regulation scoring for both teams combined, ≈ 20–25 points). Pushes cluster near a tie, which raises P(over) on totals lines set from regulation-only expectations by roughly P(OT) × P(the extra points push it over). With P(OT) ≈ 5–6% (unverified, see Gaps), the effect is about 3–6 points of "expected total" spread across only those games. That matters for alternate high totals and spreads near zero.
- **Rest:** a back-to-back vs 3+ days of rest is worth about 1.5–2.3 points of margin in older studies. Assume the market prices this in. Edge, if any, would come only from late-breaking rest or injury news.

### Gaps
- No credible source found for league-wide NBA overtime frequency in recent seasons (the commonly quoted ~6% is unverified here; StatMuse gives only team counts, e.g. CHI had 11 OT games in 2023-24).
- No peer-reviewed post-2012 test of NBA totals efficiency, or of first-half/quarter market efficiency, was found.
- No credible quantification of star-absence effects on totals, garbage-time effects, or intentional-foul effects on final totals.
- Pinnacle's period-market methodology was not found. Hobbyist sources conflict on whether Pinnacle prices Q1/H1 team totals at all.
- No credible σ for NBA full-game totals. EuroLeague-specific data (pace ~72 possessions, 40-minute games) was not found.

## Handball: scoring distributions, home advantage, draws, half-time patterns, rating models, market efficiency

### Takeaway
Team goals in handball are better modelled as binomial (under-dispersed) or approximately normal than as Poisson. Home advantage is about 2 goals, and the reported home win rate in the 2010/11 Bundesliga was 58.9%. Recent men's Bundesliga totals average about 60 goals per match, the Champions League about 57.6, and women's Bundesliga 56–61. Rating systems (Elo, pi-rating, PageRank) are the strongest predictors. No peer-reviewed study of handball betting-market efficiency was found.

### Cited Findings
- Groll et al. (arXiv 1207.0700, Bundesliga 2010/11) estimate a home win probability of 58.9% and a home advantage of roughly 2 goals. Unlike football, a **binomial** distribution fits a team's goals per match. — [arXiv 1207.0700](https://arxiv.org/pdf/1207.0700)
- A Bundesliga study (2017-18 to 2022-23) cited on a tipster site puts home advantage at 1.87 goals per match. — via [betmana handball guide](https://betmana.co.uk/guide/handball-betting-guide/) **[secondary]**
- EHF Champions League 2014–2024: 56.6% home wins, 34.3% away wins (so about 9% draws), average total 57.64 goals. — reported in [oddstricks.co.uk](https://oddstricks.co.uk/articles/european-handball-goal-margin-distributions-identifying-arb-windows-in-quarter-margins-across-major-leagues/) **[blog; data source not shown]**
- Handball-Bundesliga men 2025-26: 18,483 goals, 60.4 per match. Women 2025-26: 60.98 per match. Women 2023-24: 56.39 per match. — [Wikipedia 2025–26 HBL](https://en.wikipedia.org/wiki/2025%E2%80%9326_Handball-Bundesliga); [Wikipedia 2025–26 HBF women](https://en.wikipedia.org/wiki/2025%E2%80%9326_Handball-Bundesliga_(women)); [Wikipedia 2023–24 HBF women](https://en.wikipedia.org/wiki/2023%E2%80%9324_Handball-Bundesliga_(women))
- Felice & Ley (*J. Sports Analytics*, 2025) combine Elo, PageRank and pi-ratings with machine learning. The ratings are the best predictors, and the best model predicts women's handball scores with an error of about 3.8 goals (about 11% relative to roughly 27.9 goals per team). — [SAGE doi:10.1177/22150218251313937](https://doi.org/10.1177/22150218251313937); [ResearchGate preprint](https://www.researchgate.net/publication/372583554_Prediction_of_Handball_Matches_with_Statistically_Enhanced_Learning_via_Estimated_Team_Strengths)
- An open-source handball Elo prototype initialises teams at 1350–1725 depending on league tier and tunes a home-advantage bonus. — [GitHub luka31415/handball-prediction-model](https://github.com/luka31415/handball-prediction-model)
- Blog home-win claims of 55–70% conflict with each other and are higher than the academic 58.9%. — [betmana](https://betmana.co.uk/guide/handball-betting-guide/) **[blog]**

### Inferences
- Model each team's goals as Normal (or binomial: shots × conversion). The binomial fit implies variance below the mean, unlike Poisson. If team goals ≈ 30 with SD ≈ 4–5, the margin SD is about 5.5–7 goals. Home edge ≈ 2 goals ≈ about 0.3 SD, consistent with roughly 57–59% home wins once draws are included.
- Draws run at roughly 7–10% (from the 56.6%/34.3% CL split). Under a normal margin model, P(draw) ≈ P(|margin| < 0.5), which for σ≈6 and μ≈2 is about 6%. A 1X2 model should check draw calibration against the market.
- Use the women's game as a separate population. Totals and variance differ by league and season (56–61 per match in the HBF).

### Gaps
- No peer-reviewed study of handball betting-market efficiency, closing-line efficiency, or over/under bias was found.
- No credible half-time split data (share of goals in the 1st vs 2nd half), and no studies of 7-metre or time-out effects on totals.
- Women's international (EHF/IHF) home advantage and draw rates were not found.

## Accumulator mathematics

### Takeaway
Bookmaker margin compounds multiplicatively across accumulator legs, so the expected return of an accumulator is the product of each leg's (p × odds). The favourite-longshot bias, weaker at Pinnacle, means short-priced favourites carry less margin per leg. "Safe" legs still multiply the margin, and they add almost no expected value unless each leg individually has positive EV. Same-game parlays carry measured holds of roughly 15–35%, against about 4–5% on a single −110 bet.

### Cited Findings
- Bloomberg Businessweek (licensed-sportsbook data, 4 states reporting parlay figures): bettors lose on average 19¢ per $1 wagered on parlays. Across about 140,000 bettors in 29 states, parlays make up over 60% of some operators' revenue. — summarised from [Bloomberg 2026 feature](https://www.bloomberg.com/features/2026-sports-betting-debt-bankruptcy/) and search summary
- Reported same-game-parlay holds vary by source: 3-leg SGP 15–25% vs 12–15% for a 3-leg cross-game parlay; "15–30%"; "SGP+ realized hold 25–35%". US national hold was 10.15% in 2025 on about $165B handle. — [tech-insider.org](https://tech-insider.org/sports-betting/parlay-betting-explained/); [moneymavericksports](https://moneymavericksports.com/guides/same-game-parlays); [oddsindex](https://oddsindex.com/guides/same-game-parlay-strategy) **[industry blogs; methods not published]**
- Books price SGPs with correlation or simulation models rather than by multiplying the legs' odds. A patent describes assigning correlation values to related legs. One test of the same 3-leg slip found the implied correlation premium ranged from about 3.7% (BetRivers) to 6.8% (Caesars). — [USPTO patent 12002332](https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/12002332); [sharpfootballanalysis](https://www.sharpfootballanalysis.com/sportsbook/same-game-parlay-sites/)
- Favourite-longshot bias: Hegarty & Whelan find a much weaker FLB at Pinnacle, with substantial average losses only in the lowest decile of normalised probability. A 2025 *Applied Economics* paper finds Pinnacle's realised loss rates exceed predicted rates, consistent with some FLB in its soccer odds. Data Golf argues that two definitions of the FLB have been conflated. — [Whelan, "Market Structure and Prices in Online Betting Markets"](https://www.karlwhelan.com/Papers/Monopoly.pdf); [Applied Economics 2025](https://www.tandfonline.com/doi/full/10.1080/00036846.2025.2507979); [Data Golf](https://datagolf.com/fav-longshot-not-a-bias); [football-data.co.uk (Buchdahl)](https://www.football-data.co.uk/blog/favourite_longshot_bias_revisited_again.php)
- Example: a 4-fold at 5% overround per leg carries about 20% combined margin. — [betmana](https://betmana.co.uk/guide/why-bettors-lose-money/) **[illustrative]**

### Inferences (mathematics, derivable)
- For independent legs i with true probability p_i and decimal odds o_i: P(acca wins) = Π p_i, acca odds = Π o_i, and **expected return per unit = Π (p_i × o_i)**. If each leg has EV ratio r_i = p_i·o_i, the acca's EV ratio is Π r_i. With r = 0.95 per leg (about 5% margin), 2/3/4/6/10 legs give 0.903/0.857/0.815/0.735/0.599, i.e. expected losses of 9.7%/14.3%/18.5%/26.5%/40.1%.
- Equivalently, P(win) = Π(p_i·o_i)/Π(o_i). At "fair" bookmaker-implied p with margin m per leg, P(win) = (1/(1+m))^n / Π o_i.
- **Optimal number of legs:** if each leg has positive EV (r_i > 1), more legs raise expected return multiplicatively but variance grows explosively, and the Kelly-optimal stake on the acca shrinks. If any leg has r_i < 1, that leg strictly lowers the acca's EV. For a bettor with no proven edge, the EV-maximising number of legs is the minimum, i.e. singles.
- **"Safe" short-priced legs:** a 1.20 favourite with true p = 0.80 has r = 0.96. Five such legs give odds of 2.49 but P(win) = 0.328 and EV ratio 0.815, so the expected loss is about 18.5% even though each leg "looks safe." The favourite-longshot bias means favourites lose less margin per leg than longshots (r closer to 1). Short legs are therefore less bad than long legs, but still negative unless individually +EV.
- **Correlation:** positively correlated legs (e.g. team wins + its star scores over his line) make the true joint probability > Π p_i. That is why books charge SGP correlation premiums. Cross-game accas priced as independent are a mild positive only when legs are genuinely positively correlated (rare across games), and books typically block obvious correlated combos.
- **Accumulator bonuses** (e.g. +5–X% on 5+ legs) offset only part of the compounding: a 10% bonus on a 6-leg acca at r=0.95 gives 0.735 × 1.10 ≈ 0.81 EV, still about −19%.

### Gaps
- No peer-reviewed measurement of accumulator hold or of the parlay correlation premium.
- No published SportyBet (Nigeria) margins or acca-bonus terms were found in this research.

## Staking: Kelly, fractional Kelly, simultaneous/parlay Kelly, risk of ruin, flat staking

### Takeaway
Kelly maximises long-run log growth: f* = (b·p − q)/b = edge/odds-minus-1. Betting 2× Kelly gives roughly zero growth, and more than that leads to ruin. Half-Kelly is standard because it keeps about 75% of the growth with half the volatility and protects against overestimated edges. For simultaneous bets, size each bet down, and cut sharply for correlated bets (Thorp). Under fractional Kelly literal ruin is impossible, but deep drawdowns are near-certain over long horizons.

### Cited Findings
- Thorp, "The Kelly Criterion in Blackjack, Sports Betting and the Stock Market" (2007 handbook chapter): his sports bets across different games were roughly independent, so only modest downward adjustment was needed for simultaneous bets. Same-table blackjack hands have a pairwise correlation of about 0.5, which substantially reduces each bet's Kelly fraction. Covariance alone does not give an exact solution for simultaneous bets. He distinguishes literal ruin (impossible under fractional betting) from practical ruin (wealth falling to a tiny fraction, almost certain over long horizons at aggressive fractions). — [Thorp 2007 (Williams College copy)](https://web.williams.edu/Mathematics/sjmiller/public_html/341/handouts/Thorpe_KellyCriterion2007.pdf) (PDF not directly fetched; via search summary)
- Wikipedia: Kelly formula; fractional Kelly hedges against error in estimating edge; betting at or above 2× Kelly gives non-positive growth. — [Wikipedia: Kelly criterion](https://en.wikipedia.org/wiki/Kelly_criterion)
- Half-Kelly is popular. MacLean, Ziemba & Blazenko (1992) show favourable growth/security trade-offs for fractional Kelly. — cited in [arXiv 1503.06535](https://arxiv.org/pdf/1503.06535)
- Betting at or above the critical fraction leads to asymptotic ruin. — [arXiv 1801.01948](https://arxiv.org/pdf/1801.01948)
- Four simultaneous independent Kelly-sized bets roughly double the standard deviation of a single bet, which is why fractional sizing is used for portfolios. — [Wizard of Odds](https://wizardofodds.com/article/variance-and-bankroll-management-for-player-props/) **[secondary]**

### Inferences (standard results)
- **Kelly for decimal odds o, win prob p:** f* = (p·o − 1)/(o − 1). Example: p=0.55 at 1.91 (−110) gives f* = (1.0505−1)/0.91 = 5.5% of bankroll. Half-Kelly is 2.8% and quarter-Kelly 1.4%.
- **Growth:** at fraction c of Kelly, growth ≈ (2c − c²) × max growth. So half-Kelly ≈ 75% of maximum growth with half the SD, and 2× Kelly gives 0.
- **Drawdown:** under full Kelly (continuous approximation) the probability of ever falling to fraction x of the starting bankroll is x. That is a 50% chance of halving at some point. At half-Kelly it is x^3, so a 12.5% chance of ever halving. (Standard result from the Thorp/MacLean–Ziemba literature; exact text not retrieved here.)
- **Parlays and Kelly:** treat the parlay as one bet with p = Π p_i and o = Π o_i. Edges compound, but f* is small because o is large. Splitting the same edges into singles staked simultaneously usually gives higher growth with less variance. Model error compounds too, which strengthens the case for quarter-Kelly or less on accas.
- **Flat staking (1–2% of bankroll per unit):** robust when edge estimates are noisy, and approximately equivalent to fractional Kelly at a single typical edge and price.
- **Without a proven edge:** every staking plan has negative expectation. Staking cannot create edge. Martingale and loss-chasing raise the risk of ruin without changing EV.

### Gaps
- Thorp's exact sports-betting record (his NBA/NFL betting) and his quantitative drawdown tables could not be retrieved, because the PDF host was blocked.
- No empirical study was found comparing long-run outcomes of Kelly vs flat staking among real sports bettors.

## Measuring skill: CLV, calibration (Brier/log loss), sample sizes

### Takeaway
Profit and loss is extremely noisy. At a 2% edge on even-money odds, about 6,800 bets are needed before the yield separates statistically from zero. Closing-line value (beating Pinnacle-style closing prices) has roughly a tenth of the SD, so a CLV signal can appear in about 50–70 bets. Buchdahl still advises 1,000+ bets before drawing serious conclusions, and warns that a p-value is not the probability of skill.

### Cited Findings
- Joseph Buchdahl (interview): he would not make serious interpretations of skill until at least 1,000 bets. CLV needs fewer bets, but absence of CLV doesn't always mean absence of skill. — [sharpbetting.co.uk interview](https://sharpbetting.co.uk/articles/interview-with-joseph-buchdahl)
- A 2% edge at odds 2.00 needs about 6,800 bets to be statistically distinguishable via yield, vs about 70 via CLV. The SD of CLV at even money is about 0.10, against about 1.00 for P&L. — [howprosbet.com](https://howprosbet.com/how-to-verify-your-betting-edge/) **[secondary summary of Buchdahl]**
- A consistent 5% CLV edge could show significance in about 50 bets. — [pinnacleoddsdropper (Buchdahl CLV)](https://www.pinnacleoddsdropper.com/blog/closing-line-value--clv-demystified-by-expert-joseph-buchdahl)
- A "1% chance it happened by luck" does NOT mean a 99% chance of skill. — [Trademate Sports, Betting Experts series](https://www.tradematesports.com/en/blog/betting-experts-determine-whether-betting-results-luck-skill-part-3/)
- Not everyone accepts the CLV hypothesis, and CLV requires a sharp, low-margin close. — [collatiomedia](https://collatiomedia.com/blog/what-is-closing-line-value-clv-betting)

### Inferences
- **Sample size rule of thumb:** for edge e at decimal odds o, P&L per bet has SD ≈ √(o−1) (unit stakes, p≈1/o). Bets needed for t ≈ 2 ≈ 4(o−1)/e². At o=2, e=2% that gives about 10,000 bets (or about 6,800 at t≈1.65). At o=2, e=5% it gives about 1,600. At higher odds, multiply accordingly: an acca at odds 10 needs about 9× more bets for the same edge.
- **Calibration:** compare your model's Brier score and log loss with the de-vigged closing-market probabilities on the same games. A model that does not beat the closing market's log loss has no evidence of edge. Use reliability plots (binned predicted vs observed frequency).
- **Practical CLV for Nigerian soft books:** compare your taken price to the Pinnacle or Betfair closing price on the same market, not to the soft book's own close.

### Gaps
- Buchdahl's primary texts (*Squares & Sharps*, *Monte Carlo or Bust*) and his Pinnacle articles were not fetched directly. The 0.10 vs 1.00 SD figures are second-hand.
- No published Brier/log-loss benchmarks for NBA or handball closing markets were found.

## What does NOT work; most bettors lose; account limiting (incl. Nigeria)

### Takeaway
Large-sample evidence shows nearly all online gamblers lose: only about 4% of 700,000+ US online gamblers were net winners over 2019–2023. Following Nigerian betting influencers lost 38% on flat stakes. Bookmakers restrict winning accounts, as documented by Kaunitz et al. (2017), which caps the scalability of any edge at soft books.

### Cited Findings
- UC San Diego working paper (2025): about 4% of more than 700,000 online gamblers withdrew more than they deposited over 2019–23, so about 96% lost. The data cannot separate sports betting from casino or DFS. — [UCSD Today](https://today.ucsd.edu/story/legalized-gambling-increases-irresponsible-betting-behavior-especially-among-low-income-populations); [GamblingHarm.org summary](https://gamblingharm.org/most-online-gamblers-lose-study/)
- Field experiment (Matt Brown): high-volume sports bettors predict they will break even but lose 7.5¢ per $1 wagered. — [Brown, "Do Sports Bettors Need Consumer Protection?"](https://mattbrownecon.github.io/assets/papers/jmp/sportsbetting.pdf)
- Parlays lose 19¢ per $1 on average (Bloomberg, 4 states with parlay data). — [Bloomberg](https://www.bloomberg.com/features/2026-sports-betting-debt-bankruptcy/)
- **Nigeria:** arXiv 2604.08251 (April 2026) tracked 5,467 pre-match slips from 3 prominent Nigerian tipsters on X and Telegram, which avoids the survivorship bias of influencers posting only wins. The influencers themselves lost 25.24% on promoted bets. Flat-stake followers would have lost 38.27%. The authors attribute influencer income to affiliate deals. — [arXiv 2604.08251](https://arxiv.org/abs/2604.08251); [ResearchGate](https://www.researchgate.net/publication/403683188_The_Statistical_Profitability_of_Social_Media_Sports_Betting_Influencers_Evidence_from_the_Nigerian_Market); [Focus Nigeria](https://focusgn.com/africa/study-finds-nigerian-betting-influencers-tips-lead-to-losses-for-followers)
- Kaunitz, Zhong & Kreiner (arXiv 1710.02824, 2017) bet football using bookmakers' own consensus odds as probability estimates and were profitable in simulation and real betting. A few months into real-money betting, bookmakers severely limited their accounts with stake caps, "manual inspection" and refused bets, often offering far below their fixed $50 stake, and they stopped. — [arXiv 1710.02824](https://arxiv.org/abs/1710.02824); [MIT Technology Review](https://www.technologyreview.com/2017/10/19/67760/the-secret-betting-strategy-that-beats-online-bookmakers/); [GitHub code](https://github.com/Lisandro79/BeatTheBookie)
- Influencer marketing drives Nigerian gambling growth. — [Rest of World 2023](https://restofworld.org/2023/online-gambling-influencers-nigeria/)
- The widely quoted "95–97% of sports bettors lose" has no peer-reviewed source; it is an industry estimate. — [boydsbets](https://www.boydsbets.com/percentage-profitable-sports-bettors/)

### Inferences
- Approaches that do NOT work on the evidence: following tipsters or influencers; multi-leg accas of "safe" favourites; staking systems (martingale) as a substitute for edge; team-specific quarter-share "systems" (no hobbyist test passed); unverified referee or rest "angles" already priced by the market.
- The only edges consistently documented are narrow and fleeting: early-season NBA totals (older data), soft-book prices lagging sharp consensus (Kaunitz), and fast reaction to information. Soft books (likely including SportyBet) will limit the last two once they are exploited.

### Gaps
- No public information was found on SportyBet's account-limiting or stake-factoring policies, its margins, or its acca-bonus EV. Nothing specific to SportyBet was found in academic or credible journalistic sources.
- No Nigeria-specific aggregate win/loss data for bettors was found beyond the influencer study.
