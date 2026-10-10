# Trading Agent Monitor

Real-time terminal dashboard for monitoring the autonomous Robinhood trading agent.

## Features

- 📊 **Portfolio Summary** - Total value, buying power, daily P/L
- 📈 **Active Positions** - All holdings with entry price, current price, P/L, and stop-loss levels
- 🎯 **Risk Management** - Kill switch status, position limits, agent status
- 🔄 **Auto-refresh** - Updates every 30 seconds
- 🎨 **Color-coded** - Green for profits, red for losses

## Quick Start

```bash
# Run the monitor
python3 ~/Mattys-Robinhood-MCP/trading_monitor.py
```

## Display Layout

```
🤖 ROBINHOOD TRADING AGENT MONITOR
Account: ••••2903 | 2026-10-10 15:47:00
================================================================================

📊 PORTFOLIO SUMMARY
────────────────────────────────────────────────────────────────────────────────
  Total Value:     $34.45
  Buying Power:    $0.00
  Crypto Holdings: $34.45
  Equity Holdings: $0.00
  Daily P/L:       🟢 -$5.74 (-14.28%)

📈 ACTIVE POSITIONS
────────────────────────────────────────────────────────────────────────────────
  Asset  Quantity        Entry      Current    Value      P/L          Stop(-8%)
  ──────────────────────────────────────────────────────────────────────────────
  BTC    0.00023893      $82,904    $82,959    $19.82     🟢 +$0.01    $76,272
  ETH    0.005831        $2,506     $2,507     $14.63     🟢 +$0.01    $2,306

🎯 RISK MANAGEMENT
────────────────────────────────────────────────────────────────────────────────
  Kill Switch (-3%): ✅ INACTIVE
  Position Slots:    2/5 used
  Max Position Size: 10% of portfolio
  Loop Status:       ✅ RUNNING (every 15 min)
```

## Trading Agent Loop

The autonomous trading agent runs every 15 minutes with these rules:

1. **Stop-Loss**: Automatically sell at -8% from entry
2. **Take-Profit**: Scale out 50% at +15%, remainder at +25%
3. **Kill Switch**: No new positions if portfolio drops >3% in a day
4. **Position Limits**: Max 5 positions, 10% per position
5. **Equities Only**: Regular market hours only (9:30 AM - 4:00 PM ET)

### Loop Control

```bash
# View active loop
claude cron list

# Cancel loop (Job ID: c880d336)
# CronDelete c880d336
```

## Requirements

- Python 3.6+
- Robinhood MCP Server authenticated
- Claude Code with Robinhood trading access

## Notes

- **Display Only**: This monitor shows data but does NOT execute trades
- **Trading Loop**: Runs independently via scheduled cron job
- **Approval Mode**: OFF - agent places trades autonomously within rules
- **Refresh Rate**: 30 seconds (adjustable in code)

## Controls

- **Ctrl+C**: Exit monitor (trading loop continues in background)
- **Auto-refresh**: Every 30 seconds

## Safety

The monitor is read-only. All trading happens through the autonomous agent loop which:
- Enforces strict risk management rules
- Logs every decision with order IDs
- Respects stop-losses and take-profits automatically
- Will NOT average down on losers
- Only trades during regular market hours

---

**⚠️ Trading involves risk. This agent trades with real money. Monitor regularly.**
