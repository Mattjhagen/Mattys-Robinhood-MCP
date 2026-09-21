# Matty's Robinhood MCP Configuration

Claude Code configuration and an adaptive trading mandate for a small Robinhood
Agentic account. The selected preference is aggressive growth with large losses
accepted and occasional small withdrawals. No strategy can guarantee or maximize
returns. Trading gains are not interest.

## What is included

- Official Robinhood HTTP connection in `.mcp.json` and `mcp-config.json`.
- `CLAUDE.md` and `STRATEGY.md`: fresh balances, deposits/withdrawals, position
  limits, cost-aware decisions, order reconciliation, and autonomous preflight.
- `strategy-policy.json`: editable limits that scale with current account equity.
- `scripts/budget.py`: offline, decimal-safe buy-budget calculator and tests.
- Sanitized historical snapshot. Never use it as current account data.

With $20 in available cash, the example policy permits up to $4.95 for a first
buy and protects a $2 cash reserve. Holdings are not spendable cash. Deposits and
withdrawals resize the budget when reconciled. This is arithmetic capacity, not
a trade recommendation or a backtested return claim.

## Start

Follow [INSTALLATION.md](INSTALLATION.md), then ask Claude to run the proposal-only
preflight in [EXAMPLE_PROMPTS.md](EXAMPLE_PROMPTS.md). Read
[STRATEGY.md](STRATEGY.md) before enabling any live workflow.

```sh
python3 -m unittest discover -s tests -v
python3 scripts/budget.py examples/balance-20.json
```

## What is not included

This repository is a configuration, not a running trading service. It does not
provide an authenticated broker adapter, scheduler, durable order runner,
exclusive account lock, or broker-enforced risk controls. Claude instructions
are not a security boundary. The calculator does not execute trades or validate
live data. Autonomous operation remains conditional on the preflight and runtime
requirements in STRATEGY.md. No live orders are placed by installation or tests.

The public historical account number was removed from the current file, but it
remains in old Git commits; this change does not rewrite repository history.
Keep all future account state in ignored `runtime/` and credentials in the host's
authentication store.

## Verified references

Reviewed September 21, 2026. Account-specific tool discovery takes precedence over
examples; supported tools and products can change.

- [Robinhood Agentic setup and account scope](https://robinhood.com/us/en/support/articles/agentic-trading-overview/)
- [Robinhood tools and settlement](https://robinhood.com/us/en/support/articles/trading-with-your-agent/)
- [Robinhood fractional shares](https://robinhood.com/us/en/support/articles/fractional-shares/)
- [Claude Code MCP configuration](https://code.claude.com/docs/en/mcp)
- [Claude Code permissions](https://code.claude.com/docs/en/permissions)
