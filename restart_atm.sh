#!/bin/bash
# Restart ATM with trading status indicator

echo "🔄 Restarting ATM with trading status indicator..."

# Kill old ATM process
OLD_PID=$(lsof -ti:5050 2>/dev/null)
if [ -n "$OLD_PID" ]; then
    echo "Stopping old ATM (PID: $OLD_PID)..."
    kill $OLD_PID 2>/dev/null
    sleep 2
fi

# Load environment
if [ -f ~/.bashrc ]; then
    source ~/.bashrc
fi

# Verify keys are loaded
if [ -z "$ROBINHOOD_API_KEY" ]; then
    echo "⚠️  Warning: ROBINHOOD_API_KEY not set"
    echo "   Loading from .bashrc..."
    export ROBINHOOD_API_KEY="rh-api-3ad6835b-e308-4297-915a-92b1cfb50e22"
    export ROBINHOOD_PRIVATE_KEY_BASE64="xQnTJVeQLmw1/Mg2YimEViSpw/SdJcgNXZ5kQkAXNPU="
fi

# Start ATM in background
cd ~/Mattys-Robinhood-MCP/p3_atm
nohup python3 atm_server.py > /tmp/atm.log 2>&1 &

# Wait for it to start
sleep 3

# Check if it's running
if lsof -i:5050 > /dev/null 2>&1; then
    NEW_PID=$(lsof -ti:5050)
    echo "✅ ATM started successfully (PID: $NEW_PID)"
    echo ""
    echo "🌐 Access your ATM:"
    echo "   http://localhost:5050"
    echo "   http://100.103.3.35:5050"
    echo ""
    echo "🟢 Look for the status indicator in the top-right corner!"
    echo ""

    # Test the status endpoint
    echo "🧪 Testing status endpoint..."
    sleep 1
    curl -s http://localhost:5050/api/trading-status | python3 -m json.tool 2>/dev/null || echo "Endpoint starting up..."
else
    echo "❌ Failed to start ATM"
    echo "   Check logs: tail /tmp/atm.log"
fi
