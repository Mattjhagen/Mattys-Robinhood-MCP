#!/bin/bash
# Start ATM server with Robinhood API keys loaded

# Check if keys are set
if [ -z "$ROBINHOOD_API_KEY" ] || [ -z "$ROBINHOOD_PRIVATE_KEY" ]; then
    echo "❌ ERROR: API keys not found!"
    echo ""
    echo "Please run these commands first:"
    echo "  source ~/.bashrc"
    echo "  ./start_atm_live.sh"
    echo ""
    echo "Or set them manually:"
    echo "  export ROBINHOOD_API_KEY='your_key'"
    echo "  export ROBINHOOD_PRIVATE_KEY='your_private_key'"
    echo "  ./start_atm_live.sh"
    exit 1
fi

echo "✅ API Keys found!"
echo "   API Key: ${#ROBINHOOD_API_KEY} characters"
echo "   Private Key: ${#ROBINHOOD_PRIVATE_KEY} characters"
echo ""

# Kill any existing server more aggressively
echo "🔄 Stopping existing server..."
pkill -9 -f "python3 atm_server.py" 2>/dev/null

# Kill anything on port 5050
PORT_PID=$(lsof -ti:5050 2>/dev/null)
if [ -n "$PORT_PID" ]; then
    echo "   Killing process on port 5050 (PID: $PORT_PID)"
    kill -9 $PORT_PID 2>/dev/null
fi

sleep 2

# Verify port is free
if ss -tlnp 2>/dev/null | grep -q ":5050"; then
    echo "❌ Port 5050 still in use after cleanup!"
    ss -tlnp | grep 5050
    exit 1
fi

# Start the server with keys explicitly passed
echo "🚀 Starting ATM server in LIVE mode..."
cd ~/Mattys-Robinhood-MCP/p3_atm
ROBINHOOD_API_KEY="$ROBINHOOD_API_KEY" ROBINHOOD_PRIVATE_KEY="$ROBINHOOD_PRIVATE_KEY" nohup python3 atm_server.py > /tmp/atm.log 2>&1 &
SERVER_PID=$!

sleep 3

# Check if it started
if ps -p $SERVER_PID > /dev/null 2>&1; then
    echo ""
    echo "✅ Server started successfully (PID: $SERVER_PID)"
    echo "🌐 Access at: http://localhost:5050"
    echo ""
    
    # Test the API mode
    sleep 1
    ROBINHOOD_API_KEY="$ROBINHOOD_API_KEY" ROBINHOOD_PRIVATE_KEY="$ROBINHOOD_PRIVATE_KEY" python3 << 'PYEOF'
import os
from robinhood_api import get_robinhood_api
api = get_robinhood_api()
print('📊 API Mode:', 'LIVE ✅' if api.is_live() else 'MOCK ⚠️')
if api.is_live():
    print('🎉 Your Robinhood account is connected!')
    print('')
    print('Test your real balance:')
    print('   curl http://localhost:5050/api/quick-balance | jq')
else:
    print('⚠️  Still in mock mode - keys not loading')
PYEOF
else
    echo "❌ Server failed to start. Check /tmp/atm.log for errors"
    tail -20 /tmp/atm.log
fi
