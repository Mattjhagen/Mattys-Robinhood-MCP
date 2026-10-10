#!/bin/bash
# Restart P3 ATM with updated files

echo "Restarting P3 ATM with real trading functionality..."

# Copy files to r510
ssh matt@100.103.3.35 'cp /tmp/atm_server.py ~/Mattys-Robinhood-MCP/p3_atm/ && cp /tmp/atm.html ~/Mattys-Robinhood-MCP/p3_atm/atm_templates/'

# Restart the server (this requires running on r510 directly)
echo ""
echo "Files copied. Now restart the server on r510:"
echo ""
echo "Run this command on r510:"
echo "  pkill -f atm_server.py && sleep 2 && cd ~/Mattys-Robinhood-MCP/p3_atm && python3 atm_server.py > /tmp/atm_server.log 2>&1 &"
echo ""
echo "Or use systemd if configured:"
echo "  sudo systemctl restart p3-atm-web"
echo ""
echo "Then refresh your browser with Ctrl+Shift+R"
