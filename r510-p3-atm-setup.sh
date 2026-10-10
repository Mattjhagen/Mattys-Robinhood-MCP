#!/bin/bash
# Setup P3 Lending Inc ATM on R510 (run remotely)

echo "Setting up P3 Lending Inc ATM on R510..."
echo "This will require sudo password on r510"
echo ""

ssh -t matt@100.103.3.35 "cd /tmp && sudo bash setup_p3_atm.sh"

echo ""
echo "Setup complete! The P3 ATM should now be running on TTY2"
echo "Use ./r510-switch-to-p3-atm.sh to view it"
