#!/bin/bash
# Check P3 ATM TTY3 status
echo "========================================="
echo "  P3 Lending Inc ATM (TTY3) Status"
echo "========================================="
echo ""
ssh matt@100.103.3.35 'sudo systemctl status p3-atm-tty3 --no-pager -l'
echo ""
echo "========================================="
echo "Recent logs:"
ssh matt@100.103.3.35 'sudo journalctl -u p3-atm-tty3 -n 15 --no-pager'
