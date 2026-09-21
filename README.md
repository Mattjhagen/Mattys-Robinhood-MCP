# Matty's Robinhood MCP Configuration

This repository contains the Model Context Protocol (MCP) configuration for connecting Claude Code to Robinhood for automated trading and portfolio monitoring.

## Overview

This setup enables Claude to interact with your Robinhood account through the official Robinhood MCP server. The configuration includes:

- **Trading Account**: Agentic-enabled account for automated trading
- **Price Alerts**: Configured alerts for BTC, ETH, and DOGE
- **Watchlists**: Custom lists for tracking assets
- **Portfolio Monitoring**: Real-time account value and positions tracking

## Account Status

- **Account Type**: Individual (Limited Margin)
- **Agentic Trading**: ✓ Enabled
- **Current Portfolio Value**: ~$21.85 (primarily crypto holdings)

## MCP Server Configuration

The Robinhood MCP server is configured in Claude's settings at `~/.claude.json`:

```json
{
  "mcpServers": {
    "robinhood-trading": {
      "type": "http",
      "url": "https://agent.robinhood.com/mcp/trading"
    }
  }
}
```

### Alternative Configuration (Read-Only)

For a read-only MCP server using the npm package:

```json
{
  "mcpServers": {
    "robinhood-mcp-readonly": {
      "type": "stdio",
      "command": "npx",
      "args": ["robinhood-mcp"],
      "env": {}
    }
  }
}
```

## Setup Instructions

### 1. Enable MCP in Claude Code

1. Open Claude Code settings
2. Navigate to MCP Servers section
3. Add the Robinhood MCP server configuration
4. Authenticate with your Robinhood account using:
   ```bash
   /mcp
   ```

### 2. Authenticate

Run the `/mcp` command in Claude Code and follow the authentication flow to connect your Robinhood account.

### 3. Configure Agentic Trading

To enable automated trading:
1. Log into your Robinhood account on the web or mobile app
2. Navigate to Account Settings → Agentic Trading
3. Enable agentic trading for the desired account
4. Set your trading limits and restrictions

## Current Configuration

### Price Alerts

| Asset | Condition | Price |
|-------|-----------|-------|
| Bitcoin (BTC) | Above | $5.00 |
| Bitcoin (BTC) | Below | $5.00 |
| Ethereum (ETH) | Above | $5.00 |
| Ethereum (ETH) | Below | $5.00 |
| Dogecoin (DOGE) | Above | $0.10 |
| Dogecoin (DOGE) | Below | $0.10 |

**Note**: These alerts appear to be test thresholds and should be updated for actual trading scenarios.

### Watchlists

1. **Currently Trading** 💡 - 3 items
2. **My First List** ⚡ - 19 items
3. **Cryptos to Watch** 👾 - 1 item
4. **Options Watchlist** 💡 - Empty (options not enabled)

## Available MCP Tools

The Robinhood MCP provides access to:

- **Account Management**: `get_accounts`, `get_portfolio`
- **Trading**: `place_equity_order`, `place_crypto_order`, `place_option_order`
- **Market Data**: `get_equity_quotes`, `get_crypto_quotes`, `get_option_quotes`
- **Positions**: `get_equity_positions`, `get_crypto_positions`, `get_option_positions`
- **Orders**: `get_equity_orders`, `get_crypto_orders`, `get_option_orders`
- **Alerts**: `get_alerts`, `create_alert`, `update_alert`, `delete_alert`
- **Watchlists**: `get_watchlists`, `add_to_watchlist`, `remove_from_watchlist`
- **Research**: `get_equity_news`, `get_equity_fundamentals`, `get_financials`
- **Scanners**: `get_scans`, `create_scan`, `run_scan`

## Security Considerations

⚠️ **Important Security Notes**:

1. **Never commit API keys or tokens** to this repository
2. **Enable two-factor authentication** on your Robinhood account
3. **Set appropriate trading limits** in your agentic trading settings
4. **Monitor automated trades** regularly
5. **Start with small amounts** when testing automated strategies

## Example Claude Commands

### Check Portfolio Status
```
Check my Robinhood portfolio status
```

### Place a Trade
```
Buy $10 worth of Bitcoin on my agentic account
```

### Set Up Alerts
```
Create an alert when Bitcoin goes above $100,000
```

### View Positions
```
Show me all my crypto positions
```

## Troubleshooting

### Authentication Issues

If you encounter authentication errors:
1. Run `/mcp` to re-authenticate
2. Check that your session hasn't expired
3. Verify your account has agentic trading enabled

### Trading Restrictions

If trades are failing:
1. Verify your account type supports the asset class
2. Check your buying power with `get_portfolio`
3. Ensure you're within your configured trading limits

### MCP Connection Issues

If the MCP server won't connect:
1. Check your internet connection
2. Verify the MCP server URL is correct
3. Try restarting Claude Code
4. Check Robinhood's service status

## Resources

- [Robinhood MCP Documentation](https://agent.robinhood.com/docs)
- [Claude Code Documentation](https://docs.anthropic.com/claude/docs/claude-code)
- [Model Context Protocol Specification](https://modelcontextprotocol.io)

## License

This configuration is provided as-is for personal use. Trading involves risk - use at your own discretion.

## Contributing

Feel free to submit issues or pull requests with improvements to this configuration or documentation.

---

**Disclaimer**: This is a personal configuration repository. Automated trading carries significant financial risk. Always test thoroughly with small amounts and understand the risks before deploying automated trading strategies.
