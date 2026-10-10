#!/bin/bash
# Check R510 Trading ATM status
echo "Trading ATM Service:"
ssh matt@100.103.3.35 'sudo systemctl status trading-atm-tty2 --no-pager'
echo ""
echo "Trading Agent Keeper:"
ssh matt@100.103.3.35 'systemctl --user status trading-agent-keeper --no-pager'
