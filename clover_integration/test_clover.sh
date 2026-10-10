#!/bin/bash
#
# Quick test of Clover integration
# Tests connectivity and API endpoints
#

ATM_URL="http://100.103.3.35:5050"

echo "======================================================================"
echo "  P3 ATM - Clover Integration Test"
echo "======================================================================"
echo ""

# Colors
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m'

test_endpoint() {
    local name="$1"
    local endpoint="$2"
    local expected="$3"

    echo -n "Testing $name... "

    response=$(curl -s "$ATM_URL$endpoint" 2>/dev/null)

    if echo "$response" | grep -q "$expected"; then
        echo -e "${GREEN}✓ Pass${NC}"
        return 0
    else
        echo -e "${RED}✗ Fail${NC}"
        echo "  Response: $response"
        return 1
    fi
}

echo "1. Testing basic connectivity..."
test_endpoint "Health check" "/health" "ok"
echo ""

echo "2. Testing API status..."
test_endpoint "Status endpoint" "/api/status" "online"
echo ""

echo "3. Testing Clover configuration..."
test_endpoint "Clover status" "/api/clover/status" "configured"
echo ""

echo "4. Testing authentication endpoints..."
echo -n "  PIN auth endpoint... "
response=$(curl -s -X POST "$ATM_URL/api/authenticate" \
    -H "Content-Type: application/json" \
    -d '{"pin":"0000"}' 2>/dev/null)

if echo "$response" | grep -q "success"; then
    echo -e "${GREEN}✓ Accessible${NC}"
else
    echo -e "${RED}✗ Failed${NC}"
fi

echo -n "  Card auth endpoint... "
response=$(curl -s -X POST "$ATM_URL/api/authenticate/card" \
    -H "Content-Type: application/json" \
    -d '{"encrypted_pin":"test"}' 2>/dev/null)

if echo "$response" | grep -q "success\|message"; then
    echo -e "${GREEN}✓ Accessible${NC}"
else
    echo -e "${RED}✗ Failed${NC}"
fi
echo ""

echo "5. Testing from Clover perspective..."
echo "   On your Clover device, try:"
echo ""
echo "   ${YELLOW}Browser Test:${NC}"
echo "   http://100.103.3.35:5050"
echo ""
echo "   ${YELLOW}Bridge Test:${NC}"
echo "   http://100.103.3.35:5050/clover"
echo ""

echo "======================================================================"
echo "Test complete!"
echo ""
echo "If all tests passed:"
echo "  ✓ Server is accessible from network"
echo "  ✓ Clover integration endpoints are live"
echo "  ✓ Ready to test with Clover device"
echo ""
echo "If tests failed:"
echo "  • Check if p3-atm-web service is running:"
echo "    sudo systemctl status p3-atm-web"
echo ""
echo "  • Check firewall:"
echo "    sudo ufw status"
echo "    sudo ufw allow 5050/tcp"
echo ""
echo "  • Test from r510 first:"
echo "    curl http://localhost:5050/health"
echo ""
echo "======================================================================"
