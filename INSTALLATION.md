# Claude Code installation

## Connect the official server

Open Claude Code CLI in this repository. It reads the project `.mcp.json` after
project/server trust approval. Authenticate the `robinhood-trading` server with
`/mcp`. Do not paste tokens into files or commit authentication state.

Alternatively, register the same server with the CLI (do not create duplicate
connections if this project's server is already loaded):

```sh
claude mcp add --transport http robinhood-trading https://agent.robinhood.com/mcp/trading
```

Robinhood's desktop authentication flow handles Agentic account onboarding. Verify
the account returned by `get_accounts`; do not rely on a nickname or historical
snapshot. The MCP can read other Robinhood accounts, but trading is restricted to
the Agentic account. Crypto has separate eligibility requirements.

For Claude Desktop, use Settings → Connectors → Add custom connector with the
same URL. Project CLAUDE.md instructions and CLI settings do not automatically
apply to Desktop; this repository's workflow is designed for Claude Code CLI.

## Verify without trading

Ask Claude to read CLAUDE.md and run STRATEGY.md's proposal-only preflight. This
checks tool schemas, cash definitions, account eligibility, pending orders and
withdrawals, and portfolio limits. Missing cash/transfer information means HOLD.
Store bound account IDs, snapshots, and journals only under ignored runtime/.

The removed third-party npm server was not the official endpoint. A package name
or descriptive label does not establish read-only access. Use the official
connection with appropriate client permissions.

## Permissions

Normal Claude Code permission prompts remain in effect. The repository does not
install broad automatic write permissions. To insist on approval for every order
mutation, merge this example into `.claude/settings.local.json` while preserving
existing settings (the supported key is `ask`, not `prompt`):

```json
{
  "permissions": {
    "ask": [
      "mcp__robinhood-trading__place_*",
      "mcp__robinhood-trading__cancel_*"
    ]
  }
}
```

Check actual canonical tool names in your session; connector namespaces may
differ. Ask rules win over allow rules. These are tool approval settings, not
cash/position constraints. Do not use `--dangerously-skip-permissions` to automate
trading. Do not assume Robinhood offers every custom limit from strategy-policy.

The user's autonomous mandate is recorded in the policy. To run without per-order
prompts later, the host must grant only the specific validated tools needed by a
runner that meets STRATEGY.md's runtime requirements. This repo does not supply
that runner or silently alter your global permissions.

## Validate offline

Python 3.9+; no dependencies or broker credentials required:

```sh
python3 -m unittest discover -s tests -v
python3 scripts/budget.py examples/balance-20.json
```

Before live use, exercise stale data, pending withdrawals, partial fills,
concurrent runs, and ambiguous submission responses in a broker-adapter test
harness. The included tests cover cash math only, not live integration or returns.

## Operation and stopping

A CLI must be invoked and authenticated to perform a cycle. There is no installed
scheduler or instant transfer listener. After deposits/withdrawals, request a
fresh reconciliation. Scheduled work must hold an exclusive account lock and
persist orders before submission; without those facilities use proposals only.

Stop the runner to prevent new calls, then inspect outstanding broker orders.
Stopping Claude does not cancel orders. Reauthenticate with `/mcp` if needed;
do not delete undocumented authentication files or switch to an unverified server.
