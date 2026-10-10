#!/bin/bash
# Install P3 ATM as a system service

set -e

echo "🔧 Installing P3 Robinhood ATM Service"
echo "========================================"
echo ""

# Check if running with sudo
if [ "$EUID" -ne 0 ]; then
    echo "❌ This script needs sudo privileges"
    echo "   Run: sudo bash install-service.sh"
    exit 1
fi

# Stop any existing instances on port 5050
echo "🛑 Stopping existing ATM server..."
lsof -ti:5050 | xargs -r kill -9 2>/dev/null || true
sleep 2

# Copy service file to systemd
echo "📋 Installing systemd service..."
cp p3-atm.service /etc/systemd/system/p3-atm.service
chmod 644 /etc/systemd/system/p3-atm.service

# Reload systemd
echo "🔄 Reloading systemd..."
systemctl daemon-reload

# Enable service to start on boot
echo "✅ Enabling service to start on boot..."
systemctl enable p3-atm.service

# Start the service now
echo "🚀 Starting service..."
systemctl start p3-atm.service

# Wait a moment for it to start
sleep 3

# Check status
echo ""
echo "📊 Service Status:"
systemctl status p3-atm.service --no-pager -l || true

echo ""
echo "🌐 Testing endpoint..."
sleep 2
curl -s http://localhost:5050/health | jq '.' 2>/dev/null || curl -s http://localhost:5050/health

echo ""
echo "✅ Installation Complete!"
echo ""
echo "📝 Useful Commands:"
echo "   sudo systemctl status p3-atm     # Check status"
echo "   sudo systemctl restart p3-atm    # Restart service"
echo "   sudo systemctl stop p3-atm       # Stop service"
echo "   sudo systemctl disable p3-atm    # Disable auto-start"
echo "   sudo journalctl -u p3-atm -f     # View live logs"
echo ""
echo "🌐 Access your ATM at:"
echo "   http://localhost:5050"
echo "   http://100.103.3.35:5050  (from network)"
echo ""
