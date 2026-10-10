#!/bin/bash
# Quick setup status checker

echo "🔍 P3 ATM Setup Status Check"
echo "========================================"
echo ""

# Check service
echo "📦 Auto-Start Service:"
if systemctl is-active --quiet p3-atm; then
    echo "  ✅ Running"
    echo "  URL: http://localhost:5050"
else
    echo "  ❌ Not running"
    echo "  Fix: sudo systemctl start p3-atm"
fi
echo ""

# Check MCP keys
echo "🔑 MCP Keys (Read-Only):"
if [ -n "$ROBINHOOD_API_KEY" ]; then
    echo "  ✅ ROBINHOOD_API_KEY is set"
else
    echo "  ❌ ROBINHOOD_API_KEY not found"
    echo "  Fix: Add to ~/.bashrc and run 'source ~/.bashrc'"
fi

if [ -n "$ROBINHOOD_PRIVATE_KEY" ]; then
    echo "  ✅ ROBINHOOD_PRIVATE_KEY is set"
else
    echo "  ❌ ROBINHOOD_PRIVATE_KEY not found"
fi
echo ""

# Check Trading API keys
echo "🔐 Trading API Keys (Write Access):"
if [ -n "$ROBINHOOD_PRIVATE_KEY_PATH" ]; then
    echo "  ✅ ROBINHOOD_PRIVATE_KEY_PATH is set: $ROBINHOOD_PRIVATE_KEY_PATH"
    if [ -f "$ROBINHOOD_PRIVATE_KEY_PATH" ]; then
        echo "  ✅ PEM file exists"
        if head -1 "$ROBINHOOD_PRIVATE_KEY_PATH" | grep -q "BEGIN PRIVATE KEY"; then
            echo "  ✅ PEM file format looks correct"
        else
            echo "  ⚠️  PEM file doesn't look right (should start with -----BEGIN PRIVATE KEY-----)"
        fi
    else
        echo "  ❌ PEM file not found at path"
    fi
else
    echo "  ⏳ Not set up yet (trading disabled)"
    echo "  See: GET_TRADING_API_KEYS.md"
fi
echo ""

# Check dependencies
echo "📚 Dependencies:"
if command -v npx &> /dev/null; then
    echo "  ✅ npx installed"
    if npx --yes robinhood-mcp --version &> /dev/null 2>&1; then
        echo "  ✅ robinhood-mcp package available"
    else
        echo "  ⚠️  robinhood-mcp package not tested"
    fi
else
    echo "  ❌ npx not found"
fi

if command -v python3 &> /dev/null; then
    echo "  ✅ python3 installed"
else
    echo "  ❌ python3 not found"
fi
echo ""

# Test endpoint
echo "🌐 Endpoint Test:"
if curl -s http://localhost:5050/health > /dev/null 2>&1; then
    echo "  ✅ ATM responding on port 5050"
    RESPONSE=$(curl -s http://localhost:5050/health)
    echo "  Response: $RESPONSE"
else
    echo "  ❌ ATM not responding"
    echo "  Check: sudo journalctl -u p3-atm -n 20"
fi
echo ""

# Summary
echo "📊 Summary:"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

READY=true

if systemctl is-active --quiet p3-atm; then
    echo "✅ Service: Running"
else
    echo "❌ Service: Not running"
    READY=false
fi

if [ -n "$ROBINHOOD_API_KEY" ] && [ -n "$ROBINHOOD_PRIVATE_KEY" ]; then
    echo "✅ Read Mode: Configured"
else
    echo "⏳ Read Mode: Needs setup"
    READY=false
fi

if [ -f "$ROBINHOOD_PRIVATE_KEY_PATH" ]; then
    echo "✅ Trading Mode: Configured"
else
    echo "⏳ Trading Mode: Not set up"
fi

echo ""
if [ "$READY" = true ]; then
    echo "🎉 Your ATM is ready!"
    echo "   Access at: http://localhost:5050"
else
    echo "⚠️  Some setup required"
    echo "   See: TRADING_SETUP_COMPLETE.md"
fi
