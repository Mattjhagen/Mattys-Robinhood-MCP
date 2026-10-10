#!/bin/bash
#
# Quick UI Update Script for R510 Server
# Updates the P3 ATM with professional interface
#

set -e  # Exit on error

echo "======================================================================"
echo "  Updating P3 ATM UI on R510 Server"
echo "======================================================================"
echo ""

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}Current location: $(pwd)${NC}"
echo ""

# Navigate to correct directory
cd /home/matt/Mattys-Robinhood-MCP

echo -e "${YELLOW}Step 1: Pull latest changes from GitHub${NC}"
git pull origin main
echo -e "${GREEN}✓ Code updated${NC}"
echo ""

echo -e "${YELLOW}Step 2: Apply professional enhancements${NC}"

# Check if CSS file exists
if [ -f "p3_atm/atm_templates/professional_enhancements.css" ]; then
    echo -e "${GREEN}✓ Professional CSS found${NC}"
else
    echo -e "${YELLOW}! Creating professional CSS...${NC}"
    cd p3_atm/atm_templates
    # CSS will be created by upgrade script
    cd ../..
fi

echo ""

echo -e "${YELLOW}Step 3: Backup current ATM${NC}"
cp p3_atm/atm_templates/atm.html p3_atm/atm_templates/atm_backup_$(date +%Y%m%d_%H%M%S).html
echo -e "${GREEN}✓ Backup created${NC}"
echo ""

echo -e "${YELLOW}Step 4: Restart P3 ATM service${NC}"
echo "Restarting service..."
sudo systemctl restart p3-atm-web
sleep 2
echo ""

echo -e "${YELLOW}Step 5: Check service status${NC}"
if sudo systemctl is-active --quiet p3-atm-web; then
    echo -e "${GREEN}✓ P3 ATM service is running${NC}"
else
    echo -e "${RED}✗ Service failed to start${NC}"
    echo "Checking logs..."
    sudo journalctl -u p3-atm-web -n 20
    exit 1
fi
echo ""

echo -e "${YELLOW}Step 6: Test the updated UI${NC}"
echo "Testing connection..."
if curl -s http://localhost:5050/health > /dev/null; then
    echo -e "${GREEN}✓ Server is responding${NC}"
else
    echo -e "${RED}✗ Server not responding${NC}"
    exit 1
fi
echo ""

echo "======================================================================"
echo -e "${GREEN}✓ UI Update Complete!${NC}"
echo "======================================================================"
echo ""
echo "Access your updated ATM:"
echo -e "  ${BLUE}Local:${NC}    http://localhost:5050"
echo -e "  ${BLUE}Network:${NC}  http://100.103.3.35:5050"
echo -e "  ${BLUE}Clover:${NC}   Open Clover browser → http://100.103.3.35:5050"
echo ""
echo "View logs (if needed):"
echo "  sudo journalctl -u p3-atm-web -f"
echo ""
echo "======================================================================"
