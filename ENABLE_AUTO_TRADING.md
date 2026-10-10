# 🤖 Enable Automated Trading (15-Minute Loops)

## ✅ What Just Happened

I fixed your MCP configuration! You were using the **banking** endpoint instead of the **trading** endpoint.

**Before:**
```json
"robinhood-banking": "https://banking-agent.robinhood.com/mcp/banking"
```

**Now:**
```json
"robinhood-trading": "https://agent.robinhood.com/mcp/trading"  ✅
```

## 🔄 Step 1: Restart Claude Code

**You MUST restart Claude Code** for the trading endpoint to load:

```bash
# Close Claude Code completely, then reopen
# Or run:
pkill -f claude
# Then reopen Claude Code
```

## 🧪 Step 2: Verify Trading Tools

Once restarted, verify you have trading access:

```bash
# In Claude Code, try:
Check my Robinhood trading account
Place a $1 test order for Bitcoin
```

You should see tools like:
- `place_crypto_order`
- `place_equity_order`  
- `get_portfolio`
- `get_watchlists`

## ⏰ Step 3: Enable 15-Minute Trading Loop

Add this to your crontab:

```bash
# Edit crontab
crontab -e

# Add this line (runs every 15 minutes):
*/15 * * * * /home/matt/Mattys-Robinhood-MCP/run_trading_loop.sh
```

**Save and exit.** The bot will now run every 15 minutes.

## 📊 Step 4: Monitor the Bot

```bash
# Watch live trading activity
tail -f /tmp/trading_loop.log
tail -f /tmp/trading_agent.log

# Check cron is running
crontab -l | grep trading

# Manual test (don't wait 15min)
./run_trading_loop.sh
```

## 🎯 What the Bot Does

Every 15 minutes:
1. ✅ Checks your portfolio
2. ✅ Analyzes positions for profit-taking
3. ✅ Rebalances if positions are too large
4. ✅ Scans for new opportunities
5. ✅ Executes trades automatically
6. ✅ Logs all activity

**Current Strategy:**
- Max 25% per asset
- Take profit at 10% gain
- Stop loss at 5% loss
- Diversify across BTC, ETH, SOL, ADA
- Min $1 per trade

## ⚙️ Customize Strategy

Edit `/home/matt/Mattys-Robinhood-MCP/trading_agent.py`:

```python
# Trading parameters (line ~35)
self.min_trade_amount = 1.0        # Minimum trade
self.max_position_pct = 0.25       # Max 25% per asset
self.profit_take_pct = 0.10        # Take profit at 10%
self.stop_loss_pct = 0.05          # Stop loss at 5%
```

After changes:
```bash
# Test manually
python3 trading_agent.py

# Restart cron (it will pick up changes automatically)
```

## 📱 ATM Trading UI

Your ATM now has:
- 🔴 **Sell** buttons for each position
- 🟢 **Buy** buttons for watchlist assets
- 💵 **Transfer** to debit card
- 📊 Real-time portfolio tracking

Access: http://localhost:5050

## 🛡️ Safety Features

- ✅ Position size limits (25% max)
- ✅ Stop losses (5%)
- ✅ Profit taking (10%)
- ✅ Min trade amount ($1)
- ✅ One new position at a time
- ✅ Full audit logs

## ⚠️ Important

**This bot trades real money every 15 minutes.**

Start with small amounts to verify it's working as expected:
1. Fund your agentic account with $10-20
2. Watch logs for first few cycles
3. Verify trades in app
4. Scale up once comfortable

## 🔧 Troubleshooting

**"Trading not enabled" in logs:**
```bash
# Restart Claude Code to load trading endpoint
pkill -f claude

# Verify MCP config
cat ~/.claude.json | grep robinhood-trading
```

**No trades happening:**
```bash
# Check buying power
python3 -c "from p3_atm.robinhood_api import *; api=get_robinhood_api(); print(api.get_account())"

# Check last cycle
tail -n 50 /tmp/trading_agent.log
```

**Cron not running:**
```bash
# Check cron status
systemctl status cron

# Verify crontab entry
crontab -l

# Check cron logs
grep CRON /var/log/syslog | tail
```

## 🎉 You're Live!

Once you:
1. ✅ Restart Claude Code
2. ✅ Add cron job
3. ✅ Fund agentic account

Your bot will trade automatically every 15 minutes, 24/7! 🚀

---

**Current Status:**
- MCP endpoint: ✅ Fixed  
- Trading agent: ✅ Built
- Cron script: ✅ Ready
- ATM UI: ✅ Enhanced (see below)

**Next:** Restart Claude Code and add the cron job!
