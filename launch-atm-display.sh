#!/bin/bash
# Quick launcher for ATM display (for testing)

echo "🏧 Launching Robinhood ATM on display..."

# Check if server is running
if ! curl -sf http://localhost:5050/health > /dev/null; then
    echo "⚠️  ATM server not responding, waiting..."
    sleep 3
fi

# Launch in kiosk mode
export DISPLAY=:0
chromium-browser --kiosk \
    --noerrdialogs \
    --disable-infobars \
    --disable-session-crashed-bubble \
    --disable-restore-session-state \
    --start-fullscreen \
    http://localhost:5050 &

echo "✅ ATM display launched!"
echo "Press Alt+F4 to close"
