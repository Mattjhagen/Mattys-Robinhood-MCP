#!/bin/bash
# Test ATM kiosk mode before reboot
echo "Testing Robinhood ATM in kiosk mode..."
echo "This will open fullscreen in 5 seconds."
echo "Press Ctrl+C to cancel, or Alt+F4 to close after it opens."
echo ""
sleep 5
chromium-browser --kiosk --app=http://localhost:5050
