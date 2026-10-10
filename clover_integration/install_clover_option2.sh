#!/bin/bash
#
# Install Clover Integration (Option 2: PIN Pad)
# Sets up P3 ATM with Clover card reader support
#

set -e  # Exit on error

echo "======================================================================"
echo "  P3 Lending ATM - Clover Integration Installer"
echo "  Option 2: Secure PIN Pad + Card Reader"
echo "======================================================================"
echo ""

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Check we're in the right directory
if [ ! -f "../p3_atm/atm_server.py" ]; then
    echo -e "${RED}Error: Run this from clover_integration/ directory${NC}"
    exit 1
fi

echo -e "${YELLOW}Step 1: Backup existing ATM server${NC}"
cp ../p3_atm/atm_server.py ../p3_atm/atm_server.py.backup
echo "✓ Backed up to atm_server.py.backup"
echo ""

echo -e "${YELLOW}Step 2: Install Clover-enhanced server${NC}"
cp atm_server_with_clover.py ../p3_atm/atm_server.py
echo "✓ Installed enhanced server with Clover support"
echo ""

echo -e "${YELLOW}Step 3: Configure Clover credentials${NC}"
echo ""
echo "You'll need these from https://dashboard.clover.com:"
echo "  1. Merchant ID"
echo "  2. API Token"
echo "  3. Encryption Key"
echo ""

read -p "Enter Clover Merchant ID (or press Enter to skip): " MERCHANT_ID
read -p "Enter Clover API Key (or press Enter to skip): " API_KEY
read -p "Enter Clover Encryption Key (or press Enter to skip): " ENCRYPTION_KEY

# Create environment file for Clover credentials
ENV_FILE="$HOME/.clover_atm_env"
cat > "$ENV_FILE" << EOF
# P3 ATM Clover Configuration
export CLOVER_MERCHANT_ID="$MERCHANT_ID"
export CLOVER_API_KEY="$API_KEY"
export CLOVER_ENCRYPTION_KEY="$ENCRYPTION_KEY"
EOF

chmod 600 "$ENV_FILE"
echo "✓ Saved credentials to $ENV_FILE"
echo ""

echo -e "${YELLOW}Step 4: Update systemd service${NC}"

# Check if service exists
if systemctl list-unit-files | grep -q p3-atm-web.service; then
    SERVICE_FILE="/etc/systemd/system/p3-atm-web.service"

    if [ -f "$SERVICE_FILE" ]; then
        echo "Updating service to load Clover environment..."

        # Backup service file
        sudo cp "$SERVICE_FILE" "${SERVICE_FILE}.backup"

        # Add environment file to service
        sudo sed -i "/\[Service\]/a EnvironmentFile=$ENV_FILE" "$SERVICE_FILE"

        # Reload and restart
        sudo systemctl daemon-reload
        sudo systemctl restart p3-atm-web

        echo "✓ Service updated and restarted"
    else
        echo -e "${YELLOW}Service file not found, skipping${NC}"
    fi
else
    echo -e "${YELLOW}p3-atm-web service not found, will run manually${NC}"
fi
echo ""

echo -e "${YELLOW}Step 5: Set up Clover bridge${NC}"

# Copy bridge to templates directory
mkdir -p ../p3_atm/atm_templates
cp clover_bridge.html ../p3_atm/atm_templates/

# Update bridge with credentials if provided
if [ -n "$MERCHANT_ID" ]; then
    sed -i "s/YOUR_MERCHANT_ID/$MERCHANT_ID/g" ../p3_atm/atm_templates/clover_bridge.html
fi

if [ -n "$API_KEY" ]; then
    sed -i "s/YOUR_ACCESS_TOKEN/$API_KEY/g" ../p3_atm/atm_templates/clover_bridge.html
fi

echo "✓ Clover bridge installed"
echo ""

echo -e "${YELLOW}Step 6: Configure firewall${NC}"
if command -v ufw >/dev/null 2>&1; then
    sudo ufw allow 5050/tcp
    echo "✓ Opened port 5050 in firewall"
else
    echo "⚠ UFW not found, ensure port 5050 is open"
fi
echo ""

echo "======================================================================"
echo -e "${GREEN}✓ Installation Complete!${NC}"
echo "======================================================================"
echo ""
echo "Next Steps:"
echo ""
echo "1. ${GREEN}Test from r510 browser:${NC}"
echo "   http://localhost:5050"
echo ""
echo "2. ${GREEN}Test from Clover device:${NC}"
echo "   http://100.103.3.35:5050"
echo ""
echo "3. ${GREEN}Test Clover bridge:${NC}"
echo "   http://100.103.3.35:5050/clover"
echo ""
echo "4. ${GREEN}Configure Clover device:${NC}"
echo "   - Open Chrome on Clover"
echo "   - Navigate to: http://100.103.3.35:5050/clover"
echo "   - Bookmark it for easy access"
echo ""
echo "Credentials saved to: $ENV_FILE"
echo ""
echo "Server status:"
if systemctl is-active --quiet p3-atm-web 2>/dev/null; then
    echo -e "  Service: ${GREEN}Running${NC}"
    echo "  Check status: sudo systemctl status p3-atm-web"
else
    echo -e "  Service: ${YELLOW}Manual mode${NC}"
    echo "  Start with: cd ../p3_atm && python3 atm_server.py"
fi
echo ""
echo "To revert to original server:"
echo "  cp ../p3_atm/atm_server.py.backup ../p3_atm/atm_server.py"
echo "  sudo systemctl restart p3-atm-web"
echo ""
echo "Documentation: CLOVER_INTEGRATION_GUIDE.md"
echo "======================================================================"
