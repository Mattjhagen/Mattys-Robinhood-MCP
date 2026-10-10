#!/bin/bash
# Install P3 ATM on r510 TTY3
echo "Installing P3 Lending Inc ATM on r510 TTY3..."
echo "This requires sudo password on r510"
echo ""

ssh -t matt@100.103.3.35 "sudo bash /tmp/install_p3_atm_tty3.sh"

echo ""
echo "Installation complete!"
echo "Use ./r510-switch-to-tty3.sh to view the ATM"
