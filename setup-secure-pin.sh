#!/bin/bash
# Setup script for secure PIN authentication
# This generates the PIN hash and adds it to your environment

echo "==================================="
echo "Robinhood ATM - Secure PIN Setup"
echo "==================================="
echo

# Check if Python is available
if ! command -v python3 &> /dev/null; then
    echo "Error: Python 3 is required"
    exit 1
fi

# Get current PIN or use default
CURRENT_PIN="${1:-0213}"

echo "Generating secure hash for PIN: $CURRENT_PIN"
echo

# Generate hash using Python
PIN_HASH=$(python3 -c "import hashlib; print(hashlib.sha256('$CURRENT_PIN'.encode()).hexdigest())")

echo "Generated hash: $PIN_HASH"
echo

# Check if already in bashrc
if grep -q "ATM_PIN_HASH" ~/.bashrc; then
    echo "Found existing ATM_PIN_HASH in ~/.bashrc"
    echo "Updating..."
    sed -i "s|export ATM_PIN_HASH=.*|export ATM_PIN_HASH='$PIN_HASH'|" ~/.bashrc
else
    echo "Adding ATM_PIN_HASH to ~/.bashrc..."
    echo "" >> ~/.bashrc
    echo "# Robinhood ATM Secure PIN Hash" >> ~/.bashrc
    echo "export ATM_PIN_HASH='$PIN_HASH'" >> ~/.bashrc
fi

echo
echo "✓ PIN hash configured in ~/.bashrc"
echo
echo "Next steps:"
echo "1. Load the new environment:"
echo "   source ~/.bashrc"
echo
echo "2. Verify it's set:"
echo "   echo \$ATM_PIN_HASH"
echo
echo "3. Restart the ATM server:"
echo "   systemctl --user restart robinhood-atm-server"
echo
echo "To change the PIN in the future, run:"
echo "   bash setup-secure-pin.sh <NEW_PIN>"
echo

# Also export for current session
export ATM_PIN_HASH="$PIN_HASH"
echo "✓ PIN hash also set for current session"
