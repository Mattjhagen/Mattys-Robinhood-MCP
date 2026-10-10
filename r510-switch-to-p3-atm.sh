#!/bin/bash
# Switch R510 display to P3 Lending Inc ATM (TTY2)
ssh matt@100.103.3.35 'sudo chvt 2'
echo "✓ R510 display switched to P3 Lending Inc ATM (TTY2)"
echo "  PIN: 0213"
echo "  Auto-logout after 60 seconds of inactivity"
