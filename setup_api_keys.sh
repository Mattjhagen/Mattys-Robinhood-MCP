#!/bin/bash
# Interactive script to add Robinhood API keys to ~/.bashrc

echo "🔐 Robinhood API Key Setup"
echo "=========================="
echo ""
echo "This script will help you permanently add your API keys to ~/.bashrc"
echo ""

# Check if keys already exist in bashrc
if grep -q "ROBINHOOD_API_KEY" ~/.bashrc; then
    echo "⚠️  WARNING: ROBINHOOD_API_KEY already exists in ~/.bashrc"
    echo ""
    read -p "Do you want to update it? (y/n): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "Cancelled."
        exit 1
    fi

    # Remove old keys
    echo "Removing old keys from ~/.bashrc..."
    sed -i '/export ROBINHOOD_API_KEY=/d' ~/.bashrc
    sed -i '/export ROBINHOOD_PRIVATE_KEY=/d' ~/.bashrc
    sed -i '/export ROBINHOOD_API_SECRET=/d' ~/.bashrc
fi

echo ""
echo "📋 Where to get your API keys:"
echo "   1. Visit: https://robinhood.com/account/settings"
echo "   2. Navigate to: API & Trading"
echo "   3. Click: Generate API Credentials"
echo "   4. Copy both keys (keep them secret!)"
echo ""
echo "Press Enter when you're ready to add your keys..."
read

# Get API Key
echo ""
echo -n "Enter your ROBINHOOD_API_KEY: "
read -r API_KEY

if [ -z "$API_KEY" ]; then
    echo "❌ API Key cannot be empty"
    exit 1
fi

# Get Private Key
echo ""
echo -n "Enter your ROBINHOOD_PRIVATE_KEY: "
read -r PRIVATE_KEY

if [ -z "$PRIVATE_KEY" ]; then
    echo "❌ Private Key cannot be empty"
    exit 1
fi

# Add to bashrc
echo ""
echo "Adding keys to ~/.bashrc..."

cat >> ~/.bashrc << EOF

# Robinhood API Keys (added $(date))
export ROBINHOOD_API_KEY="$API_KEY"
export ROBINHOOD_PRIVATE_KEY="$PRIVATE_KEY"
EOF

echo "✅ Keys added to ~/.bashrc!"
echo ""

# Load immediately
export ROBINHOOD_API_KEY="$API_KEY"
export ROBINHOOD_PRIVATE_KEY="$PRIVATE_KEY"

echo "✅ Keys loaded in current session"
echo ""
echo "Key lengths:"
echo "   API Key: ${#ROBINHOOD_API_KEY} characters"
echo "   Private Key: ${#ROBINHOOD_PRIVATE_KEY} characters"
echo ""
echo "🔄 To use in future sessions, run:"
echo "   source ~/.bashrc"
echo ""
echo "🚀 Ready to start the ATM server:"
echo "   cd ~/Mattys-Robinhood-MCP/p3_atm"
echo "   ./start_atm_live.sh"
echo ""
