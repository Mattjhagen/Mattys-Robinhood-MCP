#!/bin/bash
#
# Install Robinhood ATM Interface
# Replaces current ATM with Robinhood-branded UI
#

echo "======================================================================"
echo "  Installing Robinhood ATM Interface"
echo "======================================================================"
echo ""

cd /home/matt/Mattys-Robinhood-MCP/p3_atm/atm_templates

# Backup current
echo "1. Backing up current ATM..."
cp atm.html atm_before_robinhood_$(date +%Y%m%d_%H%M%S).html
echo "✓ Backup created"
echo ""

# Copy Robinhood style
echo "2. Installing Robinhood ATM..."
cp atm_wellsfargo_style.html atm.html
echo "✓ Robinhood ATM installed"
echo ""

echo "3. Restarting service..."
sudo systemctl restart p3-atm-web
sleep 2
echo ""

echo "======================================================================"
echo "✓ Robinhood ATM Installed!"
echo "======================================================================"
echo ""
echo "Access your new Robinhood ATM:"
echo "  Local:   http://localhost:5050"
echo "  Network: http://100.103.3.35:5050"
echo ""
echo "Features:"
echo "  ✓ Robinhood branding and colors"
echo "  ✓ Promotional ads sidebar"
echo "  ✓ Fully functional trading"
echo "  ✓ Real balance display"
echo "  ✓ Professional receipt format"
echo "  ✓ Multi-language support"
echo ""
echo "======================================================================"
