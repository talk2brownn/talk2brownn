export default function AboutView({ config }) {
  const rules = Object.entries(config.rules);
  return (
    <div className="about card">
      <h2>How it works</h2>
      <p>
        Every morning the engine prices each game in seven sports. It starts from the sharpest bookmaker lines
        available (Pinnacle and the Betfair Exchange where offered), adds our own models, and works out a fair
        chance for every market: team totals, halves, quarters, “A or B” markets, combos and more.
      </p>
      <h3>Reading a market</h3>
      <ul>
        <li><strong>Chance</strong>: our estimate that the bet wins.</li>
        <li><strong>Fair</strong>: the break-even price, 1 ÷ chance.</li>
        <li><strong>Bet at X+</strong>: the lowest SportyBet price that counts as value. Below it, SportyBet's margin eats any edge.</li>
      </ul>
      <p>
        Type SportyBet's actual price into the box. If it beats the minimum, the pick turns green and goes to
        <em> My slip</em>, where the ladder (2 to 1,000 odds) and the 30-game slip are built from value picks only.
      </p>
      <h3>Value rules</h3>
      <table className="rules">
        <thead><tr><th>Sport / type</th><th>Odds band</th><th>Min. edge</th></tr></thead>
        <tbody>
          {rules.map(([k, r]) => (
            <tr key={k}><td>{k.replace('/', ' · ')}</td><td>{r.min.toFixed(2)}–{r.max.toFixed(2)}</td><td>{(r.edge * 100).toFixed(0)}%</td></tr>
          ))}
        </tbody>
      </table>
      <p className="muted small">Tier B leagues need 1 point more edge, tier C 2 points more. No leg below {config.absolute_min_odds.toFixed(2)}.</p>
      <h3>Be honest with yourself</h3>
      <ul>
        <li>No bet is safe. A 90% pick still loses one time in ten.</li>
        <li>Margin is charged on every leg, so long accumulators lose money fast unless every leg is genuine value.</li>
        <li>The 100–1,000 rungs and the 30-game slip are long shots: stake small, fixed amounts.</li>
        <li>Bookmakers often limit accounts that win consistently.</li>
      </ul>
      <p className="muted small">18+ only. Betting can be addictive. Set a budget you can afford to lose and stop if it stops being fun.</p>
    </div>
  );
}
