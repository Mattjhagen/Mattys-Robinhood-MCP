#!/bin/bash
# Update P3 ATM with keyboard navigation support

echo "========================================="
echo "  Updating P3 ATM"
echo "  • Keyboard Navigation"
echo "  • Quick Balance with Trends"
echo "========================================="
echo ""

# Copy updated HTML file
ssh matt@100.103.3.35 'cp /tmp/atm.html ~/Mattys-Robinhood-MCP/p3_atm/atm_templates/'

# Restart the service
echo "Restarting P3 ATM service..."
ssh matt@100.103.3.35 'sudo systemctl restart p3-atm-web'

echo ""
echo "Waiting for service to start..."
sleep 3

# Check if it's running
if ssh matt@100.103.3.35 'curl -s http://localhost:5050/health' | grep -q "ok"; then
    echo "✓ P3 ATM updated successfully!"
else
    echo "⚠ Service may not be running. Check status:"
    echo "  ssh matt@100.103.3.35 'sudo systemctl status p3-atm-web'"
fi

echo ""
echo "========================================="
echo "  Keyboard Navigation Features:"
echo "========================================="
echo ""
echo "PIN Entry:"
echo "  • 0-9 keys - Enter digits"
echo "  • ENTER - Submit PIN"
echo "  • BACKSPACE - Delete digit"
echo "  • ESC - Cancel"
echo ""
echo "Main Menu:"
echo "  • 1 - Balance Inquiry"
echo "  • 2 - View Positions"
echo "  • 3 - Make Trade"
echo "  • 4 or ESC - Exit"
echo ""
echo "Any Screen:"
echo "  • ESC - Go back"
echo "  • ? or H - Show keyboard shortcuts"
echo ""
echo "✨ New Features:"
echo "  • Full keyboard navigation (no mouse needed!)"
echo "  • Quick balance card on main menu"
echo "  • Live trend indicators (📈 up / 📉 down)"
echo "  • Auto-refresh every 30 seconds"
echo "  • Trend icons on all positions"
echo ""
echo "Just press ENTER and type 0213 to start! 🎹"
echo ""
