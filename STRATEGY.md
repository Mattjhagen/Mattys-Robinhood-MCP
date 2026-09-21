# Adaptive aggressive-growth mandate

## Objective and scope

The user requested aggressive growth, accepts large losses, and may make small
withdrawals. Seek net total return after fees, spread, slippage, and operating
costs. No return is guaranteed; a small balance can be lost entirely. Dividends,
interest, and trading gains are different. Do not chase dividend yield or assume
cash earns interest: verify eligibility and the current rate for this account.

The JSON policy is an agent-readable mandate, not a Robinhood API configuration
or a broker-enforced risk engine. The offline calculator enforces only arithmetic
cash ceilings on its supplied inputs. It does not verify broker data, apply the
full investment policy, choose securities, or authorize/execute orders.

## Preflight before autonomous operation

1. Read the policy. Use the authenticated official MCP connection to discover
   available tools and their exact input schemas. Do not invent API fields or
   assume tools listed in documentation are enabled on this account.
2. Select a unique active Agentic account, verify its trading eligibility, and
   bind its exact identifier in ignored runtime/policy.local.json. Never select
   the first account blindly; if multiple accounts qualify, ask which one.
   The local file may bind the account and store a user withdrawal reserve;
   it must not silently loosen risk limits or permissions.
3. Fetch portfolio, all positions, open/recent orders, pending transfers and
   spendable cash information if available. Confirm which holds are already
   included in buying power/cash. If pending withdrawals or cash availability
   cannot be reconciled from available data, stop new buys and identify the
   missing information. Do not treat an absent field as zero.
4. Run a proposal-only cycle and show available cash, reserve, proposed universe,
   position caps, costs, and maximum order size. Existing crypto exposure is
   included. Authentication and numeric defaults must be visible to the user;
   no extra approval is needed for actions already within the user's mandate.
5. Live operation requires the intended account, current schemas, successful
   read-only preflight, and actual client permissions. Repository setup itself
   must never submit an order. If the client requires approval, honor it.

## One reconciliation cycle

Use one active runner per account. Keep a durable local journal and exclusive
lock under runtime/. A prompt is not a concurrency lock: if the runner cannot
provide an exclusive lock and durable state, run proposals only. Do not start
concurrent CLI jobs. After a crash, reconcile journal entries with broker orders
before accepting another run; do not clear an unexplained lock automatically.

1. Read current policy, withdrawal reserve, unresolved journal entries, and
   today's submitted-order count (use America/New_York for the daily boundary).
2. Refresh the account snapshot, positions, orders, and cash. Required account
   data must be at most 60 seconds old and executable quotes at most 30 seconds
   old. Timestamp uncertainty or conflicting data means HOLD.
3. Compare with the previous reconciled state. A deposit is usable only when
   the broker reports it available without borrowing. A withdrawal reduces
   investable funds; it is not a trading loss. Market movements are not transfers.
   Identify transfers from transaction records, never infer them from equity alone.
4. Prioritize any user-requested withdrawal cash. Stop new buys if withdrawal
   coverage is uncertain. For a pending withdrawal, cancel this strategy's
   conflicting unfilled buy orders if cancellable; wait for confirmed cancellation
   or reconcile any fills before recalculating. Never assume cancellation succeeded.
   Do not cancel unrelated manual orders. Never initiate bank/crypto transfers.
5. Calculate the remaining buy budget with scripts/budget.py using normalized
   inputs below. Use higher actual broker minimums and cost buffers when needed.
6. Evaluate HOLD, adding to existing positions, and a small set of eligible new
   candidates. Prefer liquid, unleveraged growth exposure with a stated thesis
   and invalidation condition. Never buy purely because price fell or an LLM
   expresses confidence. No martingale, loss chasing, or invented return forecasts.
7. Below $100, aim for at most two investment positions; cash is not a position.
   Each new purchase must keep any position at or below 50% of equity and combined
   crypto at or below 50%, including pending buys. Existing overweight holdings
   block additions but do not trigger blind liquidation. A diversified ETF counts
   as one position. One new buy order per day maximum. Aggregate new spending
   per cycle cannot exceed 25% of current equity, and cannot reset on a retry.
   Maintain the 10% cash reserve plus any withdrawal reserve where feasible.
8. If costs cannot be estimated, HOLD. Avoid churn: a thesis change, available
   deposit, withdrawal need, or allocation drift above 5 percentage points is
   a reason to evaluate, not an instruction to trade. An opportunity must justify
   costs using evidence; otherwise no order. Skip uneconomic dust orders.
