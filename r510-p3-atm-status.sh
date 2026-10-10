#!/bin/bash
# Check R510 P3 Lending Inc ATM status
echo "========================================="
echo "  P3 Lending Inc ATM Status"
echo "========================================="
echo ""
echo "ATM Service:"
ssh matt@100.103.3.35 'sudo systemctl status p3-atm-tty2 --no-pager -l'
echo ""
echo "========================================="
echo ""
echo "Recent logs:"
ssh matt@100.103.3.35 'sudo journalctl -u p3-atm-tty2 -n 10 --no-pager'
