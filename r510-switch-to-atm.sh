#!/bin/bash
# Switch R510 display to Trading ATM (TTY2)
ssh matt@100.103.3.35 'sudo chvt 2'
echo "✓ R510 display switched to Trading ATM (TTY2)"
echo "  Default PIN: 1234"
