#!/bin/bash
# Agentic Trading Loop - Runs every 15 minutes via cron
# Usage: */15 * * * * /home/matt/Mattys-Robinhood-MCP/run_trading_loop.sh

# Set working directory
cd /home/matt/Mattys-Robinhood-MCP

# Load environment
if [ -f ~/.bashrc ]; then
    source ~/.bashrc
fi

# Verify keys are loaded
if [ -z "$ROBINHOOD_API_KEY" ]; then
    echo "$(date): ERROR - ROBINHOOD_API_KEY not set" >> $LOG
    exit 1
fi

# Log file
LOG="/tmp/trading_loop.log"

# Timestamp
echo "========================================" >> $LOG
echo "$(date): Starting trading cycle" >> $LOG

# Run the trading agent
python3 trading_agent.py >> $LOG 2>&1

# Status
if [ $? -eq 0 ]; then
    echo "$(date): Cycle complete ✅" >> $LOG
else
    echo "$(date): Cycle failed ❌" >> $LOG
fi

echo "" >> $LOG
