#!/bin/bash
# Automatic cron setup script - just run this!

echo "🤖 Setting up automated trading loop..."
echo ""

# Check if cron job already exists
if crontab -l 2>/dev/null | grep -q "run_trading_loop.sh"; then
    echo "⚠️  Trading loop already installed in crontab!"
    echo ""
    echo "Current crontab:"
    crontab -l | grep trading
    echo ""
    read -p "Do you want to reinstall it? (y/n) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "Keeping existing cron job."
        exit 0
    fi
    # Remove old entry
    crontab -l | grep -v "run_trading_loop.sh" | crontab -
fi

# Add new cron job
(crontab -l 2>/dev/null; echo "*/15 * * * * /home/matt/Mattys-Robinhood-MCP/run_trading_loop.sh") | crontab -

echo "✅ Cron job installed!"
echo ""
echo "📋 Your crontab now has:"
crontab -l | grep trading
echo ""
echo "⏰ The bot will run every 15 minutes:"
echo "   - :00, :15, :30, :45 of every hour"
echo "   - 24/7, automatically"
echo "   - Logs to /tmp/trading_loop.log"
echo ""
echo "📊 Monitor it:"
echo "   tail -f /tmp/trading_loop.log"
echo ""
echo "🧪 Test it now (don't wait 15min):"
echo "   ./run_trading_loop.sh"
echo ""
echo "🎉 Auto-trading is LIVE!"
