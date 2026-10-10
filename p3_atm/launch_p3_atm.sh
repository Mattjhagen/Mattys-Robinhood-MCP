#!/bin/bash
# P3 Lending Inc ATM Launcher
# Starts the web server and opens Chromium in kiosk mode

set -e

ATM_DIR="/home/matt/Mattys-Robinhood-MCP/p3_atm"
PID_FILE="$ATM_DIR/atm_server.pid"
LOG_FILE="$ATM_DIR/atm_server.log"

cd "$ATM_DIR"

# Kill any existing server
if [ -f "$PID_FILE" ]; then
    OLD_PID=$(cat "$PID_FILE")
    if kill -0 "$OLD_PID" 2>/dev/null; then
        echo "Stopping existing server (PID: $OLD_PID)"
        kill "$OLD_PID"
        sleep 2
    fi
    rm -f "$PID_FILE"
fi

# Start Flask server in background
echo "Starting P3 ATM server..."
python3 atm_server.py > "$LOG_FILE" 2>&1 &
SERVER_PID=$!
echo $SERVER_PID > "$PID_FILE"

# Wait for server to start
echo "Waiting for server to start..."
for i in {1..10}; do
    if curl -s http://localhost:5050/health > /dev/null; then
        echo "Server started successfully (PID: $SERVER_PID)"
        break
    fi
    sleep 1
done

# Set display to :0 (the main X server)
export DISPLAY=:0

# Launch Chromium in kiosk mode
echo "Launching Chromium kiosk mode..."
chromium-browser \
    --kiosk \
    --noerrdialogs \
    --disable-infobars \
    --disable-session-crashed-bubble \
    --disable-features=TranslateUI \
    --no-first-run \
    --disable-notifications \
    --disable-popup-blocking \
    --start-fullscreen \
    http://localhost:5050

# If Chromium closes, stop the server
echo "Chromium closed, stopping server..."
if [ -f "$PID_FILE" ]; then
    kill $(cat "$PID_FILE") 2>/dev/null || true
    rm -f "$PID_FILE"
fi
