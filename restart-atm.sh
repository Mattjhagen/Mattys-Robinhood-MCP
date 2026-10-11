#!/bin/bash
# Restart the Trading ATM on TTY2
# This requires sudo to restart the system service

echo "🔄 Restarting Trading ATM service on TTY2..."
echo "   (This will prompt for your sudo password)"
echo ""

sudo systemctl restart trading-atm-tty2

if [ $? -eq 0 ]; then
    echo "✅ Trading ATM service restarted successfully!"
    echo ""
    echo "To view the ATM on r510's physical display:"
    echo "  ssh matt@100.103.3.35 'sudo chvt 2'"
    echo ""
    echo "To check service status:"
    echo "  sudo systemctl status trading-atm-tty2"
else
    echo "❌ Failed to restart Trading ATM service"
    echo "   Please check service status with: sudo systemctl status trading-atm-tty2"
fi
