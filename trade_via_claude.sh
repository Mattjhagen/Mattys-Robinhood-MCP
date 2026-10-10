#!/bin/bash
# Trade via Claude Code MCP - runs every 15 minutes
# This sends commands to Claude Code to execute trades

LOG="/tmp/claude_trading.log"

echo "========================================" >> $LOG
echo "$(date): Checking portfolio via Claude Code" >> $LOG

# Use Claude Code's CLI to execute trading logic
# This requires claude-cli or similar
echo "Check my Robinhood portfolio and rebalance if needed. Max 25% per asset. Take profit at 10% gain. Add small positions in BTC, ETH, SOL, or ADA if buying power allows." | claude >> $LOG 2>&1

if [ $? -eq 0 ]; then
    echo "$(date): Trading check complete ✅" >> $LOG
else
    echo "$(date): Trading check failed ❌" >> $LOG
fi

echo "" >> $LOG
