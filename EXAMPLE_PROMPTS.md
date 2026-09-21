# Claude Code prompts

## First run: no orders

Read CLAUDE.md, STRATEGY.md, and strategy-policy.json. Run the proposal-only
preflight using fresh Robinhood MCP data. Identify my unique Agentic account,
current available cash, positions, pending orders and withdrawals. Show how the
budget changes at my current balance. Report missing capabilities and runtime
requirements. Do not place, cancel, or change orders during this setup check.

## Normal reconciliation

Run one cycle of STRATEGY.md for my bound Agentic account. Apply the aggressive
growth mandate and all cash/exposure limits. Reconcile prior intents and broker
orders before doing anything new. If live runtime requirements are not met,
produce proposals only and explain the missing requirement. HOLD is a valid result.

## After depositing money

Reconcile my deposit using broker records. Increase the investable budget only
for funds actually available without borrowing. Do not count the deposit as a
return or repeat existing orders. Apply the same risk limits to the new balance.

## Small withdrawal

I need $5 available to withdraw. Reserve that cash first and pause conflicting
new buys. Show the cash shortfall, any minimal sale needed, and the broker's
settlement/withdrawability status. Prepare a liquidation proposal if needed;
do not initiate a transfer or assume proceeds are immediately withdrawable.

## Performance

Show dollar profit/loss excluding deposits and withdrawals, trading costs, and
incremental operating costs. Separate interest, dividends and price gains.
Use flow-adjusted percentage returns only where the required data is available.

## Stop

Stop initiating new trades. Inspect open strategy orders and report which are
still pending. Do not claim stopping this session cancels broker orders.