9. Preview each candidate using the actual broker review tool when available.
   If no reliable preview/cost/tradability validation exists, do not execute it
   autonomously. For fractional orders use only supported dollar/quantity and
   order-type combinations; never substitute an oversized whole share. Prefer
   regular equity market hours verified with an exchange calendar, and avoid
   illiquid execution. Crypto hours do not imply equity hours.
10. Immediately before each submission, refresh buying power, positions, quotes,
    withdrawal holds and pending orders; recompute both cash and exposure limits.
    Journal the exact intent before submission. Use broker idempotency support
    only if exposed by the actual schema. Submit once, then record its broker ID.
    A timeout or unknown result means pause and reconcile, NEVER blindly retry.
    If history cannot disambiguate a submission, require manual reconciliation.
11. Count accepted/pending orders toward limits; partial fills reserve their
    remaining quantity and fees. A cancellation request does not release funds.
    Re-query the broker after any fill/cancellation before another decision.
12. Persist balances, transfer reconciliation, order IDs/status, costs, and thesis
    locally. Report meaningful fills, withdrawals affecting strategy, errors,
    and action needed. Say explicitly when no trade was placed and why.

## Small balances and cash normalization

The calculator takes explicit decimal strings, not raw MCP responses. Populate
these fields only after reconciling the broker's definitions:

- equity: current total Agentic account net equity, including all positions.
- available_cash: cash eligible for new purchases without borrowing, already net
  of holds the broker has applied. Do not use total equity or unsettled cash.
- buying_power: current broker purchasing limit for the intended asset class;
  it may include unsettled money, so available_cash remains a separate ceiling.
- unreserved_withdrawals: pending/user-requested withdrawal money NOT already
  deducted in available_cash/buying_power. Do not subtract the same hold twice.
- unreserved_order_costs: pending orders and fees NOT already deducted there.
- cycle_spent: gross buy notional plus costs already committed in this persisted
  cycle. Do not reset on restart, partial fill, or timeout.

Remaining notional is bounded by both cash after holds/reserve and remaining
cycle capacity, less the cost buffer. Reserve rounds up; spend rounds down.
The $1 minimum and $0.05 cost buffer are illustrative defaults: broker minimums
and current preview costs/slippage may be higher. Smaller-than-minimum budgets
produce HOLD. Never borrow or liquidate merely to satisfy a minimum order.

With $20 entirely available, example limits leave a $2 reserve and cap the first
buy at $4.95, including a separate $0.05 cost allowance. This is a ceiling, not a
recommendation to buy. A $21.85 portfolio with $0.19 cash cannot fund a new buy.
Deposits increase capacity only after availability is confirmed; withdrawals
reduce it on the next reconciliation. The system cannot observe changes while
the runner is stopped or disconnected.

## Withdrawals, exits, and performance

For a stated withdrawal amount, preserve that amount in cash before new buys.
If selling is needed, prepare the minimum justified liquidation, estimate costs
and tax-lot effects where available, and execute only within the user's stated
withdrawal instruction and the same validation/journaling rules. A detected
withdrawal alone is not permission to liquidate arbitrary holdings. Settlement
and withdrawability are broker-controlled; never promise instant cash.

Sell only owned, available quantities; reserve open sells to prevent duplicate
sales. Risk-reducing exits are not constrained by the buy notional cap, but still
require current prices, costs, order review, and the account mandate. No shorting,
options, leverage, borrowing, or automatically upgraded trading permissions.
Stopping new buys is not a guaranteed loss limit, and stop orders do not guarantee
an execution price. For irregular withdrawal needs, more cash may be appropriate.

Report period dollar P&L as ending equity minus starting equity minus deposits
plus withdrawals, using reconciled external flows. Do not call that a percentage
return. Use time-weighted subperiod returns only with reliable valuations around
flows; otherwise report dollar P&L and mark percentage performance unavailable.
Compare with a passive benchmark using the same cash-flow timing, and include
incremental Claude/hosting costs separately. Deposits must never hide losses.

## Scheduling and limitations

The MCP connection and CLAUDE.md do not run continuously. Start with one daily
review and an explicit reconciliation after a deposit or withdrawal. Do not
install a live unattended job until a runner has durable order reconciliation,
exclusive locking, logging, authentication handling, and tested kill-switch
behavior. These runtime components are NOT supplied by this configuration repo.
Use proposal-only operation until those requirements are implemented or provided
by the host. Do not describe this repository as a tested autonomous trading bot.

Stopping the runner prevents future submissions; it does not cancel existing
broker orders. Inspect and cancel eligible pending orders separately, then verify
status. Revoke the connector in Robinhood if access must be terminated.
