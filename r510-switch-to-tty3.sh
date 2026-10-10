#!/bin/bash
# Switch R510 display to TTY3 (P3 Lending Inc ATM)
ssh matt@100.103.3.35 'sudo chvt 3'
echo "✓ R510 display switched to P3 Lending Inc ATM (TTY3)"
echo "  PIN: 0213"
echo "  Auto-logout after 60 seconds of inactivity"
echo ""
echo "To switch back: sudo chvt 1  (or Ctrl+Alt+F1)"
