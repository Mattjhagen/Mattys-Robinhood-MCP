#!/bin/bash
# Setup script for Trading ATM on TTY2
# Run with: sudo bash setup-trading-atm-tty2.sh

set -e

echo "Setting up Robinhood Trading ATM on TTY2..."

# Create system service file
cat > /etc/systemd/system/trading-atm-tty2.service << 'SERVICEEOF'
[Unit]
Description=Robinhood Trading ATM Terminal on TTY2
After=multi-user.target

[Service]
Type=simple
User=matt
ExecStart=/usr/bin/python3 /home/matt/Mattys-Robinhood-MCP/trading_atm.py
StandardInput=tty
StandardOutput=tty
TTYPath=/dev/tty2
TTYReset=yes
TTYVHangup=yes
TTYVTDisallocate=yes
Restart=always
RestartSec=5

[Install]
WantedBy=multi-user.target
SERVICEEOF

echo "Service file created at /etc/systemd/system/trading-atm-tty2.service"

# Reload systemd
systemctl daemon-reload
echo "Systemd reloaded"

# Enable the service
systemctl enable trading-atm-tty2.service
echo "Service enabled"

# Start the service
systemctl start trading-atm-tty2.service
echo "Service started"

# Show status
echo ""
echo "Service status:"
systemctl status trading-atm-tty2.service --no-pager -l

echo ""
echo "✓ Setup complete!"
echo "The Trading ATM is now running on TTY2"
echo ""
echo "To switch to TTY2: sudo chvt 2"
echo "To switch back to GUI: sudo chvt 1 (or Ctrl+Alt+F1)"
echo ""
echo "Management commands:"
echo "  sudo systemctl status trading-atm-tty2"
echo "  sudo systemctl stop trading-atm-tty2"
echo "  sudo systemctl restart trading-atm-tty2"
echo "  sudo journalctl -u trading-atm-tty2 -f"
