# Matty's Robinhood MCP Configuration

This repository contains the Model Context Protocol (MCP) configuration for connecting Claude Code to Robinhood for portfolio monitoring and the P3 ATM interface.

## Current Status

**✅ What Works Now:**
- Real-time portfolio monitoring via read-only MCP
- Account balance and positions tracking  
- P3 ATM web interface on port 5050
- Holdings and allocation data

**⏳ What's Coming:**
- **Agentic Trading**: On Gold Card waitlist (invite pending)
- **Automated Trading**: Requires Gold Card approval
- **Trade Execution**: Will be enabled after Gold Card access

## Account Status

- **Account Number**: 311223129172
- **Account Type**: Individual
- **Agentic Trading**: ❌ Waitlisted (Gold Card required)
- **Current Access**: Read-only via npm MCP package
- **Current Holdings**: $0.26 (1 ADA + small ETH amount)

## MCP Server Configuration

**Current Configuration** (Read-Only npm package):

The Robinhood MCP server is configured in `~/.claude.json`:

```json
{
  "mcpServers": {
    "robinhood-mcp": {
      "type": "stdio",
      "command": "npx",
      "args": ["robinhood-mcp"],
      "env": {}
    }
  }
}
```

API keys are loaded from `~/.bashrc`:
```bash
export ROBINHOOD_API_KEY="your-rh-api-key"
export ROBINHOOD_PRIVATE_KEY="your-private-key"
```

### Future Configuration (When Gold Card Approved)

Once you receive Gold Card access, you'll use the trading server:

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

## Setup Instructions

### 1. Read-Only Access (Current Setup) ✅

Your ATM is already working with read-only access:

```bash
# API keys should be in ~/.bashrc
echo $ROBINHOOD_API_KEY
echo $ROBINHOOD_PRIVATE_KEY

# If not set, add them:
export ROBINHOOD_API_KEY="rh-api-your-key-here"
export ROBINHOOD_PRIVATE_KEY="your-agent-key-here"
```

### 2. Enable Trading (Choose ONE)

**Option A: Wait for Gold Card** (Recommended)
- ✅ Already on waitlist
- ✅ Zero setup needed
- ✅ Trading enables automatically
- See: `HOW_TO_GET_TRADING.md`

**Option B: Request Trading API Keys**
- Contact Robinhood support for PEM keys
- Manual setup required
- See: `GET_TRADING_API_KEYS.md`

### 3. Auto-Start Service ✅

Already installed! The ATM starts automatically on boot:

```bash
# Check status
sudo systemctl status p3-atm

# Access ATM
http://localhost:5050
http://100.103.3.35:5050
```

## While Waiting for Gold Card

You can still do a lot with read-only access:

1. **Monitor Portfolio** - Track your holdings in real-time
2. **Price Tracking** - Get live quotes and market data
3. **Build UI** - Develop and test the ATM interface
4. **Plan Strategies** - Design trading algorithms for when trading is enabled
5. **Historical Analysis** - Review past orders and performance

The P3 ATM interface works fully in read-only mode and will automatically support trading once your Gold Card is approved.

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

## Available MCP Tools (Current - Read-Only)

The npm `robinhood-mcp` package currently provides these **read-only** tools:

- ✅ `get_account` - View account information
- ✅ `get_holdings` - View crypto holdings
- ✅ `get_allocation` - View portfolio allocation
- ✅ `get_best_bid_ask` - Get real-time quotes
- ✅ `get_orders` - View order history
- ✅ `get_market_hours` - Check market status

**Not available until Gold Card approval:**
- ❌ Trading: `place_order`, `buy_crypto`, `sell_crypto`
- ❌ Alerts: `create_alert`, `update_alert`, `delete_alert`
- ❌ Watchlists: Write operations

## P3 ATM Interface

The repository includes a web-based ATM interface at `p3_atm/`:

- **Location**: `http://localhost:5050`
- **Features**: Balance display, position viewing, account info
- **Backend**: Python Flask server with MCP bridge
- **Auto-Start**: systemd service (install with `sudo bash install-service.sh`)

## Security Considerations

⚠️ **Important Security Notes**:

1. **Never commit API keys or tokens** to this repository
2. **Enable two-factor authentication** on your Robinhood account
3. **Set appropriate trading limits** in your agentic trading settings
4. **Monitor automated trades** regularly
5. **Start with small amounts** when testing automated strategies

## Example Commands

### ✅ What Works Now (Read-Only)

```
Check my Robinhood account balance
Show my crypto holdings
What's the current Bitcoin price?
Show my portfolio allocation
Check my order history
```

### ⏳ What Will Work After Gold Card

```
Buy $10 worth of Bitcoin
Sell 0.001 BTC
Create an alert when Bitcoin goes above $100,000
Set up automated trading strategy
```

## Troubleshooting

### MCP Connection Issues

If the MCP server won't connect:
1. Verify API keys are loaded: `echo $ROBINHOOD_API_KEY`
2. Check `~/.bashrc` has the export statements
3. Restart your shell or run `source ~/.bashrc`
4. Try running `npx robinhood-mcp` manually to test

### P3 ATM Not Starting

If the ATM interface isn't working:
1. Check if service is running: `sudo systemctl status p3-atm`
2. View logs: `sudo journalctl -u p3-atm -n 50`
3. Verify port 5050 isn't in use: `lsof -i:5050`
4. Restart: `sudo systemctl restart p3-atm`

### "Mock Mode" or No Data

If you see mock/placeholder data:
1. Verify MCP bridge is working: `python3 p3_atm/mcp_bridge.py`
2. Check that `robinhood-mcp` package is installed: `npx robinhood-mcp --version`
3. Verify API keys are valid (check Robinhood developer console)

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
