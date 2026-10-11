#!/bin/bash
# Restart the Web-based Robinhood ATM (browser kiosk display)

echo "🔄 Restarting Robinhood ATM Web Interface..."
echo ""

# Stop the browser display first
echo "1. Stopping browser display..."
systemctl --user stop robinhood-atm-display.service

# Restart the web server
echo "2. Restarting web server..."
systemctl --user restart robinhood-atm-server.service

# Wait for server to be ready
echo "3. Waiting for server to start..."
for i in {1..10}; do
    if curl -sf http://localhost:5050/health > /dev/null 2>&1; then
        echo "   ✅ Server is ready"
        break
    fi
    sleep 1
done

# Restart the browser display (which will clear cache)
echo "4. Restarting browser display..."
systemctl --user start robinhood-atm-display.service

echo ""
echo "✅ Robinhood ATM Web Interface restarted!"
echo ""
echo "📊 Service Status:"
systemctl --user status robinhood-atm-server.service --no-pager | head -5
echo ""
systemctl --user status robinhood-atm-display.service --no-pager | head -5
echo ""
echo "The ATM is now showing on your screen."
echo "It should prompt for PIN authentication on the welcome screen."
echo ""
echo "Default PIN: 0213"
