#!/bin/bash
# Helper script to load Robinhood environment variables
# Usage: source ./load_env.sh

# Load from ~/.bashrc if available
if [ -f ~/.bashrc ]; then
    source ~/.bashrc
fi

# Show what's loaded
echo "🔑 Environment Check:"
echo ""

if [ -n "$ROBINHOOD_API_KEY" ]; then
    echo "✅ ROBINHOOD_API_KEY loaded"
else
    echo "❌ ROBINHOOD_API_KEY not found"
    echo "   Add this to ~/.bashrc:"
    echo "   export ROBINHOOD_API_KEY=\"your-key-here\""
fi

if [ -n "$ROBINHOOD_PRIVATE_KEY" ]; then
    echo "✅ ROBINHOOD_PRIVATE_KEY loaded"
else
    echo "❌ ROBINHOOD_PRIVATE_KEY not found"
    echo "   Add this to ~/.bashrc:"
    echo "   export ROBINHOOD_PRIVATE_KEY=\"your-key-here\""
fi

if [ -n "$ROBINHOOD_PRIVATE_KEY_PATH" ]; then
    echo "✅ ROBINHOOD_PRIVATE_KEY_PATH: $ROBINHOOD_PRIVATE_KEY_PATH"
else
    echo "⏳ ROBINHOOD_PRIVATE_KEY_PATH not set (optional for trading)"
fi

echo ""
echo "Run 'source ~/.bashrc' to reload environment in current shell"
